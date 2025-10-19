' VBS скрипт для завершения всех программ и выключения компьютера через 5 секунд
' Автор: GitHub Copilot
' Дата: 19 октября 2025

Option Explicit

Dim objShell, objWMIService, colProcesses, objProcess
Dim strComputer, intCountdown

' Инициализация
strComputer = "."
Set objShell = CreateObject("WScript.Shell")
Set objWMIService = GetObject("winmgmts:" & "{impersonationLevel=impersonate}!\\" & strComputer & "\root\cimv2")

' Уведомление пользователя
MsgBox "ВНИМАНИЕ! Через 5 секунд компьютер будет выключен!" & vbCrLf & _
       "Все активные программы будут завершены.", vbExclamation + vbOKOnly, "Выключение системы"

' Завершение всех пользовательских процессов
WScript.Echo "Завершение активных программ..."

Set colProcesses = objWMIService.ExecQuery("SELECT * FROM Win32_Process WHERE SessionId > 0")

For Each objProcess in colProcesses
    ' Пропускаем системные процессы и критически важные
    If LCase(objProcess.Name) <> "explorer.exe" And _
       LCase(objProcess.Name) <> "winlogon.exe" And _
       LCase(objProcess.Name) <> "csrss.exe" And _
       LCase(objProcess.Name) <> "smss.exe" And _
       LCase(objProcess.Name) <> "wininit.exe" And _
       LCase(objProcess.Name) <> "services.exe" And _
       LCase(objProcess.Name) <> "lsass.exe" And _
       LCase(objProcess.Name) <> "svchost.exe" And _
       LCase(objProcess.Name) <> "dwm.exe" And _
       LCase(objProcess.Name) <> "wscript.exe" And _
       LCase(objProcess.Name) = "obs64.exe" And _
       LCase(objProcess.Name) = "chrome.exe" Then
        
        On Error Resume Next
        objProcess.Terminate()
        If Err.Number = 0 Then
            WScript.Echo "Завершен процесс: " & objProcess.Name
        End If
        On Error GoTo 0
    End If
Next

' Обратный отсчет с уведомлениями
For intCountdown = 5 To 1 Step -1
    WScript.Echo "Выключение через " & intCountdown & " секунд..."
    WScript.Sleep 1000
Next

' Принудительное выключение компьютера
WScript.Echo "Выключение компьютера..."
objShell.Run "shutdown /s /f /t 5", 0, False

' Освобождение объектов
Set objProcess = Nothing
Set colProcesses = Nothing
Set objWMIService = Nothing
Set objShell = Nothing

WScript.Echo "Команда выключения отправлена."