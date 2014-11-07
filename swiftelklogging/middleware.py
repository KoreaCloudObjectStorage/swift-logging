from datetime import datetime

from swift.common.swob import Request
from swift.common.utils import get_logger


class SwiftElkLoggingMiddleware(object):
    def __init__(self, app, conf):
        self.app = app
        self.conf = conf
        self.logger = get_logger(conf, log_route='swift_elk_logging',
                                 fmt="%(message)s")
        self.log_fm = '%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s'

    def __call__(self, env, start_response):
        req = Request(env)
        dt = datetime.now().timetuple()

        txd = req.environ['swift.trans_id']
        msg = self.log_fm % (dt[0], dt[1], dt[2], dt[3], dt[4], dt[5],
                             req.method, req.path, req.params,
                             '127.0.0.1', req.remote_addr, txd)

        def response_logging(status, response_headers, exc_info=None):
            full_msg = '%s,%s' % (msg, str(status))
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