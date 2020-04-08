
#计算测试得分并写入score.txt里
from pathlib import Path
import json

# 从result.py获得函数
from results import BalanceTestResult, LimbConflictResult, FingerHolesResult, GrasshopperResult, \
    ShapeColorInterferenceapeResult, SchulteGridResult, ObjectsTrackingResult, ReadContentResult, \
    CatchWormsResult, FeedBirdsWaterResult

LOG_LEVEL = 0


def dbgprint(dbgprint_s, level='I'):
    should_print = level == 'E' or \
                   level == 'W' and LOG_LEVEL > 0 or \
                   level == 'N' and LOG_LEVEL > 1 or \
                   level == 'I' and LOG_LEVEL > 2 or \
                   level == 'D' and LOG_LEVEL > 3
    if should_print:
        print('[' + level + ']' + dbgprint_s)


def balance_test(data,save_path):
    with open (save_path,'w')as score_path:
        start_ts = 0
        result = None
        for record in data:
            if record["type"] == "start":
                dbgprint("测试开始")
                start_ts = record["timestamp"] / 1000
                result = BalanceTestResult()
            if record["type"] == "end":
                ts = record["timestamp"] / 1000 - start_ts
                print("保持时间：{}s".format(ts))
                score_path.write(str(ts/30)+'\n')#满分30秒,坚持秒数除以30=得分(0~1)


def schulte_grid(data,save_path):
    with open (save_path,'w')as score_path:
        start_ts = 0
        result = None
        answer_count = 0
        wrong_count = 0
        order = 0

        for record in data:
            score=''
            if record["type"] == "start":
                dbgprint("测试开始")
                start_ts = record["timestamp"] / 1000
                result = SchulteGridResult()
                answer_count = 0
                wrong_count = 0
            if record["type"] == "question":
                ts = record["timestamp"] / 1000 - start_ts
                if record["data"]["numarray"][4] == 0:
                    order = 2
                elif record["data"]["numarray"][9] == 0:
                    order = 3
                else:
                    order = 4

            if record["type"] == "answer":
                ts = record["timestamp"] / 1000 - start_ts
                if record["data"]["num"] > 0:
                    answer_count += 1
                else:
                    wrong_count += 1

            if record["type"] == "end":
                ts = record["timestamp"] / 1000 - start_ts
                print("方格阶数：{}".format(order))
                print("完成个数：{}".format(answer_count))
                print("错误个数：{}".format(wrong_count))
                print("用时： {}s".format(ts))
                score = str(answer_count/(answer_count+wrong_count))+' '+ str(ts)#正确率,时间
                score_path.write(score+'\n')


def objects_tracking(data,save_path):
    with open (save_path,'w')as score_path:
        ts = 0
        total = 0
        answer_count = 0
        wrong_count = 0
        result = None

        for record in data:
            if record["type"] == "start":
                dbgprint("测试开始")
                start_ts = record["timestamp"] / 1000
                result = ObjectsTrackingResult()
                answer_count = 0
                wrong_count = 0

            if record["type"] == "answer":
                ts = record["timestamp"] / 1000 - start_ts
                total = record["data"]["total"]
                select = record["data"]["select"]
                if record["data"]["index"] < select:
                    answer_count += 1
                else:
                    wrong_count += 1

            if record["type"] == "end":
                ts = record["timestamp"] / 1000 - start_ts
                print("{}选{}：".format(total, select))
                print("正确个数：{}".format(answer_count))
                print("错误个数：{}".format(wrong_count))
                print("用时：{}".format(ts))

                #避免分母为0
                if answer_count+wrong_count != 0:
                    score = str(answer_count/(answer_count+wrong_count))+' '+ str(ts)#正确率,时间
                    score_path.write(score+'\n')
                else:
                    score = str(0)+' '+str(ts)
                    score_path.write(score+'\n')


