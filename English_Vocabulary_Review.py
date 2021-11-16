import sys
import pygame,random
from pygame.locals import *
from words_handling_library import read_taskwords_xls

from Other_library import print_text

'''
复习模式应该怎么设置？ 如何和学习模式相结合
'''



class Trivia(object):
    def __init__(self, review_file_name, train_words_number):
        self.words_list = []
        self.task_words = []
        self.words_dic = []
        self.dic = []
        self.running = True
        self.current = 0  # 当前正在拼写的单词
        self.corrected = False  # 回答正确
        self.failed = False  # 回答错误
        self.__review_file_name = review_file_name
        self.__train_words_number = train_words_number
        self.FONT1 = pygame.font.Font('Fonts/STKAITI.TTF', 35)
        self.FONT2 = pygame.font.Font('Fonts/arial.ttf', 35)
        self.voiced_lists = {'a': ['e', 'o'], 'b': ['d', 'p', 'q'], 'c': ['k', 's', 'z'], 'd': ['b', 'p', 'q'],
                             'e': ['a', 'o', 'y', 'i'], 'f': ['v', 'w'], 'g': ['j'], 'h': ['n'], 'i': ['y', 'e'],
                             'j': ['g'], 'k': ['c'], 'm': ['n', 'h'], 'n': ['m', 'h'], 'o': ['a', 'e'],
                             'p': ['d', 'b', 'q'], 'q': ['p', 'b', 'd'], 's': ['z', 'c'], 'u': ['w', 'v'],
                             'v': ['w', 'u'], 'w': ['f', 'v'], 'x': ['s', 'z'], 'y': ['i', 'e'], 'z': ['s', 'c'],
                             'r': [''], 't': [''], 'l': ['']}
        # 得到了英文单词，得到了汉语翻译
        self.words_list, self.task_words = read_taskwords_xls(self.__review_file_name, self.__train_words_number)

    # 生成答案列表
    def shuffle_alphabet (self, word):
        answers_lists = []
        alphabet_lists = []
        for i in word:
            alphabet_lists.append(i)
        chosen_alphabet = random.sample(alphabet_lists, 2)
        for i in chosen_alphabet:
            if i in self.voiced_lists.keys():
                wrong_word = word.replace(i, random.sample(self.voiced_lists[i], 1)[0])
                answers_lists.append(wrong_word)
        answers_lists.append(word)
        random.shuffle(answers_lists)
        return answers_lists

    # 问题和选项和正确的单词字母的组合列表
    def question_answers(self):
        for i in range(self.__train_words_number):
            self.words_dic.append(self.task_words[i])
            questions_list = self.shuffle_alphabet(self.words_list[i])  # 得到某个单词的错误选项
            for j in questions_list:
                self.words_dic.append(j)
            correct_index = questions_list.index(self.words_list[i])
            self.words_dic.append(correct_index)
            self.dic.append(self.words_dic)
            self.words_dic = []
        return self.dic

    def show_question(self, question_answers_index_list, number ):
        # 简单打印一些页面上的东西
        print_text(self.FONT1, 210, 5, "单项选择题")
        print_text(self.FONT1, 130, 500, "请按 1，2，3 回答问题", (255, 0, 255))
        question = question_answers_index_list[number][0]
        print_text(self.FONT1, 5, 80, "问题：" + question + '的正确拼写为：')
        print_text(self.FONT2, 20, 170, "1 : " + question_answers_index_list[number][1])
        print_text(self.FONT2, 20, 270, "2 : " + question_answers_index_list[number][2])
        print_text(self.FONT2, 20, 370, "3 : " + question_answers_index_list[number][3])
        self.correct = question_answers_index_list[number][4] + 1  # 获得当前的正确选项

        if self.corrected:
            print_text(self.FONT1, 210, 400, "回答正确!")
            if self.current + 1 < len(self.words_list):
                print_text(self.FONT1, 100, 440, "请按 Enter 回答下一个问题")
            else:
                print_text(self.FONT1, 100, 440, "学习结束，请按 ESC 返回上一菜单")
        elif self.failed:
            print_text(self.FONT1, 210, 400, "请再仔细想想")

    # 获取键盘的输入
    def handle_input(self, number):
        if not self.corrected or not self.failed:
            if number == self.correct:  # 输入的字母与正确的字母相匹配？
                self.corrected = True
            else:
                self.failed = True

    # 进入下一个问题
    def next_question(self,screen):
        if self.corrected:
            self.corrected = False
            self.failed = False
            self.current += 1


def English_review(screen):
    trivia = Trivia('words_pool/three_grade/three_grade_known.xls', 3)  # 读取文件
    question_answers_index_list = trivia.question_answers()
    while trivia.running:
        Eng_review = pygame.image.load("Game_Pictures/game_intro.jpg").convert_alpha()  # load background picture
        game_intro = pygame.transform.scale(Eng_review, (30 * 22, 30 * 22))  # scale to display
        screen.blit(game_intro, (0, 0))  # draw background picture
        trivia.show_question(question_answers_index_list,trivia.current)
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    trivia.running = False
                elif event.key == pygame.K_1:
                    trivia.handle_input(1)
                elif event.key == pygame.K_2:
                    trivia.handle_input(2)
                elif event.key == pygame.K_3:
                    trivia.handle_input(3)
                elif event.key == pygame.K_4:
                    trivia.handle_input(4)
                elif event.key == pygame.K_RETURN and trivia.current + 1 < len(trivia.words_list):
                    trivia.next_question(screen)
        pygame.display.update()
