# author: SryMkr
# date: 2021.11.6
# Snake three different food

# import package
import pygame
import random
# 导入python的一些常用的常量
from pygame.locals import *


# three different food sprites
class MySprite_food(pygame.sprite.Sprite):
    # initialize some variate
    def __init__(self):
        # extend pygame.sprite.Sprite
        pygame.sprite.Sprite.__init__(self)
        # load a picture with multi-frames
        self.multi_frames = None
        # the number of current frame
        self.current_frame = 0
        # the index of current frame
        self.current_frame_index = 0
        # the number of current task
        self.current_word_number = 0
        # the number of current frame
        self.random_frame = 0
        # the width of one frame of the picture
        self.one_frame_width = 1
        # the height of one frame of the picture
        self.one_frame_height = 1
        # the number of first frame
        self.first_frame_number =0
        # the picture's columns
        self.multi_frames_columns = 1
        # the time of change frame
        self.last_change_time = 0
        # catch the amount of correct food
        self.food_number = 0
        # 创建一个正确字母和错误字母的字典
        self.letters_dic = {0: [4, 8, 14, 20, 24], 1: [3, 15, 16, 19], 2: [10, 18, 25, 19], 3: [1, 15, 16, 19],
                            4: [0, 14, 20, 24, 8], 5: [21, 22], 6: [9, 7], 7: [12, 13], 8: [0, 8, 14, 24, 4], 9: [6, 8],
                            10: [2, 6], 11: [17, 8], 12: [13, 7], 13: [12, 7], 14: [0, 4, 8, 20, 24],
                            15: [3, 1, 16, 19], 16: [15, 1, 3, 19], 17: [11, 21], 18: [25, 2], 19: [3, 2], 20: [22, 21],
                            21: [22, 20, 5], 22: [5, 21], 23: [18, 25], 24: [8, 4], 25: [18, 2]}

    # get the x coordinate of frame
    def _get_x_coordinate(self):
        return self.rect.x
    # set the x coordinate of frame

    def _set_x_coordinate(self, value):
        self.rect.x = value
    # allow the the class have x_coordinate property with two actions
    x_coordinate = property(_get_x_coordinate,_set_x_coordinate)

    # get the y coordinate of frame
    def _get_y_coordinate(self):
        return self.rect.y
    # set the y coordinate of frame

    def _set_y_coordinate(self, value):
        self.rect.y = value
    # allow the the class have y_coordinate property with two actions
    y_coordinate = property(_get_y_coordinate, _set_y_coordinate)

    # get the topleft coordinate of frame
    def _get_topleft_position(self):
        return self.rect.topleft
    # set the topleft coordinate of frame
    def _set_topleft_position(self, pos):
        self.rect.topleft = pos
    # allow the the class have topleft_position property with two actions
    topleft_position = property(_get_topleft_position, _set_topleft_position)

    # load main variety
    def load_multi_frames(self, multi_frames_filepath, one_frame_width, one_frame_height, multi_frames_columns):
        # load a picture with multi-frames
        self.multi_frames = pygame.image.load(multi_frames_filepath).convert_alpha()
        # the width of one frame of the picture
        self.one_frame_width = one_frame_width
        # the height of one frame of the picture
        self.one_frame_height = one_frame_height
        # create a rectangle
        self.rect = Rect(0, 0, one_frame_width, one_frame_height)
        # the picture's columns
        self.multi_frames_columns = multi_frames_columns

