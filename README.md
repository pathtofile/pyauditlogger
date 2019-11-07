# pyAuditLogger
Auto-Add Python 3.8 audit hooks to all python scripts on Windows

This Package uses a `pth` file to automatically add audit hooks to
every python script run on a system. The hooks are created before any user-supplied code is run.
Any code that is exec'd or compiled is also passed to AMSI

The Hooks will then log all events to The Application Event Log under the name "Python-Audit"

# Installation
On Windows you need to pre-install the `pywin32` pip package.
Right now the current version of pywin32 doesn't support Python 3.8, so either
build it yourself, or grab it from: https://github.com/CristiFati/Prebuilt-Binaries/tree/master/PyWin32
See Issue https://github.com/mhammond/pywin32/issues/1327
Then just run
```batch
python setup.py bdist_wheel
python -m pip install dist\*.whl
```

# Viewing Audit Log
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
