from copy import copy, deepcopy
import time
import _thread
import pygame
pygame.font.init()

flag=0 #flag for assumption validation

cstate=[] #current assuption for rendering

count1=0 #assumption counter to print results once in a while
'''
Solution from the net to compare
'''
def solve(bo):
    """
    Solves a sudoku board using backtracking
    :param bo: 2d list of ints
    :return: solution
    """
    find = find_empty(bo)
    if find:
        row, col = find
    else:
        return True

    for i in range(1,10):
        if valid(bo, (row, col), i):
            bo[row][col] = i

            if solve(bo):
                return True

            bo[row][col] = 0

    return False


def valid(bo, pos, num):
    """
    Returns if the attempted move is valid
    :param bo: 2d list of ints
    :param pos: (row, col)
    :param num: int
    :return: bool
    """

    # Check row
    for i in range(0, len(bo)):
        if bo[pos[0]][i] == num and pos[1] != i:
            return False

    # Check Col
    for i in range(0, len(bo)):
        if bo[i][pos[1]] == num and pos[1] != i:
            return False

    # Check box

    box_x = pos[1]//3
    box_y = pos[0]//3

    for i in range(box_y*3, box_y*3 + 3):
        for j in range(box_x*3, box_x*3 + 3):
            if bo[i][j] == num and (i,j) != pos:
                return False

    return True


def find_empty(bo):
    """
    finds an empty space in the board
    :param bo: partially complete board
    :return: (int, int) row col
    """

    for i in range(len(bo)):
        for j in range(len(bo[0])):
            if bo[i][j] == 0:
                return (i, j)

    return None


def print_board(bo):
    """
    prints the board
    :param bo: 2d List of ints
    :return: None
    """
    for i in range(len(bo)):
        if i % 3 == 0 and i != 0:
            print("- - - - - - - - - - - - - -")
        for j in range(len(bo[0])):
            if j % 3 == 0:
                print(" | ",end="")

            if j == 8:
                print(bo[i][j], end="\n")
            else:
                print(str(bo[i][j]) + " ", end="")


'''
visualisation
'''
class table(pygame.sprite.Sprite):
    def __init__(self,win):
        
        pygame.sprite.Sprite.__init__(self)
        fnt = pygame.font.SysFont("comicsans", 40)
        self.image = pygame.Surface((450, 450))
        self.image.fill((0, 255, 0))
        self.rect = self.image.get_rect()
        self.rect.center = (225, 225)
        global cstate
        self.oldstyle=deepcopy(cstate)


    def update(self,win):
        fnt = pygame.font.SysFont("comicsans", 40)
        global cstate
        hstring=''
        #background
        self.image = pygame.Surface((450, 550))
        self.image.fill((210, 210, 210))
        self.rect = self.image.get_rect()
        self.rect.center = (225, 275)
        #numbers
        for i in range(9):
            for j in range(9):
                if len(cstate[i][j])==1:
                    #if number has changed
                    if self.oldstyle[i][j]==cstate[i][j]:
                        text = fnt.render((cstate[i][j]), 1, (0, 0, 0))
                    else:
                        #change color to red
                        text = fnt.render((cstate[i][j]), 1, (255, 0, 0))
                    self.image.blit(text, (18+j*50,15+i*50))
                else:
                    text = fnt.render((' '), 1, (0, 0, 0))
                    self.image.blit(text, (18+j*50,15+i*50))
            #horizontal lines
            pygame.draw.line(self.image,(0,0,0),(0,50+i*50),(450,50+i*50))
            #vertical lines
            pygame.draw.line(self.image,(0,0,0),(50+i*50,0),(50+i*50,450))
        #thick lines
        pygame.draw.line(self.image,(0,0,0),(150,0),(150,450),3)
        pygame.draw.line(self.image,(0,0,0),(300,0),(300,450),3)
        pygame.draw.line(self.image,(0,0,0),(0,150),(450,150),3)
        pygame.draw.line(self.image,(0,0,0),(0,300),(450,300),3)
        pygame.draw.line(self.image,(0,0,0),(0,450),(450,450),3)
        #tips to user
        text = fnt.render(('space to solve'), 1, (0, 0, 0))
        self.image.blit(text, (20,460))
        text = fnt.render(('backspace to exit'), 1, (0, 0, 0))
        self.image.blit(text, (20,490))
        #saving previous render to compare
        self.oldstyle=deepcopy(cstate)


    














