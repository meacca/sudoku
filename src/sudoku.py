import argparse
import tkinter as tk
from tkinter import font
import numpy as np
import gettext


class Sudoku:
    def __init__(self):
        """
        Sudoku class constructor.

        Initializes Tkinter window object as self.window
        Stores main interface parameters as self.params
        Configures Tkinter window and initializes sudoku grid
        """
        self.window = tk.Tk()
        self.params = {'res': "800x800", "btn_size": 10, "fnt_size": 10, 
                       "fnt_family": 'Helvetica'}
        self.font = font.Font(size=self.params["fnt_size"], family=self.params["fnt_family"])
        self.size = 9
        self.row_offset = self.params["btn_size"]//2
        
        self.btn_grid = []
        self.configure_window()
        self.init_grid()
        self.reset_grid()

    def init_grid(self):
        """
        Initializes grid with sudoku numbers buttons
        """
        for btn_ind in range(self.size * self.size):
            self.btn_grid.append(tk.Button(self.window, text=str(btn_ind + 1), bg="white", fg="black",
                                           font=self.font, width=1, height=1))
        
    def prepare_order(self):
        """
        Initializes a random sudoku numbers permutation

        return    order: np.array of size (self.size*self.size, )
        """
        order = np.zeros((self.size * self.size, ), dtype=int)
        for i in range(self.size):
            data = list(range(1, self.size + 1))
            order[i * self.size:(i + 1) * self.size] = np.random.permutation(data)
        return order

    def reset_grid(self):
        """
        Initializes sudoku buttons grid with random number permutation

        Note: button placement procedure considers offsets that divide grid into 3x3 blocks
        """
        order = self.prepare_order()
        for btn_ind, btn_val in enumerate(order):
            btn_col, btn_row = btn_ind % self.size * self.params["btn_size"],\
                               btn_ind // self.size * self.params["btn_size"] + self.row_offset
            btn_col += (btn_col >= 3 * self.params["btn_size"]) +\
                       (btn_col >= 6 * self.params["btn_size"])
            btn_row += (btn_row >= self.row_offset + 3 * self.params["btn_size"]) +\
                       (btn_row >= self.row_offset + 6 * self.params["btn_size"])
            self.btn_grid[btn_ind].grid(column=btn_col, row=btn_row,
                                        columnspan=self.params["btn_size"],
                                        rowspan=self.params["btn_size"],
                                        sticky=tk.N + tk.E + tk.S + tk.W)
            if np.random.rand() < 0.3:
                self.btn_grid[btn_ind]['text'] = ''
            else:
                self.btn_grid[btn_ind]['text'] = str(btn_val)

    def configure_window(self):
        """
        Configures Tkinter window geometry and intializes main UI buttons

        List of UI buttons:
            - Start a new game ("New")
            - Offer a hint ("Hint")
            - Check current grid layout for mistakes w.r.t sudoku rules("Check")
            - Exit the game and close the window ("Exit")
        """
        self.window.title("sudoku")
        self.window.geometry(self.params["res"])
        self.window.configure(bg="grey")
        
        rowspan = self.params["btn_size"]//3-1
        
        new_btn = tk.Button(self.window, text=_("New"),
                            command=self.reset_grid,
                            bg="white", fg="black", font=self.font, 
                             width=1, height=1)

        new_btn.grid(column=0,
                     row=0,
                     columnspan=self.params["btn_size"], rowspan=rowspan,
                     sticky=tk.N + tk.E + tk.S + tk.W)
        
        hint_btn = tk.Button(self.window, text=_("Hint"),
                             command=self.reset_grid,
                             bg="white", fg="black", font=self.font, 
                             width=1, height=1)

        hint_btn.grid(column=2 * self.params["btn_size"],
                      row=0,
                      columnspan=self.params["btn_size"], rowspan=rowspan,
                      sticky=tk.N + tk.E + tk.S + tk.W)

        check_btn = tk.Button(self.window, text=_("Check"),
                              command=self.reset_grid,
                              bg="white", fg="black", font=self.font, 
                             width=1, height=1, wraplength=self.params["btn_size"]*self.params["fnt_size"])

        check_btn.grid(column=6 * self.params["btn_size"] + 2,
                       row=0,
                       columnspan=self.params["btn_size"], rowspan=rowspan,
                       sticky=tk.N + tk.E + tk.S + tk.W)
        
        exit_btn = tk.Button(self.window, text=_("Exit"),
                             command=self.exit_game,
                             bg="white", fg="black", font=self.font, 
                             width=1, height=1)
        
        exit_btn.grid(column=8 * self.params["btn_size"] + 2,
                      row=0,
                      columnspan=self.params["btn_size"], rowspan=rowspan,
                      sticky=tk.N + tk.E + tk.S + tk.W)
        
        for i in range(self.size * self.params["btn_size"] + 2):
            self.window.grid_columnconfigure(i, weight=1)
            
        for i in range(self.size * self.params["btn_size"] + 2 + self.row_offset):
            self.window.grid_rowconfigure(i, weight=1)
        
    def start_game(self):
        """
        Tkinter "while True" loop that updates its draw engine frames
        """
        self.window.mainloop()

    def exit_game(self):
        """
        Stop Tkinter engine and close window
        """
        self.window.destroy()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Process sudoku interface parameters.')
    parser.add_argument('--lang', metavar='L', type=str, default="en",
                        help='interface language')

    args = parser.parse_args()
    
    translate = gettext.translation(domain='sudoku', localedir='../locale', languages=[args.lang])
    _ = translate.gettext
    
    game = Sudoku()
    game.start_game()
