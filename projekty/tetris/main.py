# Tetris in Pygame

# Imports
import pygame
import random
import sys

pygame.init()
pygame.init()

pygame.key.set_repeat(200, 80)

# Constant Variables
WIDHT, HEIGHT = 300, 500
FPS = 60
CELL = 20
ROWS = (HEIGHT - 120) // CELL
COLS = WIDHT // CELL

# Game Settings - screen, clock, title
SCREEN = pygame.display.set_mode((WIDHT, HEIGHT), pygame.NOFRAME)
clock = pygame.time.Clock()
pygame.display.set_caption("Tetris")


# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BG_COLOR = (31, 25, 76)
GRID = (31, 25, 132)
GHOST_GRID = (81, 75, 182)
WIN = (50, 230, 50)
LOSE = (252, 91, 122)

# Load  / Store imiges

ASSETS = {
    1: pygame.image.load("Assets/1.png"),
    2: pygame.image.load("Assets/2.png"),
    3: pygame.image.load("Assets/3.png"),
    4: pygame.image.load("Assets/4.png")
}

# Fonts
font = pygame.font.SysFont("verdana", 50)
font2 = pygame.font.SysFont("verdana", 15)


# Shape Class
class Shape:

    VERSION = {
        'I': [[1, 5, 9, 13], [4, 5, 6, 7]],
        'Z': [[4, 5, 9, 10], [2, 6, 5, 9]],
        'S': [[6, 7, 9, 10], [1, 5, 6, 10]],
        'L': [[1, 2, 5, 9], [0, 4, 5, 6], [1, 5, 9, 8], [4, 5, 6, 10]],
        'J': [[1, 2, 6, 10], [5, 6, 7, 9], [2, 6, 10, 11], [3, 5, 6, 7]],
        'T': [[1, 4, 5, 6], [1, 4, 5, 9], [4, 5, 6, 9], [1, 5, 6, 9]],
        'O': [[1, 2, 5, 6]]

    }
        
    SHAPES = ['I', 'Z', 'S', 'L', 'J', 'T', 'O' ]

    # Constructor
    def __init__(self, x, y):
       self.x = x
       self.y = y
       self.type = random.choice(self.SHAPES)
       self.shape = self.VERSION[self.type]
       self.color = random.randint(1, 4)
       self.orientation = 0

    # Image - Choose correct image
    def image(self):
        return self.shape[self.orientation]

    # Rotate
    def rotate(self):
        self.orientation = (self.orientation + 1) % len(self.shape)



# Game Class
class Tetris:
    # Constructor
    def __init__(self, rows, cols):
       self.rows = rows
       self.cols = cols
       self.score = 1000
       self.level = 1
       self.next = None
       self.end = False
       self.grid = [[0 for j in range(cols)] for i in range(rows)]
       self.new_shape()
 
    # Make Grid
    def make_grid(self):
        for i in range(self.rows+1):
            pygame.draw.line(SCREEN, GRID, (0, CELL*i), (WIDHT, CELL*i))
        for j in range(self.cols+1):
            pygame.draw.line(SCREEN, GRID, (CELL*j, 0), (CELL*j, HEIGHT-120))


    # Make new Shape
    def new_shape(self):
        if not self.next:
            self.next = Shape(5, 0)
        self.figure = self.next
        self.next = Shape(5, 0)


    # Collisions
    def collision(self):
        for i in range(4):
            for j in range(4):
                if (i*4 +j) in self.figure.image():
                    block_row = i + self.figure.y
                    block_col = j + self.figure.x

                    if (block_row >= self.rows or block_col >= self.cols or block_col < 0 or self.grid[block_row][block_col] > 0):
                        return True
        return False            

    # Remove row

    def remove_row(self):
        rerun = False
        
        for y in range(self.rows-1, 0, -1):
            completed = True
            for x in range(0, self.cols):
                if self.grid[y][x] == 0:
                    completed = False
        
            if completed:
                del self.grid[y]
                self.grid.insert(0, [0 for i in range(self.cols)])
                self.score += 1
                if self.score % 10 == 0:
                    self.level += 1
                rerun = True
        
        if rerun:
            self.remove_row()


    # Freeze
    def freeze(self):
        for i in range(4):
            for j in range(4):
                if (i*4 +j) in self.figure.image():
                    self.grid[i+self.figure.y][j+self.figure.x] = self.figure.color

        self.remove_row()
        self.new_shape()
        if self.collision():
            self.end = True

    # Move Down
    def move_down(self):
        self.figure.y += 1
        if self.collision():
            self.figure.y -= 1
            self.freeze()
        
    # Move Left
    def left(self):
        self.figure.x -= 1
        if self.collision():
            self.figure.x += 1

    # Move Right
    def right(self):
        self.figure.x += 1
        if self.collision():
            self.figure.x -= 1

    # Freefall
    def freefall(self):
        while not self.collision():
            self.figure.y += 1
        self.figure.y -= 1
        self.freeze()

    # Rotate
    def rotate(self):
        orientation = self.figure.orientation
        self.figure.rotate()
        if self.collision():
            self.figure.orientation = orientation

    # Ghost Piece
    def get_ghost_y(self):
        original_y = self.figure.y
        while not self.collision():
            self.figure.y += 1
        ghost_y = self.figure.y - 1
        self.figure.y = original_y
        return ghost_y
    
    def end_game(self):
        popup = pygame.Rect(50,140,WIDHT-100, HEIGHT - 350)
        pygame.draw.rect(SCREEN, BLACK, popup)
        pygame.draw.rect(SCREEN, LOSE, popup, 2)
        
        game_over = font2.render("GAME OVER!", True, WHITE)
        option1 = font2.render("Press r to restart", True, LOSE)
        option2 = font2.render("Press q to quit", True, LOSE)
        
        SCREEN.blit(game_over, (popup.centerx-game_over.get_width()/2, popup.y + 20))
        SCREEN.blit(option1, (popup.centerx-option1.get_width()/2, popup.y + 80))
        SCREEN.blit(option2, (popup.centerx-option2.get_width()/2, popup.y + 110))
    



