#成功将json按照传感器分开
from pathlib import Path
import json
import os,sys

def process_file(file,scene,position):
    with open(file, 'rb') as fp:

        a = str(scene) +'/'+ position+'.json'
        w = open(a, 'w')

       # dbgprint("Filename: {}".format(file, 'D'))
        data = []
        for ln, line in enumerate(fp, 1):
            try:
                #position = position.encode()
                if bytes(position,'UTF-8') in line:
                    print(line)
                    line = str(line)
                    w.write(line)
            except json.decoder.JSONDecodeError:
                dbgprint("JSON Decode Fail! Line: {}, Data: {}".format(ln, line), "W")







if __name__ == "__main__":
    patient_path = Path("/Users/zhangyiming/PycharmProjects/ADHD/确诊")
    scenes = ['grasshopper', 'shape_color_interference', 'limb_conflict', 'finger_holes', 'balance_test',
              'schulte_grid', 'objects_tracking', 'feed_birds_water', 'catch_worms']
    scene_names = {
        'grasshopper': "捉蚂蚱",
        'shape_color_interference': "形色干扰",
        'limb_conflict': "肢体冲突",
        'finger_holes': "戳洞",
        'balance_test': "乒乓球平衡",
        'schulte_grid': "舒尔特方格",
        'objects_tracking': "找小球",
        'feed_birds_water': "小鸟喂水",
        'catch_worms': "苹果捉虫"
    }

    #问张腾怎样获取json数组里某对象的某属性值(已知position返回bssid值)
    positions = ['47000000e103','47000000e303','47000000e203','47000000e403','47000000e503','470000032203']
    
    
    
    i = 1
    print("=====确诊=====")
    for person in patient_path.iterdir():
        if person.is_dir():
            print("\n")

            print("=====姓名: {}=====".format(person.stem), i)
            i=i+1


            for scene in person.iterdir():
                if scene.stem in scenes:
                    print("=====场景: {}=====".format(scene_names[scene.stem]))

                    #print(scene)

                    for data_file in scene.iterdir():
                        print("\n")
                        #此处可以加判断,是否为json文件

                        #为每个传感器位置循环一遍
                        for position in positions:
                            #process_file(data_file,scene,position)
                            print(position, data_file)








