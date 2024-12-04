#encoding=u8
#导入库函数
#添加了空格暂停开始
#添加了超级食物,吃了5个食物后会有三分之2的可能生成一个超级食物,超级食物吃了可能加分或减分,但是加分可能性高些,超级食物不吃的话5秒后消失
#添加了长按按钮增加蛇的速度
try:
    from Tkinter import * 
except:
    from tkinter import * 
import random
#从Frame派生一个snake类,这是所有widget的父容器
class snake(Frame):
    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.stop=-1 #暂停状态为-1(没有暂停),1为暂停
        self.stopid=-1
        self.died=0 #玩家是否死亡
        self.score=0 #得分
        self.body = [(0,2),[0,1],[0,0]] #蛇的身体
        self.bodyid = []
        self.lockey=0 #按下时候锁定键盘

        self.pressnum=0
        self.food = [ -1, -1 ] #食物坐标
        self.foodid = -1
        self.bigfood=[-1,-1] #奖励食物的坐标
        self.bigfoodid=-1
        self.bigfoodflg=0 #奖励标记
        self.bigfoodtimeout=0 #奖励超时
        
        self.gridcount = 25 #地图大小
        self.size = 500 #屏幕大小
        self.di = 3  #方向
        
        self.speed = 300 #速度(越小越快-隔多少毫秒走一格,刻度是ms)
        self.oldspeed=self.speed #旧的速度
        
        self.top = self.winfo_toplevel() #窗口置顶显示
        self.top.resizable(False, False) #不可调节大小
        self.grid()  #grid布局
        self.canvas = Canvas(self)
        self.canvas.grid()
        self.canvas.config(width=self.size, height=self.size,relief=RIDGE) #确定窗口大小
        self.drawgrid() #画地图 
        s = self.size/self.gridcount #单元大小
        
        id = self.canvas.create_oval(self.body[0][0]*s,self.body[0][1]*s,
            (self.body[0][0]+1)*s, (self.body[0][1]+1)*s, fill="yellow",outline="white") #绘制初始蛇头
        self.bodyid.insert(0, id)
        for i in range(1,len(self.body)):
            id = self.canvas.create_oval(self.body[i][0]*s,self.body[i][1]*s,
            (self.body[i][0]+1)*s, (self.body[i][1]+1)*s, fill="green",outline="green") #绘制初始蛇体
            self.bodyid.append(id)
            
        self.scoreid=self.canvas.create_text(self.size-50,10,  # 绘制初始分数
        text = 'score: '+str(self.score)             
        ,fill = 'black')

        self.bind_all("<KeyPress>", self.keypress) #绑定按下时的按键
        self.bind_all("<KeyRelease>", self.keyrelease) #绑定按键
        self.drawfood() #绘制食物 
        self.after(self.speed, self.drawsnake)  #定时执行drawsnake函数
    def drawgrid(self): #绘制地图
        s = self.size/self.gridcount
        for i in range(0, self.gridcount+1):
            self.canvas.create_line(i*s, 0, i*s, self.size,fill="#ccaacc") #画地图竖着的线
            self.canvas.create_line(0, i*s, self.size, i*s,fill="#ccaacc") #画地图横着的线
    def drawsnake(self): #绘制蛇体
        if self.died==1: #死亡跳出
            return
        if self.stop==1:
            if self.stopid==-1:
                self.stopid=self.canvas.create_text(self.size/2,self.size/2-20,
                text = '暂停中,点击空格继续...'      
                ,fill = '#238C23'
                #,font=font.Font(size=22)
                )
            self.after(self.speed, self.drawsnake)
            return
        else:
            if self.stopid!=-1:
                self.canvas.delete(self.stopid)
                self.stopid=-1
        self.lockey=0 #解锁按键
        
        self.drawscore()
        s = self.size/self.gridcount
        head = self.body[0] 
        new = [head[0], head[1]]  
        if self.di == 1:
            new[1] = (head[1]-1)  
        elif self.di == 2:
            new[0] = (head[0]+1) 
        elif self.di == 3:
            new[1] = (head[1]+1)  
        else:
                new[0] = (head[0]-1) 
        next = ( new[0], new[1] )
        area=[] #area是地图界限
        for i in range(self.gridcount):
            for j in range(self.gridcount):
                area.append((i,j))
        if next in self.body or next not in area: #撞到自己或者超出界限
            self.die()
        elif next == (self.food[0], self.food[1]):
            self.bigfoodflg+=1 #食物奖励标记+1
            self.score+=int(len(self.body)/5)+1  #增加得分(难度越高得分越多)
            self.body.insert(0, next)
            self.canvas.itemconfig(self.foodid,fill="green",outline="green") #更新吃掉的食物颜色变为身体颜色
            self.canvas.itemconfig(self.bodyid[0],fill="green",outline="green")  #更新身体颜色
            self.bodyid.insert(0, self.foodid)
            self.drawfood()
            if self.speed>100 and self.score%5==0: #随着难度速度提高
                self.speed-=50
                self.oldspeed=self.speed
        elif next == (self.bigfood[0], self.bigfood[1]): #吃到奖励
            self.score+=random.randrange(-2,5) #一定几率减分
            self.canvas.delete(self.bigfoodid) #移除奖励食物
            self.bigfood=[-1,-1] #奖励食物的坐标
            self.bigfoodid=-1
            self.bigfoodtimeout=0
        else:
            self.canvas.itemconfig(self.bodyid[0],fill="green",outline="green")  #更新身体颜色
            tail = self.body.pop()
            id = self.bodyid.pop()
            self.canvas.move(id, (next[0]-tail[0])*s, (next[1]-tail[1])*s)
            self.body.insert(0, next)
            self.bodyid.insert(0, id) 
            self.canvas.itemconfig(id,fill="yellow",outline="white") #更新头部颜色
        if(self.bigfoodid!=-1):
            self.bigfoodtimeout+=self.speed
            if(self.bigfoodtimeout>5000): #5秒不吃嗝屁
                self.canvas.delete(self.bigfoodid) #移除奖励食物
                self.bigfood=[-1,-1] #奖励食物的坐标
                self.bigfoodid=-1
                self.bigfoodtimeout=0
        self.after(self.speed, self.drawsnake)
    def drawscore(self): #绘制分数 
        self.canvas.delete(self.scoreid)
        self.scoreid=self.canvas.create_text(self.size-50,10,  # 使用create_text方法绘制文字  
        text = 'score: '+str(self.score)          # 所绘制文字的内容  
        ,fill = 'black')                          # 所绘制文字的颜色为灰色
    def drawfood(self): #绘制食物
        s = self.size/self.gridcount
        if(self.bigfoodflg==5):#如果吃到了第五个食物
            self.bigfoodflg=0 #标记清零
            r=random.randrange(0,3) #可能为0,1,2
            if(r!=0): #三分之二的可能产生奖励
                x = random.randrange(0, self.gridcount)
                y = random.randrange(0, self.gridcount)
                while((x, y) in self.body or (x,y)==self.food):  #确保食物和蛇体不冲突
                    x = random.randrange(0, self.gridcount)
                    y = random.randrange(0, self.gridcount)
                id = self.canvas.create_oval(x*s-2, y*s-2,(x+1)*s+2, (y+1)*s+2, fill="yellow",outline="blue")
                self.bigfood[0] = x
                self.bigfood[1] = y
                self.bigfoodid = id
        x = random.randrange(0, self.gridcount)
        y = random.randrange(0, self.gridcount)
        while (x, y) in self.body:  #确保食物和蛇体不冲突
            x = random.randrange(0, self.gridcount)
            y = random.randrange(0, self.gridcount)
        #id = self.canvas.create_rectangle(x*s,y*s, (x+1)*s, (y+1)*s, fill="yellow")
        id = self.canvas.create_oval(x*s, y*s,(x+1)*s, (y+1)*s, fill="blue",outline="blue")
        self.food[0] = x
        self.food[1] = y
        self.foodid = id
    def die(self): #死亡函数
        if len(self.bodyid)<=0:
            return
        if self.died==1: #死亡动画
            if len(self.bodyid)>0:
                self.canvas.delete(self.bodyid.pop())
                self.after(230, self.die)
        else:
            self.died=1 #标记玩家已经死亡
            self.after(self.speed, self.drawsnake)
            self.canvas.create_text(self.size/2,self.size/2-20,       # 使用create_text方法绘制文字  
            text = '最终得分: '+str(self.score)      # 所绘制文字的内容  
            ,fill = 'black'  ,    )                    # 所绘制文字的颜色为灰色
            #font=font.Font(size=34))                # 设置字体大小
            self.after(230, self.die)
    def keyrelease(self, event): #按键响应
        self.pressnum=0
        self.speed = self.oldspeed
        if event.keysym == "space": #空格
            self.stop=0-self.stop #反转暂停状态
            return 
    def keypress(self, event):
        if self.died==1 or self.stop==1: #如果玩家死亡或者处于暂停,返回
            return 
        if (event.keysym == "Up" or event.keysym.upper()=="W") and self.di != 3 and self.lockey==0: #如果玩家按上并且玩家正在前进的方向不是下
            self.di = 1 #刷新方向为上
            self.lockey=1 #锁键,防止撞入自身
        elif (event.keysym == "Right" or event.keysym.upper()=="D")  and self.di !=4 and self.lockey==0: #按右且不往左走
            self.di = 2 #刷新方向为右
            self.lockey=1
        elif (event.keysym == "Down" or event.keysym.upper()=="S")  and self.di != 1 and self.lockey==0: #按下且不往上走
            self.di = 3 #刷新方向为下
            self.lockey=1
        elif (event.keysym == "Left" or event.keysym.upper()=="A")  and self.di != 2 and self.lockey==0: #按左且不往右走
            self.di = 4 #刷新方向为左
            self.lockey=1
        self.pressnum+=1
        if(self.pressnum<2): 
            return
        else:
            self.lockey=0
            self.pressnum=0
        #按键响应-按下时候加速
        if (event.keysym == "Up" or event.keysym.upper()=="W") and self.di == 1:  
            self.speed=90
        if (event.keysym == "Right" or event.keysym.upper()=="D")  and self.di ==2: 
            self.speed=90
        if (event.keysym == "Down" or event.keysym.upper()=="S")  and self.di == 3:  
            self.speed=90
        if (event.keysym == "Left" or event.keysym.upper()=="A")  and self.di == 4:  
            self.speed=90
app = snake()
app.master.title("贪食蛇")
app.mainloop()

