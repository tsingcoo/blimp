# 主要处理拼写可能对空的情况

import re


class EvolvedTreeNode:
    def __init__(self):
        self.name = ''
        self.pron = ''
        self.child_list = []


def read_pronumAB(file_name):
    pronun_spellings = {}
    with open(file_name, 'r', encoding='utf-8') as f:
        for line in f.readlines():
            linelist = line.strip().split('    ')  # 四个空格
            # print(linelist)
            pronun = linelist[0].upper()
            spellings = linelist[1].split(', ')
            pronun_spellings[pronun] = spellings
    return pronun_spellings


def generate_tree(root, pronun_spellings, word, pronun, i, j):  # 只考虑两个音标组合

    for k in range(4):
        if (i + k < len(word)) and j < len(pronun) and (word[i:i + 1 + k] in pronun_spellings[pronun[j]]):
            node = EvolvedTreeNode()
            node.name = str(word[i:i + 1 + k])
            node.pron = str(pronun[j])
            root.child_list.append(node)
            generate_tree(root.child_list[-1], pronun_spellings, word, pronun, i + 1 + k, j + 1)
        elif k == 1 and (i + k < len(word)) and j < len(pronun) and (word[i + 1:i + 1 + k] in pronun_spellings[pronun[j]]):
            node = EvolvedTreeNode()
            node.name = str(word[i + 1:i + 1 + k])
            node.pron = str(pronun[j])
            root.child_list.append(node)
            generate_tree(root.child_list[-1], pronun_spellings, word, pronun, i + 1 + k, j + 1)

    for k in range(4):
        if (i + k < len(word)) and (j + 1 < len(pronun)) and (
                str(pronun[j]) + str(pronun[j + 1]) in pronun_spellings) and (word[i:i + 1 + k] in pronun_spellings[str(pronun[j]) + str(pronun[j + 1])]):
            node = EvolvedTreeNode()
            node.name = str(word[i:i + 1 + k])
            node.pron = str(pronun[j]) + str(pronun[j + 1]) 
            root.child_list.append(node)
            generate_tree(root.child_list[-1], pronun_spellings, word, pronun, i + 1 + k, j + 2)


def find_all_path4(root, allpath, path_word, path_pronun, word, pronun):
    if root == None:
        return
    path_word.append(root.name)
    path_pronun.append(root.pron)

    if len(root.child_list) == 0 and pronun == ''.join(
            path_pronun[1:]):
        path_word_copy = path_word[1:]
        path_pronun_copy = path_pronun[1:]
        allpath[0].append(path_word_copy)
        allpath[1].append(path_pronun_copy)
    else:
        for i in range(len(root.child_list)):
            if root.child_list[i] != None:
                find_all_path4(root.child_list[i], allpath, path_word, path_pronun, word, pronun)
    path_word.pop()
    path_pronun.pop()


def read_select2nd(filename):
    select2ndlist = []
    with open(filename, 'r', encoding='utf-8') as f1:
        for line in f1.readlines():
            line = line.strip()
            select2ndlist.append(line)
    # print(select2ndlist)
    return select2ndlist


