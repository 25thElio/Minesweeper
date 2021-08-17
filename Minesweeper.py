import random
import numpy as np


def createBoard(width,height,n):
    length=width*height
    lst=np.zeros(length)
    count=0
    while count<n:
        r=random.randint(0,length-1)
        if lst[r] == 0:
            lst[r]=1
            count+=1
    return np.reshape(lst,(height,width))

def createXBoard(Board):
    row,col=Board.shape    
    return np.reshape([' X ' for x in Board.reshape((row*col,1))],Board.shape)

def getNumbers(Board):
    Numbers=[]
    row,col=Board.shape    
    for x in range(row):
        for y in range(col):
            if Board[x][y]==1:
                N=-1
            else:
                N=0
                if y>0:
                    N+=Board[x][y-1]
                    if x>0:
                        N+=Board[x-1][y-1]
                    if x<row-1:
                        N+=Board[x+1][y-1]
                if y<col-1:
                    N+=Board[x][y+1]
                    if x>0:
                        N+=Board[x-1][y+1]
                    if x<row-1:
                        N+=Board[x+1][y+1]
                if x>0:
                    N+=Board[x-1][y]
                if x<row-1:
                    N+=Board[x+1][y]
            Numbers.append(N)
    return np.array(Numbers).reshape(row,col)

def atomicUncover(x,y,numBoard,XBoard):
    row,col=numBoard.shape
    N=numBoard[x][y]
    if N==0:
        XBoard[x][y]= '   '
        numBoard[x][y]=-2
        if y>0:
            XBoard,numBoard=atomicUncover(x,y-1,numBoard,XBoard)
            if x>0:
                XBoard,numBoard=atomicUncover(x-1,y-1,numBoard,XBoard)
            if x<row-1:
                XBoard,numBoard=atomicUncover(x+1,y-1,numBoard,XBoard)
        if y<col-1:
            XBoard,numBoard=atomicUncover(x,y+1,numBoard,XBoard)
            if x>0:
                XBoard,numBoard=atomicUncover(x-1,y+1,numBoard,XBoard)
            if x<row-1:
                XBoard,numBoard=atomicUncover(x+1,y+1,numBoard,XBoard)
        if x>0:
            XBoard,numBoard=atomicUncover(x-1,y,numBoard,XBoard)
        if x<row-1:
            XBoard,numBoard=atomicUncover(x+1,y,numBoard,XBoard)
    elif N>0:
        XBoard[x][y]=N
    return XBoard,numBoard

def uncover(x,y,numBoard,XBoard,Board):
    if numBoard[x][y]==-1:
        return False, Board
    else:
        XBoard,numBoard=atomicUncover(x,y,numBoard,XBoard)
        return True, XBoard

playing=True
print('Enter width, height, and number of mines of the minefield')

while True:
    try:
        width=int(input('Width: '))
        if width<0:
            raise ValueError
        break
    except ValueError:
        print('Only positive integers!')
while True:
    try:
        height=int(input('Height: '))
        if height<0:
            raise ValueError
        break
    except ValueError:
        print('Only positive integers!')
while True:
    try:
        n=int(input('Number of mines: '))
        if n<1 or n>width*height:
            raise ValueError
        break
    except ValueError:
        print('Only positive integers smaller than ',width*height,'!')
Board=createBoard(width,height,n)
numBoard=getNumbers(Board)
XBoard=createXBoard(Board)
V=0
print(XBoard)
count=0
while playing:
    count+=1
    print('Move ',count)
    while True:
        try:
            x=int(input('x-coordinate of your move: '))
            if x<1 or x>width:
                raise ValueError
            break
        except ValueError:
            print('Only positive integers smaller than ',width,'!')
    while True:
        try:
            y=int(input('y-coordinate of your move: '))
            if y<1 or y>height:
                raise ValueError
            break
        except ValueError:
            print('Only positive integers smaller than ',height,'!')
        
    playing,XBoard=uncover(y-1,x-1,numBoard,XBoard,Board)
    
    print(XBoard)
    
    if np.count_nonzero(XBoard.ravel() == ' X ')==n:
        V=1
        playing=False
if V==1:
    print('You win!!!')
else:
    print('You lose :(')
