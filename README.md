# README

Log handler to push log messages from micropython to remote syslog server using
RFC3164 UDP protocol. Be aware that UDP does not guarantee delivery of log
messages.

## Installation

```
mpremote mip install github:stefan-walluhn/micropython-syslog
```

## Usage

```
import logging
from usyslog import SyslogHandler

log = logging.getLogger()
log.addHandler(SyslogHandler(host='localhost', port=514, facility=Facility.LOCAL0))

log.info('hello world')
```

* `host`: hostname to send messages to, defaults to localhost
* `port`: UDP port to send messages to, defaults to 514
* `facility`: syslog facility, defaults to LOCAL0, valid keys can be found in usyslog.py

Be aware that local console (repl) logging is disabled as soon as there is any
log handler defined using `addHandler` in the `logging`-Package. If you need
console logging, add another log handler e.g:

```
class ConsoleHandler:
    def emit(self, record):
        print(record.levelname, ":", record.name, ":", record.message,
              sep="", file=sys.stderr)
```

## Testing

When we'll have a test framework for micropython?
