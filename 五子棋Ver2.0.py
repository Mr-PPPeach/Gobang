import pygame
import re
import sys
import copy
from operator import itemgetter

WINDOW_H = 700
WINDOW_W = 700
MAP_H = 15
MAP_W = 15
RD = 40#棋盘距离边界距离
PLY_FIRST = True #玩家是否先手  

class Menu:#开始菜单
    def __init__(self):
        self.start = pygame.font.SysFont("consolas",50).render("START",True,"white")
        self.start_w,self.start_h = self.start.get_size()
        self.start_pos_l = (WINDOW_W-self.start_w)/2#左
        self.start_pos_r = (WINDOW_W+self.start_w)/2#右
        self.start_pos_u = (WINDOW_H-self.start_h)/2#上
        self.start_pos_d = (WINDOW_H+self.start_h)/2#下
    def click_response(self,mx,my):
        if self.start_pos_l <= mx <=  self.start_pos_r and self.start_pos_u <= my <= self.start_pos_d:
            return True
        else:
            return False
    def draw(self,window):
        window.fill("black")
        window.blit(self.start,(self.start_pos_l,self.start_pos_u))
        pygame.draw.aaline(window,'white',(self.start_pos_l,self.start_pos_u),(self.start_pos_r,self.start_pos_u),1)
        pygame.draw.aaline(window,'white',(self.start_pos_l,self.start_pos_d),(self.start_pos_r,self.start_pos_d),1)
        pygame.draw.aaline(window,'white',(self.start_pos_l,self.start_pos_u),(self.start_pos_l,self.start_pos_d),1)
        pygame.draw.aaline(window,'white',(self.start_pos_r,self.start_pos_u),(self.start_pos_r,self.start_pos_d),1)
        pygame.display.flip()

