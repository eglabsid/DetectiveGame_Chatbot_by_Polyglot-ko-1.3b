#!/bin/bash

if [[ $(uname) == "Darwin" ]]; then
  echo "This is a Mac OS system"
elif [[ $(uname) == "Linux" ]]; then
  echo "This is a Linux system"
else
  echo "This is a Window OS system"
fi

python_path=$(which python3)

export PYTHON_PATH=$python_path

# 설정 확인
echo "Python 설치 경로: $PYTHON_PATH"


# 설치할 Python 버전
python_version="3.11.5"

# 운영체제 판별 및 설치 명령어 설정
if [[ -f /etc/os-release ]]; then
  # 대부분의 Linux 배포판
  os=$(cat /etc/os-release | grep ID= | cut -d= -f2)
  if [[ $os == "ubuntu" || $os == "debian" ]]; then
    # Ubuntu, Debian
    install_cmd="sudo apt update && sudo apt install python$python_version"
  elif [[ $os == "centos" || $os == "rhel" ]]; then
    # CentOS, RHEL
    install_cmd="sudo yum install python$python_version"
  else
    echo "지원되지 않는 Linux 배포판입니다."
    exit 1
  fi
elif [[ -e /System/Library/Frameworks/Python.framework ]]; then
  # macOS
  install_cmd="brew install python@$python_version"
fi

# Python 설치 여부 확인
if ! command -v python$python_version &> /dev/null; then
  # Python이 설치되어 있지 않으면 설치 진행
  echo "Python $python_version이 설치되어 있지 않습니다. 설치를 진행합니다..."
  $install_cmd
else
  echo "Python $python_version이 이미 설치되어 있습니다."
fi

# 가상 환경 이름
venv_name="venv"

# 가상 환경 생성 (만약 존재하지 않으면)
if [ ! -d "$venv_name" ]; then
  python3 -m ve+-nv $venv_name
fi

# 가상 환경 활성화
source $venv_name/bin/activate

# requirements.txt 파일을 이용하여 패키지 설치
pip install -r requirements.txt

pip install --upgrade pip

python_file="main.py"

# Python 스크립트 실행 예시
python $python_file