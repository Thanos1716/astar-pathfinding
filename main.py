#!/usr/bin/env python
import pygame
import random
pygame.init()


def calcGCost(y, x, j, i):
    if abs(j) + abs(i) == 2:
        return board[y][x][4] + 14
    else:
        return board[y][x][4] + 10


def calcHCost(y, x, j, i):
    return max([abs(y + j - end[0]), abs(x + i - end[1])]) * 10 + \
        min([abs(y + j - end[0]), abs(x + i - end[1])]) * 4


def calcFCost(y, x, j, i):
    gCost = calcGCost(y, x, j, i)
    hCost = calcHCost(y, x, j, i)
    board[y + j][x + i][4] = gCost
    board[y + j][x + i][5] = hCost
    print(gCost, hCost)
    return gCost + hCost


def generate():
    for y in range(cellCountVertical):
        for x in range(cellCountHorizontal):
            board[y][x][0] = random.choice(
                [True, False])

            board[y][x][1] = [0, 0]
            board[y][x][2] = float("inf")
            board[y][x][3] = 0
            board[y][x][4] = float("inf")
            board[y][x][5] = float("inf")

    start = (0, 0)
    end = start
    while start == end:
        start = (random.randint(0, cellCountVertical - 1),
                 random.randint(0, cellCountHorizontal - 1))
        end = (random.randint(0, cellCountVertical - 1),
               random.randint(0, cellCountHorizontal - 1))

        board[start[0]][start[1]][0] = False
        board[end[0]][end[1]][0] = False

    return (start, end)


def drawBoard(start, end, position, running):
    for y in range(cellCountVertical):
        for x in range(cellCountHorizontal):
            if board[y][x][0]:
                colour = (0, 0, 0)
            elif board[y][x][3] == 0:
                colour = (40, 40, 40)
            elif board[y][x][3] == 1:
                colour = (0, 0, 128)
            else:
                colour = (128, 0, 128)
            pygame.draw.rect(win, (colour), (x * (cellWidth + cellPadding) + cellPadding, y * (
                cellHeight + cellPadding) + cellPadding, cellWidth, cellHeight))

    if position == end:
        running = False
        while position != start:
            pygame.draw.rect(win, (100, 100, 0), (position[1] * (cellWidth + cellPadding) + cellPadding, position[0] * (
                cellHeight + cellPadding) + cellPadding, cellWidth, cellHeight))
            position = (position[0] + board[position[0]][position[1]][1]
                        [0], position[1] + board[position[0]][position[1]][1][1])

        position = end

    pygame.draw.rect(win, (0, 100, 0), (start[1] * (cellWidth + cellPadding) + cellPadding, start[0] * (
        cellHeight + cellPadding) + cellPadding, cellWidth, cellHeight))
    pygame.draw.rect(win, (100, 0, 0), (end[1] * (cellWidth + cellPadding) + cellPadding, end[0] * (
        cellHeight + cellPadding) + cellPadding, cellWidth, cellHeight))

    if text:
        for y in range(cellCountVertical):
            for x in range(cellCountHorizontal):
                img = font.render(
                    f"{board[y][x][2]} : {board[y][x][4]} : {board[y][x][5]}", True, (255, 255, 255))
                win.blit(img, (x * (cellWidth + cellPadding) + cellPadding, y * (
                    cellHeight + cellPadding) + cellPadding))

    return running


def findBestCell():
    best = position
    for y in range(cellCountVertical):
        for x in range(cellCountHorizontal):
            if (board[y][x][2] < board[best[0]][best[1]][2] and board[y][x][3] == 1) or (board[best[0]][best[1]][3] == 2 and board[y][x][3] == 1):
                best = (y, x)
            elif board[y][x][2] == board[best[0]][best[1]][2] and board[y][x][3] == 1:
                if board[y][x][5] < board[best[0]][best[1]][5]:
                    best = (y, x)

    return best


cellWidth = 40
cellHeight = cellWidth
cellCountVertical = 15
cellCountHorizontal = 15
cellPadding = 1
screenWidth = (cellWidth + cellPadding) * cellCountHorizontal + cellPadding
screenHeight = (cellHeight + cellPadding) * cellCountVertical + cellPadding


win = pygame.display.set_mode((screenWidth, screenHeight))
pygame.display.set_caption("A* Pathfinding")

board = []
for y in range(cellCountVertical):
    board.append([])
    for x in range(cellCountHorizontal):
        board[y].append([])
        board[y][x].append(False)  # Wall or not wall
        # Direction of previous cell on path, [0, 0] means no direction
        board[y][x].append([0, 0])
        board[y][x].append(float("inf"))  # F-cost (G-cost + H-cost)
        # State (unchecked = 0, f-checked = 1, exhausted = 2)
        board[y][x].append(0)
        board[y][x].append(float("inf"))  # G-cost (direct distance from start)
        board[y][x].append(float("inf"))  # H-cost (direct distance to end)


running = True
windowShouldClose = False
rPressed = False
tPressed = False
spacePressed = False
text = False
font = False
mode = False

start, end = generate()
position = start
board[start[0]][start[1]][4] = 0

while not windowShouldClose:
    pygame.time.delay(0)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            windowShouldClose = True

        if event.type == pygame.MOUSEBUTTONDOWN:
            mode = pygame.mouse.get_pos()

    keys = pygame.key.get_pressed()

    if keys[pygame.K_ESCAPE]:
        windowShouldClose = True

    if keys[pygame.K_r]:
        if not rPressed:
            start, end = generate()
            running = True
            position = start
            board[start[0]][start[1]][4] = 0
            rPressed = True
    else:
        rPressed = False

    if keys[pygame.K_SPACE]:
        if not spacePressed:
            running = not running
            spacePressed = True
    else:
        spacePressed = False

    if keys[pygame.K_t]:
        if not tPressed:
            tPressed = True
            text = not text
            if not font:
                font = pygame.font.SysFont("arialunicode.ttf", 8)
    else:
        tPressed = False

    if running:
        for j in range(-1, 2):
            for i in range(-1, 2):
                if 0 <= position[0] + j < cellCountVertical and 0 <= position[1] + i < cellCountHorizontal and not (j == 0 and i == 0):
                    newGCost = calcGCost(position[0], position[1], j, i)
                    newHCost = calcHCost(position[0], position[1], j, i)
                    newFCost = newGCost + newHCost

                    if not board[position[0] + j][position[1] + i][0] and board[position[0] + j][position[1] + i][2] > newFCost and not board[position[0] + j][position[1] + i][3] == 2:
                        board[position[0] + j][position[1] + i][1] = (-j, -i)
                        board[position[0] + j][position[1] + i][2] = newFCost
                        board[position[0] + j][position[1] + i][3] = 1
                        board[position[0] + j][position[1] + i][4] = newGCost
                        board[position[0] + j][position[1] + i][5] = newHCost

        position = findBestCell()
        board[position[0]][position[1]][3] = 2

    win.fill((30, 30, 30))

    running = drawBoard(start, end, position, running)

    pygame.display.update()
pygame.quit()
