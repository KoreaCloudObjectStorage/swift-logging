Swift-Logging
------

Install
-------

1) Install Swift-Logging with ``sudo python setup.py install`` or ``sudo python
   setup.py develop`` or via whatever packaging system you may be using.

2) Alter your proxy-server.conf pipeline to have swift_logging:

    [pipeline:main]
        pipeline = catch_errors cache swift3_gatekeeper
        swift3 s3token authtoken keystone swift_logging proxy-server

    ! swift_logging middleware always located after auth middleware

3) Add to your proxy-server.conf the section for the swift_logging WSGI 
filter::

    [filter:swift_logging]
    use = egg:swift_logging#swift_logging
    set log_name = swift_logging
    set log_level = INFO
    set log_facility = LOG_LOCAL6
    sentry_sdn = 125d6153cfcd4634bc6b06c6bb900a70@192.168.100.160:9000/2

You also need to add the following in '/etc/rsyslog.d/10-swift.conf

    $PrivDropToGroup adm

    local6.*;local6.!notice /var/log/swift/logs/api.log
    local6.notice           /var/log/swift/logs/api.error
    local6.*                ~

And, Make log directory on '/var/log'

    sudo mkdir -p /var/log/swift
    sudo chown -R syslog.adm /var/log/swift
    sudo chmod -R g+w /var/log/swift