import time
from datetime import datetime
from datetime import date
from time import mktime

from swift.common.swob import Request
from swift.common.utils import get_logger, whataremyips
from swift.common.utils import split_path


class SwiftElkLoggingMiddleware(object):
    def __init__(self, app, conf):
        self.app = app
        self.conf = conf
        self.logger = get_logger(conf, log_route='swift_elk_logging')
        self.log_fm = '"%s",'   # ENV RAW
        self.log_fm += '%f,'  # UNIX_TIMESTAMP
        self.log_fm += '%s,'  # DATE_YEAR
        self.log_fm += '%s,'  # DATE_MONTH
        self.log_fm += '%s,'  # DATE_DAY
        self.log_fm += '%s,'  # WEEK_DAY
        self.log_fm += '%s,'  # HOUR
        self.log_fm += '%s,'  # MIN
        self.log_fm += '%s.'  # SEC
        self.log_fm += '%s,'  # MICRO_SEC
        self.log_fm += '%s,'  # HTTP_METHOD
        self.log_fm += '%s,'  # URL
        self.log_fm += '%s,'  # account
        self.log_fm += '%s,'  # bucket
        self.log_fm += '%s,'  # object
        self.log_fm += '%s,'  # CONTENTS_LENGTH
        self.log_fm += '"%s",'  # PARAMETER
        self.log_fm += '%s,'  # SERVER_IP
        self.log_fm += '%s,'  # REMOTE_IP
        self.log_fm += '%s,'  # User Agent
        self.log_fm += '%s'  # REQUEST_ID

    def __call__(self, env, start_response):
        req = Request(env)
        dt = datetime.now()
        ts = mktime(dt.timetuple()) + (dt.microsecond / 1000000.)
        week_day = date.today().strftime("%a")
        server_ip = whataremyips()
        txd = req.environ['swift.trans_id']
        start_time = time.time()

        # URL format is http:[host]/bucket/object
        version, account, container, obj = split_path(req.path, 1, 4, True)

        if container is None:
            container = ''
        if obj is None:
            obj = ''

        str_env = str(env)
        str_env = str_env.replace('"', '\'')
        user_agent = env['HTTP_USER_AGENT'] if 'HTTP_USER_AGENT' in env else \
            ''
        msg = self.log_fm % (str_env, ts, dt.year, dt.month, dt.day, week_day,
                             dt.hour, dt.minute, dt.second, dt.microsecond,
                             req.method, req.path, account, container, obj,
                             req.content_length, req.params, server_ip[0],
                             req.remote_addr, user_agent, txd)

        def response_logging(status, response_headers, exc_info=None):
            elapse = time.time() - start_time
            full_msg = '%s,%s,%.8f' % (msg, status.split(' ', 1)[0], elapse)
            self.logger.info(full_msg)
            return start_response(status, response_headers, exc_info)

        return self.app(env, response_logging)


def filter_factory(global_conf, **local_conf):
    """Standard filter factory to use the middleware with paste.deploy"""
    conf = global_conf.copy()
    conf.update(local_conf)

    def logger_filter(app):
        return SwiftElkLoggingMiddleware(app, conf)

    return logger_filter
