import usocket as socket


class Severity:
    CRITICAL = 2
    ERROR = 3
    WARN = 4
    INFO = 6
    DEBUG = 7


class Facility:
    KERN = 0
    USER = 1
    MAIL = 2
    DAEMON = 3
    AUTH = 4
    SYSLOG = 5
    LPR = 6
    NEWS = 7
    UUCP = 8
    CRON = 9
    AUTHORIV = 10
    FTP = 11
    NTP = 12
    AUDIT = 13
    ALERT = 14
    CLOCK = 15
    LOCAL0 = 16
    LOCAL1 = 17
    LOCAL2 = 18
    LOCAL3 = 19
    LOCAL4 = 20
    LOCAL5 = 21
    LOCAL6 = 22
    LOCAL7 = 23


class SyslogMessage:
    @classmethod
    def from_record(cls, record, facility):
        return cls(record.message,
                   severity=getattr(Severity, record.levelname),
                   facility=Facility.LOCAL0)

    def __init__(self, message,
                 severity=Severity.DEBUG, facility=Facility.LOCAL0):
        self.message = message
        self.severity = severity
        self.facility = facility

    @property
    def pri(self):
        return self.severity + (self.facility << 3)


class SyslogSerializer:
    def __call__(self, syslog_message):
        return str(f'<{syslog_message.pri}>{syslog_message.message}').encode()


class SyslogClient:
    def __init__(self, host, port):
        self._host = host
        self._port = port
        self._sockaddr = None

        self._socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self._serializer = SyslogSerializer()

    @property
    def sockaddr(self):
        if not self._sockaddr:
            self._resolve_sockaddr()

        return self._sockaddr

    def send(self, syslog_message):
        try:
            self._socket.sendto(
                self._serializer(syslog_message),
                self.sockaddr
            )
        except OSError:
            pass

    def _resolve_sockaddr(self):
        self._sockaddr = socket.getaddrinfo(self._host, self._port)[0][-1]


class SyslogHandler:
    def __init__(self, host='localhost', port=514, facility=Facility.LOCAL0):
        self.syslog_client = SyslogClient(host, port)
        self.facility = facility

    def emit(self, record):
        self.syslog_client.send(
            SyslogMessage.from_record(record, self.facility)
        )
