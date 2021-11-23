import pygame
import random
import xlrd

from Other_library import print_text

'''
学生必须完成全部的复习单词才能结束复习模式，练习就20个单词所以没必要
'''


# 读取excel表里面的所有单词
def read_whole_words(path):
    words_list = []  # 创建一个英语单词列表
    task_words = []  # 创建一个汉语单词列表
    wb = xlrd.open_workbook(path)  # 打开一个excel工作簿
    sheets = wb.sheet_names()  # 根据工作表的名字查找
    worksheet = wb.sheet_by_name(sheets[0])   # 打开工作表的第一张表
    words_numbers = worksheet.nrows  # 获得单词的行数
    for i in range(words_numbers):  # 循环所有的单词
        words_list.append(worksheet.cell_value(i, 0))  # 根据索引添加第一列的英语单词
        task_words.append(worksheet.cell_value(i, 1))  # 根据索引添加第二列的汉语翻译
    return words_list, task_words  # 返回英语单词和汉语翻译


# 创建一个显示的类
class Trivia(object):
    def __init__(self, review_file_name):  # 需要输入文件
        self.words_list = []   # 创建一个英语列表
        self.task_words = []   # 创建一个汉语列表
        self.words_dic = []    # 创建一个单词列表
        self.dic = []  # 创建一个有答案的列表
        self.running = True  # 游戏运行控制按钮
        self.current = 0  # 当前正在拼写的单词
        self.correct = 0  # 当前正确选项的数字
        self.corrected = False  # 回答正确
        self.failed = False  # 回答错误
        self.__review_file_name = review_file_name  # 读取文件列表
        self.FONT1 = pygame.font.Font('Fonts/STKAITI.TTF', 35)  # 汉语字体
        self.FONT2 = pygame.font.Font('Fonts/arial.ttf', 35)   # 英语字体
        #  对应的字母列表
        self.voiced_lists = {'a': ['e', 'o'], 'b': ['d', 'p', 'q'], 'c': ['k', 's', 'z'], 'd': ['b', 'p', 'q'],
                             'e': ['a', 'o', 'y', 'i'], 'f': ['v', 'w'], 'g': ['j'], 'h': ['n'], 'i': ['y', 'e'],
                             'j': ['g'], 'k': ['c'], 'm': ['n', 'h'], 'n': ['m', 'h'], 'o': ['a', 'e'],
                             'p': ['d', 'b', 'q'], 'q': ['p', 'b', 'd'], 's': ['z', 'c'], 'u': ['w', 'v'],
                             'v': ['w', 'u'], 'w': ['f', 'v'], 'x': ['s', 'z'], 'y': ['i', 'e'], 'z': ['s', 'c'],
                             'r': [''], 't': [''], 'l': ['']}
        self.words_list, self.task_words = read_whole_words(self.__review_file_name)  # 得到了英文单词，得到了汉语翻译

    # 生成错误答案列表，要输入某一个单词
    def shuffle_alphabet(self, word):
        answers_lists = []     # 创建一个单词列表
        alphabet_lists = []    # 创建一个字母列表
        for i in word:         # 读出每一个字母
            alphabet_lists.append(i)  # 将每一个字母， 都放到字母列表中
        chosen_alphabet = random.sample(alphabet_lists, 2)  # 随机选择两个字母
        for i in chosen_alphabet:   # 遍历选择每个选择的单词
            if i in self.voiced_lists.keys():  # 得到索引
                wrong_word = word.replace(i, random.sample(self.voiced_lists[i], 1)[0])  # 随机替换字母
                answers_lists.append(wrong_word)  # 将错误的迷惑选项加到列表中
        answers_lists.append(word)   # 将正确的单词也加进去
        random.shuffle(answers_lists)  # 随机打乱答案选项
        return answers_lists  # 返回答案列表

    # 问题和选项和正确的单词字母的组合列表
    def question_answers(self):
        for i in range(len(self.words_list)):  # 看单词库有多少个单词
            self.words_dic.append(self.task_words[i])  # 先添加汉语翻译
            questions_list = self.shuffle_alphabet(self.words_list[i])  # 生成某个单词的迷惑选项
            for j in questions_list:
                self.words_dic.append(j)  # 将迷惑选项一个个加进去
            correct_index = questions_list.index(self.words_list[i])  # 正确的答案索引
            self.words_dic.append(correct_index)  # 将正确答案索引也加进去
            self.dic.append(self.words_dic)  # 将所有的都加到一个列表中
            self.words_dic = []   # 清空准备接受下一个单词
        return self.dic   # 返回问题，选项，以及正确的选项索引

    # 在屏幕上展示问题
    def show_question(self, question_answers_index_list, number):
        # 在屏幕上打印内容
        print_text(self.FONT1, 210, 5, "单项选择题")
        print_text(self.FONT1, 130, 500, "请按 1，2，3 回答问题", (255, 0, 255))
        question = question_answers_index_list[number][0]
        print_text(self.FONT1, 5, 80, "问题：" + '‘' + question + '’' + '的正确拼写为：')
        print_text(self.FONT2, 20, 170, "1 : " + question_answers_index_list[number][1])
        print_text(self.FONT2, 20, 270, "2 : " + question_answers_index_list[number][2])
        print_text(self.FONT2, 20, 370, "3 : " + question_answers_index_list[number][3])
        self.correct = question_answers_index_list[number][4] + 1  # 获得当前的正确选项的数字

        if self.corrected:   # 如果回答正确，打印
            print_text(self.FONT1, 130, 420, "回答正确! 正确答案为：" + str(self.correct))
            #  以下是判断是不是到了最后一个展示的内容不同
            if self.current + 1 < len(self.words_list):
                print_text(self.FONT1, 100, 460, "请按 Enter 回答下一个问题")
            else:
                print_text(self.FONT1, 100, 460, "学习结束，请按 ESC 返回上一菜单")
        elif self.failed:   # 如果回答错误，展示不同的东西
            print_text(self.FONT1, 210, 400, "请再仔细想想")

    # 获取键盘的输入，并判断是回答正确还是错误
    def handle_input(self, number):
        if not self.corrected or not self.failed:
            if number == self.correct:  # 输入的字母与正确的字母相匹配？
                self.corrected = True   # 回答正确
            else:
                self.failed = True   # 回答错误

    # 进入下一个问题
    def next_question(self):
        if self.corrected:
            self.corrected = False   # 修改回默认
            self.failed = False     # 修改回默认
            self.current += 1   # 当前的问题加一


