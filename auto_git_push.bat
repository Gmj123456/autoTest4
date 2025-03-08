@echo off
REM 确保在当前目录运行
cd /d %~dp0

REM 添加所有更改到暂存区
git add .
if %errorlevel% neq 0 (
    echo 执行 'git add .' 时出错
    pause
    exit /b %errorlevel%
)
echo 所有更改已添加到暂存区。

REM 提交更改
set commit_message=自动提交所有更改
git commit -m "%commit_message%"
if %errorlevel% neq 0 (
    echo 执行 'git commit' 时出错
    pause
    exit /b %errorlevel%
)
echo 更改已提交。

REM 推送更改
git push
if %errorlevel% neq 0 (
    echo 执行 'git push' 时出错
    pause
    exit /b %errorlevel%
)
echo 更改已推送到远程仓库。

pause    