class Map:#棋盘
    def __init__(self,map = [[0 for x in range(MAP_H)] for y in range(MAP_W)]):
        self.height = MAP_H
        self.width = MAP_W
        self.map = map#棋盘数组
        self.rd = RD#棋盘距离边界距离
        self.chess_size = ((WINDOW_H-RD*2)/(MAP_H-1))/5*2#棋子大小
        self.chess = []#棋子列表，落子顺序为列表顺序
        self.ply_win = False
        self.AI_win = False
    def get_map(self):
        return self.map
    def append(self,x,y,value):
        if self.map[y][x] == 0:
            self.map[y][x] = value
            self.chess.append((x,y))
            return True
        else :
            return False
    def remove(self,x,y):
        self.map[y][x] = 0
        self.chess.remove((x,y))
    def click_chess_set(self,mx,my,window):
        for y in range(self.height):
            for x in range(self.width):
                if (WINDOW_W-self.rd*2)/(self.width-1)*x+self.rd-self.chess_size <= mx <= (WINDOW_W-self.rd*2)/(self.width-1)*x+self.rd+self.chess_size and (WINDOW_H-self.rd*2)/(self.height-1)*y+self.rd-self.chess_size <= my <= (WINDOW_H-self.rd*2)/(self.height-1)*y+self.rd+self.chess_size:
                    if self.append(x,y,1):
                        self.chess_draw(window)
                        #self.new_chess_draw(window,x,y,1)
                        return True
                    else :
                        return False
        else:
            return False 
    def click_regret(self,mx,my):
        if self.regret_button_l <= mx <= self.regret_button_r and self.regret_button_u <= my <= self.regret_button_d:
            self.regret()
            return True
        else:
            return False
    def regret_button_draw(self,window):
        regret_button = pygame.font.SysFont("consolas",20).render('Regret',True,'black')
        regret_button_w,regret_button_h = regret_button.get_size()
        self.regret_button_l = WINDOW_W-RD/2-regret_button_w#左
        self.regret_button_r = WINDOW_W-RD/2#右
        self.regret_button_u = WINDOW_H - RD + (RD-regret_button_h)/2#上
        self.regret_button_d = WINDOW_H - (RD-regret_button_h)/2#下
        window.blit(regret_button,(self.regret_button_l,self.regret_button_u))
        pygame.draw.aaline(window,'black',(self.regret_button_l,self.regret_button_u),(self.regret_button_r,self.regret_button_u),1)
        pygame.draw.aaline(window,'black',(self.regret_button_l,self.regret_button_d),(self.regret_button_r,self.regret_button_d),1)
        pygame.draw.aaline(window,'black',(self.regret_button_l,self.regret_button_u),(self.regret_button_l,self.regret_button_d),1)
        pygame.draw.aaline(window,'black',(self.regret_button_r,self.regret_button_u),(self.regret_button_r,self.regret_button_d),1)
        pygame.display.flip()
    def regret(self):
        if len(self.chess) >= 2:
            self.remove(self.chess[-2][0],self.chess[-2][1])
            self.remove(self.chess[-1][0],self.chess[-1][1])
            return True
        else:
            return False

    def background_draw(self,window):
        window.fill((238,154,73))
        for x in range(self.width):
            line_x = (WINDOW_W-self.rd*2)/(self.width-1)*x+self.rd
            pygame.draw.aaline(window, 'black', (line_x, self.rd), (line_x, WINDOW_H - self.rd), 1)
        for y in range(self.height):
            line_y = (WINDOW_H-self.rd*2)/(self.height-1)*y+self.rd
            pygame.draw.aaline(window, 'black', (self.rd, line_y), (WINDOW_W - self.rd, line_y), 1)
        pygame.draw.circle(window, 'black', ((WINDOW_W-self.rd*2)/(self.width-1)*3+self.rd, (WINDOW_H-self.rd*2)/(self.height-1)*3+self.rd), WINDOW_H/150, 0)
        pygame.draw.circle(window, 'black', ((WINDOW_W-self.rd*2)/(self.width-1)*3+self.rd, (WINDOW_H-self.rd*2)/(self.height-1)*11+self.rd), WINDOW_H/150, 0)
        pygame.draw.circle(window, 'black', ((WINDOW_W-self.rd*2)/(self.width-1)*11+self.rd, (WINDOW_H-self.rd*2)/(self.height-1)*3+self.rd), WINDOW_H/150, 0)
        pygame.draw.circle(window, 'black', ((WINDOW_W-self.rd*2)/(self.width-1)*11+self.rd, (WINDOW_H-self.rd*2)/(self.height-1)*11+self.rd), WINDOW_H/150, 0)
        pygame.draw.circle(window, 'black', ((WINDOW_W-self.rd*2)/(self.width-1)*7+self.rd, (WINDOW_H-self.rd*2)/(self.height-1)*7+self.rd), WINDOW_H/150, 0)
        pygame.display.flip()
    def chess_draw(self,window):
        for chess in self.chess:
            x = chess[0]
            y = chess[1]
            value = self.map[y][x]
            if value == 0:
                pass
            elif value == 1:
                chess_x = (WINDOW_W-self.rd*2)/(self.width-1)*x+self.rd
                chess_y = (WINDOW_H-self.rd*2)/(self.height-1)*y+self.rd
                pygame.draw.circle(window, 'black', (chess_x, chess_y), self.chess_size, 0)
            elif value == 2:
                chess_x = (WINDOW_W-self.rd*2)/(self.width-1)*x+self.rd
                chess_y = (WINDOW_H-self.rd*2)/(self.height-1)*y+self.rd
                pygame.draw.circle(window, 'white', (chess_x, chess_y), self.chess_size, 0)
        pygame.display.flip()
        self.step_draw(window)
    def new_chess_draw(self,window,x,y,value):
        if value == 0:
                    pass
        elif value == 1:
            chess_x = (WINDOW_W-self.rd*2)/(self.width-1)*x+self.rd
            chess_y = (WINDOW_H-self.rd*2)/(self.height-1)*y+self.rd
            pygame.draw.circle(window, 'black', (chess_x, chess_y), self.chess_size, 0)
        elif value == 2:
            chess_x = (WINDOW_W-self.rd*2)/(self.width-1)*x+self.rd
            chess_y = (WINDOW_H-self.rd*2)/(self.height-1)*y+self.rd
            pygame.draw.circle(window, 'white', (chess_x, chess_y), self.chess_size, 0)
        pygame.display.flip()
        self.step_draw(window)
    
    def step_draw(self,window):
        last_index = len(self.chess) - 1
        for index in range(len(self.chess)):
            x = self.chess[index][0]
            y = self.chess[index][1]
            value = self.map[y][x]
            step = index + 1
            if value == 0:
                pass
            elif value == 1:
                color = 'white'
            elif value == 2:
                color = 'black'
            if index == last_index:
                color = 'red'
                #color = 'white'
            step_font = pygame.font.SysFont("consolas",15).render(str(step),True,color)
            step_font_w,step_font_h = step_font.get_size()
            step_x = (WINDOW_W-self.rd*2)/(self.width-1)*x+self.rd-step_font_w/2
            step_y = (WINDOW_H-self.rd*2)/(self.height-1)*y+self.rd-step_font_h/2
            window.blit(step_font,(step_x,step_y))
        pygame.display.flip()

    def eva_show(self,window,score_list):#展示AI此步的每个点的评价值(测试用)
        window.fill("black")
        self.background_draw(window)
        self.chess_draw(window)
        score_list = sorted(score_list,key=itemgetter(2),reverse=True)#按score降序排列
        for i in range(len(score_list)):
            tuple = score_list[i]
            x = tuple[0]
            y = tuple[1]
            score = int(tuple[2])
            score_str = str(score)
            if i == 0: 
                color = 'red'
            else:
                color = 'white'
            score_font = pygame.font.SysFont("consolas",12).render(score_str,True,color)
            score_font_w,score_font_h = score_font.get_size()
            score_x = (WINDOW_W-self.rd*2)/(MAP_W-1)*x+self.rd-score_font_w/2
            score_y = (WINDOW_W-self.rd*2)/(MAP_W-1)*y+self.rd-score_font_h/2
            window.blit(score_font,(score_x,score_y))
        pygame.display.flip()
        
    def last_line_extract(self):#将最后落子的四个方向的直线提取提取出来
        if len(self.chess) >= 1:
            last_chess_x = self.chess[-1][0]
            last_chess_y = self.chess[-1][1]
        else:
            last_chess_x = 0
            last_chess_y = 0
        line = []
        map_line = []#储存棋盘上的直线
        for y in range(15):
            line.append(self.map[y][last_chess_x])
        map_line.append(line.copy())
        line.clear()

        for x in range(15):
            line.append(self.map[last_chess_y][x])
        map_line.append(line.copy())
        line.clear()

        b = last_chess_y - last_chess_x#提取左上-右下走向的阴线
        for x in range(15):
            y = x + b 
            if 0 <= y <= 14 :
                line.append(self.map[y][x])
        map_line.append(line.copy())
        line.clear()
            
        b = last_chess_y + last_chess_x#提取左下-右上走向的阴线
        for x in range(15):
            y = -x + b 
            if 0 <= y <= 14 :
                line.append(self.map[y][x])
        map_line.append(line.copy())
        line.clear()
        
        return map_line
        
    def line_extract(self):#棋盘直线提取
        '''map = [#测试用例
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 2, 2, 2, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        ]  ''' 
        line = []
        map_line = []#储存棋盘上的72条直线
        for x in range(15):#提取垂直阳线
            for y in range(15):
                line.append(self.map[y][x])
            map_line.append(line.copy())
            line.clear()

        for y in range(15):#提取水平阳线
            for x in range(15):
                line.append(self.map[y][x])
            map_line.append(line.copy())
            line.clear()

        for i in range(-10,11):#提取左上-右下走向的阴线
            for x in range(15):
                y = x + i 
                if 0 <= y <= 14 :
                    line.append(self.map[y][x])
            map_line.append(line.copy())
            line.clear()
            
        for i in range(4,25):#提取左下-右上走向的阴线
            for x in range(15):
                y = -x + i 
                if 0 <= y <= 14 :
                    line.append(self.map[y][x])
            map_line.append(line.copy())
            line.clear()
        
        return map_line

    def line_seg(self,map_line):#根据提取的直线将直线分段

        '''self.map_line = [#测试用例
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 2, 2, 2, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        ]  ''' 

        ply_chess_type = []#对于玩家1（真人）来说的分段棋型
        for i in map_line:#录入ply方棋子数在一条直线内大于等于二的直线
            count = 0
            for j in i:
                if j == 1:
                    count += 1 
            if count >= 2:
                ply_chess_type.append(i)
        ply_new_rows = []
        ply_del_index = []
        ply_loop = True
        ply_pos = 0
        ply_len = len(ply_chess_type)

        AI_chess_type = []#对于玩家2（AI）来说的分段棋型
        for i in map_line:#录入AI方棋子数在一条直线内大于等于二的直线
            count = 0
            for j in i:
                if j == 2:
                    count += 1 
            if count >= 2:
                AI_chess_type.append(i)
        AI_new_rows = []
        AI_del_index = []
        AI_loop = True
        AI_pos = 0
        AI_len = len(AI_chess_type)
        
        while ply_loop:
            for i in range(ply_pos,ply_len):
                for j in range(len(ply_chess_type[i])):
                    if ply_chess_type[i][j] == 2 :
                        ply_del_index.append(i)#将该索引计入待删除列表
                        if len(ply_chess_type[i][:j])>=5:#切片长度大于5则加入待加入列表并结束对此直线的搜索
                            ply_new_rows.append(ply_chess_type[i][:j])
                        if len(ply_chess_type[i][j+1:])>=5:#切片长度大于5则加入待加入列表并结束对此直线的搜索
                            ply_new_rows.append(ply_chess_type[i][j+1:])
                        break
            if len(ply_new_rows)==0:#待加入表为空则无需扩展
                ply_loop = False
                ply_chess_type = [n for i, n in enumerate(ply_chess_type) if (i not in ply_del_index)]#删除待删除的所有元素
            else:
                ply_pos = ply_len
                for row in ply_new_rows:
                    ply_chess_type.append(row)#加入待加入元素
                ply_len = len(ply_chess_type)
            ply_new_rows.clear()

        while AI_loop:  
            for i in range(AI_pos, AI_len):  
                for j in range(len(AI_chess_type[i])):  
                    if AI_chess_type[i][j] == 1:  
                        AI_del_index.append(i)  # 将该索引计入待删除列表  
                        if len(AI_chess_type[i][:j]) >= 5:  # 切片长度大于5则加入待加入列表并结束对此直线的搜索  
                            AI_new_rows.append(AI_chess_type[i][:j])   
                        if len(AI_chess_type[i][j+1:]) >= 5:  # 切片长度大于5则加入待加入列表并结束对此直线的搜索  
                            AI_new_rows.append(AI_chess_type[i][j+1:])  
                        break 
            if len(AI_new_rows) == 0:  # 待加入表为空则无需扩展  
                AI_loop = False  
                AI_chess_type = [n for i, n in enumerate(AI_chess_type) if (i not in AI_del_index)]  # 删除待删除的所有元素  
            else:  
                AI_pos = AI_len  
                for row in AI_new_rows:  
                    AI_chess_type.append(row)  # 加入待加入元素  
                AI_len = len(AI_chess_type)  
            AI_new_rows.clear()
        
        return ply_chess_type, AI_chess_type

    def eva(self,ply_chess_type,AI_chess_type):#根据分段棋型得出评分，并返回评分和最后走步的坐标
        basic_chess_type = [#存储基本棋型用来与分段棋型匹配
            'XXXXX',#连五（0）
            'OXXXXO',#活四（1）
            '^XXXXO','OXXXX$','XOXXX','XXXOX','XXOXX',#冲四（2-6）
            'OOXXXO','OXXXOO','OXOXXO','OXXOXO',#活三（7-10）
            '^XXXOO','OOXXX$','^XXOXO','OXOXX$','^XOXXO','OXXOX$','XOOXX','XXOOX','XOXOX','^OXXXO$',#眠三（11-20）
            'OOXXOO','OOXOXO','OXOXOO','OOOXXO','OXXOOO','OXOOXO',#活二（21-26）
            '^OXXOO$','^OOXXO$','^OXOXO$','^XXOOO','OOOXX$','^XOXOO','OOXOX$','^XOOXO','OXOOX$','XOOOX'#眠二（27-36）
            ]
        #basic_chess_type_score = [20,120,120,720,720,4320,99999999]#0眠二，1活二，2眠三，3活三，4眠四，5活四，6连五所对应的分数
        basic_chess_type_score = [10,100,1000,10000,100000,1000000,99999999]#0眠二，1活二，2眠三，3活三，4眠四，5活四，6连五所对应的分数
        L5,H4,M4,H3,M3,H2,M2 = 6,5,4,3,2,1,0
        ply_chess_type_extract = [0,0,0,0,0,0,0]#index=0~6分别代表七种基本棋型（其中6为连五，0为眠二）,对应的数值代表该局面下该种棋型有多少
        for piece in ply_chess_type:#录入基本棋型判断表
            string = ''
            for chess in piece:
                if chess == 0:
                    string += 'O'
                else:
                    string += 'X'
            for index in range(len(basic_chess_type)):
                if re.search(basic_chess_type[index], string):
                    if index == 0:
                        ply_chess_type_extract[L5] += 1
                    elif index == 1:
                        ply_chess_type_extract[H4] += 1
                    elif 2 <= index <= 6:
                        ply_chess_type_extract[M4] += 1
                    elif 7 <= index <= 10:
                        ply_chess_type_extract[H3] += 1
                    elif 11 <= index <= 20:
                        ply_chess_type_extract[M3] += 1
                    elif 21 <= index <= 26:
                        ply_chess_type_extract[H2] += 1
                    elif 27 <= index <= 36:
                        ply_chess_type_extract[M2] += 1

        ply_score = 0
        for index in range(len(ply_chess_type_extract)):
            ply_score += basic_chess_type_score[index]*ply_chess_type_extract[index]
        if ply_chess_type_extract[L5] >= 1:#有连五则标记
            self.ply_win = True
        else:
            self.ply_win = False

        AI_chess_type_extract = [0,0,0,0,0,0,0]
        for piece in AI_chess_type:
            string = ''
            for chess in piece:
                if chess == 0:
                    string += 'O'
                else:
                    string += 'X'
            for index in range(len(basic_chess_type)):
                if re.search(basic_chess_type[index], string):
                    if index == 0:
                        AI_chess_type_extract[L5] += 1
                    elif index == 1:
                        AI_chess_type_extract[H4] += 1
                    elif 2 <= index <= 6:
                        AI_chess_type_extract[M4] += 1
                    elif 7 <= index <= 10:
                        AI_chess_type_extract[H3] += 1
                    elif 11 <= index <= 20:
                        AI_chess_type_extract[M3] += 1
                    elif 21 <= index <= 26:
                        AI_chess_type_extract[H2] += 1
                    elif 27 <= index <= 36:
                        AI_chess_type_extract[M2] += 1
        AI_score = 0
        for index in range(len(AI_chess_type_extract)):
            AI_score += basic_chess_type_score[index]*AI_chess_type_extract[index]
        if AI_chess_type_extract[L5] >= 1:#有连五则标记
            self.AI_win = True
        else:
            self.AI_win = False

        
        if len(self.chess) >= 1:#获取ply方和AI方最后下的棋子
            ply_deviation,AI_deviation = 0,0
            for chess in self.chess:#计算所有己方棋子的偏离程度
                chess_x, chess_y = chess[0], chess[1]
                if self.map[chess_y][chess_x] == 0:
                    pass
                elif self.map[chess_y][chess_x] == 1:
                    ply_deviation += abs(chess_x-7)+abs(chess_y-7)
                elif self.map[chess_y][chess_x] == 2:
                    AI_deviation += abs(chess_x-7)+abs(chess_y-7)      
    
            a = 0.5#进攻系数（范围为0到1，a越大，越倾向于打乱玩家的棋而不是下好自己的棋）
            score = (1-a)*(AI_score - 0.01*AI_deviation) - a*(ply_score - 0.01*ply_deviation)

            last_x, last_y = self.chess[-1][0], self.chess[-1][1]
            if len(self.chess) >= 2:
                if self.map[last_y][last_x] == 1:
                    ply_last_x, ply_last_y = last_x, last_y
                    AI_last_x, AI_last_y = self.chess[-2][0], self.chess[-2][1]
                else:
                    AI_last_x, AI_last_y = last_x, last_y
                    ply_last_x, ply_last_y = self.chess[-2][0], self.chess[-2][1]
            else:
                if self.map[last_y][last_x] == 1:
                    ply_last_x, ply_last_y = last_x, last_y
                    AI_last_x, AI_last_y = None,None
                else:
                    AI_last_x, AI_last_y = last_x, last_y
                    ply_last_x, ply_last_y = None,None
        else:
            score,ply_last_x, ply_last_y, AI_last_x, AI_last_y = None,None,None,None,None

        return (score,ply_last_x, ply_last_y, AI_last_x, AI_last_y)

    def evaluate(self):#将棋盘提取直线，划分棋型，并最终返回当前棋局评分和最后走步坐标的综合操作
        ply_chess_type, AI_chess_type = self.line_seg(self.line_extract())
        return self.eva(ply_chess_type, AI_chess_type)
    
    def get_win(self):#0为未可知, 1为玩家胜，2为AI胜,3为棋盘下满了（平局）
        #如果双赢，则先手者胜（因为实际上确实是先手者先胜了）
        self.evaluate()
        if self.ply_win == True and self.AI_win == True:
            if PLY_FIRST:
                return 1
            else :
                return 2
        elif self.ply_win == False and self.AI_win == False:
            if len(self.chess) >= sum(len(line) for line in self.map):
                return 3
            else:
                return 0
        elif self.ply_win == True:
            return 1
        else:
            return 2
    def spiral_matrix(matrix):#螺旋遍历矩阵
        if not matrix: return []
        l,r,u,d,result=0,len(matrix[0])-1,0,len(matrix)-1,[]
        while True:
            #从左到右
            for i in range(l,r+1):
                result.append(matrix[u][i])
            u+=1
            if u>d: break
            #从上到下
            for j in range(u,d+1):
                result.append(matrix[j][r])
            r-=1
            if l>r: break
            #从右到左
            for i in range(r,l-1,-1):
                result.append(matrix[d][i])
            d-=1
            if u>d: break
            #从下到上
            for j in range(d,u-1,-1):
                result.append(matrix[j][l])
            l+=1
            if l>r: break
        return result
    def generate_children(self,chess):#生成走步的子节点(ply是1,AI是2)
        children = []
        for y in range(MAP_H):
            for x in range(MAP_W):
                if self.append(x,y,chess):
                    children.append(copy.deepcopy(self))
                    self.remove(x,y)
        return children
    
