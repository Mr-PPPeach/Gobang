import pygame
import re
import sys
from operator import itemgetter

WINDOW_H = 700
WINDOW_W = 700
MAP_H = 15
MAP_W = 15
PLY_FIRST = False #玩家是否先手

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
        pygame.display.flip()

class Map:#棋盘
    def __init__(self):
        self.height = MAP_H
        self.width = MAP_W
        self.map = [[0 for x in range(self.width)] for y in range(self.height)]#棋盘数组
        self.rd = 40#棋盘距离边界距离
        self.chess_size = self.rd/5*2#棋子大小
        self.chess = []#棋子列表，用来显示棋子的步数
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
    def click_response(self,mx,my,window):
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
        for y in range(self.height):
            for x in range(self.width):
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
                color = 'white'
            step_font = pygame.font.SysFont("consolas",15).render(str(step),True,color)
            step_font_w,step_font_h = step_font.get_size()
            step_x = (WINDOW_W-self.rd*2)/(self.width-1)*x+self.rd-step_font_w/2
            step_y = (WINDOW_H-self.rd*2)/(self.height-1)*y+self.rd-step_font_h/2
            window.blit(step_font,(step_x,step_y))
        pygame.display.flip()

    def eva_show(self,window,score_list):#展示AI此步的每个点的评价值
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
    
class Map_node:#将当前棋局当成一个节点，对其进行扩张，评分等操作
    def __init__(self,Map):
        self.Map = Map#传入map类的一个实例
    def generate_children(self):
        children = []
        for y in range(MAP_H):
            for x in range(MAP_W):
                self.Map.append(x,y,2)
                children.append(self.Map.get_map())
                self.Map.remove(x,y)
                    
    def is_terminal_node(self):
        pass
    def evaluate(self):
        pass



