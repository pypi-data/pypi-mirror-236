# -*- coding: UTF-8 -*-
import importlib, subprocess


class PyApiB:
    """
    所有需要对外提供的类，都需要承继此类
    """
    instances = {}

    @staticmethod
    def _produce(key, cls):
        if not key:
            key = f"{cls.__name__}_default"
        else:
            key = f"{cls.__name__}{key}"
        if key not in PyApiB.instances:
            PyApiB.instances[key] = cls()
        v:cls = PyApiB.instances[key]
        return v
    
    @staticmethod
    def tryImportModule(moduleName:str, installName:str=None, source="https://mirrors.aliyun.com/pypi/simple/"):
        if installName == None:
            installName = moduleName
        try:
            importlib.import_module(moduleName)
        except ImportError:
            installNames = [installName]
            if "," in installName:
                installNames = installName.split(",")
            args = ["pip", "install",
                    # "-i", source,
                    *installNames]
            try:
                subprocess.check_call(args)
                print(f"pip install Successfull! ModuleName=[{installName}]")
                return True
            except subprocess.CalledProcessError:
                print(f"pip install ERROR! ModuleName=[{installName}]")
                return False
        return True


    def __init__(self):
        pass
