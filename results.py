class BalanceTestResult:
    def __init__(self):
        self.time = 0

    @property
    def holdtime(self):
        return self.holdtime


class SchulteGridResult:
    def __init__(self):
        self.finish_time = 0
        self.answer_mum = 0

    @property
    def answer_count(self):
        return self.answer_num

    @property
    def time(self):
        return self.finish_time


class ObjectsTrackingResult:
    def __init__(self):
        self.right = 0
        self.wrong = 0

    @property
    def answer_count(self):
        return self.answer_count

    @property
    def wrong_coung(self):
        return self.wrong_count
    
    

class LimbConflictResult:
    def __init__(self, red_question, green_question, answer_green_right, answer_green_wrong, answer_red):
        self.red_question = red_question
        self.green_question = green_question
        self.answer_green_right = answer_green_right
        self.answer_green_wrong = answer_green_wrong
        self.answer_red = answer_red

    @property
    def question_all(self):
        return self.red_question + self.green_question

    @property
    def answer_green(self):
        return self.answer_green_right + self.answer_green_wrong

    @property
    def answer_right_all(self):
        return self.answer_green_right + self.red_question - self.answer_red

    @property
    def answer_wrong_all(self):
        return self.answer_green_wrong + self.answer_red

    @property
    def right_rate(self):
        """
        计算整体正确率：(正确举起+正确无反应)/总问题数
        :return:
        """
        return self.answer_right_all / self.question_all

    @property
    def wrong_rate(self):
        """
        计算整体错误率：(错误举起+红色时冲动数)/总问题数
        :return:
        """
        return self.answer_wrong_all / self.question_all

    @property
    def miss_rate(self):
        """
        计算遗漏率：(举起问题数-举起时的反应次数)/举起问题数
        :return:
        """
        if self.green_question:
            return (self.green_question - self.answer_green) / self.green_question
        else:
            return 0

    @property
    def impulse_rate(self):
        """
        计算冲动率：冲动次数/总不举起问题数
        :return:
        """
        return self.answer_red / self.red_question


class FingerHolesResult:
    def __init__(self):
        self.question = []
        self.answer = []

    @property
    def pretty_question(self):
        return "  ".join(["{:2d}".format(i) for i in self.question])

    @property
    def pretty_answer(self):
        return "  ".join(["{:2d}".format(i) for i in self.answer])

    @property
    def disorder_right_rate(self):
        """
        乱序正确率，只看是否正确
        :return:
        """
        return len([i for i in self.answer if i in self.question]) / len(self.question)

    @property
    def ordered_right_rate(self):
        """
        顺序正确率，考虑顺序的正确率
        :return:
        """
        return len([i for i in range(0, min(len(self.question), len(self.answer)))
                    if self.question[i] == self.answer[i]]) / len(self.question)


class GrasshopperResult:
    def __init__(self):
        self.right = 0
        self.wrong = 0

    @property
    def right_rate(self):
        if self.right + self.wrong:
            return self.right / (self.right + self.wrong)
        else:
            return 0


class ShapeColorInterferenceapeResult:
    def __init__(self):
        self.right = 0
        self.wrong = 0
        self.total = 0

    @property
    def right_rate(self):
        if self.total:
            return self.right / self.total
        else:
            return 0

    @property
    def miss_rate(self):
        return (self.total - self.right - self.wrong) / self.total


#阅读结果？？
class ReadContentResult:
    def __init__(self):
        self.file = 0


#苹果捉虫结果
class CatchWormsResult:
    def __init__(self):
        self.right = 0
        self.wrong = 0
        self.total = 0

    @property
    def right_rate(self):
        if self.right + self.wrong:
            return self.right / (self.right + self.wrong)
        else:
            return 0


#小鸟喂水结果
class FeedBirdsWaterResult:
    def __init__(self):
        self.total = 0

    @property
    def time(self):
        return self.total