def sudobomber(a,n,m):
    global flag
    k=a[n][m]
    #if guessed the number
    if len(k)==1:
        for i in range(9):
            if i!=m:
                if k in a[n][i]:
                    #delete this number from possible numbers in the same column
                    a[n][i]=a[n][i][0:a[n][i].index(k)]+a[n][i][a[n][i].index(k)+1:len(a[n][i])]
                    if len(a[n][i])==0:
                        #if have 0 possible numbers then  stop
                        flag=1
                        return

                    if len(a[n][i])==1:
                        #if guessed the number start chain reaction
                        sudobomber(a,n,i)
        for i in range(9):
            if i!=n:
                if k in a[i][m]:
                    #delete this number from possible numbers in the same row  
                    a[i][m]=a[i][m][0:a[i][m].index(k)]+a[i][m][a[i][m].index(k)+1:len(a[i][m])]
                    if len(a[i][m])==0:
                        #if  have 0 possible numbers then  stop
                        flag=1
                        return

                    if len(a[i][m])==1:
                        #if  guessed the number start chain reaction
                        sudobomber(a,i,m)
        tx=n//3
        ty=m//3
        for i in range(tx*3,(tx+1)*3):
            for j in range(ty*3,(ty+1)*3):
                if i!=n or j!=m:
                    if k in a[i][j]:
                        #delete this number from possible numbers in the same 3x3 square
                        a[i][j]=a[i][j][0:a[i][j].index(k)]+a[i][j][a[i][j].index(k)+1:len(a[i][j])]
                        if len(a[i][j])==0:
                            #if  have 0 possible numbers then stop
                            flag=1
                            return

                        if len(a[i][j])==1:
                            #if guessed the number start chain reaction
                            sudobomber(a,i,j)
        #trust=1
        for i in range(9):
            for letter in '123456789':
                sum=0
                #check row if the number is possible in single space only
                for j in range(9): 
                    if letter in a[i][j]:
                        sum+=1

                if sum==0:
                    #if have 0 possible numbers then stop
                    flag=1
                    return

                if sum==1:
                    for j in range(9):
                         if letter in a[i][j] and len(a[i][j])>1:
                             #if guessed the number start chain reaction
                             a[i][j]=letter
                             sudobomber(a,i,j)

        for i in range(9):
            #check column if the number is possible in single space only
            for letter in '123456789':
                sum=0
                for j in range(9): 
                    if letter in a[j][i]:
                        sum+=1
                if sum==0:
                    #if have 0 possible numbers then stop
                    flag=1
                    return

                if sum==1:
                    for j in range(9):
                         if letter in a[j][i] and len(a[j][i])>1:
                             #if guessed the number start chain reaction
                             a[j][i]=letter
                             sudobomber(a,j,i)

        for tx in range(3):
            for ty in range(3):
                #check 3x3 square if the number is possible in single space only
                for letter in '123456789':
                    sum=0
                    for i in range(tx*3,(tx+1)*3):
                        for j in range(ty*3,(ty+1)*3):
                            if letter in a[j][i]:
                                sum+=1
                    if sum==0:
                        #if have 0 possible numbers then stop
                        flag=1
                        return

                    if sum==1:
                        for i in range(tx*3,(tx+1)*3):
                            for j in range(ty*3,(ty+1)*3):
                                if letter in a[j][i] and len(a[j][i])>1:
                                    #if guessed the number start chain reaction
                                    a[j][i]=letter
                                    sudobomber(a,j,i)    

                
                    
                
                                   


#if have have multiple options after chain reaction
def assumpt(a,n,m,deep):
    global flag
    global cstate
    #time.sleep(0.5)
    #save current state for rendering
    cstate=deepcopy(a)
    k=a[n][m]
    #save current options for assumption
    t=k
    point1=0
    for i in k:
        #deepcopy a so we dont mess with our starting material
        assumption=deepcopy(a)
        assumption[n][m]=i
        #assuming our assumption is valid
        flag=0
        #code for debugging
        #print('assumpting a ',n,m," is ",i, " deep is ", deep)
        #starting chain reaction in assumption
        sudobomber(assumption,n,m)
        #if it is legit
        if flag==0:
            test=0
            for y in range(9):
                for j in range(9): 
                    if len(assumption[y][j])==2:
                        #check if still have multiple options, if true, make next level assumtion  
                        assumption=assumpt(assumption,y,j,deep+1)
                        #if all deeper assumption failed, delete current assumption from possible options
                        if flag==1:
                            a[n][m]=a[n][m][0:a[n][m].index(i)]+a[n][m][a[n][m].index(i)+1:len(a[n][m])]
                            test=1

                            break
                        #if have succeeded then stop, printing in the end
                        else:
                            a=deepcopy(assumption)
                            if deep==0:
                                for i in range(9):
                                    print(cstate[i])
                            return assumption
                             
                if flag==1:
                    #if current assumption failed, delete it from possible assumptions
                    flag=0
                    t=t[0:t.index(i)]+t[t.index(i)+1:len(t)]
                    break
            #since we go from left top corner to right bottom one,  may have new 2-way options after chain reactions, 
            # in this case return this assumption as posssible
            if test==0:
                a=deepcopy(assumption)
                if flag==0:
                    cstate=deepcopy(a)
                    return a
                    
        
        else:
            #print("assumption failed")
            #if current assumption failed, delete it from possible assumptions
            t=t[0:t.index(i)]+t[t.index(i)+1:len(t)]
            flag=0
        if point1==1:
            break
    #if current assumption has no possible options, return it with flag=1 as incorrect assumtion
    if len(t)==0:
        flag=1
        '''
        debugging output to check if we are in infinite loop
        global count1
        count1+=1
        if count1%82==0:
            print("assumption failed, deep is ", deep)
        if deep<10 or deep>33:
            print("assumption failed, deep is ", deep)
            time.sleep(0.5)
            '''
    return a
        
        


    