def read_unresolved2(filename1, filename2, filename3, pronun_spellings, probTable, select2ndlist, word_rank):
    num1 = 0
    num2 = 0
    num3 = 0
    num4 = 0
    num5 = 0
    with open(filename1, 'r', encoding='utf-8') as f1, open(filename2, 'w', encoding='utf-8') as f2, open(filename3,
                                                                                                          'w',
                                                                                                          encoding='utf-8') as f3:
        for line in f1.readlines():
            linelist = line.strip().split(' ')
            root = EvolvedTreeNode()
            root.name = 'rootname'
            root.pron = 'rootpron'
            word = re.sub('[^a-zA-Z]', '', linelist[0])  # 去掉特殊字符
            pronun = linelist[1:]
            generate_tree(root, pronun_spellings, word, pronun, 0, 0)
            allpath = []
            allpath.append([])  # 存放word中的一些字母
            allpath.append([])  # 存放pronun中的一些拼写
            path_word = []
            path_pronun = []
            pronun_str = ''.join(pronun)
            find_all_path4(root, allpath, path_word, path_pronun, word, pronun_str)

            if len(allpath[0]) == 1:
                num1 += 1
                f2.write(word)
                f2.write('\n')
                # print(word)

                s = ''
                p = ''
                for i in range(len(allpath[0][0])):
                    if allpath[1][0][i] in ['AAR', 'EHR', 'IHR', 'AHL', 'HHW']:  # 前两个连在一起
                        s += allpath[0][0][i]
                        s += '-'
                        s += allpath[1][0][i][:2]
                        s += ' '
                        p += allpath[1][0][i][:2]
                        p += ' '

                        s += allpath[0][0][i]
                        s += '-'
                        s += allpath[1][0][i][2:]
                        s += ' '
                        p += allpath[1][0][i][2:]
                        p += ' '
                    elif allpath[1][0][i] in ['YUW', 'KS', 'YAH', 'GZ', 'YUH']:  # 前一个独自为音标
                        s += allpath[0][0][i]
                        s += '-'
                        s += allpath[1][0][i][:1]
                        s += ' '
                        p += allpath[1][0][i][:1]
                        p += ' '

                        s += allpath[0][0][i]
                        s += '-'
                        s += allpath[1][0][i][1:]
                        s += ' '
                        p += allpath[1][0][i][1:]
                        p += ' '
                    else:
                        s += allpath[0][0][i]
                        s += '-'
                        s += allpath[1][0][i][:2]
                        s += ' '
                        p += allpath[1][0][i][:2]
                        p += ' '

                f2.write(p)
                f2.write('\n')
                f2.write(s)
                f2.write('\n')
            elif len(allpath[0]) == 2:  # 就选第一个
                num2 += 1
                f2.write(word)
                f2.write('\n')

                word1 = ''.join(allpath[0][0])
                word2 = ''.join(allpath[0][1])
                if len(word1) > len(word2):
                    index = 0
                elif len(word1) < len(word2):
                    index = 1
                elif word1 == word2:  # 两者一样，随便选
                    index = 0
                else:  # 两者相同长度但不一样，就选第一个
                    index = 0

                s = ''
                p = ''
                for i in range(len(allpath[0][index])):
                    if allpath[1][index][i] in ['AAR', 'EHR', 'IHR', 'AHL', 'HHW']:  # 前两个连在一起
                        s += allpath[0][index][i]
                        s += '-'
                        s += allpath[1][index][i][:2]
                        s += ' '
                        p += allpath[1][index][i][:2]
                        p += ' '

                        s += allpath[0][index][i]
                        s += '-'
                        s += allpath[1][index][i][2:]
                        s += ' '
                        p += allpath[1][index][i][2:]
                        p += ' '
                    elif allpath[1][index][i] in ['YUW', 'KS', 'YAH', 'GZ', 'YUH']:  # 前一个独自为音标
                        s += allpath[0][index][i]
                        s += '-'
                        s += allpath[1][index][i][:1]
                        s += ' '
                        p += allpath[1][index][i][:1]
                        p += ' '

                        s += allpath[0][index][i]
                        s += '-'
                        s += allpath[1][index][i][1:]
                        s += ' '
                        p += allpath[1][index][i][1:]
                        p += ' '
                    else:
                        s += allpath[0][index][i]
                        s += '-'
                        s += allpath[1][index][i][:2]
                        s += ' '
                        p += allpath[1][index][i][:2]
                        p += ' '

                f2.write(p)
                f2.write('\n')
                f2.write(s)
                f2.write('\n')

            elif len(allpath[0]) >= 3:
                num3 += 1
            else:  # 没找到路径
                num4 += 1

                if word in word_rank:
                    num5 += 1
                    f3.write(word)
                    f3.write('  ')
                    for i in range(len(pronun)):
                        f3.write(pronun[i])
                        f3.write(' ')
                    f3.write('\n')

    print(num1)
    print(num2)
    print(num3)
    print(num4)
    print(num5)


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


if __name__ == '__main__':
    pronun_spellings = read_pronumAB("../Spelling-patterns/pronunAB_origin.txt")
    select2ndlist = read_select2nd("../Spelling-patterns/select2nd.txt")
    probTable = {}
    word_rank = read_wordrank("../Spelling-patterns/word_rank.txt")
    read_unresolved2("../unresolved2.txt", "../unresolved2_align.txt",
                     "../unresolved3.txt", pronun_spellings, probTable, select2ndlist,
                     word_rank)
