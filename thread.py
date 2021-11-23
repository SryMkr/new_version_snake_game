import threading
from word_pronounciation_library import *
from words_phonetic_library import *
import time


# 为了下载音频所以需要创建线程来单独下载单词的发音，直接将所有的单词列表读取进去就能下载， 音标里面的文件名改一下就行
# 做实验，不要下载那么多单词了

class myThread(threading.Thread):  # 继承父类threading.Thread
    def __init__(self, threadID, name, words_list):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.words_list = words_list

    def run(self):  # 把要执行的代码写到run函数里面 线程在创建后会直接运行run函数
        # load pronunciation
        for i in range(len(self.words_list) - 1):
            sp = youdao(self.words_list[i])
            sp.down()
        time.sleep(0.1)


class myThread_PHO(threading.Thread):  # 继承父类threading.Thread
    def __init__(self, threadID, name, words_list):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.words_list = words_list

    def run(self):  # 把要执行的代码写到run函数里面 线程在创建后会直接运行run函数
        # load pronunciation
        for i in range(len(self.words_list)):
            # 这个地方需要修改你想要存入的excel文件名
            wp = OxfordDictionary(self.words_list[i], 'sis.xls')
            wp._getPho()
            time.sleep(0.1)


'''
本代码的运行实例就是，首先输入是一个words 列表
list = ['a','b','c','d']
# 线程名字和ID无所谓，随便列举
a= myThread(1,'haha',list)
a.run()
b = myThread_PHO(2,'xixi',list)
b.run()

'''
