import time
import pygame
import numpy as np

COLOR_BACKGROUND = (10, 10, 10)#The RGB code for the background.
COLOR_GRID = (40,40,40) #The RGB code for the grid color. Makes it dark grey.
COLOR_DIE_NEXT = (170,70,30) #This is the color you turn if you are going to die in the next round
COLOR_ALIVE_NEXT = (255,255,255) #This is the color you turn if youre alive in the next round.

#This contains the game logic and drawing proccess.
def update(screen,cells,size,with_progress=False):
    updated_cells=np.zeros((cells.shape[0],cells.shape[1]))


#Iterate though the range of
    for row,col in np.ndindex(cells.shape): # Do this action for each Cell.
        #This counts how many of the neighboring cells are alive.
        #This last bit excludes the cell the the iterato is on so that we do not
        #count ourselves.
        alive = np.sum(cells[row-1:row+2, col-1:col+2])-cells[row,col]
        #This line says the variable color is equal to the black background
        #if the cells that is being indexed is equal to 0 (dead) by default.
        #Otherwise the varibale color will be assigened to alive color for the next round.
        color=COLOR_BACKGROUND if cells[row, col] == 0 else COLOR_ALIVE_NEXT

        #THESE ARE THE RULES OF THE GAME:
        if cells[row,col] == 1: #If the cell that is looked at is alive
            if alive < 2 or alive > 3: #and if the cell has only one neighbor or over three neighbors
                if with_progress: #and if with progress is turned on:
                    color = COLOR_DIE_NEXT #The varibale color is set to indicate a death in the next update.
            elif 2<=alive<=3: #However if there are only 2 or 3 neighbors:
                updated_cells[row,col] = 1 #That cells value is set to alive.
                if with_progress: #and if the progress is true:
                    color= COLOR_ALIVE_NEXT #the variable of color is set to indicate that the cell will be alive in the next round

        else: #if the cell was dead.
            if alive==3: # and there were 3 neighboring cells.
                updated_cells[row,col]=1 #The cells value is set to being alive.
                if with_progress: #If there were 3 neighbors and you have progress turned on then
                    #the varible color is set to be alive in the next round
                    color=COLOR_ALIVE_NEXT
        #for whatever row or column your on, draw a rectangle
        pygame.draw.rect(screen,color,(col*size,row*size, size-1,size-1))

    return updated_cells

def main():
    pygame.init() #Initializes the game from pygame
    screen = pygame.display.set_mode((900,600))

    cells= np.zeros((60,90)) #The number of cells
    screen.fill(COLOR_GRID) #Fill the screen with the color of the grid
    update(screen,cells,10)

    pygame.display.flip()
    pygame.display.update()
    running=False

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            elif event.type == pygame.KEYDOWN:
                if event.key==pygame.K_SPACE:
                    running = not running
                    update(screen,cells, 10)
                    pygame.display.update()
            if pygame.mouse.get_pressed()[0]:
                pos=pygame.mouse.get_pos()
                cells[pos[1]//10,pos[0]//10]=1
                update(screen,cells,10)
                pygame.display.update()
        screen.fill(COLOR_GRID)

        if running:
            cells = update(screen,cells, 10, with_progress=True)
            pygame.display.update()

        time.sleep(0.0001)

if __name__ == '__main__':
    main()
