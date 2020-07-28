import tkinter as tk
from tkinter import ttk
import PIL.Image as pilimg
import pickle
import os

class PokemonList():
    def __init__(self):
        pass
    def __iter__(self):
        counter = 0
        __iterator = iter(self.__dict__.values())
        return __iterator
    
    def __next__(self):
        if counter == len(self.__dict__.values()):
            counter = 0
            raise StopIteration
        else:
            counter += 1
            return __iterator

    def __str__(self):
        return self.Name

class Pokemon():
    def __init__(self, line = None, Ctrl = None):
        pass

    def __iter__(self):
        counter = 0
        __iterator = iter(self.__dict__.values())
        return __iterator
    
    def __next__(self):
        if counter == len(self.__dict__.values()):
            counter = 0
            raise StopIteration
        else:
            counter += 1
            return __iterator

    def __str__(self):
        return self.Name

class AttackList():
    def __init__(self):
        pass

    def __iter__(self):
        counter = 0
        __iterator = iter(self.__dict__.values())
        return __iterator
    
    def __next__(self):
        if counter == len(self.__dict__.values()):
            counter = 0
            raise StopIteration
        else:
            counter += 1
            return __iterator

class Attacks():
    def __init__(self):
        pass

    def __iter__(self):
        counter = 0
        __iterator = iter(self.__dict__.values())
        return __iterator
    
    def __next__(self):
        if counter == len(self.__dict__.values()):
            counter = 0
            raise StopIteration
        else:
            counter += 1
            return __iterator

PKMN_STATS = pickle.load(open('pkmn-stats.p', 'rb'))

pkmn_list = [_.Name for _ in PKMN_STATS]
pkmn_list.sort()

root = tk.Tk()
root.title("PoDu ReDux Figure Browser")

def get_entry(event):
    global image_viewer, current_image, img
    file_search_string = ''
    search_string = pkmn_dropdown.get()
    for pkmn in PKMN_STATS:
        if pkmn.Name == search_string:
            file_search_string = pkmn.Spritefile
    image_viewer.delete(current_image)
    img = tk.PhotoImage(file = os.path.join(
        'images',
        'cards',
        f'{file_search_string[:-4]}_card.png'))
    current_image = image_viewer.create_image(129, 182, image=img)
    
def close_window():
    root.destroy()

#searchbox = ttk.Entry(root)
#searchbox.pack()
#searchbox.bind('<Key>', get_entry)

pkmn_dropdown = ttk.Combobox(root, values = pkmn_list)
pkmn_dropdown.pack()
pkmn_dropdown.bind('<<ComboboxSelected>>', get_entry)

image_viewer = tk.Canvas(root, width = 256, height = 365)
image_viewer.pack()
img = tk.PhotoImage(file = os.path.join(
    'images',
    'cards',
    f'003MMS_card.png'))
current_image = image_viewer.create_image(129, 182, image=img)

root.mainloop()
