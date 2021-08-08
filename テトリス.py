#!/usr/bin/env python
# coding: utf-8

# In[91]:


import pygame
from pygame.locals import *
import sys
import random
import copy
import numpy as np
import time


# In[92]:


MAX_Y = 22
MAX_X = 10
Mini_Y = 7
Mini_X = 7
screen_size = 1000,800
block_position = 5,1
next_block_position = 4,4
MOVE_LEFT = 0  
MOVE_RIGHT = 1  
MOVE_DOWN = 2 
MOVE_ROT = 3


# In[93]:


next_board_array = [
    [1,1,1,1,1,1,1],
    [1,0,0,0,0,0,1],
    [1,0,0,0,0,0,1],
    [1,0,0,0,0,0,1],
    [1,0,0,0,0,0,1],
    [1,0,0,0,0,0,1],
    [1,1,1,1,1,1,1]
]


# In[155]:


board_array = [[-10,0,0,0,0,0,0,0,0,-10],
               [-10,0,0,0,0,0,0,0,0,-10],
               [1,0,0,0,0,0,0,0,0,1],
               [1,0,0,0,0,0,0,0,0,1],
               [1,0,0,0,0,0,0,0,0,1],
               [1,0,0,0,0,0,0,0,0,1],
               [1,0,0,0,0,0,0,0,0,1],
               [1,0,0,0,0,0,0,0,0,1],
               [1,0,0,0,0,0,0,0,0,1],
               [1,0,0,0,0,0,0,0,0,1],
               [1,0,0,0,0,0,0,0,0,1],
               [1,0,0,0,0,0,0,0,0,1],
               [1,0,0,0,0,0,0,0,0,1],
               [1,0,0,0,0,0,0,0,0,1],
               [1,0,0,0,0,0,0,0,0,1],
               [1,0,0,0,0,0,0,0,0,1],
               [1,0,0,0,0,0,0,0,0,1],
               [1,0,0,0,0,0,0,0,0,1],
               [1,0,0,0,0,0,0,0,0,1],
               [1,0,0,0,0,0,0,0,0,1],
               [1,0,0,0,0,0,0,0,0,1],
               [1,1,1,1,1,1,1,1,1,1]           
              ]
shape = [[[0, -1], [0, 0], [0, 1], [0, 2]], # I block
         [[-1, -1], [0, -1], [0, 0], [0, 1]], # J block
         [[0, -1], [0, 0], [0, 1], [-1, 1]], # L block
         [[0, -1], [0, 0], [-1, 0], [-1, 1]], # S blosk
         [[-1, -1], [-1, 0], [0, 0], [0, 1]], # Z block
         [[0, -1], [0, 0], [-1, 0], [0, 1]], # T block
         [[0, 0], [-1, 0], [0, 1], [-1, 1]] # square
        ]
color = [(0, 100, 50), 
         (150, 150, 150), 
         (255, 0, 0), 
         (0, 0, 255), 
         (255, 165, 0),
         (255, 0, 255), 
         (0, 255, 0)] 


# In[156]:


class Board():#ボードの描画を管理する
    def __init__(self,board_array):
        self.board = copy.deepcopy(board_array)
        self.music = pygame.mixer.Sound("shoot4.mp3")
    def draw(self,screen):
        for y in range(MAX_Y):
            for x in range(MAX_X):
                if self.board[y][x] <= 0:
                    pygame.draw.rect(screen, 
                                     (0, 0, 0), 
                                     Rect(30+35*x, 30+35*y, 35, 35))
                else:
                    pygame.draw.rect(screen, 
                                     (255, 255, 255), 
                                     Rect(30+35*x, 30+35*y, 35, 35))
    def fix_board(self,x,y,shape,game):
        board_array = np.array([y,x])+np.array(shape)
        for Y,X in board_array:
            self.board[Y][X] += 1
        game.next_block(game.next_block_board.getNextblocktype())
        game.new_next_block()
    def delete_line(self,board_array,screen,game):
        self.delete_num = 0
        for Y in range(2,MAX_Y-1):
            if 0 not in board_array[Y][1:MAX_X-1]:
                self.delete_num +=1
                (board_array).pop(Y)
                (board_array).insert(2,[1, 0, 0, 0, 0, 0, 0, 0, 0, 1]) 
                (self.music).play()
        game.score.record(game)


# In[157]:


class Score():
    def __init__(self):
        self.score = 0
        font = pygame.font.Font(None, 50)
    def record(self,game):
        self.score += 150*game.board.delete_num
    def draw(self,screen):
        font = pygame.font.Font(None, 50)
        score_text = font.render("SCORE " + str(self.score), True, (255, 255, 255))
        screen.blit(score_text, (720, 600))


# In[158]:


class Next_block_board():
    def __init__(self):
        self.block_type = random.randint(0,6)
        self.board = copy.deepcopy(next_board_array)
        self.shape = copy.deepcopy(copy.deepcopy(shape)[self.block_type])
        self.color = copy.deepcopy(copy.deepcopy(color)[self.block_type])
        self.x,self.y = 3,3
    def draw(self,screen):
        for Y in range(Mini_Y):
            for X in range(Mini_X):
                if self.board[Y][X] <= 0:
                    pygame.draw.rect(screen, 
                                     (0, 0, 0), 
                                     Rect(410+35*X, 30+35*Y, 35, 35))
                else:
                    pygame.draw.rect(screen, 
                                     (255, 255, 255), 
                                     Rect(410+35*X, 30+35*Y, 35, 35))  
        for y,x in self.shape:
            pygame.draw.rect(screen, 
                             self.color, 
                             Rect(410+35*(x+self.x), 30+35*(y+self.y), 35, 35))
    def getNextblocktype(self):
        return self.block_type


