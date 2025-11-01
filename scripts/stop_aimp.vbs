Set objShell = CreateObject("WScript.Shell")
Set objWMI = GetObject("winmgmts:\\.\root\cimv2")

' Получаем все процессы AIMP
Set colProcesses = objWMI.ExecQuery("SELECT * FROM Win32_Process WHERE Name LIKE '%aimp%'")

' Завершаем все найденные процессы AIMP
For Each objProcess in colProcesses
    objProcess.Terminate()
Next

' Альтернативный способ через taskkill
On Error Resume Next
objShell.Run "taskkill /f /im aimp.exe", 0, True
objShell.Run "taskkill /f /im aimp5.exe", 0, True
On Error GoTo 0

WScript.Echo "AIMP плейер закрыт"