# -*- coding: UTF-8 -*-
import os, sys
import importlib
from py_api_b import PyApiB
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

def list_files(dir_path):
    return os.listdir(dir_path)

def delete_files_and_dirs(dir_path):
    if os.path.isdir(dir_path):
        file_list = list_files(dir_path)
        for file_name in file_list:
            file_path = os.path.join(dir_path, file_name)
            if os.path.isfile(file_path):
                os.remove(file_path)  # 删除文件
            elif os.path.isdir(file_path):
                delete_files_and_dirs(file_path)  # 递
        os.rmdir(dir_path)  # 删除子目录本身
    else:
        os.remove(dir_path)

def load_module(handlers):
    if handlers.__file__ == None:
        with open(f"pyuc/{handlers.__name__}/__init__.py", "w", encoding="utf-8") as f:
            f.write("# -*- coding: UTF-8 -*-\n")
        handlers = importlib.import_module(handlers.__name__, __package__)
    cwd = os.path.dirname(os.path.abspath(handlers.__file__))
    files = os.listdir(cwd)
    need_import = {}
    for i in files:
        if not i.startswith('_') and i.endswith('.py'):
            m = '.' + i[:-3]
            mdl = importlib.import_module(m, handlers.__package__)
            if "__all__" in mdl.__dict__:
                names = mdl.__dict__["__all__"]
            else:
                names = [x for x in mdl.__dict__ if not x.startswith("_")]
            need_import_cls = {}
            need_import_cls.update({k: getattr(mdl, k) for k in names})
            for c in need_import_cls:
                if hasattr(need_import_cls[c], '__mro__'):
                    if PyApiB.__name__ != need_import_cls[
                            c].__name__ and PyApiB.__name__ in list(map(lambda x:x.__name__, need_import_cls[c].__mro__)):
                        need_import[
                            need_import_cls[c].__module__] = need_import_cls[c]
    return need_import


def firstLower(str):
    return f"{str[:1].lower()}{str[1:]}"


def appendDoc(str, doc):
    str = f"{str}        '''\n"
    if doc == None:
        doc = ''
    docs = doc.split('\n')
    for d in docs:
        str = f"{str}        {d.lstrip()}\n"
    str = f"{str}        '''\n"
    return str


def printHelp():
    print('printHelp')


def reinitFile():
    __initPath = "pyuc/__init__.py"
    # delete_files_and_dirs(__initPath)
    with open(__initPath, "w", encoding="utf-8") as f:
        f.write("# -*- coding: UTF-8 -*-\n")
    initFile = "# -*- coding: UTF-8 -*-\n"
    pwd = os.path.dirname(os.path.abspath(__file__))
    fs = os.listdir(pwd)
    all_class = {}
    for i in fs:
        print(i, __package__)
        if os.path.isdir(f"{pwd}/{i}") and i.startswith('py_'):
            m = '.' + i
            mdl = importlib.import_module(i, __package__)
            all_class.update(load_module(mdl))
    for mcls_name in all_class:
        cls_name = all_class[mcls_name].__name__
        moduleName = mcls_name
        # print(moduleName)
        initFile = f"{initFile}try:\n"
        initFile = f"{initFile}    def {firstLower(cls_name)}(key=None):\n"
        initFile = appendDoc(initFile, all_class[mcls_name].__doc__)
        initFile = f"{initFile}        from pyuc.{moduleName} import {cls_name}\n\n"
        initFile = f"{initFile}        o:{cls_name} = {cls_name}.produce(key)\n"
        initFile = f"{initFile}        return o\n"
        initFile = f"{initFile}except ImportError as e:\n"
        initFile = f"{initFile}    pass\n\n"
    
    with open(__initPath, "w", encoding="utf-8") as f:
        f.write(initFile)


if __name__ == "__main__":
    option = '--help'
    if len(sys.argv) > 1:
        option = sys.argv[1]
    if option in ['-h','--help', '-H']:
        printHelp()
    elif option in ['-i','--init', '-I']:
        reinitFile()
