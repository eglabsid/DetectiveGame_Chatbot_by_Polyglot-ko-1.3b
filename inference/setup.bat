@echo off

REM Python 및 pip 설치 확인, 설치시 추가 설치 체크 필요
py --version >nul 2>&1 
if %ERRORLEVEL% neq 0 (
    echo Setting installation of python ... 
    call %~dp0pyinstall.bat
)

REM 설치 확인
py --version
if %ERRORLEVEL% neq 0 (
    echo Python installation failed.
    exit /b 1
) else (
    echo Python %PYTHON_VERSION% installed successfully.
)

echo Setting venv ...
call %~dp0pyvenv.bat

pip --version >nul 2>&1
if %ERRORLEVEL% neq 0 (
    echo pip is not installed or not found in PATH. Attempting to install pip...
    python -m ensurepip --upgrade 
)

REM 필요한 패키지 설치 (필요 시)
%~dp0venv/Scripts/python -m pip install --upgrade pip

REM 설치할 패키지 이름 설정
set PACKAGE_NAME=requirements.txt

REM pip 명령어로 패키지 설치
echo Installing %~dp0%PACKAGE_NAME% using pip...
pip install -r %~dp0%PACKAGE_NAME%

@REM pip3 install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118
@REM pip3 install torch torchvision torchaudio

pip3 install optimum onnx onnxruntime


