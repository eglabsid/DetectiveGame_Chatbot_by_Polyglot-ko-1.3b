@echo off

REM 가상 환경을 생성할 디렉토리 설정
set VENV_DIR=%~dp0venv

REM 가상 환경 활성화
echo Activating the virtual environment...
call %VENV_DIR%\Scripts\activate

REM 가상 환경 활성화 확인
if "%VIRTUAL_ENV%"=="" (
    echo Failed to activate the virtual environment.
    exit /b 1
) else (
    echo Virtual environment activated successfully.
    echo Your virtual environment is now active. Run 'deactivate' to exit the virtual environment.
)

REM Transformers 서버 실행
python %~dp0main.py


