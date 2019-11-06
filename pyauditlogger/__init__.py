import sys
import os
from .known_events import KNOWN_EVENTS
# On Windows we'll use the Event Log Service
# and on *nix we'll use syslog
if sys.platform == "win32":
    import win32evtlogutil
    import win32evtlog
else:
    import logging
    import logging.handlers
    LOGGER = logging.getLogger(__name__)


def audit_hook_nix(event, args):
    """
    Use Syslog to log all events on *nix
    This should also work for MacOS/BSD, but haven't confirmed
    """
    cmd = f"{sys.executable} " + " ".join(sys.argv)
    log = f"python-audit: [cmd={cmd!r} event={event!r} args={args!r}]"
    LOGGER.info(log)

def audit_hook_windows(event, args):
    """
    Log all events to the Application Event Log service
    A better way would be to log to either ETW or a structured/compiled
    specific Python-Audit Event log, but for now we'll just log to Application
    """
    # Each event type will be it's own unique event ID
    event_id = KNOWN_EVENTS.index(event) if event in KNOWN_EVENTS else 999
    cmd = f"{sys.executable} " + " ".join(sys.argv)
    # We'll just log an array of strings instead of compiling something
    # more structured. This is a dodgy way to do this, but its just a PoC
    strings = [
        f"PID: {os.getpid()}",
        f"Commandline: {cmd}",
        f"Event: {event}"
    ]
    for arg in args:
        strings.append(f"{arg!r}")
    win32evtlogutil.ReportEvent(
        "Python-Audit",
        event_id,
        eventCategory=1,
        eventType=win32evtlog.EVENTLOG_INFORMATION_TYPE,
        strings=strings)

if sys.platform == "win32":
    sys.addaudithook(audit_hook_windows)
else:
    LOGGER.setLevel(logging.INFO)
    handler = logging.handlers.SysLogHandler(address='/dev/log')
    formatter = logging.Formatter('%(message)s')
    handler.setFormatter(formatter)
    LOGGER.addHandler(handler)
    sys.addaudithook(audit_hook_nix)
