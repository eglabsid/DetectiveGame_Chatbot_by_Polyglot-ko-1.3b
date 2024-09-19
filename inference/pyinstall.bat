
@echo off

REM Python 설치 버전 및 URL 설정
set PYTHON_VERSION=3.11.5
set PYTHON_INSTALLER=python-%PYTHON_VERSION%-amd64.exe
set DOWNLOAD_URL=https://www.python.org/ftp/python/%PYTHON_VERSION%/%PYTHON_INSTALLER%

REM Python 설치 파일 다운로드
echo Downloading Python %PYTHON_VERSION% installer...
powershell -Command "Invoke-WebRequest -Uri %DOWNLOAD_URL% -OutFile %PYTHON_INSTALLER%"

REM Python 설치
echo Installing Python %PYTHON_VERSION%...
start /wait %PYTHON_INSTALLER% /quiet InstallAllUsers=1 PrependPath=1 Include_test=0

REM 설치 파일 삭제
del %PYTHON_INSTALLER%