class AI:#用于分析棋局
    def __init__(self):
        self.map_line = []#储存棋盘上的72条直线
        self.ply_chess_type = []#对于玩家1（真人）来说的分段棋型
        self.AI_chess_type = []#对于玩家2（AI）来说的分段棋型
        self.basic_chess_type = [#存储基本棋型用来与分段棋型匹配
            'XXXXX',#连五（0）
            'OXXXXO',#活四（1）
            '^XXXXO','OXXXX$','XOXXX','XXXOX','XXOXX',#冲四（2-6）
            'OOXXXO','OXXXOO','OXOXXO','OXXOXO',#活三（7-10）
            '^XXXOO','OOXXX$','^XXOXO','OXOXX$','^XOXXO','OXXOX$','XOOXX','XXOOX','XOXOX','^OXXXO$',#眠三（11-20）
            'OOXXOO','OOXOXO','OXOXOO','OOOXXO','OXXOOO','OXOOXO',#活二（21-26）
            '^OXXOO$','^OOXXO$','^OXOXO$','^XXOOO','OOOXX$','^XOXOO','OOXOX$','^XOOXO','OXOOX$','XOOOX'#眠二（27-36）
            ]
        self.basic_chess_type_score = [20,120,120,720,720,4320,99999999]
        #self.basic_chess_type_score = [10,100,1000,10000,100000,1000000,99999999]#0眠二，1活二，2眠三，3活三，4眠四，5活四，6连五所对应的分数
        '''[10,100,1000,10000,100000,1000000,99999999]#不同参数'''
        self.a = 0.9#进攻系数（范围为0到1，a越大，越倾向于打乱玩家的棋而不是下好自己的棋）
        self.ply_win = False
        self.AI_win = False

    def get_win(self):#1为玩家胜，0为未可知，2为AI胜
        #如果双赢，则先手者胜（因为实际上确实是先手者先胜了）
        if self.ply_win == True and self.AI_win == True:
            if PLY_FIRST:
                return 1
            else :
                return 2
        elif self.ply_win == False and self.AI_win == False:
            return 0
        elif self.ply_win == True:
            return 1
        else:
            return 2
        
    def line_extract(self,map):#直线提取
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
        for x in range(15):#提取垂直阳线
            for y in range(15):
                line.append(map[y][x])
            self.map_line.append(line.copy())
            line.clear()

        for y in range(15):#提取水平阳线
            for x in range(15):
                line.append(map[y][x])
            self.map_line.append(line.copy())
            line.clear()

        for i in range(-10,11):#提取左上-右下走向的阴线
            for x in range(15):
                y = x + i 
                if 0 <= y <= 14 :
                    line.append(map[y][x])
            self.map_line.append(line.copy())
            line.clear()
            
        for i in range(4,25):#提取左下-右上走向的阴线
            for x in range(15):
                y = -x + i 
                if 0 <= y <= 14 :
                    line.append(map[y][x])
            self.map_line.append(line.copy())
            line.clear()

    def line_seg(self):#直线分段

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

        self.ply_chess_type = []
        for i in self.map_line.copy():#录入ply方棋子数在一条直线内大于等于二的直线
            count = 0
            for j in i:
                if j == 1:
                    count += 1 
            if count >= 2:
                self.ply_chess_type.append(i)
        ply_new_rows = []
        ply_del_index = []
        ply_loop = True
        ply_pos = 0
        ply_len = len(self.ply_chess_type)

        self.AI_chess_type = []
        for i in self.map_line.copy():#录入AI方棋子数在一条直线内大于等于二的直线
            count = 0
            for j in i:
                if j == 2:
                    count += 1 
            if count >= 2:
                self.AI_chess_type.append(i)
        AI_new_rows = []
        AI_del_index = []
        AI_loop = True
        AI_pos = 0
        AI_len = len(self.AI_chess_type)
        
        while ply_loop:
            for i in range(ply_pos,ply_len):
                for j in range(len(self.ply_chess_type[i])):
                    if self.ply_chess_type[i][j] == 2 :
                        ply_del_index.append(i)#将该索引计入待删除列表
                        if len(self.ply_chess_type[i][:j])>=5:#切片长度大于5则加入待加入列表并结束对此直线的搜索
                            ply_new_rows.append(self.ply_chess_type[i][:j])
                        if len(self.ply_chess_type[i][j+1:])>=5:#切片长度大于5则加入待加入列表并结束对此直线的搜索
                            ply_new_rows.append(self.ply_chess_type[i][j+1:])
                        break
            if len(ply_new_rows)==0:#待加入表为空则无需扩展
                ply_loop = False
                self.ply_chess_type = [n for i, n in enumerate(self.ply_chess_type) if (i not in ply_del_index)]#删除待删除的所有元素
            else:
                ply_pos = ply_len
                for row in ply_new_rows:
                    self.ply_chess_type.append(row)#加入待加入元素
                ply_len = len(self.ply_chess_type)
            ply_new_rows.clear()

        while AI_loop:  
            for i in range(AI_pos, AI_len):  
                for j in range(len(self.AI_chess_type[i])):  
                    if self.AI_chess_type[i][j] == 1:  
                        AI_del_index.append(i)  # 将该索引计入待删除列表  
                        if len(self.AI_chess_type[i][:j]) >= 5:  # 切片长度大于5则加入待加入列表并结束对此直线的搜索  
                            AI_new_rows.append(self.AI_chess_type[i][:j])   
                        if len(self.AI_chess_type[i][j+1:]) >= 5:  # 切片长度大于5则加入待加入列表并结束对此直线的搜索  
                            AI_new_rows.append(self.AI_chess_type[i][j+1:])  
                        break 
            if len(AI_new_rows) == 0:  # 待加入表为空则无需扩展  
                AI_loop = False  
                self.AI_chess_type = [n for i, n in enumerate(self.AI_chess_type) if (i not in AI_del_index)]  # 删除待删除的所有元素  
            else:  
                AI_pos = AI_len  
                for row in AI_new_rows:  
                    self.AI_chess_type.append(row)  # 加入待加入元素  
                AI_len = len(self.AI_chess_type)  
            AI_new_rows.clear()

    def eva(self):#评价当前棋型对AI方的评分
        L5,H4,M4,H3,M3,H2,M2 = 6,5,4,3,2,1,0
        ply_chess_type_extract = [0,0,0,0,0,0,0]#index=0~6分别代表七种基本棋型（其中6为连五，0为眠二）,对应的数值代表该局面下该种棋型有多少
        for piece in self.ply_chess_type:#录入基本棋型判断表
            string = ''
            for chess in piece:
                if chess == 0:
                    string += 'O'
                else:
                    string += 'X'
            for index in range(len(self.basic_chess_type)):
                if re.search(self.basic_chess_type[index], string):
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
            ply_score += self.basic_chess_type_score[index]*ply_chess_type_extract[index]
        if ply_chess_type_extract[L5] >= 1:#有连五则标记
                self.ply_win = True

        AI_chess_type_extract = [0,0,0,0,0,0,0]
        for piece in self.AI_chess_type:
            string = ''
            for chess in piece:
                if chess == 0:
                    string += 'O'
                else:
                    string += 'X'
            for index in range(len(self.basic_chess_type)):
                if re.search(self.basic_chess_type[index], string):
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
            AI_score += self.basic_chess_type_score[index]*AI_chess_type_extract[index]
        if AI_chess_type_extract[L5] >= 1:#有连五则标记
                self.AI_win = True
       
        score = (1-self.a)*AI_score - self.a*ply_score
        return score

    def AI_eva(self,map):#将传入的棋盘提取直线，划分棋型，并最终返回一个对当前棋局评分的综合操作
        self.line_extract(map)
        self.line_seg()
        return self.eva()

    def maxmin_search(self,map,depth):#最大最小值搜索
        pass

#初始化类
game = Game()
menu = Menu()
map = Map()
ai = AI()
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
#游戏事件循环
game_loop = True
while game_loop:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:#退出则结束
            pygame.quit()
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN and game.get_plysturn():#玩家行动
            mx,my = event.pos
            if map.click_response(mx,my,window):
                game.change_plysturn()
        elif game.get_plysturn() == False:#AI行动
            score_list = []
            highest_score_tuple = (0,0,-sys.float_info.max)
            for y in range(MAP_H):
                for x in range(MAP_W):
                    if map.append(x,y,2):
                        ai.__init__()#清空ai实例中的数据
                        score = ai.AI_eva(map.get_map()) - (abs(x-7)+abs(y-7)) #对于当前棋局的评分减去落子偏离棋盘中心的程度
                        if score>=highest_score_tuple[2]:
                            highest_score_tuple = (x,y,score)
                        score_list.append((x,y,score))
                        map.remove(x,y)
            map.append(highest_score_tuple[0],highest_score_tuple[1],2)
            map.chess_draw(window)
            #map.new_chess_draw(window,highest_score_tuple[0],highest_score_tuple[1],2)
            game.change_plysturn()
            map.eva_show(window,score_list)
            print(score_list)
            print('\n')