class Game:#游戏操作处理
    def __init__(self):
        pygame.init()
        self.window=pygame.display.set_mode((WINDOW_W,WINDOW_H))
        pygame.display.set_caption("五子棋")
        self.plysturn = PLY_FIRST #玩家下棋许可（
    def get_window(self):
        return self.window
    def get_plysturn(self):
        return self.plysturn
    def change_plysturn(self):
        if self.plysturn == True :
            self.plysturn = False
        else :
            self.plysturn = True
    def plysturn_show(self,window):
        font = pygame.font.SysFont("consolas",20).render('Your turn',True,'black')
        font_w,font_h = font.get_size()
        x = (WINDOW_W-font_w)/2
        y = (RD-font_h)/2
        window.blit(font,(x,y))
        pygame.display.flip()
    def AIsturn_show(self,window):
        font = pygame.font.SysFont("consolas",20).render('AI is thinking',True,'black')
        font_w,font_h = font.get_size()
        x = (WINDOW_W-font_w)/2
        y = (RD-font_h)/2
        window.blit(font,(x,y))
        pygame.display.flip()
    def winner_show(self,window,get_win):
        if get_win == 1:
            font = pygame.font.SysFont("consolas",20).render('Player wins!',True,'black')
            font_w,font_h = font.get_size()
            x = (WINDOW_W-font_w)/2
            y = WINDOW_H - RD + (RD-font_h)/2
            window.blit(font,(x,y))
            pygame.display.flip()
        elif get_win == 2:
            font = pygame.font.SysFont("consolas",20).render('AI wins!',True,'black')
            font_w,font_h = font.get_size()
            x = (WINDOW_W-font_w)/2
            y = WINDOW_H - RD + (RD-font_h)/2
            window.blit(font,(x,y))
            pygame.display.flip()
        else:
            font = pygame.font.SysFont("consolas",20).render('Draw',True,'black')
            font_w,font_h = font.get_size()
            x = (WINDOW_W-font_w)/2
            y = WINDOW_H - RD + (RD-font_h)/2
            window.blit(font,(x,y))
            pygame.display.flip()