#easy sudoky, solvable by chain reaction only
a=[
[5,3,0,0,7,0,0,0,0],
[6,0,0,1,9,5,0,0,0],
[0,9,8,0,0,0,0,6,0],
[8,0,0,0,6,0,0,0,3],
[4,0,0,8,0,3,0,0,1],
[7,0,0,0,2,0,0,0,6],
[0,6,0,0,0,0,2,8,0],
[0,0,0,4,1,9,0,0,5],
[0,0,0,0,8,0,0,7,9] ]

#hard sudoku, solvable with assumptions
a1=[
[8,0,0,0,0,0,0,0,0],
[0,0,3,6,0,0,0,0,0],
[0,7,0,0,9,0,2,0,0],
[0,5,0,0,0,7,0,0,0],
[0,0,0,0,4,5,7,0,0],
[0,0,0,1,0,0,0,3,0],
[0,0,1,0,0,0,0,6,8],
[0,0,8,5,0,0,0,1,0],
[0,9,0,0,0,0,4,0,0] ]

#dummy 9x9 lists
b=[
[5,3,0,0,7,0,0,0,0],
[6,0,0,1,9,5,0,0,0],
[0,9,8,0,0,0,0,6,0],
[8,0,0,0,6,0,0,0,3],
[4,0,0,8,0,3,0,0,1],
[7,0,0,0,2,0,0,0,6],
[0,6,0,0,0,0,2,8,0],
[0,0,0,4,1,9,0,0,5],
[0,0,0,0,8,0,0,7,9] ]

b1=[
[5,3,0,0,7,0,0,0,0],
[6,0,0,1,9,5,0,0,0],
[0,9,8,0,0,0,0,6,0],
[8,0,0,0,6,0,0,0,3],
[4,0,0,8,0,3,0,0,1],
[7,0,0,0,2,0,0,0,6],
[0,6,0,0,0,0,2,8,0],
[0,0,0,4,1,9,0,0,5],
[0,0,0,0,8,0,0,7,9] ]

#converting sudoku to "possibilities" format
for i in range(9):
    for j in range(9):
        if a1[i][j]==0:
            b[i][j]='123456789'
        else:
            b[i][j]=str(a1[i][j])

#saving it for the render
cstate=deepcopy(b)
#converting sudoku to "possibilities" format
for i in range(9):
    for j in range(9):
        if a[i][j]==0:
            b1[i][j]='123456789'
        else:
            b1[i][j]=str(a[i][j])

#rendering window
pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((450, 550))
pygame.display.set_caption("Sudoku")
clock = pygame.time.Clock()
all_sprites = pygame.sprite.Group()
all_sprites.add(table(screen))


running = True



#solving easy sudoku by chain reaction only
for i in range(9):
    for j in range(9):
        sudobomber(b1,i,j)
for i in range(9):
    print(b1[i])

#algoritm effectivness check
#t1_start = time.perf_counter()

#solving hard sudoku by chain reaction only
for i in range(9):
    for j in range(9):
        sudobomber(b,i,j)

#saving it for the render        
cstate=deepcopy(b)

'''
built in start 

for i in range(9):
    for j in range(9):
        if len(b[i][j])==2:
            _thread.start_new_thread(assumpt,(b,i,j,0,))
            #b=assumpt(b,i,j,0)
            break
'''
'''
algoritm effectivness check

t1_stop = time.perf_counter()
print(t1_stop-t1_start,"\n")
t1_start = time.perf_counter()
#solve(a1)
print("solution from the net:\n")
for kol in range(9):
    print(a1[kol])
t1_stop = time.perf_counter()
print(t1_stop-t1_start,"\n")
'''
#flag if started solving to prevent multiple threads
started=0

while running:
    # low fps so can see some steps
    clock.tick(2)

    for event in pygame.event.get():
        # check for closing window
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            for i in range(9):
                for j in range(9):
                    if len(b[i][j])==2:
                        if started==0:
                            #if sudoku is not solved by chain reaction, start solving it by assumtions in a new thread
                            started=1
                            _thread.start_new_thread(assumpt,(b,i,j,0,))
                            #b=assumpt(b,i,j,0)
                            break
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_BACKSPACE:
            #backspace for exit
            running = False

            
       
    

    #pygame render update    
    all_sprites.update(screen)

    screen.fill((255, 255, 255))
    all_sprites.draw(screen)
    pygame.display.flip()

pygame.quit()

#before  exit, print solution
for i in range(9):
    print(cstate[i])



