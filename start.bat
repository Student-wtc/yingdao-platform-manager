@echo off
chcp 65001
echo ========================================
echo    影刀可视化调度神器 启动脚本
echo ========================================
echo.
echo 正在检查Python环境...
python --version
if errorlevel 1 (
    echo 错误: 未找到Python环境，请先安装Python 3.7+
    pause
    exit /b 1
)

echo.
echo 正在检查依赖包...
pip show flask >nul 2>&1
if errorlevel 1 (
    echo 正在安装依赖包...
    pip install -r requirements.txt
    if errorlevel 1 (
        echo 错误: 依赖包安装失败
        pause
        exit /b 1
    )
) else (
    echo 依赖包检查完成
)

echo.
echo 正在启动Web服务器...
echo 请在浏览器中访问: http://localhost:5000
echo 按 Ctrl+C 停止服务器
echo.
python app.py

echo.
echo 服务器已停止
pause