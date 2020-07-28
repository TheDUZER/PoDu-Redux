
import tkinter as tk
from tkinter import ttk
import pickle

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
    
search_string = ''
check_string = ''
last_search = []

root = tk.Tk()
root.title("PoDu ReDux Figure Browser")

rel_stats = ['Ability',
             'Evolutions',
             'Forms',
             'Move',
             'Name',
             'Type1',
             'Type2',
             'CombatRange']

def get_entry(event):
    textbox.delete("1.0", tk.END)
    search_string = pkmn_dropdown.get()
    pkmn_data = {}
    for pkmn in PKMN_STATS:
        if pkmn.Name == search_string:
            pkmn_data = dict(pkmn.__dict__)
    display_string = ''

    for keys, values in pkmn_data.items():
        if keys == 'Attacks':
            atk_counter = 1
            display_string += '\n++++Attacks++++\n'
            for attacks in pkmn_data['Attacks']:
                display_string += f"\tAttack {atk_counter}\n"
                atk_counter += 1
                for atk_keys, atk_values in attacks.__dict__.items():
                    display_string += f'\t\t{atk_keys}:\t{atk_values}\n'
            display_string += '-------------\n\n'
        elif keys in rel_stats:
            display_string += f'{keys}:\t{values}\n'
        else:
            pass
            
    textbox.insert(tk.END, display_string)
    
def close_window():
    root.destroy()

pkmn_dropdown = ttk.Combobox(root, values = pkmn_list)
pkmn_dropdown.pack()
pkmn_dropdown.bind('<<ComboboxSelected>>', get_entry)

textbox = tk.Text(root, width=80, height=60)
textbox.pack()

root.mainloop()
