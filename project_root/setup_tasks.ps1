$python_exe = python -c "import sys; print(sys.executable)"
$project_path = "C:\Users\User\Downloads\SIMULATIVE\Final_project_Automatization\project_root"

Write-Host "Python: $python_exe"
Write-Host "Project: $project_path"

# Очистка
Unregister-ScheduledTask -TaskName "GenerateSalesData" -Confirm:$false -ErrorAction SilentlyContinue
Unregister-ScheduledTask -TaskName "LoadToDB" -Confirm:$false -ErrorAction SilentlyContinue

# BAT пути
$bat_generate = "$project_path\run_generate.bat"
$bat_database = "$project_path\run_database.bat"
$principal = New-ScheduledTaskPrincipal -UserId "SYSTEM" -LogonType ServiceAccount -RunLevel Highest

# Генерация
$trigger1 = New-ScheduledTaskTrigger -Weekly -DaysOfWeek Monday,Tuesday,Wednesday,Thursday,Friday,Saturday -At "10:30"
$action1 = New-ScheduledTaskAction -Execute $bat_generate
Register-ScheduledTask -TaskName "GenerateSalesData" -Action $action1 -Trigger $trigger1 -Principal $principal -Force

# БД
$trigger2 = New-ScheduledTaskTrigger -Weekly -DaysOfWeek Monday,Tuesday,Wednesday,Thursday,Friday,Saturday -At "10:45"
$action2 = New-ScheduledTaskAction -Execute $bat_database
Register-ScheduledTask -TaskName "LoadToDB" -Action $action2 -Trigger $trigger2 -Principal $principal -Force

Write-Host "BAT is created!"

