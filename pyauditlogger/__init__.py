import sys
import os
import win32evtlogutil
import win32evtlog
import atexit
from ctypes import *
from .known_events import KNOWN_EVENTS

AMSI = None
AMSI_CONTEXT = c_void_p(None)
AMSI_SESSION = c_void_p(None)


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
    strings = [f"PID: {os.getpid()}", f"Commandline: {cmd}", f"Event: {event}"]
    for arg in args:
        strings.append(f"{arg!r}")
    win32evtlogutil.ReportEvent(
        "Python-Audit",
        event_id,
        eventCategory=1,
        eventType=win32evtlog.EVENTLOG_INFORMATION_TYPE,
        strings=strings)

    if event == "compile" or event == "cpython.run_command":
        # Also pass to AMSI to scan
        to_scan = repr(strings).encode()
        to_scan_size = len(to_scan) * 2
        amsi_result = c_void_p(None)
        AMSI.AmsiScanBuffer(AMSI_CONTEXT, to_scan, to_scan_size, "Python",
                            AMSI_SESSION, byref(amsi_result))
        if amsi_result.value >= 32768:
            # MALWARE!
            print(f"MALWARE DETECTED: {args}")
            sys.exit(1)


def shutdown():
    """
    Finilize AMSI Session Context
    """
    AMSI.AmsiCloseSession(AMSI_CONTEXT, AMSI_SESSION)
    AMSI.AmsiUninitialize(AMSI_CONTEXT)


def setup():
    """
    Load AMSI DLL, Initialize AMSI and AMSI Session
    """
    global AMSI
    global AMSI_CONTEXT
    global AMSI_SESSION
    try:
        AMSI = cdll.LoadLibrary('amsi.dll')
        if AMSI is not None:
            ret = AMSI.AmsiInitialize("Python", byref(AMSI_CONTEXT))
            if ret == 0:
                ret = AMSI.AmsiOpenSession(AMSI_CONTEXT, byref(AMSI_SESSION))
                if ret == 0:
                    return True
    except FileNotFoundError:
        pass
    except OSError:
        pass
    return False


if setup():
    atexit.register(shutdown)
    sys.addaudithook(audit_hook_windows)
