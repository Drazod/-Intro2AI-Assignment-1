import pygame

pygame.font.init()
pygame.display.set_caption("SUDOKU SOLVER USING HILL CLIMBING")
screen = pygame.display.set_mode((500, 600))

x = 0
y = 0
dif = 500 / 9
val = 0

grid =[
    [7, 8, 0, 4, 0, 0, 1, 2, 0],
    [6, 0, 0, 0, 7, 5, 0, 0, 9],
    [0, 0, 0, 6, 0, 1, 0, 7, 8],
    [0, 0, 7, 0, 4, 0, 2, 6, 0],
    [0, 0, 1, 0, 5, 0, 9, 3, 0],
    [9, 0, 4, 0, 6, 0, 0, 0, 5],
    [0, 7, 0, 3, 0, 0, 0, 1, 2],
    [1, 2, 0, 0, 0, 7, 4, 0, 0],
    [0, 4, 9, 2, 0, 6, 0, 0, 7]
]

font1 = pygame.font.SysFont("comicsans", 40)
font2 = pygame.font.SysFont("comicsans", 20)

def get_cord(pos):
    global x, y
    x = pos[0]//dif
    y = pos[1]//dif

def draw_box():
    for i in range(2):
        pygame.draw.line(screen, (255, 0, 0), (x * dif-3, (y + i)*dif), (x * dif + dif + 3, (y + i)*dif), 7)
        pygame.draw.line(screen, (255, 0, 0), ( (x + i)* dif, y * dif ), ((x + i) * dif, y * dif + dif), 7)

def draw():
    for i in range (9):
        for j in range (9):
            if grid[i][j] != 0:
                pygame.draw.rect(screen, (0, 153, 153), (i * dif, j * dif, dif + 1, dif + 1))
                text1 = font1.render(str(grid[i][j]), 1, (0, 0, 0))
                screen.blit(text1, (i * dif + 15, j * dif + 5))

    for i in range(10):
        if i % 3 == 0 :
            thick = 7
        else:
            thick = 1
        pygame.draw.line(screen, (0, 0, 0), (0, i * dif), (500, i * dif), thick)
        pygame.draw.line(screen, (0, 0, 0), (i * dif, 0), (i * dif, 500), thick)

def draw_val(val):
    text1 = font1.render(str(val), 1, (0, 0, 0))
    screen.blit(text1, (x * dif + 15, y * dif+15))

def raise_error1():
    text1 = font1.render("WRONG !!!", 1, (0, 0, 0))
    screen.blit(text1, (20, 570))

def raise_error2():
    text1 = font1.render("Wrong !!! Not a valid Key", 1, (0, 0, 0))
    screen.blit(text1, (20, 570))

def valid(m, i, j, val):
    for it in range(9):
        if m[i][it] == val:
            return False
        if m[it][j] == val:
            return False
    it = i//3
    jt = j//3
    for i in range(it * 3, it * 3 + 3):
        for j in range (jt * 3, jt * 3 + 3):
            if m[i][j] == val:
                return False
    return True
#!DFS
# def solve(grid, i, j):
#     while grid[i][j] != 0:
#         if i < 8:
#             i += 1
#         elif i == 8 and j < 8:
#             i = 0
#             j += 1
#         elif i == 8 and j == 8:
#             return True

#     pygame.event.pump()
#     for it in range(1, 10):
#         if valid(grid, i, j, it):
#             grid[i][j] = it
#             global x, y
#             x = i
#             y = j
#             screen.fill((255, 255, 255))
#             draw()
#             draw_box()
#             pygame.display.update()
#             pygame.time.delay(20)
#             if solve(grid, i, j):
#                 return True
#             else:
#                 grid[i][j] = 0
#                 screen.fill((255, 255, 255))
#                 draw()
#                 draw_box()
#                 pygame.display.update()
#                 pygame.time.delay(50)
#     return False



#!Hill Climbing combine Backtracking finding Most constraint value

def solve(grid):
    while True:
        conflicts = count_conflicts(grid)
        if conflicts == 0:
            # No conflicts, solution found
            return grid

        # Find the cell with the most conflicts
        max_conflicts = -1
        max_conflict_cell = None
        for i in range(9):
            for j in range(9):
                if grid[i][j] == 0:
                    cell_conflicts = count_cell_conflicts(grid, i, j)
                    if cell_conflicts > max_conflicts:
                        max_conflicts = cell_conflicts
                        max_conflict_cell = (i, j)

        if max_conflict_cell is None:
            
            # Stuck, no empty cell found
            return False  # Backtrack

        # Generate all possible values for the cell
        i, j = max_conflict_cell
        possible_values = get_possible_values(grid, i, j)

        if not possible_values:
            # No possible values for this cell, backtrack
            return False

        # Try each possible value and choose the one with the fewest conflicts
        for val in possible_values:
            grid[i][j] = val
            cell_conflicts = count_cell_conflicts(grid, i, j)

            if cell_conflicts == 0:
                # If no conflicts with this value, continue to the next cell
                result = solve(grid)
                if result is not False:
                    return result

            # Reset the cell since this value did not lead to a solution
            grid[i][j] = 0

        # If we reach here, all possible values failed, so backtrack
        

        # Update the Pygame display
        screen.fill((255, 255, 255))
        draw()
        draw_box()
        pygame.display.update()
        pygame.time.delay(50)  # Add a small delay for visualization
        return False

