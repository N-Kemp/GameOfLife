import pygame
import random

width, height = 700, 700

white = (255, 255, 255)
black = (0, 0, 0)

# Game goes crazy fast without a tick counter
clock = pygame.time.Clock()

screen = pygame.display.set_mode((width, height))

# Class used to share list of cell states.
class Conway():
    def __init__(self):
        self.resolution = 5 # This controls the size of the cells and the rows and columns in the array
        self.col = int(width/self.resolution) # Number of columns
        self.row = int(height/self.resolution) # Number of rows
        self.value_grid = [[0 for x in range(self.col)] for y in range(self.row)] # Generates an array with dimensions col,row. Fills them with '0'

    def generate_grid(self):
        # Loops through each index of value_grid and randomly places 1's
        for n in range(self.col):
            for m in range(self.row):
                # This confines the placing of 1's to the center of the array just to start with a smaller generations.
                # Remove this and the whole array will be populated randomly with 1's and things get chaotic.
                if n > self.col / 3 and n < self.col / 2 and m > self.row / 3 and m < self.row / 2:
                    self.value_grid[n][m] = random.randint(0,1)
                

    def grid(self):
        # This method draws the squares with their respective colour values.
        for i in range(self.col):
            for j in range(self.row):
                if self.value_grid[i][j] == 1:
                    pygame.draw.rect(screen, white, (i*self.resolution, j*self.resolution, self.resolution, self.resolution))
        
    def check_neighbours(self,next_grid,x,y):
        #Checking all neighbours around the current cell to see if they're alive or dead.
        #We only really care if they are alive so we count those with 'value_sum'.
        #Since we using 1's and 0's for cell values we just add the cell value/state and it ends up giving the count of live cells.
        value_sum = 0
        for i in range(-1,2):
            for j in range(-1,2):
                if i==0 and j==0:
                    continue
                else:
                    value_sum += next_grid[x+i][y+j]
        value_sum -= next_grid[x][y]
        return value_sum

    def game_of_life(self):
        # For this method we need a duplicate array so that the next generation is calculated based on the old gen. and there are no issues arising from having the previous cells value changed while we still calculate with the older gen.
        next_grid = []
        next_grid = self.value_grid
        state = 0 # This is the value of the index points in the array. 1=alive 0=dead
        for x in range(self.col-1):
            for y in range(self.row-1):   
                    state = self.value_grid[x][y]
                    if (x == 0 or x == width or y == 0 or y == height): # This ignores all edge values
                        next_grid[x][y] = state
                        continue
                    else:
                        value_sum = self.check_neighbours(self.value_grid,x,y)
                        if next_grid[x][y] == 0 and value_sum == 3:                       # Life by reproduction
                            next_grid[x][y] = 1
                        elif next_grid[x][y] == 1 and (value_sum == 2 or value_sum == 3): # Sastained life
                            next_grid[x][y] = 1
                        elif (next_grid[x][y] == 1 and (value_sum < 2 or value_sum > 3)): # Death by underpopulation or overpopulation
                            next_grid[x][y] = 0
                        else: next_grid[x][y] = state
        self.value_grid = next_grid


pygame.init()
running = True

game = Conway()
game.generate_grid()

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill(black)

    game.grid()
    game.game_of_life()

    pygame.display.update()

    clock.tick(30)

pygame.quit()