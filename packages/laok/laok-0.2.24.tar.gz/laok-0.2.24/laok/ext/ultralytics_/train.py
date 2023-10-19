#! /usr/bin/env python
# -*- coding: utf-8 -*-
'''
Created on 2023/5/4 20:27:02
@author: LiuKuan
@copyright: Apache License, Version 2.0
'''
import os
import shutil

import laok
from laok.ext.cv2_.io import fix_cv_read
from laok.ext.yaml_ import save_yaml_file
from laok import log_info
from ultralytics import YOLO
#===============================================================================
r'''支持 yolo训练的脚本
需要 文件夹 root_dir下:
                ---- xxx.pt
                ---- xxx.names
                ---- Image/
'''
#===============================================================================
__all__ = ['train_det', 'export_onnx']

def _gen_data():
    dataset = laok.Dict()
    dataset.path = os.getcwd()
    dataset.train = 'Image'
    dataset.val = 'Image'
    dataset.test = None
    names_file = laok.path_search_cur_ext('.', ".names")
    dataset.names = list(laok.file_read_lines(names_file))
    data_file = laok.path_replace_ext(names_file, ".yaml")
    save_yaml_file(data_file, dataset, indent=4, encoding='utf8')
    # 删除cache文件
    cache_file = laok.path_search_under_ext('Image', ".cache")
    if cache_file:
        laok.file_delete(cache_file)
    log_info(f'save yaml file= {data_file}')
    return data_file

def export_onnx(in_file, imgsz, out_file=None):
    model2 = YOLO(in_file)
    model2.export(format='onnx', opset=12, dynamic = False, imgsz=imgsz)
    onnx_model = laok.path_replace_ext(in_file, 'onnx')
    log_info(f'export onnx file= {onnx_model}')
    if out_file:
        shutil.copyfile(onnx_model, out_file)

def train_det(root_dir, model_file=None, imgsz=(512, 1248), epochs=100, batch=16, **kws):
    log_info(f'root_dir= {root_dir}')
    fix_cv_read()
    with laok.workdir_scope(root_dir):
        if model_file is None:
            model_file = laok.path_search_cur_ext('.', ".pt")
        model_file = laok.path_abs(model_file)
        log_info(f'model_file= {model_file}')
        data_file = _gen_data()
        log_info(f'data_file= {data_file}' )

        # 训练
        model_name = laok.path_basename(model_file)
        model = YOLO(model_file)
        kws['task'] = 'detect'
        kws['data'] = data_file
        kws['epochs'] = epochs
        kws['imgsz'] = imgsz
        kws['batch'] = batch
        kws['format'] = 'onnx'
        kws['opset'] = 12
        kws.setdefault('save_txt', True)
        kws.setdefault('save_conf', True)
        kws.setdefault('save_crop', True)
        kws.setdefault('amp', False)
        kws.setdefault('degrees', 3)
        if laok.is_windows():
            kws.setdefault('workers', 0)
        model.train(**kws)

        # 导出onnx
        best_model = laok.path_search_under_file(str(model.trainer.wdir), 'best.pt')
        export_onnx(best_model, imgsz)
