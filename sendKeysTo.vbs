Set objShell = WScript.CreateObject("WScript.Shell")
Set objWMIService = GetObject("winmgmts:\\.\root\cimv2")

query = Replace ("Select * From Win32_Process where name='{0}'", "{0}", WScript.Arguments(0))
Set colItems = objWMIService.ExecQuery(query)

Function SendKeysTo (processID, keys)
    objShell.AppActivate(processID)
    objShell.SendKeys keys
End Function

For Each objItem in colItems
    SendKeysTo objItem.ProcessID, WScript.Arguments(1)
Next

