from pathlib import Path
path = '/Users/zhangyiming/PycharmProjects/ADHD/确诊/baojiarui/shape_color_interference/20190803_114031_123.json'
out = '/Users/zhangyiming/PycharmProjects/ADHD/确诊/baojiarui/shape_color_interference'


f = open(path,'r')
a = out + '/Waist.json'
w = open(a,'w')
lines = f.readlines()
for line in lines:
    if '470000032203' in line:
        print(line)
        w.write(line)



f = open(path,'r')
a = out + '/Neck.json'
w = open(a,'w')
lines = f.readlines()
for line in lines:
    if '47000000e503' in line:
        print(line)
        w.write(line)


f = open(path,'r')
a = out + '/RightAnkle.json'
w = open(a,'w')
lines = f.readlines()
for line in lines:
    if '470000071203' in line:
        print(line)
        w.write(line)

f = open(path,'r')
a = out + '/LeftAnkle.json'
w = open(a,'w')
lines = f.readlines()
for line in lines:
    if '47000000e303' in line:
        print(line)
        w.write(line)

f = open(path,'r')
a = out + '/RightWrist.json'
w = open(a,'w')
lines = f.readlines()
for line in lines:
    if '470000032d03' in line:
        print(line)
        w.write(line)

f = open(path,'r')
a = out + '/LeftWrist.json'
w = open(a,'w')
lines = f.readlines()
for line in lines:
    if '47000000e103' in line:
        print(line)
        w.write(line)