def limb_conflict(data,save_path):
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

    with open (save_path,'w')as score_path:

        for record in data:
            dbgprint(record, 'D')
            if record["type"] == "start":
                dbgprint("测试开始")
                start_ts = record["timestamp"] / 1000
                result = LimbConflictResult(0, 0, 0, 0, 0)
            if record["type"] == "question":
                ts = record["timestamp"] / 1000 - start_ts
                duration = record["data"]['duration']
                dbgprint("{:.3f}秒出现{}".format(ts, q_dict[record['data']["action"]]))
                #print("{:.3f}秒出现{}".format(ts, q_dict[record['data']["action"]]))
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
                    continue
                #dbgprint("{}已经产生动作".format(last_question))

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
                print("{:.3f}秒结束，测试难度为{}".format(ts, l_dict[duration]))
                print("本次测试难度为{}".format(l_dict[duration]))
                print("整体正确率：{}".format(result.right_rate))
                print("整体错误率: {}".format(result.wrong_rate))
                print("遗漏率: {}".format(result.miss_rate))
                print("冲动率: {}".format(result.impulse_rate))
                score_path.write(str(result.right_rate)+'\n')


def finger_holes(data,save_path):
    with open (save_path,'w')as score_path:
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
                    score_path.write(str(result.ordered_right_rate)+'\n')#记录顺序正确率
                else:
                    dbgprint("No hole pressed!", "E")

# 捉蚂蚱统计正确次数
def grasshopper(data,save_path):
    with open (save_path,'w')as score_path:
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
                    score_path.write(str(result.right_rate) +'\n')
                else:
                    dbgprint("No threshold!", "E")


def shape_color_interferenceape(data,save_path):
    with open (save_path,'w')as score_path:
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
        score=''
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
                                                        rd['box_color'], rd['box_shape']))
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
                    score = str(result.right_rate) +' '+ str(result.miss_rate)
                    score_path.write(score+'\n')#输出: 正确率,遗漏率
                else:
                    dbgprint("No rule!", "E")



# 需要将阅读的m4a格式读进来，以什么格式呢
#阅读没有分数
def raed_content(data,save_path):
    with open (save_path,'w')as score_path:
        num = 0
        start_ts = 0
        end_ts = 0
        for record in data:
            if record["type"] == "start":
                dbgprint("测试开始")
                start_ts = record["timestamp"] / 1000
                result = ReadContentResult()
            if record["type"] == "end":
                num += 1
                end_ts = record["timestamp"] / 1000
                dbgprint("第{}首，{:.3f}秒开始,{:.3f}秒结束".format(num, start_ts, end_ts))




def catch_worms(data,save_path):
    with open (save_path,'w')as score_path:
        start_ts = 0
        result = None
        threshold = None
        l_dict = {0: "第一首", 1: "第二首", 2: "第三首"}
        m_nTimes = [[12905, 19280, 23845, 34095, 35562, 45485], \
                    [3843, 5402, 23252, 28191, 29747, 33073, 45455, 47032], \
                    [15376, 22827, 28649, 39641, 41649, 53835], \
                    [5334, 7185, 30057, 36297, 38283, 42621, 58848, 60961]]
        for record in data:
            if record["type"] == "start":
                dbgprint("测试开始")
                start_ts = record["timestamp"] / 1000
                result = CatchWormsResult()

            if record["type"] == "answer":
                ts = record["timestamp"] / 1000 - start_ts
                skip = 0
                for i in range(m_nTimes[record['data']['index']].__len__()):
                    delta = record['data']['ms'] - m_nTimes[record['data']['index']][i]
                    if delta > 0 and delta < 1500:
                        skip = 1
                        break
                if skip:
                    result.right += 1
                else:
                    result.wrong += 1
                dbgprint("{:.3f}秒儿童出手{}虫子".format(ts, "捉到了" if skip else "未捉到"))
                threshold = record['data']['index']

            if record["type"] == "end":
                ts = record["timestamp"] / 1000 - start_ts
                dbgprint("{:.3f}秒结束".format(ts))
                #print("====={}测试=====".format(l_dict[threshold]))
                print("捉虫次数: {}".format(result.right))
                print("失手次数: {}".format(result.wrong))
                print("正确率: {}".format(result.right_rate))
                score_path.write(str(result.right_rate)+'\n')

