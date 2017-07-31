import re


class MultiTreeNode:
    def __init__(self):
        self.name = ''
        self.child_list = []


class EvolvedTreeNode:
    def __init__(self):
        self.name = ''
        self.pron = ''
        self.child_list = []


def generate_tree(root, pronun_spellings, word, pronun, i, j):
    # 设置拼写可以是1-4个字母
    for k in range(4):
        if (i + k < len(word)) and (j < len(pronun)) and (word[i:i + 1 + k] in pronun_spellings[pronun[j]]):
            node = MultiTreeNode()
            node.name = word[i:i + 1 + k]
            root.child_list.append(node)
            generate_tree(root.child_list[-1], pronun_spellings, word, pronun, i + 1 + k, j + 1)


def read_pronumAB(file_name):
    pronun_spellings = {}
    with open(file_name, 'r', encoding='utf-8') as f:
        for line in f.readlines():
            linelist = line.strip().split('    ')  # 四个空格
            # print(linelist)
            pronun = linelist[0].upper()
            spellings = linelist[1].split(', ')
            pronun_spellings[pronun] = spellings
    print(pronun_spellings)
    return pronun_spellings


def print_path(path):
    p = ''
    for i in range(len(path)):
        p += path[i]
        p += ' '
    print(p)


def find_all_path2(root, allpath, path, word, deepth, length):
    if root == None:
        return
    path.append(root.name)
    if len(root.child_list) == 0 and word == ''.join(path[1:]) and deepth == length:  # 去掉最开始的root
        # if len(root.child_list) == 0 :
        # print_path(path)
        pathcopy = path[1:]
        allpath.append(pathcopy)  # all_path是一个二维list
    else:
        for i in range(len(root.child_list)):
            if root.child_list[i] != None:
                find_all_path2(root.child_list[i], allpath, path, word, deepth + 1, length)
    path.pop()


def read_select2nd(filename):
    select2ndlist = []
    with open(filename, 'r', encoding='utf-8') as f1:
        for line in f1.readlines():
            line = line.strip()
            select2ndlist.append(line)
    print(select2ndlist)
    return select2ndlist


def read_wordrank(filename):
    word_rank = []
    cnt = 1
    with open(filename, 'r', encoding='utf-8') as f1:
        for line in f1.readlines():
            linelist = line.strip().split(' ')
            if cnt <= 30000:
                word_rank.append(linelist[0])
            cnt += 1
    return word_rank


def read_cmudict(filename, outputname1, outputname2, pronun_spellings, probTable, select2ndlist, word_rank):
    num1 = 0
    num2 = 0
    num3 = 0
    num4 = 0
    num5 = 0
    twoalign = {}
    with open(filename, 'r', encoding='utf-8') as f1, open(outputname1, 'w', encoding='utf-8') as f2, open(
            outputname2, 'w', encoding='utf-8') as f3:
        for line in f1.readlines():
            linelist = line.strip().split(' ')
            root = MultiTreeNode()
            root.name = 'root'
            word = linelist[0]
            # word = re.sub('[^a-zA-Z]', '', linelist[0])  # 去掉特殊字符
            pronun = linelist[1:]
            generate_tree(root, pronun_spellings, word, pronun, 0, 0)
            allpath = []
            path = []
            find_all_path2(root, allpath, path, word, 0, len(pronun))

            # path_word = []
            # path_pronun = []
            # pronun_str = ''.join(pronun)
            # find_all_path3(root, allpath, path_word, path_pronun, word, pronun_str)

            if len(allpath) == 1:
                num1 += 1
                f2.write(word)
                f2.write('\n')

                s = ''
                p = ''
                for i in range(len(allpath[0])):
                    s += allpath[0][i]
                    s += '-'
                    s += pronun[i]
                    s += ' '
                    p += pronun[i]
                    p += ' '

                f2.write(p)
                f2.write('\n')
                f2.write(s)
                f2.write('\n')
            elif len(allpath) == 2:
                num2 += 1
                f2.write(word)
                f2.write('\n')
                treeIndex = 0  # 标识是否应该选择哪一棵树🌲
                ta = ''
                for i in range(len(allpath[0])):
                    if allpath[0][i] != allpath[1][i]:
                        ta += allpath[0][i]

                if ta in select2ndlist:
                    treeIndex = 1

                s = ''
                p = ''
                for i in range(len(allpath[treeIndex])):
                    s += allpath[treeIndex][i]
                    s += '-'
                    s += pronun[i]
                    s += ' '
                    p += pronun[i]
                    p += ' '

                f2.write(p)
                f2.write('\n')
                f2.write(s)
                f2.write('\n')


            elif len(allpath) >= 3:
                num3 += 1
                # print(word)
                # print(pronun)
                # print(allpath[0])
                # print(allpath[1])
                # print(allpath[2])


            else:  # 没找到路径
                num4 += 1
                f3.write(word)
                f3.write(' ')
                for i in range(len(pronun)):
                    f3.write(pronun[i])
                    f3.write(' ')
                f3.write('\n')

                if word in word_rank:
                    num5 += 1

    print(num1)
    print(num2)
    print(num3)
    print(num4)
    print(num5)

def writeps(filename, pronun_spellings):
    with open(filename, 'w', encoding='utf-8') as f:
        for k in pronun_spellings:

            f.write('{slim::Phoneme("')
            f.write(k)
            f.write('"), {')
            startposi = 0
            for s in pronun_spellings[k]:
                if startposi == 0:
                    startposi = 1
                else:
                    f.write(' ,')
                f.write('"')
                f.write(s)
                f.write('"')
            f.write('}')
            f.write('}')
            f.write(',')
            f.write('\n')


def writes2nd(filename, select2ndlist):
    with open(filename, 'w', encoding='utf-8') as f:
        for s in select2ndlist:
            f.write('"')
            f.write(s)
            f.write('"')
            f.write(',')
            f.write('\n')


if __name__ == '__main__':
    pronun_spellings = read_pronumAB(
        "../Spelling-patterns/pronunAB_origin.txt")

    select2ndlist = read_select2nd("../Spelling-patterns/select2nd.txt")
    probTable = {}
    word_rank = read_wordrank("../Spelling-patterns/word_rank.txt")
    read_cmudict("../cmudict-en-us.dict",
                 "../align.txt", "../unresolved.txt",
                 pronun_spellings, probTable, select2ndlist, word_rank)

    writeps("../Spelling-patterns/pronunAB_origin_cp.txt", pronun_spellings)
    writes2nd("../Spelling-patterns/select2ndlist_cp.txt", select2ndlist)
