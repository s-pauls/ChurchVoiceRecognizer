Set WshShell = CreateObject("WScript.Shell")
Set fso = CreateObject("Scripting.FileSystemObject")

' Получаем путь к директории скрипта
scriptPath = fso.GetParentFolderName(WScript.ScriptFullName)

' Создаем лог файл для отладки
logFile = scriptPath & "\logs\silent_run.log"

' Запускаем bat файл с перенаправлением вывода в лог
command = Chr(34) & scriptPath & "\run_silent.bat" & Chr(34) & " silent > " & Chr(34) & logFile & Chr(34) & " 2>&1"
WshShell.Run command, 0, True

Set WshShell = Nothing
Set fso = Nothing