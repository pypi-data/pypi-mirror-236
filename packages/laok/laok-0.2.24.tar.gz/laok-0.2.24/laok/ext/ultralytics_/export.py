#! /usr/bin/env python
# -*- coding: utf-8 -*-
'''
Created on 2023/8/11 12:35:20

@author: LiuKuan
@copyright: Apache License, Version 2.0
'''
import laok
import shutil
from ultralytics import YOLO
# ===============================================================================
r'''
'''
# ===============================================================================
__all__ = ['export_onnx']

def export_onnx(src_file, imgsz, dst_file=None):
    model2 = YOLO(src_file)
    model2.export(format='onnx', opset=12, dynamic=False, imgsz=imgsz)
    onnx_model = laok.path_replace_ext(src_file, 'onnx')
    if dst_file:
        shutil.copy(onnx_model, dst_file)
