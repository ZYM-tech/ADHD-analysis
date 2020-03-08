from pathlib import Path
import json

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
    positions = {
        'Left_Wrist','Right_Wrist','Head','Left_Ankle','Right_Ankle','Waist'
    }

    print("=====确诊=====")
    for person in patient_path.iterdir():
        if person.is_dir():

            print("=====姓名: {}=====".format(person.stem))
            print("\n")

            for scene in person.iterdir():
                if scene.stem in scenes:
                    print("=====场景: {}=====".format(scene_names[scene.stem]))

                    for data_file in scene.iterdir():
                        
                        

                        print(data_file)

