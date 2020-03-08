from pathlib import Path
import json

from results import LimbConflictResult, FingerHolesResult, GrasshopperResult, ShapeColorInterferenceapeResult

LOG_LEVEL = 0


def dbgprint(dbgprint_s, level='I'):
    should_print = level == 'E' or \
                   level == 'W' and LOG_LEVEL > 0 or \
                   level == 'N' and LOG_LEVEL > 1 or \
                   level == 'I' and LOG_LEVEL > 2 or \
                   level == 'D' and LOG_LEVEL > 3
    if should_print:
        print('[' + level + ']' + dbgprint_s)


def limb_conflict(data):
    start_ts = 0
    q_dict = {'leftarm_red': "左手臂红色", 'rightarm_red': "右手臂红色",
              'leftarm_green': "左手臂绿色", 'rightarm_green': "右手臂绿色",
              'leftleg_red': "左腿红色", 'rightleg_red': "右腿红色",
              'leftleg_green': "左腿绿色", 'rightleg_green': "右腿绿色"}
    a_dict = {'leftarm_green': "左手臂抬起", 'rightarm_green': "右手臂抬起",
              'leftleg_green': "左腿抬起", 'rightleg_green': "右腿抬起"}
    l_dict = {2000: "简单", 1000: "普通", 500: "困难"}
    duration = 2000
    last_question = ""
    answered = False
    result = None

    for record in data:
        dbgprint(json.dumps(record), 'D')
        if record["type"] == "start":
            dbgprint("测试开始")
            start_ts = record["timestamp"] / 1000
            result = LimbConflictResult(0, 0, 0, 0, 0)
        if record["type"] == "question":
            ts = record["timestamp"] / 1000 - start_ts
            duration = record["data"]['duration']
            dbgprint("{:.3f}秒出现{}".format(ts, q_dict[record['data']["action"]]))
            last_question = record['data']["action"]
            answered = False
            if 'red' in last_question:
                result.red_question += 1
            else:
                result.green_question += 1
        if record["type"] == "answer":
            ts = record["timestamp"] / 1000 - start_ts
            dbgprint("{:.3f}秒{}".format(ts, a_dict[record['data']["action"]]))
            answer = record['data']["action"]
            if answered:
                dbgprint("{}已经产生动作".format(last_question))
                continue
            if answer == last_question:
                result.answer_green_right += 1
            elif 'red' in last_question:
                result.answer_red += 1
            else:
                result.answer_green_wrong += 1
            answered = True
        if record["type"] == "end":
            ts = record["timestamp"] / 1000 - start_ts
            dbgprint("{:.3f}秒结束，测试难度为{}".format(ts, l_dict[duration]))
            print("本次测试难度为{}".format(l_dict[duration]))
            print("整体正确率：{}".format(result.right_rate))
            print("整体错误率: {}".format(result.wrong_rate))
            print("遗漏率: {}".format(result.miss_rate))
            print("冲动率: {}".format(result.impulse_rate))


def finger_holes(data):
    start_ts = 0
    result = None
    for record in data:
        if record["type"] == "start":
            dbgprint("测试开始")
            start_ts = record["timestamp"] / 1000
            result = FingerHolesResult()
        if record["type"] == "question":
            ts = record["timestamp"] / 1000 - start_ts
            dbgprint("{:.3f}秒医生戳了洞{}".format(ts, record['data']['index']))
            result.question.append(record['data']['index'])
        if record["type"] == "answer":
            ts = record["timestamp"] / 1000 - start_ts
            dbgprint("{:.3f}秒儿童戳了洞{}".format(ts, record['data']['index']))
            result.answer.append(record['data']['index'])
        if record["type"] == "end":
            ts = record["timestamp"] / 1000 - start_ts
            dbgprint("{:.3f}秒结束".format(ts))
            if len(result.question):
                print("====={}洞测试=====".format(len(result.question)))
                print("医生戳洞: {}".format(result.pretty_question))
                print("儿童戳洞: {}".format(result.pretty_answer))
                print("乱序正确率: {}".format(result.disorder_right_rate))
                print("顺序正确率: {}".format(result.ordered_right_rate))
            else:
                dbgprint("No hole pressed!", "E")


def grasshopper(data):
    l_dict = {'1.20': "简单", '1.10': "普通", '1.05': "困难", '1.08': "困难"}

    start_ts = 0
    result = None
    threshold = None
    for record in data:
        if record["type"] == "start":
            dbgprint("测试开始")
            start_ts = record["timestamp"] / 1000
            result = GrasshopperResult()
        if record["type"] == "answer":
            ts = record["timestamp"] / 1000 - start_ts
            catched = record['data']['num'] > 0
            if catched:
                result.right += 1
            else:
                result.wrong += 1
            dbgprint("{:.3f}秒儿童出手{}蚂蚱".format(ts, "捉到了" if catched else "未捉到"))
            threshold = record['data']['threshold']
        if record["type"] == "end":
            ts = record["timestamp"] / 1000 - start_ts
            dbgprint("{:.3f}秒结束".format(ts))
            if threshold:
                print("====={}测试=====".format(l_dict[threshold]))
                print("捉住次数: {}".format(result.right))
                print("失手次数: {}".format(result.wrong))
                print("正确率: {}".format(result.right_rate))
            else:
                dbgprint("No threshold!", "E")


