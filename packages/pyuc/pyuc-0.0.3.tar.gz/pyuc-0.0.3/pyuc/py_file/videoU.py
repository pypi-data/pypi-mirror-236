# -*- coding: UTF-8 -*-
from pyuc.py_api_b import PyApiB
import os
if PyApiB.tryImportModule("ffmpy"):
    import ffmpy
if PyApiB.tryImportModule("moviepy"):
    from moviepy.editor import VideoFileClip, vfx


class VideoU(PyApiB):
    """
    视频文件格式相关工具
    """
    @staticmethod
    def produce(key=None):
        return PyApiB._produce(key, __class__)

    def __init__(self):
        pass

    def formatTo(self, videoPath, toVideoPath, rmEnd=False):
        ff = ffmpy.FFmpeg(inputs={videoPath: None},
                          outputs={toVideoPath: None})
        ff.run()
        if rmEnd:
            os.remove(videoPath)

    def flip(self, videoPath, savePath=None):
        """ 水平翻转 """
        if savePath == None:
            savePath = f"{videoPath}.flip.mp4"
        video = VideoFileClip(videoPath)
        out = video.fx(vfx.mirror_x)
        out.write_videofile(savePath)
