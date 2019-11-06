# pyAuditLogger
Auto-Add Python 3.8 audit hooks to all python scripts

This Package uses a `pth` file to automatically add audit hooks to
every python script run on a system. The hooks are created before any user-supplied code is run

The Hooks will then log all events to either:
Windows: The Application Event Log
Linux/MacOS: Syslog


# Installation - Linux/MacOS
First make sure `rsyslog` is installed and running
As you might have multiple pythons installed, run:
```bash
python3.8 setup.py bdist_wheel
python3.8 -m pip install dist/*.whl
```

# Installation - Windows
On Windows you need to pre-install the `pywin32` pip package.
Right now the current version of pywin32 doesn't support Python 3.8, so either
build it yourself, or grab it from: https://github.com/CristiFati/Prebuilt-Binaries/tree/master/PyWin32
See Issue https://github.com/mhammond/pywin32/issues/1327
Then just run
```batch
python setup.py bdist_wheel
python -m pip install dist\*.whl
```

# Viewing Audit Log - Linux/MacOS
You should see logs going into `/var/log/syslog`

# Viewing Audit Log - Windows
The Events are being written to the `Application` Event Log. To make it easier to see the events,
you can create a Filter with the following filter XML:
```XML
<QueryList>
  <Query Id="0" Path="Application">
    <Select Path="Application">*[System[Provider[@Name='Python-Audit']]]</Select>
  </Query>
</QueryList>
```

# Uninstallation
Simply run
```bash
python -m pip uninstall pyauditlogger
```
If something is broken, in your `site-packages` folder, remove:
* zpyauditlogger.pth
* pyauditlogger*

# Future Work
This is a PoC, so probably won't get worked on.
But if it was, I would change the Windows Logging to use either ETW, or compile our own
structured events, instead of putting everything to arbitrary string fields.

