# -*- coding: utf-8 -*-
'''
@Time          : 20/04/25 15:49
@Author        : huguanghao
@File          : demo.py
@Noice         :
@Modificattion :
    @Author    :
    @Time      :
    @Detail    :
'''

# import sys
# import time
# from PIL import Image, ImageDraw
# from models.tiny_yolo import TinyYoloNet
from tool.utils import *
from tool.torch_utils import *
from tool.darknet2pytorch import Darknet
import argparse
from tool.draw_trajectory import *
from pathlib import Path

"""hyper parameters"""
use_cuda = True

dribble_type = -1

def detect_cv2_video(cfgfile, weightfile, videofile):
    import cv2
    import math
    import numpy as np
    import numpy.linalg as LA

    m = Darknet(cfgfile)

    m.print_network()
    m.load_weights(weightfile)
    print('Loading weights from %s... Done!' % (weightfile))

    if use_cuda:
        m.cuda()

    cap = cv2.VideoCapture(videofile)
    cap.set(3, 1280)
    cap.set(4, 720)
    print("Starting the YOLO loop...")

    num_classes = m.num_classes
    if num_classes == 20:
        namesfile = 'data/voc.names'
    elif num_classes == 80:
        namesfile = 'data/coco.names'
    else:
        namesfile = 'data/x.names'
    class_names = load_class_names(namesfile)

    invideo_name = str(videofile).replace("data/", "").replace(".mp4", "")
    result_path = "Cutclip/" + str(videofile).replace("data/", "").replace(".mp4", "")
    Path(result_path).mkdir(parents=True, exist_ok=True)
    result_txt = result_path + "/bbox.txt"
    f = open(result_txt, 'w')

    # 判別輸入影片種類
    if "SH" in invideo_name:
        dribble_type = "SH"
        print("單手運球")
    elif "CO" in invideo_name:
        dribble_type = "CO"
        print("換手運球")
    elif "BH" in invideo_name:
        dribble_type = "BH"
        print("背後運球")
    elif "BL" in invideo_name:
        dribble_type = "BL"
        print("胯下運球")
    elif "LP" in invideo_name:
        dribble_type = "LP"
        print("低運球")


    fourcc = cv2.VideoWriter_fourcc('M', 'P', '4', 'V')
    

    id = 0
    
    changes = 0
    last_centerx, last_centery = 0, 0
    coordList = []
    imgList = []
    bounce = False
    cutframe = -1    # 記錄從哪一個 frame 點截斷
    startcut = False
    loop = 0            # 一次 bounce 為一次 loop


    

    wave = 0
    # 波峰 crest
    # 波谷 trough
    wave_type = "none"

    while cap.isOpened():
        ret, img = cap.read()   
        sized = cv2.resize(img, (m.width, m.height))
        sized = cv2.cvtColor(sized, cv2.COLOR_BGR2RGB)

        start = time.time()
        boxes = do_detect(m, sized, 0.4, 0.6, use_cuda) # do_detect 定義於 torch_utils.py
        finish = time.time()
        print('Predicted in %f seconds.' % (finish - start))

        # 取得 person bounding box 左上、右下兩點
        print(boxes)
        point_1x, point_1y = boxes[0][0][0]*1280, boxes[0][0][1]*720
        point_2x, point_2y = boxes[0][0][2]*1280, boxes[0][0][3]*720
        bbox_centerx, bbox_centery = (point_1x + point_2x)/2, (point_1y + point_2y)/2
        coordList.append({"x" : bbox_centerx, "y": bbox_centery})
        imgList.append({"id": id, "image":img})

        
        if(id < 2):
            pass
        else:
            p1_y = coordList[id].get("y")   # 最新
            p2_y = coordList[id-1].get("y") # 舊
            p3_y = coordList[id-2].get("y") # 最舊

            # 如果 v1 v2 是 + 代表往下走，如果 v1 v2 是 - 代表下上走
            v1 = p1_y - p2_y # 新
            v2 = p2_y - p3_y # 舊

            # 如果 兩個 異號 代表達波峰或波谷
            if(v1 * v2 < 0):
                wave = wave + 1
                # 波峰 crest
                # 波谷 trough
                # wave_type = "none"
                if(v1 < 0 and v2 > 0): # v1 向上走 波谷
                    wave_type = "trough"
                    print(("Frame " + str(id-1) + "發生波谷"), file = f)
                if(v1 > 0 and v2 < 0):
                    wave_type = "crest"
                    print(("Frame " + str(id-1) + "發生波峰"), file = f)
            

            if(wave == 1 and wave_type == "trough"):
                startcut = False
                wave = 0
            elif(wave == 1 and wave_type == "crest" and startcut == False):
                startcut = True
                print(("Frame " + str(id-1) + "發生初次波峰 ==================="), file = f)
                cut_video = result_path + "/" + invideo_name + "_sf_" + str(id-1) + ".mp4"
                cutvideo = cv2.VideoWriter(cut_video, fourcc, 20.0, (1280, 720))
            
            # 確保起頭為波峰
            if(startcut == True):
                cutvideo.write(imgList[id-1].get("image"))
                # 寫入最後 1 frame，換下一隻影片

                # 雙手運球
                if((dribble_type == "CO" or dribble_type == "BH" or dribble_type == "BL") and wave == 5):
                    wave = 0
                    startcut = False

                # 單手運球
                if((dribble_type == "SH" or dribble_type == "LP") and wave == 3):
                    wave = 0
                    startcut = False


       

        # framename = result_path + "/" + invideo_name + "frame_save_" + str(id) + ".jpg"
        # cv2.imwrite(framename, img)


        # result_img = plot_boxes_cv2(img, boxes[0], savename=None, class_names=class_names)

        id = id + 1
        cv2.imshow('Yolo demo', img)
        cv2.waitKey(1)

    cap.release()

def get_args():
    parser = argparse.ArgumentParser('Test your image or video by trained model.')
    parser.add_argument('-cfgfile', type=str, default='./cfg/yolov4.cfg',
                        help='path of cfg file', dest='cfgfile')
    parser.add_argument('-weightfile', type=str,
                        default='./checkpoints/Yolov4_epoch1.pth',
                        help='path of trained model.', dest='weightfile')
    parser.add_argument('-imgfile', type=str,
                        default='./data/mscoco2017/train2017/190109_180343_00154162.jpg',
                        help='path of your image file.', dest='imgfile')
    args = parser.parse_args()

    return args


if __name__ == '__main__':
    args = get_args()
    if args.imgfile:
        detect_cv2_video(args.cfgfile, args.weightfile, args.imgfile)
    else:
        detect_cv2_camera(args.cfgfile, args.weightfile)