#  以下是在主程序中要使用的函数，仅仅导入这个函数就可以
def English_review(screen):
    trivia = Trivia('words_pool/three_grade/three_grade_known.xls')  # 读取文件
    question_answers_index_list = trivia.question_answers()  # 所有的顺序到拍好
    while trivia.running:
        Eng_review = pygame.image.load("Game_Pictures/game_intro.jpg").convert_alpha()  # 加载背景
        game_intro = pygame.transform.scale(Eng_review, (30 * 22, 30 * 22))  # 适应到屏幕大小
        screen.blit(game_intro, (0, 0))  # 将图片画到屏幕上
        remaining_task = len(trivia.words_list) - trivia.current  # 剩余的任务个数
        print_text(trivia.FONT1, 410, 5, "剩余任务:" + str(remaining_task))  # 展示剩余任务还有多少个
        trivia.show_question(question_answers_index_list, trivia.current)  # 在屏幕上展示
        # 获取玩家在键盘上的输入
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE and trivia.current + 1 == len(trivia.words_list): # 必须回答完才能结束
                    trivia.running = False
                elif event.key == pygame.K_1:
                    trivia.handle_input(1)
                elif event.key == pygame.K_2:
                    trivia.handle_input(2)
                elif event.key == pygame.K_3:
                    trivia.handle_input(3)
                elif event.key == pygame.K_RETURN and trivia.current + 1 < len(trivia.words_list):  # 直到最后一个才能结束
                    trivia.next_question()
        pygame.display.update()  # 只要有操作就会有更新，所以要持续刷洗屏幕
