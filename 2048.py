import random, pygame, math, webbrowser
from pygame.locals import*

# initialise global variables
running = True
win = False
no_file = True
fail = False
wipe = False
reset = False
help_bol = False
move = None
# initialising Pygame and fonts
pygame.init()
pygame.font.init()

# Setting constants for cursors to be used when hovering over text
DEFAULT_CURSOR = pygame.mouse.get_cursor()
_HAND_CURSOR = (
"     XX         ",
"    X..X        ",
"    X..X        ",
"    X..X        ",
"    X..XXXXX    ",
"    X..X..X.XX  ",
" XX X..X..X.X.X ",
"X..XX.........X ",
"X...X.........X ",
" X.....X.X.X..X ",
"  X....X.X.X..X ",
"  X....X.X.X.X  ",
"   X...X.X.X.X  ",
"    X.......X   ",
"     X....X.X   ",
"     XXXXX XX   ")
_HCURS, _HMASK = pygame.cursors.compile(_HAND_CURSOR, ".", "X")
HAND_CURSOR = ((16, 16), (5, 1), _HCURS, _HMASK)


def winning_check(new_block):
    # Used to check if a user has a block with a value of 2048. If they do then they have won.
    if new_block == 2048 or win:
        return True
    else:
        return False


class Screen:

    def __init__(self):
        # Initialises all of the attributes of the screen
        self.height = 700
        self.width = 765
        self.pygame_screen = pygame.display.set_mode((self.width, self.height))
        self.grid_colour = 170, 175, 183
        self.line_colour = 71, 71, 71
        self.background_colour = 255, 255, 255
        self.text = pygame.font.SysFont('123.oft', 60).render('2048', True, (0, 0, 0))
        self.winning = pygame.font.SysFont('123.oft', 120).render('Winner!', True, (255, 255, 255))
        self.loser = pygame.font.SysFont('123.oft', 120).render('Loser!', True, (255, 255, 255))
        self.help_text = pygame.font.SysFont('123.oft', 30).render('To win match the tiles with the same number',
                                                                   True, (0, 0, 0))
        self.score_font = pygame.font.SysFont('123.oft', 40)
        self.button_font = pygame.font.SysFont('123.oft', 30)
        self.numbers_font = pygame.font.SysFont('123.oft', 30)
        self.block_colours = [(102, 102, 102),
                              (247, 0, 0),
                              (247, 123, 0),
                              (247, 238, 0),
                              (181, 247, 0),
                              (74, 247, 0),
                              (0, 247, 57),
                              (0, 247, 218),
                              (0, 107, 247),
                              (193, 0, 247),
                              (255, 255, 255)]
        self.restart_colour = (170, 175, 183)
        self.wipe_colour = (170, 175, 183)
        self.help_colour = (170, 175, 183)
        self.up_colour = (170, 175, 183)
        self.down_colour = (170, 175, 183)
        self.left_colour = (170, 175, 183)
        self.right_colour = (170, 175, 183)

    def load_screen(self):
        # Displays all items on the screen
        self.pygame_screen.fill(self.background_colour)
        self.pygame_screen.blit(self.text, (250, 10))
        self.pygame_screen.blit(self.score_font.render('Score: ' + str(num.score), True, (0, 0, 0)), (50, 50))
        self.pygame_screen.blit(self.score_font.render('Best: ' + str(num.best), True, (0, 0, 0)), (50, 80))
        self.pygame_screen.blit(self.help_text, (50, 125))
        self.buttons()
        # This displays 'Winner!' when the user has won
        if win:
            pygame.draw.rect(self.pygame_screen, self.line_colour,
                             (50, 150, 500, 500), 0)
            self.pygame_screen.blit(self.winning, (150, 350))
        # This displays 'Loser!' when the user has lost
        elif fail:
            pygame.draw.rect(self.pygame_screen, self.line_colour,
                             (50, 150, 500, 500), 0)
            self.pygame_screen.blit(self.loser, (150, 350))
        # this displays all the blocks on the screen
        else:
            self.draw_grid()
            self.display_numbers()
        pygame.display.flip()

    def draw_grid(self):
        # This draws the grid
        pygame.draw.rect(self.pygame_screen, self.line_colour, (50, 150, 500, 500), 0)
        y = 160 # first line position on the y axis
        while y <= 527.50: # Loops until bottom of grid
            x = 60 # first line on the x axis
            while x <= 427.50: # Loops until it gets to the right of the grid
                pygame.draw.rect(self.pygame_screen, self.grid_colour, (x, y, 112.5, 112.5), 0)
                x += 122.50
            y += 122.50

    def display_numbers(self):
        # Displays the blocks on the grid
        for y in range(0, 4):
            for x in range(0, 4):
                if num.list[y][x]:
                    # use logs to work out the index of the list
                    x_block = (x*112.5+(x+1)*10)+50
                    y_block = (y*112.5+(y+1)*10)+150
                    pygame.draw.rect(self.pygame_screen, self.block_colours[int(math.log(num.list[y][x], 2))-1],
                                     (x_block, y_block, 112.5, 112.5), 0)
                    if num.list[y][x] < 10:
                        self.pygame_screen.blit(self.numbers_font.render(str(num.list[y][x]), True, (0, 0, 0,)),
                                                ((x_block+50), (y_block+45)))
                    elif num.list[y][x] < 100:
                        self.pygame_screen.blit(self.numbers_font.render(str(num.list[y][x]), True, (0, 0, 0,)),
                                                ((x_block + 45), (y_block + 45)))
                    elif num.list[y][x] < 1000:
                        self.pygame_screen.blit(self.numbers_font.render(str(num.list[y][x]), True, (0, 0, 0,)),
                                                ((x_block + 40), (y_block + 45)))
                    else:
                        self.pygame_screen.blit(self.numbers_font.render(str(num.list[y][x]), True, (0, 0, 0,)),
                                                ((x_block + 35), (y_block + 45)))

    def buttons(self):
        # Restart button
        pygame.draw.rect(self.pygame_screen, (71, 71, 71), (450, 30, 100, 70))
        pygame.draw.rect(self.pygame_screen, self.restart_colour, (455, 35, 90, 60))
        self.pygame_screen.blit(self.button_font.render('Restart', True, (0, 0, 0)), (466, 55))

        # Wipe best score
        pygame.draw.rect(self.pygame_screen, (71, 71, 71), (600, 150, 130, 70))
        pygame.draw.rect(self.pygame_screen, self.wipe_colour, (605, 155, 120, 60))
        self.pygame_screen.blit(self.button_font.render('Wipe Best', True, (0, 0, 0)), (616, 175))

        # Help button
        pygame.draw.rect(self.pygame_screen, (71, 71, 71), (600, 30, 130, 70))
        pygame.draw.rect(self.pygame_screen, self.help_colour, (605, 35, 120, 60))
        self.pygame_screen.blit(self.button_font.render('Help', True, (0, 0, 0)), (640, 55))

        # Arrow keys
        pygame.draw.rect(self.pygame_screen, (71, 71, 71), (635, 410, 50, 50))
        pygame.draw.rect(self.pygame_screen, self.up_colour, (640, 415, 40, 40))
        self.pygame_screen.blit(self.button_font.render('UP', True, (0, 0, 0)), (647, 426))

        pygame.draw.rect(self.pygame_screen, (71, 71, 71), (635, 520, 50, 50))
        pygame.draw.rect(self.pygame_screen, self.down_colour, (640, 525, 40, 40))
        self.pygame_screen.blit(self.button_font.render('D', True, (0, 0, 0)), (652, 536))

        pygame.draw.rect(self.pygame_screen, (71, 71, 71), (585, 465, 50, 50))
        pygame.draw.rect(self.pygame_screen, self.left_colour, (590, 470, 40, 40))
        self.pygame_screen.blit(self.button_font.render('L', True, (0, 0, 0)), (605, 480))

        pygame.draw.rect(self.pygame_screen, (71, 71, 71), (685, 465, 50, 50))
        pygame.draw.rect(self.pygame_screen, self.right_colour, (690, 470, 40, 40))
        self.pygame_screen.blit(self.button_font.render('R', True, (0, 0, 0)), (700, 480))



