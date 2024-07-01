@echo off
:: 获取当前批处理文件所在目录
set "MY_HOME_DIR=%~dp0"

:: 打开三个命令行窗口并执行指定命令，自动识别当前目录

:: 第一个窗口
start cmd /k "cd /d %MY_HOME_DIR%myhome & workon pyspider & python .\run.py -c .\conf_prod.json"

echo 所有任务已启动.
pause