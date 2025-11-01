Set objShell = CreateObject("WScript.Shell")

' Попытка запустить AIMP из стандартных путей установки
On Error Resume Next

' Пробуем найти AIMP в Program Files
aimp_path = "C:\Program Files\AIMP\AIMP.exe"
If objShell.FileExists(aimp_path) Then
    objShell.Run """" & aimp_path & """"
    WScript.Quit
End If

' Пробуем найти AIMP в Program Files (x86)
aimp_path = "C:\Program Files (x86)\AIMP\AIMP.exe"
If objShell.FileExists(aimp_path) Then
    objShell.Run """" & aimp_path & """"
    WScript.Quit
End If

' Пробуем найти AIMP в стандартном пути AIMP5
aimp_path = "C:\Program Files\AIMP5\AIMP.exe"
If objShell.FileExists(aimp_path) Then
    objShell.Run """" & aimp_path & """"
    WScript.Quit
End If

' Пробуем найти AIMP в Program Files (x86) AIMP5
aimp_path = "C:\Program Files (x86)\AIMP5\AIMP.exe"
If objShell.FileExists(aimp_path) Then
    objShell.Run """" & aimp_path & """"
    WScript.Quit
End If

' Если не найден в стандартных путях, пробуем запустить через ассоциацию файлов
objShell.Run "AIMP.exe", 0, False

On Error GoTo 0