def alpha_beta_search(map, depth, alpha, beta, is_max):#递归的基于alpha_beta剪枝算法的MINMAX算法
    if depth == 0 or map.get_win() != 0:
        return map.evaluate()

    if is_max:
        tuple = (float('-inf'),0,0)
        for child in map.generate_children(2):#max方一定是AI，所以生成AI走步的子节点
            next_tuple = alpha_beta_search(child, depth - 1, alpha, beta, False)
            tuple = max(tuple, next_tuple,key=itemgetter(0))
            alpha = max(alpha, tuple[0])
            if alpha >= beta:
                break
        return tuple
    else:
        tuple = (float('inf'),0,0)
        for child in map.generate_children(1):
            next_tuple = alpha_beta_search(child, depth - 1, alpha, beta, True)
            tuple = min(tuple, next_tuple,key=itemgetter(0))
            beta = min(beta, tuple[0])
            if alpha >= beta:
                break
        return tuple
    

#初始化类
game = Game()
menu = Menu()
map = Map()
#菜单界面渲染
window = game.get_window()
menu.draw(window)
#菜单事件循环
menu_loop = True
while menu_loop:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mx,my = event.pos
            if menu.click_response(mx,my):
                menu_loop = False
                break
#游戏界面渲染
map.background_draw(window)
map.regret_button_draw(window)
#游戏事件循环
if game.get_plysturn():
    count = 0
