'''
author SryMkr
date 2021.8
final version of Snake English Game
复习模式和学习模式的切换会出现问题
1： 但是要记录下来再游戏结束收显示玩家在哪里拼错了,
3： 选择题
2： 加减分数显示
3： 个性化游戏
'''

# 每个单词需要记录的数据基于大数据分析,然后给出合适的难度


# import packages
import pygame
from English_Vocabulary_Review import English_review
from Snake_body_library import *
from game_introducation import *
import time, datetime, sys
from words_handling_library import *
# 导入得出音标的函数
from words_phonetic_library import get_word_pho
import pygame_menu

# 玩家启动游戏的日期 (year-month-day)
TODAY = datetime.date.today()
# 游戏运行开始计时为 0
t0 = time.perf_counter()
# 玩家玩了多长时间
player_played_game = 0
# 玩家本次游戏得了多少分
current_score = 0
# 玩家本次游戏记了多少单词
current_remembered_words = 0
# 总记忆单词数，总共玩游戏的时间，历史最高得分，历史最高记忆的单词数
total_remembered_words, total_spent_words, highest_score, highest_words = \
    read_excel_game_record('saved_files/game_record.xls')
record_list = [total_remembered_words, total_spent_words, highest_score, highest_words]

# 本次游戏已经记忆的单词列表（英文）
words_list_known = []
# 本次游戏已经记忆的单词列表（汉语）
task_words_known = []
# 记录玩家的拼写
player_spelling = []
# 要记录这个单词已经拼写到哪了
spell_list = list()
# 玩家选择此次学习多少单词
train_words_number = 9
# 要记录玩家已经练习多少个单词了，要是练习玩了要游戏结束
words_number = 0

# ------------------------------------------------------------------------------------------
# 对游戏屏幕，标题，字体的初始化
# 设置屏幕有多少30像素
screen_grid_width = 22
screen_grid_high = 22
# initialize some modules
pygame.init()
# set the width and height of window
screen = pygame.display.set_mode((FRAME_WIDTH * screen_grid_width, FRAME_WIDTH * screen_grid_high))
# set screen caption
pygame.display.set_caption("English Vocabulary Practice")
# show the Chinese fonts on the display
CHINESE_FONT = pygame.font.Font('Fonts/STKAITI.TTF', 25)
INTRO_FONT = pygame.font.Font('Fonts/STKAITI.TTF', 25)
SCORE_FONT = pygame.font.Font('Fonts/STKAITI.TTF', 50)
# show  English font on the display
OTHER_FONT = pygame.font.Font('Fonts/arial.ttf', 25)
# shoe the phonetic font on the display
PHONETIC_FONT = pygame.font.Font('Fonts/Lucida-Sans-Unicode.ttf', 25)


# ------------------------------------------------------------------------------------------


# 保存玩家的游戏记录代码
def save_game_record():
    global total_spent_words
    # 玩家本次玩游戏一共玩了多少分钟
    player_played_game = (time.perf_counter() - t0) / 60
    # 记录本论游戏玩家的游戏记录
    review_list = [str(TODAY), round(player_played_game, 2), current_score, current_remembered_words]
    total_spent_words += player_played_game
    # 总共记忆的单词，和总的游戏时间
    record_list[0] = total_remembered_words + current_remembered_words
    record_list[1] = total_spent_words
    write_excel_game_review('saved_files/game_review.xls', review_list)
    write_excel_game_record('saved_files/game_record.xls', record_list)
    # 原单词表中删除已经记住的单词
    delete_taskwords_xls(word_file_path, words_list_known)
    # 英语单词，和翻译都要写进已经记住的单词库里面
    write_knownwords_xls(word_review_file_path, words_list_known, task_words_known)
    sys.exit(0)


