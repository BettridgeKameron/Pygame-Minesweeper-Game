import pygame
import sys
import MineSweeperLogic as Mine
print('''
Hi! Welcome to Minesweeper! 
Left click to uncover a square.
Right click to flag/unflag a square. 
You have as many flags as there are mines.
The number tells you how many mines are around the square! 
Reveal all non-mine squares to win!
Press \"r\" to restart, and \"ESC\" to exit. 
Good Luck!
''')
print("Grid Width? (5 to 40 is recommended.)")
if (blocksX := abs(int(input()))) == 0:
    raise Exception("Please enter a valid number!")
print("Grid Height? (5 to 20 is recommended.)")
if (blocksY := abs(int(input()))) == 0:
    raise Exception("Please enter a valid number!")
blockspX = 45
blockspY = 45
print("Mine Percent? (as a decimal, so .1 for easy, .15 for medium, .2 for hard, or custom.)")
minePercent = abs(float(input()))
if minePercent < 0 or minePercent > 1:
    raise Exception("Please enter a number between 0 and 1!")
flagCount = 0

SCREEN_WIDTH = blocksX*blockspX
SCREEN_HEIGHT = blocksY*blockspY
GREEN = (76, 206, 35)
RED = (200, 0, 0)
GRAY = (85, 85, 85)
TOPGRAY = (130, 130, 130)
BLUE = (15,200,255)
num2 = (156, 208, 32)
num3 = (207, 209, 30)
num4 = (243, 210, 29)
num5 = (246, 178, 37)
num6 = (249, 143, 46)
num7 = (252, 105, 55)
num8 = (255, 65, 65)

clock = pygame.time.Clock()

pygame.init()

sysfont = pygame.font.get_default_font()
font = pygame.font.SysFont(None, blockspX)
num = [font.render("", True, GREEN), font.render("1", True, GREEN), font.render("2", True, num2),
       font.render("3", True, num3), font.render("4", True, num4), font.render("5", True, num5),
       font.render("6", True, num6), font.render("7", True, num7), font.render("8", True, num8)]

surface = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Minesweeper")
surface.fill(GREEN)

logic = Mine.MineSweeperLogic(blocksX, blocksY)
mineCount = min(blocksX*blocksY-1, max(1, round(minePercent*blocksX*blocksY)))

logic.generateMines(logic.grid, mineCount)
logic.generateNums(logic.grid)

win = False
lost = False
firstClick = True

def drawGrid(surface, logic):
    for x in range(blocksX):
        for y in range(blocksY):
            bottomRect = pygame.Rect(x * blockspX, y * blockspY, blockspX, blockspY)
            topRect = pygame.Rect(x * blockspX, y * blockspY, blockspX, blockspY)
            if logic.grid[x + 1][y + 1] == 10:
                if win:
                    color = GREEN
                else:
                    color = RED
                pygame.draw.rect(surface, color, bottomRect)
            else:
                pygame.draw.rect(surface, GRAY, bottomRect)
                if logic.grid[x + 1][y + 1] != 0:
                    surface.blit(num[logic.grid[x + 1][y + 1]], (x * blockspX + 15, y * blockspY + 10))
            if logic.clickGrid[x + 1][y + 1] == 0:
                if logic.flagGrid[x + 1][y + 1] == 0:
                    color = TOPGRAY
                elif win:
                    color = GREEN
                else:
                    color = BLUE
                pygame.draw.rect(surface, color, topRect)


def drawLine(surface):
    for i in range(blocksX):
        new_width = round(i * blockspX)
        pygame.draw.line(surface, (245, 245, 245), (new_width, 0), (new_width, SCREEN_HEIGHT), 2)
    for j in range(blocksY):
        new_height = round(j * blockspY)
        pygame.draw.line(surface, (245, 245, 245), (0, new_height), (SCREEN_WIDTH, new_height), 2)

def clickSquare(x,y):
    if logic.clickGrid[x + 1][y + 1] == 0 and logic.flagGrid[x + 1][y + 1] == 0:
        logic.clickGrid[x + 1][y + 1] = 1
        if logic.grid[x + 1][y + 1] == 0:
            for i in range(-1, 2):
                for j in range(-1, 2):
                    if i == j == 0:
                        continue
                    clickSquare(x+i,y+j)

def checkWin():
    for x in range(blocksX):
        for y in range(blocksY):
            if logic.clickGrid[x + 1][y + 1] == 0 and logic.grid[x + 1][y + 1] != 10:
                break
        else:
            continue
        break
    else:
        print("You won! press \'r\' to try again. or ESC to quit.")
        global win
        win = True
        revealMines()

def revealMines():
    for x in range(blocksX):
        for y in range(blocksY):
            if logic.grid[x + 1][y + 1] == 10:
                clickSquare(x,y)

while True:
    pos = pygame.mouse.get_pos()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            row = int(pos[0] // (SCREEN_WIDTH / blocksX))
            column = int(pos[1] // (SCREEN_HEIGHT / blocksY))
            if event.button == 1:
                if firstClick and logic.flagGrid[row + 1][column + 1] == 0:
                    firstClick = False
                    if logic.grid[row + 1][column + 1] == 10:
                        logic.grid[row + 1][column + 1] = 0
                        for x in range(blocksX):
                            for y in range(blocksY):
                                if logic.grid[x + 1][y + 1] != 10 and not(row == x and column == y):
                                    logic.grid[x + 1][y + 1] = 10
                                    logic.generateNums(logic.grid)
                                    break
                            else:
                                continue
                            break
                if not lost and not win:
                    clickSquare(row,column)
                    checkWin()
                if logic.grid[row + 1][column + 1] == 10 and logic.flagGrid[row + 1][column + 1] == 0 and not lost and not win:
                    lost = True
                    revealMines()
                    print("You lost! press \'r\' to try again. or ESC to quit.")
            elif event.button == 3:
                if not lost and not win and flagCount <= mineCount and logic.clickGrid[row + 1][column + 1] == 0:
                    if flagCount != mineCount or logic.flagGrid[row + 1][column + 1] == 1:
                        flagCount = flagCount + 1 if logic.flagGrid[row + 1][column + 1] == 0 else flagCount - 1
                        print("You have {} flags left and have used {} flags.".format(mineCount - flagCount, flagCount))
                        logic.flagGrid[row + 1][column + 1] = 1 if logic.flagGrid[row + 1][column + 1] == 0 else 0
                    else:
                        print("You have no more flags! Unflag existing flags to get more.\nYou can also click all unflagged tiles if you think you flagged all mines.")


        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:
                logic = Mine.MineSweeperLogic(blocksX, blocksY)
                mineCount = min(blocksX*blocksY-1, max(1, round(minePercent*blocksX*blocksY)))
                logic.generateMines(logic.grid, mineCount)
                logic.generateNums(logic.grid)
                firstClick = True
                lost = False
                win = False
                flagCount = 0
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit()

    pygame.display.update()
    drawGrid(surface, logic)
    drawLine(surface)
    clock.tick(60)
