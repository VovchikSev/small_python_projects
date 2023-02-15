import tkinter as tk
from random import shuffle
from tkinter.messagebox import showinfo

colors = {
    1: 'blue',
    2: 'green',
    3: '#fc6b03',
    4: '#6203fc',
    5: '#f403fc',
    6: '#a13b5b',
    7: '#a13b82',
    8: '#ff0000'
}


class MyButton(tk.Button):
    def __init__(self, master, x, y, number=0, *args, **kwargs):
        super(MyButton, self).__init__(master, width=3, font='calibri 15 bold', *args, **kwargs)
        self.x = x
        self.y = y
        self.is_mine = False
        self.number = number
        self.count_mine = 0
        self.is_open = False

    def __repr__(self):
        return f'[btn:{self.x} {self.y} number:{self.number} {self.is_mine}]'


class MineSweeper:
    window = tk.Tk()
    ROWS = 10
    COLUMNS = 10
    MINES = 20
    IS_GAME_OVER = False
    IS_FIRST_CLICK = True

    def __init__(self):
        self.buttons = []

        for row_count in range(MineSweeper.ROWS + 2):
            temp = []
            for columns_count in range(MineSweeper.COLUMNS + 2):
                btn = MyButton(MineSweeper.window, x=row_count, y=columns_count)
                btn.config(command=lambda button=btn: self.click(button))
                btn.bind('<Button-3>', self.right_click)
                temp.append(btn)

            self.buttons.append(temp)
        MineSweeper.IS_GAME_OVER = False
        MineSweeper.IS_FIRST_CLICK = True

    @staticmethod
    def right_click(event):
        if MineSweeper.IS_GAME_OVER:
            return 
        
        clicked_btn = event.widget
        if clicked_btn['state'] == 'normal':
            clicked_btn['state'] = 'disabled'
            clicked_btn['text'] = '🚩'
            clicked_btn['disabledforeground'] = 'red'
        elif clicked_btn['text'] == '🚩':
            clicked_btn['state'] = 'normal'
            clicked_btn['text'] = ''
            clicked_btn['disabledforeground'] = 'black'

    def click(self, clicked_button: MyButton):
        if MineSweeper.IS_GAME_OVER:
            return

        if MineSweeper.IS_FIRST_CLICK:
            self.insert_mines(clicked_button.number)
            self.count_mines_on_cells()
            self.print_buttons()
            MineSweeper.IS_FIRST_CLICK = False

        if clicked_button.is_mine:
            clicked_button.config(text="*", background='red', disabledforeground='black')
            clicked_button.is_open = True
            MineSweeper.IS_GAME_OVER = True
            showinfo('Game over', 'Вы проиграли!')
            for rows_count in range(1, MineSweeper.ROWS + 1):
                for columns_count in range(1, MineSweeper.COLUMNS + 1):
                    btn = self.buttons[rows_count][columns_count]
                    if btn.is_mine:
                        btn['text'] = '*'
        else:
            color = colors.get(clicked_button.count_mine, 'black')
            if clicked_button.count_mine:
                clicked_button.config(text=clicked_button.count_mine, disabledforeground=color)
                clicked_button.is_open = True
            else:
                self.breadth_first_search(clicked_button)
        clicked_button.config(state="disable")

    def settings_game(self):
        win_settings = tk.Toplevel(self.window)
        win_settings.wm_title('Настройки')

        tk.Label(win_settings, text='Количество строк').grid(row=0, column=0)
        row_entry = tk.Entry(win_settings)
        row_entry.grid(row=0, column=1, padx=20, pady=20)
        row_entry.insert(0, MineSweeper.ROWS)

        tk.Label(win_settings, text='Количество колонок').grid(row=1, column=0)
        column_entry = tk.Entry(win_settings)
        column_entry.grid(row=1, column=1, padx=20, pady=20)
        column_entry.insert(0, MineSweeper.COLUMNS)

        tk.Label(win_settings, text='Количество мин').grid(row=2, column=0)
        mines_entry = tk.Entry(win_settings)
        mines_entry.grid(row=2, column=1, padx=20, pady=5)
        mines_entry.insert(2, MineSweeper.MINES)

        save_btn = tk.Button(win_settings, text="Применить",
                             command=lambda: self.change_settings(row_entry, column_entry, mines_entry))

        save_btn.grid(row=3, column=0, columnspan=2, padx=10, pady=5)

    def change_settings(self, row: tk.Entry, column: tk.Entry, mines: tk.Entry):
        try:
            int(row.get()), int(column.get()), int(mines.get())
        except ValueError:
            showinfo('Ошибка', 'Введено не допустимое значепние!')
            return

        MineSweeper.ROWS = int(row.get())
        MineSweeper.COLUMNS = int(column.get())
        MineSweeper.MINES = int(mines.get())
        self.reload()

    def reload(self):

        [child.destroy() for child in self.window.winfo_children()]

        self.__init__()
        self.create_widgets()

    def create_widgets(self):

        menu_bar = tk.Menu(self.window)
        self.window.config(menu=menu_bar)

        settings_menu = tk.Menu(menu_bar, tearoff=0)
        settings_menu.add_command(label='Играть', command=self.reload)
        settings_menu.add_command(label='Настройки', command=self.settings_game)
        settings_menu.add_command(label='Выход', command=self.window.destroy)
        menu_bar.add_cascade(label='Файл', menu=settings_menu)

        count = 1
        for rows_count in range(1, MineSweeper.ROWS + 1):
            for columns_count in range(1, MineSweeper.COLUMNS + 1):
                btn = self.buttons[rows_count][columns_count]
                btn.number = count
                btn.grid(row=rows_count, column=columns_count, stick='NWES')
                count += 1

        for rows_count in range(1, MineSweeper.ROWS + 1):
            tk.Grid.rowconfigure(self.window, rows_count, weight=1)

        for columns_count in range(1, MineSweeper.COLUMNS + 1):
            tk.Grid.columnconfigure(self.window, columns_count, weight=1)

    def open_all_buttons(self):
        for row_count in range(MineSweeper.ROWS + 2):
            for columns_count in range(MineSweeper.COLUMNS + 2):
                btn = self.buttons[row_count][columns_count]
                if btn.is_mine:
                    btn.config(text="*", background='red')
                elif btn.count_mine in colors:
                    color = colors.get(btn.count_mine, 'black')
                    btn.config(text=btn.count_mine, fg=color)

    def start(self):
        self.create_widgets()
        MineSweeper.window.mainloop()

    def print_buttons(self):
        for rows_count in range(1, MineSweeper.ROWS + 1):
            for column_count in range(1, MineSweeper.COLUMNS + 1):
                btn = self.buttons[rows_count][column_count]
                if btn.is_mine:
                    print('X', end="")
                else:
                    print(btn.count_mine, end="")
            print()

    def insert_mines(self, number: int):
        indexes_mines = get_mines_places(number)
        print(indexes_mines)
        for rows_count in range(1, MineSweeper.ROWS + 1):
            for column_count in range(1, MineSweeper.COLUMNS + 1):
                btn = self.buttons[rows_count][column_count]
                if btn.number in indexes_mines:
                    btn.is_mine = True

    def count_mines_on_cells(self):
        for rows_count in range(1, MineSweeper.ROWS + 1):
            for column_count in range(1, MineSweeper.COLUMNS + 1):
                btn = self.buttons[rows_count][column_count]
                count_mines = 0
                if not btn.is_mine:
                    for row_dx in [-1, 0, 1]:
                        for col_dx in [-1, 0, 1]:
                            placed = self.buttons[rows_count + row_dx][column_count + col_dx]
                            if placed.is_mine:
                                count_mines += 1
                btn.count_mine = count_mines

    def breadth_first_search(self, btn: MyButton):
        queue = [btn]
        while queue:
            cur_btn = queue.pop()
            color = colors.get(cur_btn.count_mine, 'black')
            if cur_btn.count_mine:
                cur_btn.config(text=cur_btn.count_mine, fg=color)
            else:
                cur_btn.config(text='', fg=color)
            cur_btn.is_open = True
            cur_btn.config(state='disabled')
            cur_btn.config(relief=tk.SUNKEN)

            if cur_btn.count_mine == 0:
                x, y = cur_btn.x, cur_btn.y
                for dx in [-1, 0, 1]:
                    for dy in [-1, 0, 1]:
                        next_btn = self.buttons[x + dx][y + dy]
                        if not next_btn.is_open and 1 <= next_btn.x <= MineSweeper.ROWS and \
                                1 <= next_btn.y <= MineSweeper.COLUMNS and next_btn not in queue:
                            queue.append(next_btn)


def get_mines_places(exclude_number: int):
    indexes = list(range(1, MineSweeper.ROWS * MineSweeper.COLUMNS + 1))
    indexes.remove(exclude_number)
    shuffle(indexes)
    return indexes[:MineSweeper.MINES]


game = MineSweeper()

game.start()

# создание барьерных элементов https://www.youtube.com/watch?v=E9lIYJoA_0Y
# подстчет соседей кнопок https://www.youtube.com/watch?v=mLySBcS-6p0
# список видео https://www.youtube.com/watch?v=Ye9VSmJZqTo&list=PLQAt0m1f9OHtfXxDph-MJvYCLaOvildGQ&index=8