# -------------------------------------------------------------------------------------------
    # this function is for showing correct alphabet
    def target_update(self, al_dic, current_time, change_rate, x_position, y_position):
        # continuously change frame with time
        if current_time > self.last_change_time + change_rate:
            # reach the end then go to first
            if self.food_number == len(al_dic):
                self.food_number = 0
            # get values
            al_list_values = list(al_dic.values())
            # get values index
            al_list_index = list(al_dic.keys())
            # catch current frame
            self.current_frame = al_list_values[self.food_number]
            # catch current frame index
            self.current_frame_index = al_list_index[self.food_number]
            # get the number of current word
            self.current_word_number = str(self.current_frame_index).split('-')[0]
            # choose a random postion (waiting modify)
            self.topleft_position = (x_position[0] , y_position[0] )
            # replace last last_change_time with current time
            self.last_change_time = current_time
            # the x coordinate of current frame
            current_frame_x_coordinate = (self.current_frame % self.multi_frames_columns) * self.one_frame_width
            # the y coordinate of current frame
            current_frame_y_coordinate = (self.current_frame // self.multi_frames_columns) * self.one_frame_height
            # the rectangle of current frame
            current_frame_rect = Rect(current_frame_x_coordinate, current_frame_y_coordinate, self.one_frame_width, self.one_frame_height)
            # get a new surface from main picture
            self.image = self.multi_frames.subsurface(current_frame_rect)
            # 所有的单词的字母单词一个一个的更新，更新一个到下一个
            self.food_number += 1

# -------------------------------------------------------------------------------------------
    # this function is for showing tip
    def tip_update(self, current_time, change_rate, x_position, y_position):
        # continuously change frame with time
        if current_time > self.last_change_time + change_rate:
            self.current_frame = 0
            # choose a random postion (waiting modify)
            self.topleft_position = (x_position[1] , y_position[1] )
            # replace last last_change_time with current time
            self.last_change_time = current_time
            # the x coordinate of current frame
            current_frame_x_coordinate = (self.current_frame % self.multi_frames_columns) * self.one_frame_width
            # the y coordinate of current frame
            current_frame_y_coordinate = (self.current_frame // self.multi_frames_columns) * self.one_frame_height
            # the rectangle of current frame
            current_frame_rect = Rect(current_frame_x_coordinate, current_frame_y_coordinate, self.one_frame_width, self.one_frame_height)
            # get a new surface from main picture
            self.image = self.multi_frames.subsurface(current_frame_rect)

# -------------------------------------------------------------------------------------------
    # 得出当前的碰撞的字母的图片，得出以后主要是添加在蛇的后面
    # this function is for adding to snake body
    def draw_current_frame(self,frame_number):
        # the x coordinate of current frame
        current_frame_x_coordinate = (frame_number % self.multi_frames_columns) * self.one_frame_width
        # the y coordinate of current frame
        current_frame_y_coordinate = (frame_number // self.multi_frames_columns) * self.one_frame_height
        # the rectangle of current frame
        rect = Rect(current_frame_x_coordinate, current_frame_y_coordinate, self.one_frame_width, self.one_frame_height)
        # get a new surface from main picture
        self.image = self.multi_frames.subsurface(rect)

# -------------------------------------------------------------------------------------------
    # this function is for wrong answer 更新错误字母的单词，每个错误字母都有更新，改为按照一定的要求更新
    # confict_number cannot the same as correct answer
    def random_backup(self, confict_number,current_time, change_rate, x_position, y_position):
        # randomly change frame with time
        if current_time > self.last_change_time + change_rate:
            alphabet_list = list(range(0, 26))
            # remove the correct number
            alphabet_list.remove(confict_number)
            # randomly choose a alphabet
            self.random_frame = random.choice(alphabet_list)
            # random position
            self.topleft_position = (x_position, y_position)
            # replace last last_change_time with current time
            self.last_change_time = current_time
            # the x coordinate of current frame
            current_frame_x_coordinate = (self.random_frame % self.multi_frames_columns) * self.one_frame_width
            # the y coordinate of current frame
            current_frame_y_coordinate = (self.random_frame // self.multi_frames_columns) * self.one_frame_height
            # the rectangle of current frame
            random_rect = Rect(current_frame_x_coordinate, current_frame_y_coordinate, self.one_frame_width,
                        self.one_frame_height)
            # get the image surface
            self.image = self.multi_frames.subsurface(random_rect)

    # this function is for wrong answer 更新错误字母的单词，每个错误字母都有更新，改为按照一定的要求更新
    # confict_number cannot the same as correct answer
    def random_update(self, confict_number, current_time, change_rate, x_position, y_position):
        # randomly change frame with time
        if current_time > self.last_change_time + change_rate:
            confused_letters = self.letters_dic[confict_number]
            # randomly choose a alphabet
            self.random_frame = random.choice(confused_letters)
            # random position
            self.topleft_position = (x_position, y_position)
            # replace last last_change_time with current time
            self.last_change_time = current_time
            # the x coordinate of current frame
            current_frame_x_coordinate = (self.random_frame % self.multi_frames_columns) * self.one_frame_width
            # the y coordinate of current frame
            current_frame_y_coordinate = (self.random_frame // self.multi_frames_columns) * self.one_frame_height
            # the rectangle of current frame
            random_rect = Rect(current_frame_x_coordinate, current_frame_y_coordinate, self.one_frame_width,
                               self.one_frame_height)
            # get the image surface
            self.image = self.multi_frames.subsurface(random_rect)



