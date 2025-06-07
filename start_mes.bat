@echo off

for /f "tokens=5" %%a in ('netstat -ano ^| findstr ":5000 "') do (
    set pid=%%a
    taskkill /PID !pid! /F
    goto :done
)
:done
start D:\python_workspace\equipment_sequence\.venv\Scripts\pythonw.exe D:\python_workspace\equipment_sequence\main.py
exit