# initial
def game_init():
    # global variate
    global snake, alphabet, alphabet_group, snake_speed, background_music_setting, \
        tip_group, track_spelling_setting, words_list, task_words, \
        tip, wrong_words_num_setting, continuous_correct_alphabet, \
        words_phonetic_setting, tip_show_setting, train_words_num_setting, word_file_path, \
        phonetic_file_path, pronunciation_file_path, train_words_number, word_review_file_path

    # 初始化蛇
    snake = Snake_body_Sprite()
    # 先把蛇头添加进去
    snake.creat_snake()

    # 创建一个正确单词的组
    alphabet_group = pygame.sprite.Group()
    alphabet = MySprite_food()
    alphabet.load_multi_frames("Game_Pictures/lower_letter.png", FRAME_WIDTH, FRAME_WIDTH, 13)
    alphabet_group.add(alphabet)

    # 第一页的菜单，背景和标题背景都会有默认值很丑，所以这句话的意思是给他全部弄成透明的就不会在游戏上显示了
    mytheme_fix = pygame_menu.themes.Theme(background_color=(0, 0, 0, 0), title_background_color=(0, 0, 0, 0))
    # 实例化第一层菜单
    game_fix_menu = pygame_menu.Menu(400, 400, '', theme=mytheme_fix, menu_position=(80, 60))
    # 设置第二层菜单主题格式
    mytheme1 = pygame_menu.themes.Theme(background_color=(0, 0, 0, 0), title_background_color=(0, 0, 0, 0))
    # 第二层菜单的位置和大小
    game_first_mune = pygame_menu.Menu(400, 200, '', theme=mytheme1, menu_position=(65, 60))
    # 设置本次训练的单词个数
    train_words_num_setting = game_fix_menu.add_text_input('单词数(5-15): ', default='9', font_name='Fonts/STKAITI.TTF',
                                                           selection_color=(255, 0, 0), background_color=(0, 255, 0))
    # 选择词库
    grade_setting = game_fix_menu.add_selector('选择词库',
                                               [('三年级', screen), ('四年级', screen), ('五年级', screen), ('六年级', screen),
                                                ('初一', screen), ('初二', screen), ('初三', screen)],
                                               font_name='Fonts/STKAITI.TTF',
                                               selection_color=(255, 0, 0), background_color=(0, 255, 0))
    # 进入游戏
    game_fix_menu.add_button('进入游戏', game_first_mune, font_name='Fonts/STKAITI.TTF', background_color=(0, 255, 0),
                             selection_color=(255, 0, 0))

    # 第二页游戏设置里的背景图片，设置一个主题
    myimage = pygame_menu.baseimage.BaseImage('Game_Pictures/game_intro.jpg')
    mytheme = pygame_menu.themes.Theme(background_color=myimage, title_background_color=(0, 0, 0, 0),
                                       title_font_color=(255, 0, 0))
    game_setting_mune = pygame_menu.Menu(FRAME_WIDTH * screen_grid_width, FRAME_WIDTH * screen_grid_high, '',
                                         theme=mytheme, menu_id='game_setting')

    # 设置干扰选项
    wrong_words_num_setting = game_setting_mune.add_text_input('干扰选项(1-3): ', default='1',
                                                               font_name='Fonts/STKAITI.TTF',
                                                               selection_color=(255, 0, 0))

    # 蛇的移动速度设置
    snake_speed = game_setting_mune.add_text_input('蛇的移动速度(100-800): ', default='200', font_name='Fonts/STKAITI.TTF',
                                                   textinput_id='snake_speed', selection_color=(255, 0, 0))
    # 有无字母追踪
    track_spelling_setting = game_setting_mune.add_selector('拼写追踪', [('YES', screen), ('NO', screen)],
                                                            font_name='Fonts/STKAITI.TTF', selection_color=(255, 0, 0))
    # 有无背景音乐
    background_music_setting = game_setting_mune.add_selector('背景音乐', [('YES', screen), ('NO', screen)],
                                                              font_name='Fonts/STKAITI.TTF',
                                                              selection_color=(255, 0, 0))
    # 有无提示
    tip_show_setting = game_setting_mune.add_selector('单词提示', [('YES', screen), ('NO', screen)],
                                                      font_name='Fonts/STKAITI.TTF', selection_color=(255, 0, 0))
    # 有无音节
    words_phonetic_setting = game_setting_mune.add_selector('单词音节', [('YES', screen), ('NO', screen)],
                                                            font_name='Fonts/STKAITI.TTF', selection_color=(255, 0, 0))
    # 保存设置，并返回上一级菜单
    game_setting_mune.add_button('保存并返回', pygame_menu.events.BACK,
                                 font_name='Fonts/STKAITI.TTF', selection_color=(255, 0, 0))
    # 第一页菜单所展示的内容
    # game_first_mune.add_button('复习模式', main_game, True, font_name='Fonts/STKAITI.TTF', background_color=(0, 255, 0),
    #                           selection_color=(255, 0, 0))
    game_first_mune.add_button('复习模式', English_review, screen, font_name='Fonts/STKAITI.TTF',
                               background_color=(0, 255, 0),
                               selection_color=(255, 0, 0))
    game_first_mune.add_button('开始游戏', main_game, font_name='Fonts/STKAITI.TTF', background_color=(0, 255, 0),
                               selection_color=(255, 0, 0))
    game_first_mune.add_button('游戏设置', game_setting_mune, font_name='Fonts/STKAITI.TTF',
                               background_color=(0, 255, 0), selection_color=(255, 0, 0))
    game_first_mune.add_button('游戏记录', game_record, screen, INTRO_FONT, font_name='Fonts/STKAITI.TTF',
                               background_color=(0, 255, 0), selection_color=(255, 0, 0))
    game_first_mune.add_button('游戏帮助', game_intro, screen, INTRO_FONT, font_name='Fonts/STKAITI.TTF',
                               background_color=(0, 255, 0), selection_color=(255, 0, 0))
    game_first_mune.add_button('结束游戏', save_game_record, font_name='Fonts/STKAITI.TTF', background_color=(0, 255, 0),
                               selection_color=(255, 0, 0))

    # play the background music
    game_audio("game_sound/bgm.wav", volumn=0.3, times=-1)

    # load the background of first menu
    game_bgp = pygame.image.load("Game_Pictures/Snake_Begin_UI.png").convert_alpha()
    # 有时候图片太大，需要调整图片大小符合目标屏幕大小
    game_bgp = pygame.transform.scale(game_bgp, (FRAME_WIDTH * screen_grid_width, FRAME_WIDTH * screen_grid_high))

    while True:
        screen.blit(game_bgp, (0, 0))
        if train_words_num_setting.get_selected_time():
            # 取得玩家设置的单词数
            train_words_number = game_play_setting(train_words_num_setting)
            # 选择词库
            if grade_setting.get_value()[0][0] == '三年级':
                word_file_path = 'words_pool/three_grade/three_grade_unknown.xls'
                phonetic_file_path = 'Words_phonetic/three_grade/three_grade_phonetic.xls'
                pronunciation_file_path = 'Speech_EN/three_grade/'
                word_review_file_path = 'words_pool/three_grade/three_grade_known.xls'
            elif grade_setting.get_value()[0][0] == '四年级':
                word_file_path = 'words_pool/four_grade/four_grade_unknown.xls'
                phonetic_file_path = 'Words_phonetic/four_grade/four_grade_phonetic.xls'
                pronunciation_file_path = 'Speech_EN/four_grade/'
                word_review_file_path = 'words_pool/four_grade/four_grade_known.xls'
            elif grade_setting.get_value()[0][0] == '五年级':
                word_file_path = 'words_pool/five_grade/five_grade_unknown.xls'
                phonetic_file_path = 'Words_phonetic/five_grade/five_grade_phonetic.xls'
                pronunciation_file_path = 'Speech_EN/five_grade/'
                word_review_file_path = 'words_pool/five_grade/five_grade_known.xls'
            elif grade_setting.get_value()[0][0] == '六年级':
                word_file_path = 'words_pool/six_grade/six_grade_unknown.xls'
                phonetic_file_path = 'Words_phonetic/six_grade/six_grade_phonetic.xls'
                pronunciation_file_path = 'Speech_EN/six_grade/'
                word_review_file_path = 'words_pool/six_grade/six_grade_known.xls'
            elif grade_setting.get_value()[0][0] == '初一':
                word_file_path = 'words_pool/seven_grade/seven_grade_unknown.xls'
                phonetic_file_path = 'Words_phonetic/seven_grade/seven_grade_phonetic.xls'
                pronunciation_file_path = 'Speech_EN/seven_grade/'
                word_review_file_path = 'words_pool/seven_grade/seven_grade_known.xls'
            elif grade_setting.get_value()[0][0] == '初二':
                word_file_path = 'words_pool/eight_grade/eight_grade_unknown.xls'
                phonetic_file_path = 'Words_phonetic/eight_grade/eight_grade_phonetic.xls'
                pronunciation_file_path = 'Speech_EN/eight_grade/'
                word_review_file_path = 'words_pool/eight_grade/eight_grade_known.xls'
            elif grade_setting.get_value()[0][0] == '初三':
                word_file_path = 'words_pool/nine_grade/nine_grade_unknown.xls'
                phonetic_file_path = 'Words_phonetic/nine_grade/nine_grade_phonetic.xls'
                pronunciation_file_path = 'Speech_EN/nine_grade/'
                word_review_file_path = 'words_pool/nine_grade/nine_grade_known.xls'
            # 得到单词，和翻译 是分开的
            words_list, task_words = read_taskwords_xls(word_file_path,
                                                        train_words_number)
            # 这是一个字典 第几个单词-第几个字母：以及对应单词的字母索引
            continuous_correct_alphabet = built_spelling_dic(words_list, ALPHABET_LIST)

        # 获得当前所有事件
        events = pygame.event.get()
        # 如果第一页菜单处于运行状态
        if game_fix_menu.is_enabled():
            # 抓取菜单的改变
            game_fix_menu.update(events)
            # 将改变后的菜单画到桌面上
            game_fix_menu.draw(screen)
        # 整个游戏更新
        pygame.display.update()