def count_conflicts(grid):
    conflicts = 0
    for i in range(9):
        for j in range(9):
            if grid[i][j] == 0:
                conflicts += count_cell_conflicts(grid, i, j)
    return conflicts

def count_cell_conflicts(grid, i, j):
    conflicts = 0
    for x in range(9):
        if (grid[x][j] == grid[i][j] and x != i) or grid[i][j]==0 :
            conflicts += 1
        if (grid[i][x] == grid[i][j] and x != j)  or grid[i][j]==0:
            conflicts += 1
    box_x = j // 3
    box_y = i // 3
    for x in range(box_y * 3, (box_y + 1) * 3):
        for y in range(box_x * 3, (box_x + 1) * 3):
            if (grid[x][y] == grid[i][j] and x != i and y != j) or grid[i][j]==0:
                conflicts += 1
    return conflicts

def get_possible_values(grid, i, j):
    # A set of all possible values
    possible_values = set(range(1, 10))
    
    # Remove values already in the same row
    possible_values -= set(grid[i])
    
    # Remove values already in the same column
    possible_values -= set(grid[k][j] for k in range(9))
    
    # Remove values already in the same 3x3 block
    block_row, block_col = 3 * (i // 3), 3 * (j // 3)
    possible_values -= set(grid[r][c] for r in range(block_row, block_row + 3) for c in range(block_col, block_col + 3))
    
    return list(possible_values)


def instruction():
    text1 = font2.render("PRESS D TO RESET TO DEFAULT / R TO EMPTY", 1, (0, 0, 0))
    text2 = font2.render("ENTER VALUES AND PRESS ENTER TO VISUALIZE", 1, (0, 0, 0))
    screen.blit(text1, (20, 520))
    screen.blit(text2, (20, 540))

def result():
    text1 = font1.render("FINISHED PRESS R or D", 1, (0, 0, 0))
    screen.blit(text1, (20, 570))

run = True
flag1 = 0
flag2 = 0
rs = 0
error = 0

while run:
    screen.fill((255, 255, 255))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            flag1 = 1
            pos = pygame.mouse.get_pos()
            get_cord(pos)
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                x -= 1
                flag1 = 1
            if event.key == pygame.K_RIGHT:
                x += 1
                flag1 = 1
            if event.key == pygame.K_UP:
                y -= 1
                flag1 = 1
            if event.key == pygame.K_DOWN:
                y += 1
                flag1 = 1
            if event.key == pygame.K_1:
                val = 1
            if event.key == pygame.K_2:
                val = 2
            if event.key == pygame.K_3:
                val = 3
            if event.key == pygame.K_4:
                val = 4
            if event.key == pygame.K_5:
                val = 5
            if event.key == pygame.K_6:
                val = 6
            if event.key == pygame.K_7:
                val = 7
            if event.key == pygame.K_8:
                val = 8
            if event.key == pygame.K_9:
                val = 9
            if event.key == pygame.K_RETURN:
                flag2 = 1
            if event.key == pygame.K_r:
                rs = 0
                error = 0
                flag2 = 0
                grid = [
                    [0, 0, 0, 0, 0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0, 0, 0, 0, 0]
                ]
            if event.key == pygame.K_d:
                rs = 0
                error = 0
                flag2 = 0
                grid = [
                    [7, 8, 0, 4, 0, 0, 1, 2, 0],
                    [6, 0, 0, 0, 7, 5, 0, 0, 9],
                    [0, 0, 0, 6, 0, 1, 0, 7, 8],
                    [0, 0, 7, 0, 4, 0, 2, 6, 0],
                    [0, 0, 1, 0, 5, 0, 9, 3, 0],
                    [9, 0, 4, 0, 6, 0, 0, 0, 5],
                    [0, 7, 0, 3, 0, 0, 0, 1, 2],
                    [1, 2, 0, 0, 0, 7, 4, 0, 0],
                    [0, 4, 9, 2, 0, 6, 0, 0, 7]
                ]

    if flag2 == 1:
        if solve(grid) == False:
            error = 1
        else:
            rs = 1
        flag2 = 0

    if val != 0:
        draw_val(val)
        if valid(grid, int(x), int(y), val):
            grid[int(x)][int(y)] = val
            flag1 = 0
        else:
            grid[int(x)][int(y)] = 0
            raise_error2()
        val = 0

    if error == 1:
        raise_error1()

    if rs == 1:
        result()

    draw()

    if flag1 == 1:
        draw_box()

    instruction()

    pygame.display.update()

pygame.quit()
