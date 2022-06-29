import numpy 
import pygame
import random
pygame.init()


font=pygame.font.SysFont(None,70)
win=pygame.display.set_mode((450,500))
check_matrix=numpy.zeros((9,9),dtype=int)
matrix=numpy.zeros((9,9),dtype=int)

def generateBoard():
    for i in range(20):
        x=random.randint(0,8)
        y=random.randint(0,8)
        num=random.randint(1,9)
        if checkMove(x,y,num):
            matrix[y][x]=num
            check_matrix[y][x]=2

def drawBoard():
    win.fill((255,255,255))

    #inserting all the numbers and colors
    for i in range(9):
        for j in range(9):
            if check_matrix[i][j]==2 or check_matrix[i][j]==1:
                if check_matrix[i][j]==2:
                    pygame.draw.rect(win,(200,100,100),(j*50,i*50,50,50))
                else:
                    pygame.draw.rect(win,(100,100,200),(j*50,i*50,50,50))
                img=font.render(str(matrix[i][j]),True,(0,0,0))
                win.blit(img,(j*50+12,i*50+4))

    #drawing lines for the board
    for i in range(1,10):
            pygame.draw.line(win,(0,0,0),(0,i*50),(450,i*50))
            if i!=9:
                pygame.draw.line(win,(0,0,0),(i*50,0),(i*50,450))
    for i in range(1,3):
        pygame.draw.line(win,(0,0,0),(0,i*150),(450,i*150),width=3)
        pygame.draw.line(win,(0,0,0),(i*150,0),(i*150,450),width=3)
    
    pygame.draw.rect(win,(0,0,0),(0,450,450,50))
    img=font.render("Solve it",True,(0,255,0))
    win.blit(img,(135,452))
    pygame.display.update()


def highlight():
    x,y = pygame.mouse.get_pos()
    if y>450:
        return x,y,True
    x=x//50
    y=y//50
    if check_matrix[y][x]!=2:
        pygame.draw.rect(win,(255,0,0),(x*50,y*50,50,50),width=3)
        pygame.display.update()
    return x,y,False


def insertNumber(x,y,event):
    if check_matrix[y][x]==2:
        drawBoard()
        return False
    if event.key==pygame.K_BACKSPACE:
        matrix[y][x]=0
        check_matrix[y][x]=0
        drawBoard()
        return False
    elif '0'<=event.unicode<='9':
        if  checkMove(x,y,int(event.unicode)):
            matrix[y][x]=int(event.unicode)
            check_matrix[y][x]=1
            drawBoard()
            return True
        drawBoard()
        return False

def checkMove(x,y,num):
    for i in range(9):
        if matrix[i][x]==num or matrix[y][i]==num:
            return False
    return True
    
def checkWin():
    for i in range(9):
        row=[]
        for j in range(9):
            if matrix[i][j] in row or matrix[i][j]==0:
                return False
            else:
                row.append(matrix[i][j]) 
    
    for i in range(9):
        column=[]
        for j in range(9):
            if matrix[j][i] in column or matrix[j][i]==0:
                return False
            else:
                column.append(matrix[j][i]) 
    return True


def solveGame():
    for i in range(9):
        for j in range(9):
            if check_matrix[i][j]!=2:
                check_matrix[i][j]=0
                matrix[i][j]=0
    drawBoard()

    row=0
    while row<=8:
        col=0
        while col<=8:
            for event in pygame.event.get():
                if event.type==pygame.QUIT:
                    return

            if check_matrix[row][col]!=2:
                num=1
                while not checkMove(col,row,num) and num<=9:
                    num+=1
                if num<=9:
                    check_matrix[row][col]=1
                    matrix[row][col]=num
                else:
                    while row>=0:
                        col-=1
                        next=False
                        if col<0:
                            col=9
                            row-=1
                            continue

                        if check_matrix[row][col]!=2:
                            num=matrix[row][col]
                            num+=1
                            while not checkMove(col,row,num) and num<=9:
                                num+=1
                            if num<=9:
                                matrix[row][col]=num
                                next=True
                            else:
                                matrix[row][col]=0
                                check_matrix[row][col]=0
                            pygame.time.delay(50)
                            drawBoard()
                        
                        if next:
                            break

                pygame.time.delay(50)
                drawBoard()

            col+=1
        row+=1

    return


generateBoard()
drawBoard()
wait=True
running=True
selected=False


while running:
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            running=False
            wait=False
        elif event.type==pygame.MOUSEBUTTONDOWN:
            if selected==True:
                drawBoard()
            x,y,solve=highlight()
            if solve:
                solveGame()
                drawBoard()
                running=False
                wait=True
            else:
                selected=True
        
        elif selected and event.type==pygame.KEYDOWN:
            inserted=insertNumber(x,y,event)
            selected=False
            if inserted and checkWin():
                font=pygame.font.SysFont(None,110)
                img=font.render("YOU WON",True,(0,255,0))
                win.blit(img,(0,100))
                pygame.display.update()
                running=False
              

if wait:
    running=True
    while running:
        for event in pygame.event.get():
            if event.type==pygame.KEYDOWN or event.type==pygame.QUIT:
                running=False