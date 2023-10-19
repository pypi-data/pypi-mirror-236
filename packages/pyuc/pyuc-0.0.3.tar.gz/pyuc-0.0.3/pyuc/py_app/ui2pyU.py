import pyuc
from pyuc.py_api_b import PyApiB
if PyApiB.tryImportModule("PyQt5",installName="PyQt5,PyQt5-tools"):
    from PyQt5.uic import pyuic
    from PyQt5.QtWidgets import QMainWindow


class Ui2pyU(PyApiB):
    """
    PC界面相关工具
    # pip install -i https://mirrors.aliyun.com/pypi/simple/ PyQt5
    # pip install -i https://mirrors.aliyun.com/pypi/simple/ PyQt5-tools
    """
    @staticmethod
    def produce(key=None):
        return PyApiB._produce(key, __class__)

    def __init__(self):
        pass

    def compile(self, uiFile, pyFile):
        # import sys
        # if len(sys.argv) <= 1:
        #     sys.argv.append(uiFile)
        # else:
        #     sys.argv[1] = uiFile
        # if len(sys.argv) <= 2:
        #     sys.argv.append(pyFile)
        # else:
        #     sys.argv[2] = pyFile
        pyuc.cmdU("ui2py").run(f"'{pyuic.__file__}' {uiFile} {pyFile}")
        