class Numbers:

    def __init__(self):
        # Initialise the numbers class
        self.list = []
        self.number_blocks = 0
        self.score = 0
        self.best = 0

    def move_numbers(self, direction):
        global win
        if not fail and not win:
            if direction == 'UP':
                # Works out how blocks are merged when up arrow key is pressed
                for counter in range(0, 3):
                    for y in range(0, 4):
                        for x in range(0, 4):
                            if self.list[y][x]:
                                if y != 0:
                                    if self.list[y-1][x]:
                                        if y == 1:
                                            if self.list[y-1][x] == self.list[y][x]:
                                                self.list[y-1][x] += self.list[y][x]
                                                win = winning_check(self.list[y-1][x])
                                                self.list[y][x] = None
                                                self.score += self.list[y-1][x]
                                                self.number_blocks -= 1
                                        elif self.list[y-1][x] == self.list[y][x] and \
                                                self.list[y-2][x] != self.list[y-1][x]:
                                            self.list[y-1][x] += self.list[y][x]
                                            win = winning_check(self.list[y-1][x])
                                            self.score += self.list[y-1][x]
                                            self.list[y][x] = None
                                            self.number_blocks -= 1

                                    else:
                                        self.list[y-1][x] = self.list[y][x]
                                        self.list[y][x] = None

            elif direction == 'DOWN':
                # Works out how blocks are merged when down arrow key is pressed
                for counter in range(0, 3):
                    for y in range(3, -1, -1):
                        for x in range(0, 4):
                            if self.list[y][x]:
                                if y != 3:
                                    if self.list[y+1][x]:
                                        try:
                                            if self.list[y+1][x] == self.list[y][x] and \
                                                            self.list[y+2][x] != self.list[y+1][x]:
                                                self.list[y+1][x] += self.list[y][x]
                                                win = winning_check(self.list[y+1][x])
                                                self.list[y][x] = None
                                                self.score += self.list[y+1][x]
                                                self.number_blocks -= 1
                                        except IndexError:
                                            if self.list[y+1][x] == self.list[y][x]:
                                                self.list[y+1][x] += self.list[y][x]
                                                win = winning_check(self.list[y+1][x])
                                                self.list[y][x] = None
                                                self.score += self.list[y+1][x]
                                                self.number_blocks -= 1
                                    else:
                                        self.list[y+1][x] = self.list[y][x]
                                        self.list[y][x] = None

            elif direction == 'LEFT':
                # Works out how blocks are merged when left arrow key is pressed
                for counter in range(0, 3):
                    for y in range(0, 4):
                        for x in range(3, -1, -1):
                            if self.list[y][x]:
                                if x != 0:
                                    if self.list[y][x-1]:
                                        if x == 1:
                                            if self.list[y][x-1] == self.list[y][x]:
                                                self.list[y][x-1] += self.list[y][x]
                                                win = winning_check(self.list[y][x-1])
                                                self.list[y][x] = None
                                                self.score += self.list[y][x-1]
                                                self.number_blocks -= 1
                                        elif self.list[y][x-1] == self.list[y][x] and \
                                                self.list[y][x-2] != self.list[y][x-1]:
                                            self.list[y][x-1] += self.list[y][x]
                                            win = winning_check(self.list[y][x-1])
                                            self.list[y][x] = None
                                            self.score += self.list[y][x-1]
                                            self.number_blocks -= 1

                                    else:
                                        self.list[y][x-1] = self.list[y][x]
                                        self.list[y][x] = None

            elif direction == 'RIGHT':
                # Works out how blocks are merged when right arrow key is pressed
                for counter in range(0, 3):
                    for y in range(0, 4):
                        for x in range(0, 4):
                            if self.list[y][x]:
                                if x != 3:
                                    if self.list[y][x+1]:
                                        try:
                                            if self.list[y][x+1] == self.list[y][x] and \
                                                            self.list[y][x+2] != self.list[y][x+1]:
                                                self.list[y][x+1] += self.list[y][x]
                                                win = winning_check(self.list[y][x+1])
                                                self.list[y][x] = None
                                                self.score += self.list[y][x+1]
                                                self.number_blocks -= 1
                                        except IndexError:
                                            if self.list[y][x+1] == self.list[y][x]:
                                                self.list[y][x+1] += self.list[y][x]
                                                self.score += self.list[y][x+1]
                                                win = winning_check(self.list[y][x+1])
                                                self.list[y][x] = None
                                                self.number_blocks -= 1
                                    else:
                                        self.list[y][x+1] = self.list[y][x]
                                        self.list[y][x] = None
            self.add_block()

    def reset(self):
        # Resets all of the blocks to nothing
        self.list = [[None, None, None, None],
                     [None, None, None, None],
                     [None, None, None, None],
                     [None, None, None, None]]
        # If the current score is bigger than the best score the best score is over written
        if self.score > self.best:
            self.best = self.score

    def starting(self):
        global fail
        global win
        win = False
        fail = False
        # Sets up the starting grid
        self.reset()
        self.add_block()
        self.add_block()
        self.score = 0

    def add_block(self):
        #adds a new block
        global running
        global fail
        if self.number_blocks == 16:
            fail = True
        else:
            x = random.randint(0, 3)
            y = random.randint(0, 3)
            while self.list[x][y]:
                x = random.randint(0, 3)
                y = random.randint(0, 3)
            self.list[x][y] = 2
            self.number_blocks += 1


