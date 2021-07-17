"""
process original dataset into form that softregex use
e.g.
"""
import re

import numpy as np


def transformReg(regex, index):
    global label_map_lines
    regex = " ".join(regex)
    regex = regex.replace(" ".join('AEIOUaeiou'), "<VOW>")
    regex = regex.replace(" ".join('0-9'), "<NUM>")
    regex = regex.replace(" ".join('A-Za-z'), "<LET>")
    regex = regex.replace(" ".join('A-Z'), "<CAP>")
    regex = regex.replace(" ".join('a-z'), "<LOW>")

    label_map_line = label_map_lines[index]
    data = label_map_line.split("\t")
    for i in range(len(data) - 1):
        if (i % 2 == 0):
            regex = regex.replace(" ".join(data[i + 1]), data[i])


    return regex

map_label = open('../data/KB13/map_label.txt', 'w+')
def transformDesc(description):
    matches = re.findall('\'(\w+)\'', description)
    label_count = 0
    for meaning in matches:
        label = '<M' + str(label_count) + '>'
        label_count = label_count + 1
        map_label.write(label + "\t" + meaning + "\t")
        description = description.replace("\'" + meaning + "\'", label)

    map_label.write("\n")
    return description


with open('../data/KB13/src.txt', 'r') as src:
    descriptions = src.read().splitlines()

# transform descriptions and write map label to file
for i in range(len(descriptions)):
    descriptions[i] = transformDesc(descriptions[i])

map_label.close()

with open('../data/KB13/targ.txt', 'r') as targ:
    regexes = targ.read().splitlines()

with open('../data/KB13/map_label.txt', 'r+') as label_map:
    label_map_lines = label_map.read().splitlines()

regexSketches = []
for index in range(len(regexes)):
    regexSketches.append(transformReg(regexes[index], index))
label_map.close()

lineNums = np.arange(len(descriptions))
dataset = zip(lineNums, descriptions, regexes, regexSketches)

np.random.shuffle(dataset)

#print(dataset)

# train 6500
train_data = dataset[0:618]
# test 2500
test_data = dataset[618:]
# evaluate 1000
eval_data = test_data

writer = open('../data/KB13/data_for_debug.txt', 'w+')
for data in dataset:
    line = '%s\t%s\t%s\t%s\n' % data
    writer.write(line)
writer.close()

# prepare train data
input_writer = open('../data/KB13/train/data.txt', 'w+')
map_writer = open('../data/KB13/train/map_targ.txt', 'w+')
map_label = open('../data/KB13/train/map_label.txt', 'w+')
for data in train_data:
    input_data = "{}\t{}\n".format(data[1], data[3]) # description and sketch
    map_data = "{}\t{}\t{}\t\n".format(data[0], data[1], data[2]) # line number and target regex
    input_writer.write(input_data)
    map_writer.write(map_data)
    map_label.write(label_map_lines[data[0]] + "\n")
input_writer.close()
map_writer.close()
map_label.close()

# prepare test data
input_writer = open('../data/KB13/test/data.txt', 'w+')
map_writer = open('../data/KB13/test/map_targ.txt', 'w+')
map_label = open('../data/KB13/test/map_label.txt', 'w+')
for data in test_data:
    input_data = "{}\t{}\n".format(data[1], data[3]) # description and sketch
    map_data = "{}\t{}\t{}\t\n".format(data[0], data[1], data[2]) # line number and target regex
    input_writer.write(input_data)
    map_writer.write(map_data)
    map_label.write(label_map_lines[data[0]] + "\n")
input_writer.close()
map_writer.close()
map_label.close()

# prepare evaluate data
input_writer = open('../data/KB13/val/data.txt', 'w+')
map_writer = open('../data/KB13/val/map_targ.txt', 'w+')
map_label = open('../data/KB13/val/map_label.txt', 'w+')
for data in eval_data:
    input_data = "{}\t{}\n".format(data[1], data[3]) # description and sketch
    map_data = "{}\t{}\t{}\t\n".format(data[0], data[1], data[2]) # line number and target regex
    input_writer.write(input_data)
    map_writer.write(map_data)
    map_label.write(label_map_lines[data[0]] + "\n")
input_writer.close()
map_writer.close()
map_label.close()