def shape_color_interferenceape(data):
    r_dict = {'color': "颜色", 'shape': "形状", 'both': "形状和颜色"}
    color_dict = {'red': "红色",
                  'green': "绿色",
                  'blue': "蓝色",
                  'orange': "橙色"}
    shape_dict = {'square': "正方形",
                  'triangle': "三角形",
                  'circular': "圆形",
                  'pentagon': "五边形"}

    start_ts = 0
    label_set = set()
    answer_count = 0
    result = None
    rule = None
    for record in data:
        if record["type"] == "start":
            dbgprint("测试开始")
            start_ts = record["timestamp"] / 1000
            answer_count = 0
            rule = None
            result = ShapeColorInterferenceapeResult()
        if record["type"] == "answer":
            ts = record["timestamp"] / 1000 - start_ts
            rd = record['data']
            if rd['label_color'] + rd['label_shape'] in label_set:
                dbgprint("Label {} already in box".format(rd['label_color'] + ' ' + rd['label_shape']), 'W')
                continue

            label_set.add(rd['label_color'] + rd['label_shape'])
            answer_count += 1
            rule = rd['rule']
            if rule == 'color':
                match = rd['label_color'] == rd['box_color']
            elif rule == 'shape':
                match = rd['label_shape'] == rd['box_shape']
            else:  # Both
                match = rd['label_color'] == rd['box_color'] and rd['label_shape'] == rd['box_shape']
            if match:
                result.right += 1
            else:
                result.wrong += 1
            dbgprint("{:.3f}秒儿童将{}{}投入了{}{}盒子".format(ts,
                                                      rd['label_color'], rd['label_shape'],
                                                      rd['box_color'],  rd['box_shape']))
        if record["type"] == "end":
            ts = record["timestamp"] / 1000 - start_ts
            dbgprint("{:.3f}秒结束".format(ts))
            if answer_count == 0:
                continue
            if rule:
                if rule in ['shape', 'color']:
                    result.total = 16
                else:
                    result.total = 4
                print("====={}测试=====".format(r_dict[rule]))
                print("正确次数: {}".format(result.right))
                print("错误次数: {}".format(result.wrong))
                print("正确率: {}".format(result.right_rate))
                print("遗漏率: {}".format(result.miss_rate))
            else:
                dbgprint("No rule!", "E")


def process_file(file, scene_name):
    with open(file, 'r', encoding="UTF-8") as fp:
        dbgprint("Filename: {}".format(file), 'D')
        data = []
        for ln, line in enumerate(fp, 1):
            try:
                record = json.loads(line)
            except json.decoder.JSONDecodeError:
                dbgprint("JSON Decode Fail! Line: {}, Data: {}".format(ln, line), "W")
            if record['type'] != "sensorbind" and record['type'] != "sensordata":
                data.append(record)

        if scene_name == "limb_conflict":
            limb_conflict(data)

        if scene_name == "finger_holes":
            finger_holes(data)

        if scene_name == "grasshopper":
            grasshopper(data)

        if scene_name == "shape_color_interference":
            shape_color_interferenceape(data)




if __name__ == "__main__":
    patient_path = Path("/Users/zhangyiming/PycharmProjects/ADHD/确诊")
    control_path = Path("/Users/zhangyiming/PycharmProjects/ADHD/正常")
    scenes = ['grasshopper', 'shape_color_interference', 'limb_conflict', 'finger_holes']
    scene_names = {
        'grasshopper': "捉蚂蚱",
        'shape_color_interference': "形色干扰",
        'limb_conflict': "肢体冲突",
        'finger_holes': "戳洞"
    }

    print("=======确诊=======")
    for person in patient_path.iterdir():
        if person.is_dir():
            print("=====姓名: {}=====".format(person.stem))
            for scene in person.iterdir():
                if scene.stem in scenes:
                    print("=====场景: {}=====".format(scene_names[scene.stem]))
                    for data_file in scene.iterdir():
                        process_file(data_file, scene.stem)
                    print()
            print("\n")

    print("=======正常=======")
    for person in control_path.iterdir():
        if person.is_dir():
            print("=======姓名: {}=======".format(person.stem))
            for scene in person.iterdir():
                if scene.stem in scenes:
                    print("=======场景: {}=======".format(scene_names[scene.stem]))
                    for data_file in scene.iterdir():
                        process_file(data_file, scene.stem)
                    print()
            print("\n")
            
            
            
            
            
            
            
            
            
            
            
            
            
            