# quantity为喝水时间
def feed_birds_water(data,save_path):
    with open (save_path,'w')as score_path:
        start_ts = 0
        result = None
        quantity = 0
        for record in data:
            if record["type"] == "start":
                dbgprint("测试开始")
                start_ts = record["timestamp"] / 1000
                result = CatchWormsResult()
            if record["type"] == "answer":
                quantity = record['data']['quantity']

            if record["type"] == "end":
                result.total = quantity
                ts = record["timestamp"] / 1000 - start_ts
                dbgprint("共计{:.3f}秒结束".format(ts))
                print("正确率: {}".format(result.total))

                #???????输出保持喝水时间,怎样计算正确率
                score_path.write(str(result.total)+'\n')


def process_file(file, scene_name,save_path):

    with open(file, 'r', encoding="UTF-8") as fp:
        dbgprint("Filename: {}".format(file, 'D'))
        data = []
        for ln, line in enumerate(fp, 1):
            try:
                record = json.loads(line)
            except json.decoder.JSONDecodeError:
                dbgprint("JSON Decode Fail! Line: {}, Data: {}".format(ln, line), "W")
            if record['type'] != "sensorbind" and record['type'] != "sensordata":
                data.append(record)

        if scene_name == "balance_test":
            balance_test(data,save_path)

        if scene_name == "limb_conflict":
            limb_conflict(data,save_path)

        if scene_name == "finger_holes":
            finger_holes(data,save_path)

        if scene_name == "grasshopper":
            grasshopper(data,save_path)

        if scene_name == "shape_color_interference":
            shape_color_interferenceape(data,save_path)


        if scene_name == "schulte_grid":
            schulte_grid(data,save_path)

        if scene_name == "objects_tracking":
            objects_tracking(data,save_path)

        if scene_name == "raed_content":
            raed_content(data,save_path)

        if scene_name == "feed_birds_water":
            feed_birds_water(data,save_path)

        if scene_name == "catch_worms":
            catch_worms(data,save_path)


if __name__ == "__main__":
    patient_path = Path("/Users/zhangyiming/PycharmProjects/ADHD-analysis/正常")
    control_path = Path("/Users/zhangyiming/PycharmProjects/ADHD-analysis/正常")
    scenes = ['grasshopper', 'shape_color_interference', 'limb_conflict', 'finger_holes', 'balance_test',
              'schulte_grid', 'objects_tracking', 'feed_birds_water', 'catch_worms']
    scene_names = {
        'grasshopper': "grasshopper捉蚂蚱",
        'shape_color_interference': "shape_color_interference形色干扰",
        'limb_conflict': "limb_conflict肢体冲突",
        'finger_holes': "finger_holes戳洞",
        'balance_test': "balance_test乒乓球平衡",
        'schulte_grid': "schulte_grid舒尔特方格",
        'objects_tracking': "objects_tracking找小球",
        'feed_birds_water': "feed_birds_water小鸟喂水",
        'catch_worms': "catch_worms苹果捉虫"
    }

    print("=====正常=====")
    for person in patient_path.iterdir():
        if person.is_dir():

            print("=====姓名: {}=====".format(person.stem))
            for scene in person.iterdir():
                if scene.stem in scenes:

                    print("=====场景: {}=====".format(scene_names[scene.stem]))
                    for data_file in scene.iterdir():
                        #判断是否为json文件
                        if data_file.suffix == ".json":
                            save_fp = scene /('score.txt')
                            process_file(data_file, scene.stem,save_fp)
                            print(save_fp)
                        else:
                            continue

            print("\n\n\n")

