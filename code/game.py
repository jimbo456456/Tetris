from settings import *
from random import choice

from timer import Timer

class Game:
    def __init__(self):
        
        # general
        # creates game display
        self.surface = pygame.Surface((GAME_WIDTH, GAME_HEIGHT))
        # gets the display surface from main window
        self.display_surface = pygame.display.get_surface()
        # game border rectangle
        self.rect = self.surface.get_rect(topleft = (PADDING,PADDING))

        self.sprites = pygame.sprite.Group()

        # lines (for lowering opacity)
        self.line_surface = self.surface.copy()
        self.line_surface.fill((0,255,0))
        self.line_surface.set_colorkey((0,255,0))
        self.line_surface.set_alpha(120)

        # test
        self.tetromino = Tetromino(choice(list(TETROMINOS.keys())), self.sprites)

        # timer
        self.timers = {
            'vertical move': Timer(UPDATE_START_SPEED, True, self.move_down)
        }
        self.timers['vertical move'].activate()

    def timer_update(self):
        for timer in self.timers.values():
            timer.update()

    def move_down(self):
        #print('timer')
        self.tetromino.move_down()

    # grid (WANT TO GET RID OF THIS AT THE END)
    def draw_grid(self):

        for col in range(1, COLUMNS):
            x = col * CELL_SIZE
            pygame.draw.line(self.line_surface, LINE_COLOR, (x,0), (x,self.surface.get_height()), 1)
        for row in range(1, ROWS):
            y = row * CELL_SIZE
            pygame.draw.line(self.line_surface, LINE_COLOR, (0,y), (self.surface.get_width(),y), 1)

        self.surface.blit(self.line_surface, (0,0))

    def run(self):

        # update
        self.timer_update()
        self.sprites.update()

        # drawing
        self.surface.fill('black')
        self.sprites.draw(self.surface)

        # places grid lines (THIS WILL BE REMOVED AT THE END)
        self.draw_grid()
        # places game surface on display surface
        self.display_surface.blit(self.surface, (PADDING,PADDING))
        # draws border
        pygame.draw.rect(self.display_surface, LINE_COLOR, self.rect, 2, 2)

class Tetromino:
    def __init__(self, shape, group):
        
        # setup
        self.block_positions = TETROMINOS[shape]['shape']
        self.color = TETROMINOS[shape]['color']

        # create blocks in tetromino
        self.blocks = [Block(group, pos, self.color) for pos in self.block_positions]

    def move_down(self):
        for block in self.blocks:
            block.pos.y += 1

class Block(pygame.sprite.Sprite):
    def __init__(self, group, pos, color):
        
        # general
        super().__init__(group)
        self.image = pygame.Surface((CELL_SIZE,CELL_SIZE))
        self.image.fill(color)

        # position
        self.pos = pygame.Vector2(pos) + BLOCK_OFFSET
        self.rect = self.image.get_rect(topleft = self.pos * CELL_SIZE)

    def update(self):
        self.rect.topleft = self.pos * CELL_SIZE