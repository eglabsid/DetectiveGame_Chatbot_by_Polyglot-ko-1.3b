
import os
import io

import json
import re

from typing import Optional, Sequence, Union
import os.path as osp


import traceback
from queue import Queue
from threading import Thread

# [JKC:20240408-1354] 한글 지원을 위한, 파일 인코딩 적용
def _make_w_io_base(f, mode: str, encoding: str):
    if not isinstance(f, io.IOBase):
        f_dirname = os.path.dirname(f)
        if f_dirname != "":
            os.makedirs(f_dirname, exist_ok=True)
        f = open(f, mode=mode, encoding=encoding)
    return f


def _make_r_io_base(f, mode: str, encoding: str):
    if not isinstance(f, io.IOBase):
        f = open(f, mode=mode, encoding=encoding)
    return f


def jdump(obj, f, mode="w", encoding="utf-8", indent=4, default=str):
    """
    문자열 또는 사전을 json 형식의 파일로 덤프합니다.

    Args:
        obj: 쓰여질 객체
        f: 디스크 위치에 대한 문자열 경로입니다.
        mode: 파일을 여는 모드입니다.
        indent: json 사전을 저장하기 위한, 들여쓰기 사이즈
        default: 직렬화할 수 없는 항목을 처리하는 함수입니다. 기본값은 'str'입니다.
    """
    f = _make_w_io_base(f, mode, encoding)
    if isinstance(obj, (dict, list)):
        json.dump(obj, f, indent=indent, default=default)
    elif isinstance(obj, str):
        f.write(obj)
    else:
        raise ValueError(f"Unexpected type: {type(obj)}")
    f.close()


def jload(f, mode="r", encoding="utf-8"):
    """
    .json 파일을 사전에 로드합니다.
    """
    f = _make_r_io_base(f, mode, encoding)
    jdict = json.load(f)
    f.close()
    return jdict

class Prompter(object):
    __slots__ = ("template", "_verbose")

    def __init__(self, template_name: str = "", verbose: bool = False):
        self._verbose = verbose
        # if not template_name:
            # template_name = "polyglot-ko"   # 여기에 기본값을 적용하면, 생성자가 ''로 호출될 수 있는데, 중단되지 않습니다.
        
        # file_name = osp.join("templates", f"{template_name}.json")
        file_name = template_name
        if not osp.exists(file_name):
            raise ValueError(f"Can't read {file_name}")
        # [JKC:20240406-1107] 한글 지원을 위한, 파일 인코딩 적용
        with _make_r_io_base(file_name, "r", "utf-8") as fp:
            self.template = json.load(fp)
        if self._verbose:
            print(
                f"Using prompt template {template_name}: {self.template['description']}"
            )

    def generate_ask(
        self,
        instruction: str,
        input: Union[None, str] = None
    ) -> str:
        pattern = r"\{[^}]*\}"
        if instruction:
            if input:
                return re.sub(pattern=pattern, repl=input, string=instruction)
            return instruction
        else:
            return input

    def generate_prompt(
        self,
        instruction: str,
        input: Union[None, str] = None,
        label: Union[None, str] = None,
    ) -> str:
        # 명령 및 선택적 입력에서 전체 프롬프트를 반환합니다.
        # 레이블(=response, =output)이 제공되면, 레이블도 추가됩니다.
        if input:
            res = self.template["prompt_input"].format(
                instruction=instruction, input=input
            )
        else:
            res = self.template["prompt_no_input"].format(
                instruction=instruction
            )
        if label:
            res = f"{res}{label}"
        if self._verbose:
            print(res)
        return res

    def get_response(self, output: str) -> str:
        return output.split(self.template["response_split"])[1].strip()
    

class Iteratorize:
    """
    콜백을 게으른 반복자(생성기)로 변환하는 함수를 변환합니다.
    """

    def __init__(self, func, kwargs={}, callback=None):
        self.mfunc = func
        self.c_callback = callback
        self.q = Queue()
        self.sentinel = object()
        self.kwargs = kwargs
        self.stop_now = False

        def _callback(val):
            if self.stop_now:
                raise ValueError
            self.q.put(val)

        def gentask():
            try:
                ret = self.mfunc(callback=_callback, **self.kwargs)
            except ValueError:
                pass
            except:
                traceback.print_exc()
                pass

            self.q.put(self.sentinel)
            if self.c_callback:
                self.c_callback(ret)

        self.thread = Thread(target=gentask)
        self.thread.start()

    def __iter__(self):
        return self

    def __next__(self):
        obj = self.q.get(True, None)
        if obj is self.sentinel:
            raise StopIteration
        else:
            return obj

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.stop_now = True
