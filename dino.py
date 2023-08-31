import pygame 
import random 
from matplotlib import pyplot as plt
import numpy as np
#-----------參數設定----------------------------------------------

  # 動畫設定
value = 0
FPS = 60
  # 位置參數
width, height = 600, 250     #設定視窗 600X250
fix_h=15    
dino_boundry=height-fix_h+4.5 

  # 物理條件參數             
bg_speed=2   
GRAVITY=0.9

  # 顏色參數
BLACK = (0, 0, 0)
WHITE = (233, 233, 233)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)

 #遊戲分數參數
score=0  #分數
iteration=0 #死亡次數
BestGrade=0 #最高分數
 
 #遊戲統計
graph_x=[]
graph_y=[]


#-----------------------------------------------------------------

pygame.init()
screen = pygame.display.set_mode((width, height))   
pygame.display.set_caption("   Dino Dinasour Demo ")         

clock = pygame.time.Clock()   #建立時間元件

#地板精靈----------------------------------------------------------
class Ground(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        #先給物件加載圖片 圖片大小 寬X高 = 600 X 12
        self.ground_1= pygame.image.load("dino_png/ground_1.png")
        self.ground_2= pygame.image.load("dino_png/ground_2.png")
        #給予物件碰撞框
        self.ground_1_rect=self.ground_1.get_rect()
        self.ground_2_rect=self.ground_2.get_rect()
        #給予物件座標
            # 定義問題 :1. x位置會移動，y不變
            #          2. g1 完接 g2 所以x位置應該為 
            #             變數x+g1之寬度
        self.x_a=0 #給予x 原點位置
        self.x_b=width # B皆在A後面 
        
    # update 持續跟新之內容 
    def update(self):
        self.x_a -= bg_speed
        self.x_b -= bg_speed
    # 畫圖上去之screen
    def draw(self):     
        # location
        self.ground_1_rect.bottomleft=(self.x_a , height-fix_h)
        self.ground_2_rect.bottomleft=(self.x_b , height-fix_h)

        # boundary condition , bg1 connect bg2 & bg2 end connect bg1
        if self.ground_1_rect.right < 0 : #when a run out(a_end reach 0) 
            # when a_end happed
            # A_start with b_end
            self.x_a = width
            self.ground_1_rect.bottomleft = ( self.x_a , height-fix_h)
            
        if self.ground_2_rect.right < 0 :
            self.x_b = width
            self.ground_2_rect.bottomleft = ( self.x_b , height-fix_h)

            
        screen.blit(self.ground_1,self.ground_1_rect)
        screen.blit(self.ground_2,self.ground_2_rect)
#-----------------------------------------------------------------
#人物精靈--------------------------------------------------------
class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        
        #狀態:跑步連續動畫、跳躍時、碰到仙人掌時
          # 定義狀態變數 : 二元變數
          # 三個狀態  ->   三個外觀
        self.status_run = True
        self.status_jump = False
        self.status_die = True
        self.value=0
        
        if self.status_run is True:
            self.image_sprite = [pygame.image.load("dino_png/dino_run1.png") ,
                pygame.image.load("dino_png/dino_run1.png") ,
                pygame.image.load("dino_png/dino_run1.png") ,
                pygame.image.load("dino_png/dino_run1.png") ,
                pygame.image.load("dino_png/dino_run1.png") ,
                pygame.image.load("dino_png/dino_run1.png") ,
                pygame.image.load("dino_png/dino_idle.png") ,
                pygame.image.load("dino_png/dino_idle.png") ,
                pygame.image.load("dino_png/dino_run2.png") , 
                pygame.image.load("dino_png/dino_run2.png") ,
                pygame.image.load("dino_png/dino_run2.png") ,
                pygame.image.load("dino_png/dino_run2.png") ,
                pygame.image.load("dino_png/dino_run2.png") ,
                ]

            self.image = self.image_sprite[self.value]
            self.rect = self.image.get_rect()
        
        if self.status_jump is True:
            self.image = pygame.image.load("dino_png/dino_run1.png")
            self.rect = self.image.get_rect()
            
        if self.status_die is True:
            self.image =pygame.image.load("dino_png/dino_dies.png")
            self.rect = self.image.get_rect()
            self.status_run = False
            self.status_jump = False
            
            
        self.rect.center = (70 ,height-25)
           # 初始_y 速度為零
        self.vel_y=0
           

    def update(self):
        y_move=0
        
        #案件觸發狀態_bool
        key_pressed = pygame.key.get_pressed()
        
        if self.status_die == True:
            self.rect.x = 0 
            self.rect.y = 0 
            
        #定義案件
        if key_pressed[pygame.K_RIGHT]:
            self.rect.x += 5
            
        if key_pressed[pygame.K_LEFT]:
            self.rect.x -= 4
            
        if key_pressed[pygame.K_UP] and self.status_jump is False:
            self.vel_y = -15
            self.status_jump = True
            self.status_run = False
        #避免按一下會飛起來    
        if not key_pressed[pygame.K_UP] :
            self.status_jump= False
            self.status_run= True
        #避免在空中還能跳躍
        if self.rect.y < dino_boundry-50 :
            self.status_jump = True
            self.status_run = False
        
        #物理條件
          #1. 自動向前 (取消)
        #self.rect.x +=1
          #2. 重力
        self.vel_y += GRAVITY
        if self.vel_y >10:
            self.vel_y =10
        y_move += self.vel_y
        self.rect.y += y_move
        
        #大於視窗寬度之邊界設定
          # 邊界
        if self.rect.right > width:
            self.rect.right = width 
            if  self.rect.bottom > dino_boundry:
                self.rect.bottom = dino_boundry
        elif self.rect.left < 0:
            self.rect.left = 0
            if  self.rect.bottom > dino_boundry:
                self.rect.bottom = dino_boundry
          # 地板 ground
        elif self.rect.bottom > dino_boundry:  #4.5是物件之間之空白
            self.rect.bottom = dino_boundry # 碰到ground       
        
    def draw(self,value):
        #定義狀態外觀
        if self.status_jump == True:
            screen.blit(self.image_sprite[5],self.rect)
        if self.status_run == True:
            screen.blit(self.image_sprite[value],self.rect)
        if self.status_die == True:    
            screen.blit(self.image,self.rect)
        pygame.draw.rect(screen,(255,0,0),self.rect,1)
                
#障礙物精靈--------------------------------------------------------

#問題 list不能是單純之路徑
cactus_small=[pygame.image.load("dino_png/cactus_small_1.png") ,
            pygame.image.load("dino_png/cactus_small_2.png") ,
            pygame.image.load("dino_png/cactus_small_3.png") ]

cactus_big=[
            pygame.image.load("dino_png/cactus_big_1.png") ,
            pygame.image.load("dino_png/cactus_big_2.png") ,
            pygame.image.load("dino_png/cactus_big_3.png") ]

bird_list=[
            pygame.image.load("dino_png/bird_1.png"),
            pygame.image.load("dino_png/bird_1.png"),
            pygame.image.load("dino_png/bird_2.png"),
            pygame.image.load("dino_png/bird_2.png")]

class Obstacle:
    def __init__(self, imageList : list, typeObject : int):
        self.image_list = imageList  # 以變數儲存障礙物類型
        self.type = typeObject  # 以變數儲存障礙物樣貌
        self.image = self.image_list[self.type] # 將障礙物框起
        self.rect = self.image.get_rect()  # 將障礙物框起

    def update(self):
        self.rect.x -= bg_speed
        
        if self.rect.x <-75:
            self.rect.x= width+75

    def draw(self):
        screen.blit(self.image, (self.rect.x,self.rect.y))
        pygame.draw.rect(screen,(255,0,0),self.rect,1)

class LargeCactus(Obstacle): #高50 寬25、50、75
    def __init__(self, image_list : list):
        self.type = random.randint(0, 2)  # 三種大仙人掌型態隨機選取一種
        super().__init__(image_list, self.type)  # 繼承障礙物屬性與動作
        self.rect.x = width + random.randint(0,100)
        self.rect.y = height-fix_h-50  # Y座標位置

class SmallCactus(Obstacle): #高35 寬17、34、51
    def __init__(self, image_list : list):
        self.type = random.randint(0, 2)  # 三種小仙人掌型態隨機選取一種
        super().__init__(image_list, self.type)  # 繼承障礙物屬性與動作
        self.rect.x = width + random.randint(0,100)
        self.rect.y = height-fix_h-35 # Y座標位置

class Bird(Obstacle):  #width 42
    def __init__(self,image_list : list):
        self.type=0 #不重要
        super().__init__(image_list, self.type)
        self.bird_value=0
        self.rect.y = height // 3  # Y座標位置
        self.rect.x = width+10
        
    def update(self):
        self.rect.x -= bg_speed + random.randint(0,1)
        self.bird_value +=0.1   # b_value改以微小增量，避免list清單過大。
        
        if self.bird_value >= len(self.image_list)-1:
            self.bird_value=0
        if self.rect.x <= -50:
            self.rect.x = width + 20

    def draw(self):
        y=round(self.bird_value)
        screen.blit(self.image_list[y], self.rect)
        pygame.draw.rect(screen,(255,0,0),self.rect,1)  
        
#-----------------------------------------------------------------
#分數系統---------------------------------------------------------
class TextSystem(pygame.sprite.Sprite):
    def __init__(self,text:str,size:int,color:pygame.Color,postition:tuple):
        pygame.sprite.Sprite.__init__(self)
        self.font = pygame.font.SysFont('freesansbold.ttf', size)
        self.surface = self.font.render(text, True, color)  # 印出的字串(參數)與呈現
        self.position=postition  # 文字的中心位置(參數)
        self.rect = self.surface.get_rect()  # 文字框起
        self.rect.center=self.position
    
        self.death_text_position = (width // 2, height // 2)  # 死亡文字顯示的座標位置
        self.dino_position = (width // 2 - 20, height // 2 - 140)  # 恐龍顯示的座標位置
        self.grade=0
        
    def draw(self):
        screen.blit(self.surface,self.rect)
        
#----------------------------------------------------------------
#障礙物產生 產生出障礙物清單(可迭代物件) ，將用for迴圈逐一執行各list內之物件
obstacle_list = []

def obstacle_gererate():

    rand_value= random.randint(0,2)
    if rand_value == 0:
        obstacle_list.append(SmallCactus(cactus_small))
    if rand_value == 1:
        obstacle_list.append(LargeCactus(cactus_big))
    if rand_value == 2:
        obstacle_list.append(Bird(bird_list))

#-----------------------------------------------------------------

#def--------------------------------------------------------------

def create_picture(x:list,y:list):
    screen_statist = pygame.display.set_mode((600, 400))   
    pygame.display.set_caption("Game statist")
    
    plt.figure(figsize=(6, 4))
    plt.xlabel('# of deaths',fontsize="10") # 設定 x 軸標題
    plt.ylabel('Best score',fontsize="10") # 設定 y 軸標題
    plt.plot(x ,y , marker='o')
    
    
    plt.savefig("statist.png")
    statist_mode=pygame.image.load("statist.png")
    #screen_statist.fill(WHITE)
    screen_statist.blit(statist_mode,(0,0))
    pygame.display.update()      

    
#----------------------------------------------------------------

#實例化 呼叫類別使用物件

#放置物件
ground=Ground()
dino=Player()

#關閉程式的程式碼
running = True
while running:
    clock.tick(FPS)        #每秒執行30次

    #角色死掉時顯示
    
    if dino.status_die is True:
        #遊戲開始畫面
        if iteration == 0:
             #文字顯示
            screen.fill( (255,255,255) )
            a=TextSystem(f"Dino Dinasour Demo ",40,BLACK,(width//2,height//3-10))
            m=TextSystem("Please ckick the mouse to start",40,BLACK,(width//2,height//2+30))
            a.draw()
            m.draw()
            pygame.display.update()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    score=0 #歸零計分
                    dino.status_die = False #點滑鼠進入主要遊戲迴圈
                    iteration = 1
        #第一次到第n次死掉畫面
        if iteration >= 1:
            
            #文字顯示
            num_dies=TextSystem(f"Death : {iteration} ",30,BLACK,(125,100))
            finalScore=TextSystem(f"Your score : {score//30}",30,BLACK,(145,120))
            messege=TextSystem("Please ckick the mouse to restart",40,BLACK,(width//2,150))
            num_dies.draw()
            finalScore.draw()
            messege.draw()
            
            dino.rect.bottomleft =  20,height-fix_h+50 # 角色重新定位
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    graph_x.append(iteration)
                    graph_y.append(score//30)
                    score=0 #歸零計分
                    iteration +=1
                    dino.status_die = False
                    
            key_pressed = pygame.key.get_pressed()
            if key_pressed[pygame.K_ESCAPE]:
                running = False
            if key_pressed[pygame.K_SPACE]: #想要展示數據圖表
                graph_x.append(iteration)
                graph_y.append(score//30)
                running = False
                
        pygame.display.update()  
    #腳色活著時
    if dino.status_die is False:
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        
        #定義動畫，不會超過list之值
        if value >= len(dino.image_sprite):
            value = 0
        
        #分數迴圈
        if dino.status_die != True: #不加入限制式會持續計分
            grade=TextSystem(f"Yor score:{score//30}",25,BLACK,(525,40))
            deaths=TextSystem(f"Deaths:{iteration-1}",25,BLACK,(50,40))
            MaxGrade=TextSystem(f"best score:{BestGrade//30}",25,BLACK,(300,40))
        if score >= BestGrade:
            BestGrade = score

        #持續跟新
        
        dino.update()
        ground.update()

        #繪圖  // 每秒繪圖60次 如果白先先填 那整個畫面都會是白色的
        #順序 1. 重製畫面為白色
        #     2. 物件地板放上去
        screen.fill( (255,255,255) )  # 若不加會移動物件會有拖移痕跡，畫面清空
         # 文字
        grade.draw()
        deaths.draw()
        MaxGrade.draw()
         # 物件
        ground.draw()        # 繪製地板精靈
        dino.draw(value)     # 繪製腳色物件 
        
        #定義障礙物產生 必須是畫在screen.fill後
        if len(obstacle_list) == 0 :
            obstacle_gererate()    
        for i in  obstacle_list:
            result = pygame.sprite.collide_mask(dino,i)
            
            i.update()
            i.draw()
                
            if len(obstacle_list) == 1 and i.rect.x < width // 2 : #第二個物件產生
                obstacle_gererate()
                
            if i.rect.x < 0 :
                obstacle_list.pop(0)     #'Bird' object has no attribute 'pop'不能寫i要寫type為list
                                         #pop() index -1 是最後一個，目標是先進先出，所以先pop調iondex為0值
            
            #碰撞檢測 
            print(f"Dino die.,list of y is {graph_y} \n list of x is {graph_x}" if ( result != None) else "No hit.")
            
                
            if result != None:          #dino 死亡
                dino.status_die = True
                obstacle_list=[]
            
        pygame.display.update()     #更新視窗
        score +=1
    value +=1


#繪製統計圖表

create_picture(graph_x,graph_y )

# 游戏主循环
stastist_running = True
while stastist_running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            stastist_running = False

# 退出 PyGame

pygame.quit()  # WHILE 迴圈跳脫後執行結束