# Main Game Lode
def Main():
    tetris = Tetris(ROWS, COLS)
    run = True
    counter = 0
    move = True
    space_pressed = False



    while run:
        SCREEN.fill(BG_COLOR)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                sys.exit()

            # Event Loop

            keys = pygame.key.get_pressed()
            if not tetris.end:
                if keys[pygame.K_LEFT]:
                    tetris.left()
                elif keys[pygame.K_RIGHT]:
                    tetris.right()
                elif keys[pygame.K_UP]:
                    tetris.rotate()
                elif keys[pygame.K_DOWN]:
                    tetris.move_down()
                elif  keys[pygame.K_SPACE]:
                    space_pressed = True
            if keys[pygame.K_r]:
                tetris.__init__(ROWS, COLS)
            if keys[pygame.K_ESCAPE] or keys[pygame.K_q]:
                run = False 



        counter += 1
        if counter >= 20000:
            counter = 0


        if move:
            if counter % (FPS // (tetris.level*2)) == 0:
                if not tetris.end:
                    if space_pressed:
                        tetris.freefall()
                        space_pressed = False


                    tetris.move_down()

        tetris.make_grid()

        # Keep Fallen Shape on screen
        for x in range(ROWS):
            for y in range(COLS):
                if tetris.grid[x][y] > 0:
                    value = tetris.grid[x][y]
                    image = ASSETS[value]
                    SCREEN.blit(image, (y*CELL, x*CELL))
                    pygame.draw.rect(SCREEN, WHITE, (y*CELL, x*CELL, CELL, CELL), 1)

        if tetris.figure and not tetris.end:
                ghost_y = tetris.get_ghost_y()
                for i in range(4):
                    for j in range(4):
                        if (i * 4 + j) in tetris.figure.image():
                            x = CELL * (tetris.figure.x + j)
                            y = CELL * (ghost_y + i)
                            # Vykreslí jemný šedý obrys dopadu
                            pygame.draw.rect(SCREEN, GHOST_GRID, (x, y, CELL, CELL), 1)

        # show Shape on Game Screen
        if tetris.figure:
            for i in range(4):
                for j in range(4):
                    if (i *4 + j) in tetris.figure.image():
                        shape = ASSETS[tetris.figure.color]
                        x = CELL * (tetris.figure.x + j)
                        y = CELL * (tetris.figure.y + i)
                        SCREEN.blit(shape, (x, y))
                        pygame.draw.rect(SCREEN, WHITE, (x, y, CELL, CELL), 1 )



        # Control Panel
        if tetris.next:
            for i in range(4):
                for j in range(4):
                    if (i *4 + j) in tetris.next.image():
                        image = ASSETS[tetris.next.color]
                        x = CELL * (tetris.next.x + j -4)
                        y = HEIGHT -100 + CELL * (tetris.next.y +i)
                        SCREEN.blit(image,(x,y))

        if tetris.end:
            tetris.end_game()
            # end the game

        
        score_text = font.render(f"{tetris.score}",True, WHITE)
        level_text = font2.render(f"level: {tetris.level}",True, WHITE)
        SCREEN.blit(score_text,(250-score_text.get_width()//2, HEIGHT-110))
        SCREEN.blit(level_text,(250-level_text.get_width()//2, HEIGHT-30))
        


        pygame.display.update()
        clock.tick(FPS)



if __name__ == "__main__":
    Main()