# define pause and continue game
def checkquit(events):
    global pause, main_game_running
    for event in events:
        if event.type == pygame.QUIT:
            if game_over == False:
                save_game_record()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                main_game_running = False
            elif event.key == pygame.K_p:
                pause = False
            elif event.key == pygame.K_SPACE:
                pause = True
            elif event.key == pygame.K_q:
                word_pro = words_list[int(alphabet.current_word_number) - 1]
                pygame.mixer.music.load(pronunciation_file_path + word_pro + ".mp3")
                pygame.mixer.music.set_volume(1)
                pygame.mixer.music.play()


def main_game(review_mode=False):
    global highest_words, highest_score, task_words, \
        pause, record_list, words_number, game_over, \
        current_score, words_lock, continuous_correct_alphabet, \
        current_remembered_words, main_game_running, words_list, \
        phonetic_file_path, pronunciation_file_path, word_review_file_path
    # 得到玩家设置的蛇的移动速度
    snake_moving_speed = game_play_setting(snake_speed)

    # 背景音乐设置
    bgm = game_play_setting(background_music_setting)
    if bgm[0][0] == 'YES':
        # 先得把开始设置的那个背景音乐停止
        pygame.mixer.stop()
        # 才能开始新的，不然就会有双重奏乐
        game_audio("game_sound/bgm.wav", volumn=0.3, times=-1)
    # mute the bgm
    elif bgm[0][0] == 'NO':
        pygame.mixer.stop()

    # 单词提示 ‘yes’ 'no'
    prompt_show = game_play_setting(tip_show_setting)
    # 拼写追踪 ‘yes’ 'no'
    track_spelling = game_play_setting(track_spelling_setting)
    # 有无音节 ‘yes’ 'no'
    word_phone = game_play_setting(words_phonetic_setting)
    # 迷惑字母个数
    wrong_letters_num = int(game_play_setting(wrong_words_num_setting))

    # 复习模式 训练单词数相同 但是单词库变了 这块在切换上面还有问题
    if review_mode == True:
        words_list, task_words = read_taskwords_xls(word_review_file_path, int(train_words_number))
        continuous_correct_alphabet = built_spelling_dic(words_list, ALPHABET_LIST)

    # 默认需要提示，然后设置一个精灵库 在这里修改字母照片
    if prompt_show[0][0] == 'YES':
        # create tip sprite
        tip_group = pygame.sprite.Group()
        tip = MySprite_food()
        tip.load_multi_frames("Game_Pictures/health.png", FRAME_WIDTH, FRAME_WIDTH, 1)
        tip_group.add(tip)

    # 根据迷惑单词个数创造精灵
    random_alphabet_group = pygame.sprite.Group()
    for i in range(wrong_letters_num):
        random_alphabet = MySprite_food()
        random_alphabet.load_multi_frames("Game_Pictures/lower_letter.png", FRAME_WIDTH, FRAME_WIDTH, 13)
        random_alphabet_group.add(random_alphabet)

    # game_over switch
    game_over = False
    # pause and play switch
    pause = False
    # 下面这两个参数完全是为了避免出现的精灵位置和蛇偶然重叠
    food_snake_conflict = False
    count = 0
    # 追踪蛇已经吃的字母
    eating_spelling = list()
    # 下面的参数是为了设置提示
    tip_time = 0
    tip_show = False
    # 玩家有没有用提示？
    tip_use = False
    # 控制分数
    score_show_time = 0
    score_show = False
    correct_increase = False
    wrong_decrease = False
    tip_decrease = False
    # 主要是控制结束的那个声音，不然游戏结束了那个声音会一直响
    write_button = False
    # 防止重复写
    game_over_buzz = True
    main_game_running = True
    while main_game_running:
        # game clock
        timer = pygame.time.Clock()
        # how many frames in 1S
        timer.tick(60)
        # get kinds of events
        events = pygame.event.get()
        checkquit(events)
        # update drawing paper every loop
        # it seems like replace the last picture with new picture
        screen.fill((255, 255, 255))
        # 记录游戏运行的时间
        gameplay_time = pygame.time.get_ticks()
        # 得到玩家的最高分数和最高单词记录
        record_list[2] = highest_score
        record_list[3] = highest_words
        grid_bg = pygame.image.load("Game_Pictures/grid_bgb.png").convert_alpha()
        screen.blit(grid_bg, (0, 180))
        # 更新记录
        if current_score > int(highest_score):
            highest_score = current_score
        if current_remembered_words > int(highest_words):
            highest_words = current_remembered_words

        # once out of words, then game over
        if words_number == len(task_words) and game_over_buzz == True:
            words_number = 0
            game_over = True
            write_button = True

        # once game is paused
        if pause:
            pygame.mixer.pause()  # Pause BGM
            pause_pic = pygame.image.load("Game_Pictures/pause.png").convert_alpha()
            screen.blit(pause_pic, (150, 400))

        # ----------------------------------------------------------------------------------------------------------------------
        # 以下代码都是为了控制蛇的方向，
        else:
            pygame.mixer.unpause()  # Unpause BGM
            # Snake appear from another wall once contact walls
            x = snake.segments[0].x_coordinate // 30
            y = snake.segments[0].y_coordinate // 30
            # appear from other side when contact wall
            if x < 0:
                snake.segments[0].x_coordinate = 21 * 30
            elif x >= 22:
                snake.segments[0].x_coordinate = 0
            elif y < 6:
                snake.segments[0].y_coordinate = 21 * 30
            elif y >= 22:
                snake.segments[0].y_coordinate = 30 * 6
            # control the directions of snake
            for event in events:
                if 0 <= x <= 22 and 6 <= y <= 22:
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_w and snake.velocity.second_variate != 1:  # up
                            snake.velocity = two_Variate(0, -1)
                        elif event.key == pygame.K_s and snake.velocity.second_variate != -1:  # down
                            snake.velocity = two_Variate(0, 1)
                        elif event.key == pygame.K_a and snake.velocity.first_variate != 1:  # left
                            snake.velocity = two_Variate(-1, 0)
                        elif event.key == pygame.K_d and snake.velocity.first_variate != -1:  # right
                            snake.velocity = two_Variate(1, 0)
            snake_head_direction(snake, snake.velocity)  # get the direction of snake
            snake.snake_head.head_update(gameplay_time, 100)  # update the snake' head frame
            # ----------------------------------------------------------------------------------------------------------------------
            # if not game over
            if not game_over:

                # 游戏没有结束，必须先判断坐标有没有重叠
                while not food_snake_conflict:
                    # 得到蛇头的坐标
                    snake_head_x_coordinate = snake.snake_head.x_coordinate
                    snake_head_y_coordinate = snake.snake_head.y_coordinate
                    # 在这里修改要添加字母的个数，随机位置首先不能刚好在蛇头那个方向上，会误吃
                    x_position_list, y_position_list = food_random_position(snake_head_x_coordinate,
                                                                            snake_head_y_coordinate,
                                                                            wrong_letters_num + 2)
                    # 生成的位置同样不能在蛇的身上
                    food_position, snake_position = snake.snake_position(x_position_list, y_position_list)
                    # 将所有的坐标和蛇所有的坐标进行比对
                    for i in food_position:
                        # if not go on
                        if i not in snake_position:
                            count += 1
                        # if so, get new position
                        else:
                            count = 0
                            break
                    # 当所有的坐标和蛇都不重叠
                    if count == wrong_letters_num + 2:
                        food_snake_conflict = True
                # reset，这两个参数完全是为了上面的避免重叠服务
                food_snake_conflict = False
                count = 0

                # 首先更新提示
                if prompt_show[0][0] == 'YES':
                    tip.tip_update(1, 0, x_position_list, y_position_list)
                # 还没吃的时候要先更新，但是当更新一次之后，后面就不在更新了，因为在更新代码里时间卡住了
                alphabet.target_update(continuous_correct_alphabet, 1, 0, x_position_list, y_position_list)
                # 保证错误字母不会和正确的字母一样，也不能互相相同
                wrong_letters_image = [1, 1]
                while len(wrong_letters_image) != len(set(wrong_letters_image)):
                    wrong_letters_postion = 2  # 每生成一个错误字母，都要在坐标中依次选择
                    wrong_letters_image.clear()
                    for sprite in random_alphabet_group.sprites():
                        sprite.random_update(alphabet.current_frame, 1, 0, x_position_list[wrong_letters_postion],
                                             y_position_list[wrong_letters_postion])
                        wrong_letters_postion += 1
                        wrong_letters_image.append(sprite.random_frame)

                # ------------------------------------------------------------------------------------------------------

                #   如果吃了头部触碰到了正确的字母
                if len(pygame.sprite.spritecollide(snake.segments[0], alphabet_group, False)) > 0:
                    # 获得当前正确字母
                    current_frame = alphabet.current_frame
                    score_show_time = gameplay_time  # 得到当前得游戏事件
                    score_show = True
                    correct_increase = True

                    # 得到当前碰撞的字母
                    a = Snakebody_alphabet(current_frame)
                    # 记录单词拼写到哪里了只记录正确的
                    spell_list.append(ALPHABET_LIST[current_frame])
                    # 记录吃了的字母不管对错
                    eating_spelling.append(ALPHABET_LIST[current_frame])
                    # 添加到蛇的尾部
                    snake.add_segment(a)
                    # 更新到下一个单词
                    alphabet.target_update(continuous_correct_alphabet, gameplay_time + 1, 1, x_position_list,
                                           y_position_list)

                    # 保证扰乱的字母和正确的字母各不相同，错误的字母也要更新
                    wrong_letters_image = [1, 1]
                    # 三个字母不能相同，只有相同就必须重新选择
                    while len(wrong_letters_image) != len(set(wrong_letters_image)):
                        # 给错误选择位置
                        wrong_letters_postion = 2
                        wrong_letters_image.clear()
                        for sprite in random_alphabet_group.sprites():
                            sprite.random_update(alphabet.current_frame, gameplay_time + 10, 10,
                                                 x_position_list[wrong_letters_postion],
                                                 y_position_list[wrong_letters_postion])
                            wrong_letters_postion += 1
                            # 将错误字母的图片都保存起来
                            wrong_letters_image.append(sprite.random_frame)

                    # 如果有提示的话，提示更新
                    if prompt_show[0][0] == 'YES':
                        tip.tip_update(gameplay_time + 100, 100, x_position_list, y_position_list)
                    # 字母吃对了有一个声音
                    game_audio("game_sound/right.wav")
                    # 分数加10分
                    current_score += 10


                # ----------------------------------------------------------------------------------------------------------------------
                #   如果蛇的头部碰到了错误的字母
                elif len(pygame.sprite.spritecollide(snake.segments[0], random_alphabet_group, False, False)) > 0:
                    # 到底碰到了那个错误字母
                    collide_sprite = pygame.sprite.spritecollide(snake.segments[0], random_alphabet_group, False, False)
                    score_show_time = gameplay_time  # 得到当前得游戏事件
                    score_show = True
                    wrong_decrease = True
                    # wrong buzz
                    game_audio("game_sound/wrong.wav")
                    # 得到碰撞的那个字母的编号
                    random_frame = collide_sprite[0].random_frame
                    # 即使吃错了也要加进去
                    eating_spelling.append(ALPHABET_LIST[random_frame])
                    b = wrong_alphabet(random_frame)

                    # 保证出现位置不会重复，在这只关心错误字母的更新
                    wrong_letters_image = [1, 1]
                    while len(wrong_letters_image) != len(set(wrong_letters_image)):
                        wrong_letters_postion = 2
                        wrong_letters_image.clear()
                        for sprite in random_alphabet_group.sprites():
                            sprite.random_update(alphabet.current_frame, gameplay_time + 10, 10,
                                                 x_position_list[wrong_letters_postion],
                                                 y_position_list[wrong_letters_postion])
                            wrong_letters_postion += 1
                            wrong_letters_image.append(sprite.random_frame)
                    # 提示也要更新
                    if prompt_show[0][0] == 'YES':
                        tip.tip_update(gameplay_time + 100, 100, x_position_list, y_position_list)
                    # 得到的分数也减10
                    current_score -= 10

                #   如果触碰到了提示
                if prompt_show[0][0] == 'YES':
                    if len(pygame.sprite.groupcollide(snake.segments, tip_group, False, False)) > 0:
                        c = pygame.sprite.spritecollide(snake.segments[0], tip_group, False,
                                                        False)
                        # print correct spelling of current task
                        tip_show = True
                        tip_time = gameplay_time
                        score_show_time = gameplay_time  # 得到当前得游戏时间
                        score_show = True
                        tip_decrease = True
                        # 到蛇的第二个就开始消失计时
                        if len(pygame.sprite.spritecollide(snake.segments[1], tip_group, False, False)) > 0:
                            # score -30
                            current_score -= 30
                            # tip update
                            tip.tip_update(gameplay_time + 100, 100, x_position_list, y_position_list)
                            # tip buzz
                            game_audio("game_sound/health.wav")
                # 游戏没有结束，首先移动蛇
                snake.snake_moving(gameplay_time, snake_moving_speed)
        # ----------------------------------------------------------------------------------------------------------------------
        # 游戏结束后的代码
        if game_over:
            if write_button:  # 因为游戏结束了会一直循环这个代码，所以这个变量的功能是为了让下面循环的代码只执行一次
                pygame.mixer.stop()  # 主游戏背景要结束
                # game over buzz
                game_audio("game_sound/game_over.wav")
                game_over_buzz = False
                del snake.segments[2:]  # 每次游戏结束之后，要清除蛇后面的东西
                write_button = False  # 在结尾改为FALSE
            # 游戏结束时的背景板
            game_over_image = pygame.image.load("Game_Pictures/game_intro.jpg").convert_alpha()
            game_over_image = pygame.transform.scale(game_over_image, (FRAME_WIDTH * 27, FRAME_WIDTH * 24))
            screen.blit(game_over_image, (0, 0))
            # print results after game over
            print_text(CHINESE_FONT, 0 * 0, 0, "学习结束")
            print_text(CHINESE_FONT, FRAME_WIDTH * 7, 0, "本轮完成: " + str(len(words_list_known)))
            print_text(CHINESE_FONT, FRAME_WIDTH * 15, 0, "本轮得分: " + str(current_score))
            # show how many words player remembered in one round
            print_text(CHINESE_FONT, 0, FRAME_WIDTH * 2, "正确拼写")
            print_result(OTHER_FONT, 0, FRAME_WIDTH * 4, words_list)
            print_text(CHINESE_FONT, 200, FRAME_WIDTH * 2, "汉语翻译")
            print_result(CHINESE_FONT, 200, FRAME_WIDTH * 4, task_words)
            print_text(CHINESE_FONT, 400, FRAME_WIDTH * 2, "你的拼写")
            print_result(CHINESE_FONT, 400, FRAME_WIDTH * 4, player_spelling)
        # ----------------------------------------------------------------------------------------------------------------------
        else:
            title_bg = pygame.image.load("Game_Pictures/title-bgd.png").convert_alpha()
            screen.blit(title_bg, (0, 0))
            # show tip
            print_text(CHINESE_FONT, FRAME_WIDTH * 14, 75, "提示: ")

            if tip_show == True:
                print_text(OTHER_FONT, FRAME_WIDTH * 16, 75,
                           words_list[int(alphabet.current_word_number) - 1],
                           color=(255, 0, 0))
                # flay us if you use tip
                tip_use = True
                # 1.5S之后提示消失
                if gameplay_time > tip_time + 1500:
                    tip_show = False

            # 以下代码是为了展示分数的变化
            if score_show:
                if snake.velocity.first_variate == -1 or snake.velocity.first_variate == 1:  # 如何蛇横向移动
                    score_position_y = -60
                    score_position_x = 0
                elif snake.velocity.second_variate == -1 or snake.velocity.second_variate == 1:  # 如何蛇纵向移动
                    score_position_y = 0
                    score_position_x = 30
                if correct_increase:
                    print_text(SCORE_FONT, snake.snake_head.x_coordinate+score_position_x, snake.snake_head.y_coordinate + score_position_y, '+10')
                elif wrong_decrease:
                    print_text(SCORE_FONT, snake.snake_head.x_coordinate+score_position_x, snake.snake_head.y_coordinate + score_position_y, '-10')
                elif tip_decrease:
                    print_text(SCORE_FONT, snake.snake_head.x_coordinate+score_position_x, snake.snake_head.y_coordinate + score_position_y, '-30')
                if gameplay_time > score_show_time + 450:
                    score_show = False
                    correct_increase = False
                    wrong_decrease = False
                    tip_decrease = False

            # print current state
            print_text(CHINESE_FONT, FRAME_WIDTH * 6 + 2, 15,
                       "当前任务: " + task_words[int(alphabet.current_word_number) - 1])

            # 音标
            if word_phone[0][0] == 'YES':
                print_text(CHINESE_FONT, FRAME_WIDTH
                           * 14, 15, '音标： ')
                pho_current_words = get_word_pho(phonetic_file_path, words_list[int(alphabet.current_word_number) - 1])
                print_text(PHONETIC_FONT, FRAME_WIDTH
                           * 16, 15, '/' + pho_current_words + '/')

            print_text(CHINESE_FONT, 0, 15, "当前得分: " + str(current_score))
            print_text(CHINESE_FONT, FRAME_WIDTH * 16, FRAME_WIDTH * 4 + 10,
                       "剩余任务: " + str(len(task_words) - int(alphabet.current_word_number) + 1))
            print_text(CHINESE_FONT, 0, FRAME_WIDTH * 2 + 15, "最高分数: " + str(int(highest_score)))
            print_text(CHINESE_FONT, 0, FRAME_WIDTH * 4 + 10, "单词记录: " + str(int(highest_words)))

            # 刚刚拼写完成的单词，当前在拼第几个单词，第二个之后才显示
            if int(alphabet.current_word_number) > 1:
                print_text(CHINESE_FONT, FRAME_WIDTH * 6 + 2, FRAME_WIDTH * 4 + 10,
                           "刚完成:" + task_words[int(alphabet.current_word_number) - 2] + ': ' + words_list[
                               int(alphabet.current_word_number) - 2])
            # 第一个单词的时候没有任何单词
            else:
                print_text(CHINESE_FONT, FRAME_WIDTH * 6 + 2, FRAME_WIDTH * 4 + 10, "刚完成: " + '    ')

            # 追踪单词的正确拼写
            if track_spelling[0][0] == 'YES':
                print_text(CHINESE_FONT, FRAME_WIDTH * 6 + 2, FRAME_WIDTH * 2 + 15, '拼写追踪：')
                for i in range(len(spell_list)):
                    print_text(OTHER_FONT, FRAME_WIDTH * 10 + i * 15 + 2, FRAME_WIDTH * 2 + 15, spell_list[i],
                               color=(255, 0, 0))

            # 如果当前单词已经拼写完毕
            if ''.join(spell_list) == words_list[int(alphabet.current_word_number) - 2]:
                # 如果已经拼写完毕，删除蛇后面的所有字母
                del snake.segments[2:]
                # 每次在单词拼写完成后，都要强制发音
                word_pro = words_list[int(alphabet.current_word_number) - 2]
                pygame.mixer.music.load(pronunciation_file_path + word_pro + ".mp3")
                pygame.mixer.music.set_volume(1)
                pygame.mixer.music.play()
                # record word from words_list if do not make mistake，如果没有拼错，就完全添加到review里面
                if words_list[int(alphabet.current_word_number) - 2] not in words_list_known:
                    if ''.join(eating_spelling) == words_list[
                        int(alphabet.current_word_number) - 2] and tip_use == False:
                        words_list_known.append(words_list[int(alphabet.current_word_number) - 2])
                        task_words_known.append(task_words[int(alphabet.current_word_number) - 2])
                        current_remembered_words += 1
                # clear the two list once task change
                player_spelling.append(''.join(eating_spelling))
                eating_spelling.clear()
                words_number += 1
                spell_list.clear()
                tip_use = False

            # draw all sprites
            snake.draw(screen)
            random_alphabet_group.draw(screen)
            alphabet_group.draw(screen)

            # set up whether there are prompts or not
            if prompt_show[0][0] == 'YES':
                tip_group.draw(screen)
        # draw all sprites
        pygame.display.update()


game_init()