num = Numbers()  # Instantiate the numbers
main_game = Screen()  # Instantiates the screen
num.starting()

# If no file for best score one is created
while no_file:
    try:
        file = open('score.dat')
        no_file = False
    except IOError:
        file = open('score.dat', 'w')
        file.write('0')
        file.close()
# Best is read from file
num.best = int(file.read())
file.close()

while running:

    mouse_pos = pygame.mouse.get_pos()
    # if mouse in box then reset button colour changes and mouse cursor is a hand
    if 450 <= mouse_pos[0] and mouse_pos[0] <= 550 and 30 <= mouse_pos[1] and mouse_pos[1] <= 100:
        # Checks to see if mouse is in the reset box
        pygame.mouse.set_cursor(*HAND_CURSOR)
        main_game.restart_colour = (204, 204, 204)
        reset = True

    elif 600 <= mouse_pos[0] and mouse_pos[0] <= 730 and 150 <= mouse_pos[1] and mouse_pos[1] <= 220:
        # Checks if cursor in wipe box
        pygame.mouse.set_cursor(*HAND_CURSOR)
        main_game.wipe_colour = (204, 204, 204)
        wipe = True

    elif 600 <= mouse_pos[0] and mouse_pos[0] <= 730 and 30 <= mouse_pos[1] and mouse_pos[1] <= 115:
        # Checks if cursor in help box
        pygame.mouse.set_cursor(*HAND_CURSOR)
        main_game.help_colour = (204, 204, 204)
        help_bol = True

    elif 635 <= mouse_pos[0] and mouse_pos[0] <= 685 and 410 <= mouse_pos[1] and mouse_pos[1] <= 460:
        # Checks if cursor in up box
        pygame.mouse.set_cursor(*HAND_CURSOR)
        main_game.up_colour = (204, 204, 204)
        move = 'UP'

    elif 635 <= mouse_pos[0] and mouse_pos[0] <= 685 and 520 <= mouse_pos[1] and mouse_pos[1] <= 570:
        # Checks if cursor in down box
        pygame.mouse.set_cursor(*HAND_CURSOR)
        main_game.down_colour = (204, 204, 204)
        move = 'DOWN'

    elif 585 <= mouse_pos[0] and mouse_pos[0] <= 635 and 465 <= mouse_pos[1] and mouse_pos[1] <= 515:
        # Checks if cursor in left box
        pygame.mouse.set_cursor(*HAND_CURSOR)
        main_game.left_colour = (204, 204, 204)
        move = "LEFT"

    elif 685 <= mouse_pos[0] and mouse_pos[0] <= 735 and 465 <= mouse_pos[1] and mouse_pos[1] <= 515:
        # Checks if cursor in right box
        pygame.mouse.set_cursor(*HAND_CURSOR)
        main_game.right_colour = (204, 204, 204)
        move = "RIGHT"

    else:
        # if the mouse not in any boxes then set to default
        pygame.mouse.set_cursor(*DEFAULT_CURSOR)
        main_game.restart_colour = (170, 175, 183)
        main_game.wipe_colour = (170, 175, 183)
        main_game.help_colour = (170, 175, 183)
        main_game.up_colour = (170, 175, 183)
        main_game.down_colour = (170, 175, 183)
        main_game.left_colour = (170, 175, 183)
        main_game.right_colour = (170, 175, 183)
        reset = False
        wipe = False
        help_bol = False
        move = None

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False
            print('Exiting game')

        elif event.type == pygame.MOUSEBUTTONUP:

            if reset:
                num.starting()

            elif wipe:
                num.best = 0

            elif help_bol:
                webbrowser.open_new('http://2048game.mobi/howtoplay.htm')

            elif move:
                num.move_numbers(move)

        elif event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                running = False
            elif not win:
                if event.key == K_UP:
                    num.move_numbers('UP')
                elif event.key == K_DOWN:
                    num.move_numbers('DOWN')
                elif event.key == K_LEFT:
                    num.move_numbers('LEFT')
                elif event.key == K_RIGHT:
                    num.move_numbers("RIGHT")

    main_game.load_screen()
# Saves best score out to file
file = open('score.dat', 'w')
file.write(str(num.best))
file.close()