# In[159]:


class Block():#移動中のブロックを管理する
    def __init__(self,block_type,block_position):
        self.shape = copy.deepcopy(copy.deepcopy(shape)[block_type])
        self.color = copy.deepcopy(copy.deepcopy(color)[block_type])
        self.x,self.y = block_position
        self.music = pygame.mixer.Sound("short_punch1.mp3")
    def draw(self,screen):
        for y,x in self.shape:
            pygame.draw.rect(screen, 
                             self.color, 
                             Rect(30+35*(x+self.x), 30+35*(y+self.y), 35, 35))
            
    def get_moved_cord(self,direction):
        if direction == MOVE_LEFT:
            return self.x-1,self.y
        elif direction == MOVE_RIGHT:
            return self.x+1,self.y
        elif direction == MOVE_DOWN:
            return self.x,self.y+1
        elif direction == MOVE_ROT:
            return self.x,self.y
        
    def judge_moveable(self,direction,board):
        x,y = self.get_moved_cord(direction)
        moved_block_position = np.array([y,x])+np.array(self.shape)
        for y,x in moved_block_position:
            if board[y][x] != 0:
                return False,direction
        return True,direction
    
        
    def judge_rotable(self,direction,board,shape):
        x,y = self.get_moved_cord(direction)
        moved_block_position = np.array([y,x])+np.array(shape)
        for y,x in moved_block_position:
            if board[y][x] != 0:
                return False,direction
        return True,direction
    
    def move_block(self,direction,board_array,screen,board,game):
        flag,direction = self.judge_moveable(direction,board_array)
        if flag:
            self.x,self.y = self.get_moved_cord(direction)
            self.draw(screen)
        else:
            if direction == MOVE_DOWN: 
                (self.music).play()
                board.fix_board(self.x,self.y,self.shape,game)
                board.delete_line(board_array,screen,game)
    def rot_block(self,direction,board_array,screen,board,game):
        rot_block_list = []
        for y,x in self.shape:
            rot_y = x*(1)+y*0
            rot_x = x*0-y*1
            rot_block_list.append([rot_y,rot_x])
        flag,direction = self.judge_rotable(direction,board_array,rot_block_list)
        if flag:
            self.shape = rot_block_list
            self.draw(screen)
        else:
            pass


# In[160]:


class Game():
    def __init__(self,board_array):
        self.board = Board(board_array)
        self.button = Button()
        self.score = Score()
        self.block = None
        self.next_block_board = None
        self.gameover = None
    def start(self):
        self.new_block()
        self.new_next_block()
    def new_block(self):
        block_type = random.randint(0,6)
        self.block = Block(block_type,block_position)
    def next_block(self,block_type):
        self.block = Block(block_type,block_position)
    def new_next_block(self):
        self.next_block_board = Next_block_board()
    def end(self,screen):
        self.gameover = Gameover(screen)


# In[161]:


class Button():
    def __init__(self):
        self.button = pygame.Rect(400, 600, 300, 125)
        self.font = pygame.font.SysFont(None, 25)
        self.text = (self.font).render("Restart", True, (0,0,0))
    def draw(self,screen):
        pygame.draw.rect(screen, (255, 255, 255), self.button)
        screen.blit(self.text, (510, 650))


# In[162]:


class Gameover():
    def __init__(self,screen):
        self.font = pygame.font.Font(None, 50)
        self.gameover_text = (self.font).render("GAMEOVER", True, (0, 0, 0))
        screen.blit(self.gameover_text, (450, 500))
    def draw(self,screen):
        self.gameover_text = (self.font).render("GAMEOVER", True, (75, 0, 0))
        screen.blit(self.gameover_text, (450, 500))


# In[163]:


def Event(screen,game,timer_event):
    while True:
        
        game.board.draw(screen)
        game.block.draw(screen)
        game.button.draw(screen)
        screen.fill((0,0,0),(720, 600,280,200))
        game.score.draw(screen)
        game.next_block_board.draw(screen)
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_DOWN:
                    game.block.move_block(MOVE_DOWN,game.board.board,screen,game.board,game)
                if event.key == K_LEFT:
                    game.block.move_block(MOVE_LEFT,game.board.board,screen,game.board,game)
                if event.key == K_RIGHT:
                    game.block.move_block(MOVE_RIGHT,game.board.board,screen,game.board,game)
                if event.key == K_SPACE:
                    game.block.rot_block(MOVE_ROT,game.board.board,screen,game.board,game)
                    
            elif event.type == timer_event:
                game.block.move_block(MOVE_DOWN,game.board.board,screen,game.board,game)
            
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if (game.button.button).collidepoint(event.pos):
                    game = Game(board_array)
                    game.start()
                    game.end(screen)
            if not(game.block.judge_moveable(MOVE_DOWN,game.board.board)[0]) and game.block.x == 5 and game.block.y == 1:
                game.end(screen)
                game.gameover.draw(screen)


# In[164]:


def main():
    pygame.init()
    screen = pygame.display.set_mode((1000,800))
    pygame.display.set_caption("Tetris")
    
    game = Game(board_array)
    game.start()
    
    timer_interval = 1500 # 0.5 seconds
    timer_event = pygame.USEREVENT + 1
    pygame.time.set_timer(timer_event , timer_interval)
    
    pygame.mixer.init(frequency = 44100)
    mp3_BGM = pygame.mixer.Sound("MBkachusha.mp3")
    mp3_BGM.play(-1)
    Event(screen,game,timer_event)


# In[165]:


if __name__ == "__main__":
    main()


# In[ ]:





# In[ ]:




