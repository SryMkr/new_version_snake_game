"""
author SryMkr
date: 2021.11.6
the function of this library is to download words' phonetics
有时候单词比较多会不下载，但是也不是找不到的原因，可能是网络问题
最好的办法就是我们已经下载好了，尽量网络的还有机器的依赖
本算法最基本的逻辑结构就是一个单词一个音标写到excel中,并且也是在xls中读取单词音标,仅限与做实验使用
本文件中有一个函数是要在游戏中使用，在毕业之前本页函数没有任何需要改的地方
"""

# import packages
import os
import requests
import re
from xlutils.copy import copy
import xlrd


# ----------------------------------------------------------------------------------------------------------------------
# write format: list[word,phonetic] into excel.xls 该函数仅限于本页代码使用
# 本代码的作用是将下载好的单词和音标写到文件中 是下载一组写一组, 一个英语单词和一个音标为一组
def write_excel_xls_append(path, value):
    # get the len of value 只有单词和音标所以总为2
    index = len(value)
    # open a workbook，打开要写进去的目标文件
    workbook = xlrd.open_workbook(path)
    # get all sheet names 打开文件簿中所有的文件
    sheets = workbook.sheet_names()
    # get the first sheet，打开第一页
    worksheet = workbook.sheet_by_name(sheets[0])
    # get the rows of sheet，得到文件中有多少行
    rows_old = worksheet.nrows
    # copy the workbook，需要复制一个文件来覆盖原文件
    new_workbook = copy(workbook)
    # get the first worksheet，复制文件的第一页
    new_worksheet = new_workbook.get_sheet(0)
    # 先写单词，再写音标
    for i in range(0, index):
        # column always is 0 and 1  参数i其实就是列 第一列写单词 第二列写发音，
        new_worksheet.write(rows_old, i, value[i])
    # save file 保存并覆盖原文件
    new_workbook.save(path)


# 试验代码
# write_excel_xls_append('Words_phonetic\sis.xls',['word', 'wəːd'])  实验代码
# ----------------------------------------------------------------------------------------------------------------------


# 该代码仅限于本页使用
# check whether the words in excel.xls 检查即将下载的单词有没有已经下载好了
def read_excel_xls(path, word):
    # open workbook
    workbook = xlrd.open_workbook(path)
    # get all sheets by sheet names
    sheets = workbook.sheet_names()
    # get the first sheet
    worksheet = workbook.sheet_by_name(sheets[0])
    # get the correspond content，得到第一列的所有单词
    words = worksheet.col_values(0)
    # if word in words，查看所需要的单词在不在列表中
    if word in words:
        return True
    else:
        return False


# 试验代码
# print(read_excel_xls('Words_phonetic\sis.xls', 'word'))

# ----------------------------------------------------------------------------------------------------------------------


# 以下代码是下载牛津的音标
# phonetic alphabet class
class OxfordDictionary:
    # initialize empty string 初始化一个空的字符串
    phoneticSpelling = ""

    # create directory for phonetic format ['word','xxx.xls']
    def __init__(self, word, filename):
        # convert to lowercase word 小写
        word = word.lower()
        # move space 两边去空字符
        self._word = word.strip()
        # filename 得到要写入的文件
        self._fileName = filename
        # get the absolute current path，首先得到这个页面所在的绝对路径
        self._dirRoot = os.path.dirname(os.path.abspath(__file__))
        # concatenate the file path 将绝对文件路径和我们要下载进去的音标文件夹连接起来
        self._dirSpeech = os.path.join(self._dirRoot, 'Words_phonetic')
        # 如果这个文件夹不存在就创建文件
        # file exist?
        if not os.path.exists('Words_phonetic'):
            # create if no
            os.makedirs('Words_phonetic')
        # 将文件夹和指定的excel表连接
        # get the filename path,直接定位到指定的xls文件
        self._filePath = os.path.join(self._dirSpeech, self._fileName)

    # 找到牛津的页面下载音标
    def _getPho(self):
        # phonetic exist? 首先检查单词有没有已经下载好了
        if read_excel_xls(self._filePath, self._word):
            # yes pass  如果已经下载好了，就直接跳过
            pass
        # no download 如果没有下载好 就去找网页
        else:
            list = []
            # 先将单词添加到列表中
            list.append(self._word)
            # get the url 连接单词去网页
            request = requests.get("https://en.oxforddictionaries.com/definition/" + self._word)
            # convert the whole content to text
            html = request.text
            # locate the target content
            regularExpression = r'<span\s+class="phoneticspelling">/([^\/]*)/</span>'
            # scan all content and return the first matched content with ignoring the l_u case letter
            matchObject = re.search(regularExpression, html, re.I)
            # if get
            if matchObject:
                # if phonetic exist
                if matchObject.group(1):
                    self.phoneticSpelling = matchObject.group(1)
                else:
                    self.phoneticSpelling = None
            # make the list format 已经有单词了，再添加音标
            list.append(self.phoneticSpelling)
            # write into the excel.xls 直接写道文件夹中
            write_excel_xls_append(self._filePath, list)


# ----------------------------------------------------------------------------------------------------------------------
# get the word phonetic in excel.xls   path使用绝对路径和相对路径都可以 这个在游戏中显示
def get_word_pho(path, word):
    # open workbook
    workbook = xlrd.open_workbook(path)
    # get all sheets by sheet names
    sheets = workbook.sheet_names()
    # get the first sheet
    worksheet = workbook.sheet_by_name(sheets[0])
    # get the correspond content 先得到第一列的单词
    words = worksheet.col_values(0)
    # if word in words
    if word in words:
        # return the word index 如果有这个单词就返回这个单词的索引
        word_index = words.index(word)
        # return the phonetic 根据索引返回音标
        return worksheet.cell_value(word_index, 1)
    else:
        return None
