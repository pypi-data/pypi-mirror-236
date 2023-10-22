import sqlite3
import os
import json
from importlib.resources import path

import numpy as np
from sklearn.linear_model import LinearRegression

import pygame

TABLE_BEFORE = "offset_data_before"
TABLE_AFTER = "offset_data_after"
DB_PATH = 'pygamecentering/offsets.db'
letters = ['B', 'D', 'I', 'E', 'T']

def generate_offset_data(params=None):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    if params is None:
        table_name = TABLE_BEFORE
    else:
        table_name = TABLE_AFTER


    cursor.execute(f'''
    CREATE TABLE IF NOT EXISTS {table_name} (
        font_size INTEGER,
        offset INTEGER
    )''')
    cursor.execute(f"DELETE FROM {table_name}")
    conn.commit()


    pygame.init()
    dim = (2000, 3000)
    screen = pygame.display.set_mode(dim)
    screen.fill((0, 0, 0))

    screen_rect = screen.get_rect()

    COLOR = (255, 255, 255)

    font_list = []
    offset_list = []
    for font_size in range(10, 2000):
        for letter in letters:
            screen.fill((0, 0, 0))
            font = pygame.font.Font(None, font_size)
            render = font.render(letter, True, COLOR)
            font_rect = render.get_rect(center = screen_rect.center)
            if params:
                font_rect.centery += font_size*params['coef'] + params['intercept']
            screen.blit(render, font_rect)

            text_top = -1 
            text_bot = -1

            center_x = screen_rect.centerx
            center_y = screen_rect.centery

            for y in range(0, center_y):
                pos = (center_x, y)
                color = screen.get_at(pos)[1]

                if color > 0:
                    text_top = y
                    break

            for y in range(dim[1] - 1, center_y, -1):
                pos = (center_x, y)
                color = screen.get_at(pos)[1]

                if color > 0:
                    text_bot = y
                    break


            if text_top == -1 or text_bot == -1:
                raise Exception(letter, text_top, text_bot)

            letter_centery = (text_top + text_bot)//2

            offset = center_y - letter_centery

            font_list.append(font_size)
            offset_list.append(offset)
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()

    for font_size, offset in zip(font_list, offset_list):
        cursor.execute(f"INSERT INTO {table_name} (font_size, offset) VALUES (?, ?)", (font_size, offset))
    conn.commit()
    conn.close()
    pygame.quit()
    

def generate_linear_regression(params=None):
    if params is None:
        table_name = TABLE_BEFORE
    else:
        table_name = TABLE_AFTER

    generate_offset_data(params)
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute(f'''
    SELECT font_size, offset FROM {table_name}
    ''')
    data = cursor.fetchall()
    x_data, y_data = zip(*data)

    x_data = np.array(x_data).reshape(-1, 1)
    y_data = np.array(y_data).reshape(-1, 1)

    model = LinearRegression()
    model.fit(x_data, y_data)

    percent_error = np.abs(y_data / x_data) * 100
    mape = np.mean(percent_error)
    coef = float(model.coef_[0][0])
    intercept = float(model.intercept_[0])
    params = {'coef': round(coef, 4), 'intercept': round(intercept, 4), 'MAPE': round(mape, 4)}
    return params


data = {}
data['unadjusted_data'] = generate_linear_regression()
data['adjusted_data'] = generate_linear_regression(data['unadjusted_data'])

offset_reduction = (data['unadjusted_data']['MAPE'] - data['adjusted_data']['MAPE']) / data['unadjusted_data']['MAPE']
data['offset_reduction'] = f"{round(offset_reduction, 2)*100}%"

with open('pygamecentering/offset_data_results.json', 'w') as file:
    json.dump(data, file, indent=4)

