#将json按照传感器分开
from pathlib import Path
import json

def process_file(file, position, save_fp):
    bssid = ''
    with open(file, 'br') as fp, open (save_fp,'w')as save_fp:

        for ln, line_bytes in enumerate(fp, 1):
            try:
                line = line_bytes.decode("UTF-8")
            except UnicodeDecodeError:
                continue
            try:
                record = json.loads(line)
            except json.decoder.JSONDecodeError:
                continue
            #如果是第一行,确定传感器位置对应编号
            if record['type'] == "sensorbind":
                bind_infos = record['data']
                for bind_info in bind_infos:
                    if bind_info['position'] == position:
                        bssid = bind_info['bssid'].lower()
                        print(position+ '对应编号: ' + bssid)
                    else:
                        continue

                #如果是动作数据行,把该行的timestamp和value存下来
            elif record['type'] == "sensordata" and record['data']['bssid'] == bssid:
                record.pop('type')
                record['data'].pop('bssid')
                record['timestamp'] = int(record['timestamp']/1000)
                print(record)
                save_fp.write(str(record))

                #save_fp.write(str(int(record['timestamp']/1000))+","+str(record['data']['values'])+'\n')

            else:
                continue
        print(position+'已写入done\n')


if __name__ == "__main__":
    patient_path = Path("/Users/zhangyiming/PycharmProjects/ADHD-analysis/正常")
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
    bind_pos = ["LeftWrist", "RightWrist", "LeftAnkle", "RightAnkle", "Neck", "Waist"]

    i = 1
    print("=====正常=====")
    for person in patient_path.iterdir():
        if person.is_dir():

            print("=====姓名: {}=====".format(person.stem), i)
            i=i+1
            for scene in person.iterdir():
                if scene.stem in scenes:
                    print("=====场景: {}=====".format(scene_names[scene.stem]))
                    for data_file in scene.iterdir():
                        #判断是否为json文件
                        if data_file.suffix == ".json":
                            #为每个传感器位置循环一遍
                            for position in bind_pos:
                                #save_fp = scene /(position+'.csv')
                                save_fp = scene /(position+'.json')
                                process_file(data_file,position,save_fp)
                        else:
                            continue