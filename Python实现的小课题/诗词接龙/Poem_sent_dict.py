import re
import pickle
from xpinyin import Pinyin
from collections import defaultdict


def main():
    with open('poem.txt', 'r') as f:
        poems = f.readlines()

    sents = []
    for poem in poems:
        parts = re.split(r'([。？！])', poem.strip())
        parts.append("")
        parts = ["".join(i) for i in zip(parts[0::2], parts[1::2])]

        index = 0
        while parts[index] != '':
            if len(parts[index]) >= 5:
                sents.append(parts[index])
            index += 1
    poem_dict = defaultdict(list)
    for sent in sents:
        head = Pinyin().get_pinyin(sent, tone_marks='marks', splitter=' ').split()[0]
        poem_dict[head].append(sent)
    with open('poemDict.pk', 'wb') as f:
        pickle.dump(poem_dict, f)


main()
