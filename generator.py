import csv
from PIL import Image, ImageDraw, ImageFont

def create_possibility_matrix(sudoku):
    n = len(sudoku)
    possibilities = [[[i for i in range(1, n+1)] if sudoku[row][col] == 0 else [] for col in range(n)] for row in range(n)]
    for row in range(n):
        for col in range(n):
            if sudoku[row][col] != 0:
                block_x = row//3
                block_y = col//3
                for iter_x in range(3):
                    for iter_y in range(3):
                        x = block_x*3 + iter_x
                        y = block_y*3 + iter_y
                        if sudoku[row][col] in possibilities[x][y]:
                            possibilities[x][y].remove(sudoku[row][col])
                for i in range(n):
                    if sudoku[row][col] in possibilities[i][col]:
                        possibilities[i][col].remove(sudoku[row][col])
                    if sudoku[row][col] in possibilities[row][i]:
                        possibilities[row][i].remove(sudoku[row][col])
    
    return possibilities

def print_possibility_matrix(possibility_matrix):
    for row in range(9):
        if row % 3 == 0 and row != 0:
            print("-" * 21)
        for col in range(9):
            if col % 3 == 0 and col != 0:
                print("|", end=" ")
            if len(possibility_matrix[row][col]) == 0:
                print("X", end=" ")
            else:
                for num in range(1, 10):
                    if num in possibility_matrix[row][col]:
                        print(num, end=" ")
                    else:
                        print(" ", end=" ")
            print()
        print()

sudoku = []

with open('in.csv', newline='') as csvfile:
    csvreader = csv.reader(csvfile)
    for i in range(9):
        row = [int(item) for item in next(csvreader)]
        sudoku.append(row)

print(sudoku)


possibility_matrix = create_possibility_matrix(sudoku)

string_grid = [[None for _ in range(9)] for _ in range(9)]

sudoku_2_print = [[None for _ in range(9)] for _ in range(9)]

for i in range(9):
    for j in range(9):
        string_grid[i][j] = ''.join(map(str, possibility_matrix[i][j]))
        if sudoku[i][j]!=0:
            sudoku_2_print[i][j] = str(sudoku[i][j])
        else:
            sudoku_2_print[i][j] = ''
        


cell_size = (100, 100)  
padding = 10
line_width = 2
image_width = len(string_grid[0]) * cell_size[0] + padding * (len(string_grid[0]) - 1)
image_height = len(string_grid) * cell_size[1] + padding * (len(string_grid) - 1)

img = Image.new('RGB', (image_width, image_height), color='white')

draw = ImageDraw.Draw(img)

font = ImageFont.truetype("arial.ttf", 20)  
font1 = ImageFont.truetype("arial.ttf", 50)
for row_idx, row in enumerate(string_grid):
    for col_idx, text in enumerate(row):
        x = col_idx * cell_size[0] + padding * col_idx + 2
        y = row_idx * cell_size[1] + padding * row_idx + font.getsize(text)[1]
        draw.text((x, y), text, fill=(0, 0, 255), font=font)  

for row_idx, row in enumerate(sudoku_2_print):
    for col_idx, text in enumerate(row):
        x = (col_idx + 1) * cell_size[0] - padding  
        y = (row_idx + 1) * cell_size[1] - padding  
        text_width, text_height = draw.textsize(text, font=font)
        x -= text_width
        y -= text_height
        draw.text((x, y), text, fill=(0, 0, 0), font=font1) 

for i in range(len(string_grid) + 1):
    y = i * cell_size[1] + padding * i
    if (i%3)==0:
        draw.line([(0, y), (image_width, y)], fill=(0, 0, 0), width=3*line_width)
    else:
        draw.line([(0, y), (image_width, y)], fill=(0, 0, 0), width=line_width)        
    if i < len(string_grid[0]):
        x = i * cell_size[0] + padding * i
        if (i%3)!=0:
            draw.line([(x, 0), (x, image_height)], fill=(0, 0, 0), width=line_width)
        else:
            draw.line([(x, 0), (x, image_height)], fill=(0, 0, 0), width=3*line_width)

img.save("output.png")