game_loop = True
game_over = False
while game_loop:
    for event in pygame.event.get():
        
        if event.type == pygame.QUIT:#退出则结束
            pygame.quit()
            sys.exit()

        get_win = map.get_win()
        if get_win != 0:#棋局结束
            window.fill('black')
            map.background_draw(window)
            map.chess_draw(window)
            map.regret_button_draw(window)
            game.winner_show(window,get_win)
            pygame.display.flip()
            game_over = True
        
        elif game.get_plysturn() == True:#玩家行动
            if count == 0:
                game.plysturn_show(window)
                count += 1
            pygame.display.flip()#因为窗口会未响应所以仍需不断刷新窗口才能正常显示内容
            if event.type == pygame.MOUSEBUTTONDOWN:
                mx,my = event.pos
                if map.click_regret(mx,my):
                    window.fill('black')
                    map.background_draw(window)
                    map.regret_button_draw(window)
                    map.chess_draw(window)
                    game.plysturn_show(window)
                elif map.click_chess_set(mx,my,window):
                    window.fill('black')
                    map.background_draw(window)
                    map.regret_button_draw(window)
                    map.chess_draw(window)
                    game.change_plysturn()

        elif game.get_plysturn() == False:#AI行动
            think_start_time =  pygame.time.get_ticks()
            game.AIsturn_show(window)
            _,_,_,x,y = alpha_beta_search(map = map,depth = 2,alpha = float('-inf'), beta = float('inf'), is_max = True)
            window.fill('black')
            map.background_draw(window)
            map.regret_button_draw(window)
            map.append(x,y,2)
            map.chess_draw(window)
            #map.new_chess_draw(window,highest_score_tuple[0],highest_score_tuple[1],2)
            game.change_plysturn()
            count = 0
            think_period =  pygame.time.get_ticks() - think_start_time
            print(str(think_period*0.001)+'seconds')

        while game_over:#游戏结束循环
            for event in pygame.event.get():
                pygame.display.flip()
                if event.type == pygame.QUIT:#退出则结束
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mx,my = event.pos
                    if map.click_regret(mx,my):
                        window.fill('black')
                        map.background_draw(window)
                        map.regret_button_draw(window)
                        map.chess_draw(window)
                        game_over = False
                        break

while True:#游戏结束循环
    for event in pygame.event.get():
        pygame.display.flip()
        if event.type == pygame.QUIT:#退出则结束
            pygame.quit()
            sys.exit()