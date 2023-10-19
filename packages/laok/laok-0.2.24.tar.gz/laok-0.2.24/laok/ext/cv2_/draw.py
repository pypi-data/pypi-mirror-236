#! /usr/bin/env python
# -*- coding: utf-8 -*-
'''
Created on 2023/7/11 20:36:06

@author: LiuKuan
@copyright: Apache License, Version 2.0
'''
import cv2
from laok.base.colors import color_rand
from .info import image_size, image_center
from .util import keep_int32
# ===============================================================================
r'''

绘制图元:
    line
    circle
    rectangle
    ellipse
    putText

常见参数:
    img：您要绘制形状的图像
    color：形状的颜色。
        对于BGR，将其作为元组传递，例如：(255,0,0)对于蓝色。
        对于灰度，只需传递标量值即可。
    thickness：线或圆等的粗细。
        如果对闭合图形（如圆）传递-1 ，它将填充形状。默认厚度= 1
    lineType：线的类型，是否为8连接线，抗锯齿线等。
        默认情况下，为8连接线。**cv.LINE_AA**给出了抗锯齿的线条，看起来非常适合曲线。
'''
# ===============================================================================
__all__ = [
            'draw_point',
            'draw_line', 'draw_polylines',
            'draw_rect',
            'draw_circle', 'draw_ellipse', 'draw_arc',
            'draw_text',
            'draw_contour', 'draw_contours'
]

def draw_point(img, pt=None, size=1, color=(255,255,255)):
    if pt is None: #默认使用中心点
        pt = image_center(img)
    return cv2.circle(img, center=keep_int32(pt), radius=int(size), color=color, thickness=-1, lineType=cv2.LINE_AA)


def draw_line(img, pt1, pt2, color=(255,255,255), thickness=1, lineType=cv2.LINE_AA):
    return cv2.line(img, pt1=keep_int32(pt1), pt2=keep_int32(pt2), color=color, thickness=thickness, lineType=lineType)

def draw_polylines(img, pts, isClosed=False, color=(255,255,255), thickness=1, lineType=cv2.LINE_AA):
    '''
    pts可以设置为 点列表: [[10,5],[20,30],[70,20],[50,10]]
    '''
    return cv2.polylines(img, pts=[ keep_int32(pts) ],
                         isClosed=isClosed, color=color, thickness=thickness, lineType=lineType)

def draw_rect(img, rect=None, color=(255,255,255), thickness=1, lineType=cv2.LINE_AA):
    if rect is None: #默认是图片的中心1/2大小
        w, h = image_size(img)
        rect = (w//4, h//4, w//2, h//2)
    return cv2.rectangle(img, rec=keep_int32(rect), color=color, thickness=thickness, lineType=lineType)

def draw_circle(img, center=None, radius= 5, color=(255,255,255), thickness=1, lineType=cv2.LINE_AA):
    if center is None: #默认使用中心点
        center = image_center(img)
    return cv2.circle(img, center=keep_int32(center), radius=int(radius), color=color, thickness=thickness, lineType=lineType)

def draw_ellipse(img, center=None, axes=(10, 5), angle=0,
                 color=(255,255,255), thickness=1, lineType=cv2.LINE_AA):
    if center is None:
        center = image_center(img)
    return cv2.ellipse(img, center= keep_int32(center), axes=keep_int32(axes), angle=angle,
                startAngle=0, endAngle=360,
                color=color, thickness=thickness, lineType=lineType)

def draw_arc(img, center=None, axes=(10, 5), angle=0, startAngle=0, endAngle=90,
             color=(255,255,255), thickness=1, lineType=cv2.LINE_AA):
    if center is None:
        center = image_center(img)
    return cv2.ellipse(img, center=center, axes=axes, angle=angle,
                startAngle=startAngle, endAngle=endAngle,
                color=color, thickness=thickness, lineType=lineType)

def draw_text(img, text='lk', pos=None, fontFace=cv2.FONT_HERSHEY_SIMPLEX, fontScale=1.0,
              color=(255,255,255), thickness=2, lineType=cv2.LINE_AA):
    if pos is None:
        pos = image_center(img)
    return cv2.putText(img, text=text, org=pos, fontFace=fontFace, fontScale=fontScale,
                color=color, thickness=thickness, lineType=lineType)

def draw_contour(img, contour, color=(255,255,255), thickness=2, lineType=cv2.LINE_AA):
    return cv2.drawContours(img, [contour], contourIdx=-1, color=color, thickness=thickness, lineType=lineType)

def draw_contours(img, contours, color=(255,255,255), thickness=2, lineType=cv2.LINE_AA):
    if color is None:
        for i, contour in enumerate(contours):
            draw_contour(img, contour, color=color_rand(i), thickness=thickness, lineType=lineType)
    else:
        return cv2.drawContours(img, contours, contourIdx=-1, color=color, thickness=thickness, lineType=lineType)