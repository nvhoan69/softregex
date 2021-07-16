"""
process original dataset into form that softregex use
e.g.
"""
import numpy as np


def transformReg(regex):
    regex = " ".join(regex)
    regex = regex.replace(" ".join('AEIOUaeiou'), "<VOW>")
    regex = regex.replace(" ".join('0-9'), "<NUM>")
    regex = regex.replace(" ".join('A-Za-z'), "<LET>")
    regex = regex.replace(" ".join('A-Z'), "<CAP>")
    regex = regex.replace(" ".join('a-z'), "<LOW>")

    regex = regex.replace(" ".join('dog'), "<M0>")
    regex = regex.replace(" ".join('truck'), "<M1>")
    regex = regex.replace(" ".join('ring'), "<M2>")
    regex = regex.replace(" ".join('lake'), "<M3>")
    return regex

def transformDesc(description):
    description = description.replace("\'dog\'", "<M0>")
    description = description.replace("\'truck\'", "<M1>")
    description = description.replace("\'ring\'", "<M2>")
    description = description.replace("\'lake\'", "<M3>")
    return description


with open('../data/NL-RX-Turk/src.txt', 'r') as src:
    descriptions = src.read().splitlines()

for i in range(len(descriptions)):
    descriptions[i] = transformDesc(descriptions[i])

with open('../data/NL-RX-Turk/targ.txt', 'r') as targ:
    regexes = targ.read().splitlines()

regexSketchs = (transformReg(regex) for regex in regexes)

lineNums = np.arange(len(descriptions))
dataset = zip(lineNums, descriptions, regexes, regexSketchs)

np.random.shuffle(dataset)

#print(dataset)

# train 6500
train_data = dataset[0:6500]
# test 2500
test_data = dataset[6500:9000]
# evaluate 1000
eval_data = dataset[9000:]

writer = open('../data/NL-RX-Turk/data_for_debug.txt', 'w+')
for data in dataset:
    line = '%s\t%s\t%s\t%s\n' % data
    writer.write(line)
writer.close()

# prepare train data
input_writer = open('../data/NL-RX-Turk/train/data.txt', 'w+')
map_writer = open('../data/NL-RX-Turk/train/map_targ.txt', 'w+')
for data in train_data:
    input_data = "{}\t{}\n".format(data[1], data[3]) # description and sketch
    map_data = "{}\t{}\t{}\t\n".format(data[0], data[1], data[2]) # line number and target regex
    input_writer.write(input_data)
    map_writer.write(map_data)
input_writer.close()
map_writer.close()

# prepare test data
input_writer = open('../data/NL-RX-Turk/test/data.txt', 'w+')
map_writer = open('../data/NL-RX-Turk/test/map_targ.txt', 'w+')
for data in test_data:
    input_data = "{}\t{}\n".format(data[1], data[3]) # description and sketch
    map_data = "{}\t{}\t{}\t\n".format(data[0], data[1], data[2]) # line number and target regex
    input_writer.write(input_data)
    map_writer.write(map_data)
input_writer.close()
map_writer.close()

# prepare evaluate data
input_writer = open('../data/NL-RX-Turk/val/data.txt', 'w+')
map_writer = open('../data/NL-RX-Turk/val/map_targ.txt', 'w+')
for data in eval_data:
    input_data = "{}\t{}\n".format(data[1], data[3]) # description and sketch
    map_data = "{}\t{}\t{}\t\n".format(data[0], data[1], data[2]) # line number and target regex
    input_writer.write(input_data)
    map_writer.write(map_data)
input_writer.close()
map_writer.close()


