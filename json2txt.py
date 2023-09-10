"""
    将yolo标注的annotation从json文件形式转为txt文件形式
"""

import json
import numpy

with open('./annotations.json') as f:
    j = json.load(f)
    # print (j['images'][0]['width'])
    label_id = 0
    for i in range (63):
        file_name = (j['images'][i]['file_name']).split('.')[0]
        out_file = open('./label_txt\%s.txt' % (file_name), 'w')

        for h in range(10):
            if j['annotations'][label_id + h]['image_id'] == i+1:
                l = j['annotations'][label_id + h]['bbox'][0]
                t = j['annotations'][label_id + h]['bbox'][1]
                w = j['annotations'][label_id + h]['bbox'][2]
                h = j['annotations'][label_id + h]['bbox'][3]
                xx = (l + w/2)/640
                yy = (t + h/2)/360
                ww = w/640
                hh = h/360
                out_file.write("1 " + str(xx) + " " + str(yy) + " " + str(ww) + " " + str(hh) + '\n')
            else:
                label_id += h
                break