#! /usr/bin/env python
# -*- coding: utf-8 -*-
'''
Created on 2023/8/28 08:40:06

@author: LiuKuan
@copyright: Apache License, Version 2.0
'''
import imagesize
import laok
import laok.ext.lxml_ as lxml_
#===============================================================================
r'''
'''
#===============================================================================
__all__ = ['voc_to_yolo', 'yolo_to_voc', 'voc_fix_resize', 'voc_empty_remove', 'json_to_yolo']

def _read_xml(xml_file):
    vocs = {}
    root = lxml_.load_xml(xml_file)
    size = root.find('size')
    w = size.find('width').text
    h = size.find('height').text
    vocs['width'] = int(w)
    vocs['height'] = int(h)
    vocs['filename'] = root.find('filename').text
    obj_arr = []
    for obj in root.findall('object'):
        bndbox = obj.find('bndbox')
        xmin, xmax, ymin, ymax = bndbox.find('xmin').text, bndbox.find('xmax').text, \
            bndbox.find('ymin').text, bndbox.find('ymax').text
        obj_arr.append({
            'name': obj.find('name').text,
            'xmin': float(xmin),
            'xmax': float(xmax),
            'ymin': float(ymin),
            'ymax': float(ymax),
        })
    vocs['object'] = obj_arr
    return vocs

def _save_xml(xml_file, vocs):
    E = lxml_.get_maker()
    annotation = E.annotation(
        E.size(E.width(vocs['width']), E.height(vocs['height'])),
        E.filename(vocs['filename']),
    )
    for voc in vocs['object']:
        obj = E.object(
            E.name(voc['name']),
            E.bndbox( E.xmin(voc['xmin']), E.ymin(voc['ymin']), E.xmax(voc['xmax']), E.ymax(voc['ymax']) ),
        )
        annotation.append(obj)
    lxml_.save_xml(xml_file, annotation)

def _read_txt(txt_file):
    yolos = []
    for line in laok.file_read_lines(txt_file, strip=True, skip_empty=True):
        idx, cx, cy, rw, rh = line.split()
        data = int(idx), float(cx), float(cy), float(rw), float(rh)
        yolos.append( data )
    return yolos

def _box_to_voc(imgsz, cx, cy, rw, rh):
    cx, cy, rw, rh = float(cx), float(cy), float(rw), float(rh)
    w,h = imgsz
    w2 = w * rw
    h2 = h * rh
    x1 = cx * w - w2/2
    y1 = cy * h - h2/2
    x2 = x1 + w2
    y2 = y1 + h2
    return round(x1), round(y1), round(x2), round(y2)

def _box_to_yolo(w, h, xmin, ymin, xmax, ymax):
    dw = 1. / w
    dh = 1. / h
    cx = ( (xmin + xmax) / 2.0 )*dw
    cy = ( (ymin + ymax) / 2.0 )*dh
    rw = (xmax - xmin) * dw
    rh = (ymax - ymin) * dh
    return cx, cy, rw, rh

def _data_to_yolo(xml_file, nameIdx):
    txt_file = laok.path_replace_ext(xml_file, '.txt')
    with open(txt_file, mode='w', encoding='utf8') as f:
        vocs = _read_xml(xml_file)
        w = vocs['width']
        h = vocs['height']
        for obj in vocs['object']:
            name = obj['name']
            idx = nameIdx.getIndex(name)
            assert idx != -1 and f"{xml_file} can't find [{name}]"
            cx, cy, rw, rh = _box_to_yolo(w, h,
                                        obj['xmin'], obj['ymin'],
                                        obj['xmax'], obj['ymax'])
            f.write(f"{idx} {cx} {cy} {rw} {rh}\n")

def _data_to_voc(img_file, nameIdx):
    txt_file = laok.path_replace_ext(img_file, ".txt")
    if not laok.path_exist(txt_file):
        return

    imgsz = imagesize.get(img_file)
    w, h = imgsz

    vocs = {}
    vocs['width'] = w
    vocs['height'] = h
    vocs['filename'] = laok.path_basename(img_file)
    obj_arr = []
    vocs['object'] = obj_arr
    for idx, cx, cy, rw, rh in _read_txt(txt_file):
        name = nameIdx.getName(idx)
        assert name and f"{txt_file} can't find [{idx}]"
        x1, y1, x2, y2 = _box_to_voc(imgsz, cx, cy, rw, rh)
        obj_arr.append({
            'name':name,
            'xmin': x1,
            'ymin': y1,
            'xmax': x2,
            'ymax': y2,
        })
    _save_xml(txt_file, vocs)

def _voc_fix(img_file):
    xml_file = laok.path_replace_ext(img_file, ".xml")
    if not laok.path_exist(xml_file):
        return

    imgsz = imagesize.get(img_file)
    w, h = imgsz
    vocs = _read_xml(xml_file)

    w2, h2 = vocs['width'], vocs['height']
    if w2 == w and h2 == h:
        return

    dw = w / w2
    dh = h / h2
    vocs['width'] = w
    vocs['height'] = h
    for voc in vocs['object']:
        voc['xmin'] = int(voc['xmin'] * dw)
        voc['xmax'] = int(voc['xmax'] * dw)
        voc['ymin'] = int(voc['ymin'] * dh)
        voc['ymax'] = int(voc['ymax'] * dh)
    _save_xml(xml_file, vocs)

def _voc_remove_empty(img_file):
    #如果没有xml或则txt,则删除img_file
    txt_file = laok.path_replace_ext(img_file, 'txt')
    xml_file = laok.path_replace_ext(img_file, 'xml')

    if laok.path_exist(xml_file):
        vocs = _read_xml(xml_file)
        if len(vocs['object']) == 0:
            laok.file_delete(img_file)
            laok.file_delete(xml_file)
            laok.file_delete(txt_file)
            print(f'empty xml label, del: {img_file}')
    elif laok.path_exist(txt_file):
        yolos = _read_txt(txt_file)
        if len(yolos) == 0:
            laok.file_delete(img_file)
            laok.file_delete(txt_file)
            print(f'empty txt label, del: {img_file}')
    else:
        laok.file_delete(img_file)
        print(f'no label file, del: {img_file}')


def voc_to_yolo(data_dir, name_file):
    nameIdx = laok.NameIndexFile(name_file)
    for xml_file in laok.files_under(data_dir, ".xml"):
        _data_to_yolo(xml_file, nameIdx)

def yolo_to_voc(data_dir, name_file):
    nameIdx = laok.NameIndexFile(name_file)
    for img_file in laok.image_under(data_dir):
        _data_to_voc(img_file, nameIdx)


def voc_fix_resize(data_dir):
    for img_file in laok.image_under(data_dir):
        _voc_fix(img_file)

def voc_empty_remove(data_dir):
    for img_file in laok.image_under(data_dir):
        _voc_remove_empty(img_file)

def json_to_yolo(data_dir):
    pass