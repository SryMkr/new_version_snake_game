'''
    author SryMkr
    date:2021.11.6
    this library is for snake head
    本页函数的目的只是为了控制头部，因为蛇的头部只需要控制方向，其他的不用管
'''


# import package
import pygame
from pygame.locals import *


# 定义蛇的头部的类
class MySprite_head(pygame.sprite.Sprite):
    # initialize some parameters
    def __init__(self):
        # extend pygame.sprite.Sprite
        pygame.sprite.Sprite.__init__(self)
        # main picture consists of neat frames
        self.multi_frames = None
        # the number of current frame
        self.current_frame = 0
        # the number of first frame
        self.first_frame = 0
        # the number of last frame
        self.last_frame = 1
        # the width of one frame
        self.one_frame_width =1
        # the height of one frame
        self.one_frame_height = 1
        # the columns of main picture
        self.multi_frames_columns = 1
        # for record last change time
        self.last_time = 0
        # control the direction of head
        self.head_direction = 0
    # get x_coordinate of one frame
    def _get_x_coordinate(self):
        return self.rect.x
    # set x_coordinate of one frame
    def _set_x_coordinate(self,value):
        self.rect.x = value
    # 蛇头部的X的坐标，可以读取，可以玩家自行设置
    x_coordinate = property(_get_x_coordinate,_set_x_coordinate)

    # get y_coordinate of one frame
    def _get_y_coordinate(self):
        return self.rect.y

    # set y_coordinate of one frame
    def _set_y_coordinate(self, value):
        self.rect.y = value
    # 蛇头部的Y的坐标，可以读取，可以玩家自行设置
    y_coordinate = property(_get_y_coordinate, _set_y_coordinate)

    # load frame parameters 加载蛇头部的图片
    def load_head_frames(self, multi_frames_filepath, one_frame_width, one_frame_height, multi_frames_columns):
        # load main picture
        self.multi_frames = pygame.image.load(multi_frames_filepath).convert_alpha()
        # load frame width
        self.one_frame_width = one_frame_width
        # load frame height
        self.one_frame_height = one_frame_height
        # Create frame Rect(left, top, width, height) the position，精灵中必须得有位置坐标
        self.rect = Rect(0, 0, one_frame_width, one_frame_height)
        # frame's columns
        self.multi_frames_columns = multi_frames_columns

    # snake head action   头部动态显示
    def head_update(self, current_time, change_rate=30):
        if current_time > self.last_time + change_rate:
            # frame loop
            if self.current_frame > self.last_frame:
                self.current_frame = self.first_frame
            # record time
            self.last_time = current_time
            # the x coordinate of current frame
            frame_x = (self.current_frame % self.multi_frames_columns) * self.one_frame_width
            # the y coordinate of current frame
            frame_y = (self.current_frame // self.multi_frames_columns) * self.one_frame_height
            # locate target range
            rect = Rect(frame_x, frame_y, self.one_frame_width, self.one_frame_height)
            # get target frame   return surface 精灵中必须得有对应要显示的图片，切割对应图片
            self.image = self.multi_frames.subsurface(rect)
            # change to next frame 自动到下一个图片编号
            self.current_frame += 1


# define the snake head direction 该函数得目的是得到蛇得方向，切换对应得头部图片，然后编号 （0，-1，1）编号
def snake_head_direction(snake, snake_direction):
    # up
    if snake_direction.second_variate < 0:
        snake.snake_head.first_frame = 1 * snake.snake_head.multi_frames_columns
        snake.snake_head.last_frame = snake.snake_head.first_frame + 1
    # down
    elif snake_direction.second_variate > 0:
        snake.snake_head.first_frame = 3 * snake.snake_head.multi_frames_columns
        snake.snake_head.last_frame = snake.snake_head.first_frame + 1
    # lift
    elif snake_direction.first_variate < 0:
        snake.snake_head.first_frame = 0 * snake.snake_head.multi_frames_columns
        snake.snake_head.last_frame = snake.snake_head.first_frame + 1
    # right
    elif snake_direction.first_variate > 0:
        snake.snake_head.first_frame = 2 * snake.snake_head.multi_frames_columns
        snake.snake_head.last_frame = snake.snake_head.first_frame + 1
    # 其实大小方向都变了，只不过小于在这边，大于在update里面变了
    if snake.snake_head.current_frame < snake.snake_head.first_frame:
        snake.snake_head.current_frame = snake.snake_head.first_frame
