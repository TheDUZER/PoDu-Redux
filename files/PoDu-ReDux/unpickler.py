import pickle, os, json

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

pickled_file = open(os.path.join(os.path.curdir + "/pkmn-stats.p"), "rb")

placeholder_file = pickle.load(pickled_file)
complete_dict = {}

for x in placeholder_file:
    temp_dict = x.__dict__
    temp_dict['Attacks'] = x.Attacks.__dict__
    for a, b in zip(Attacks.__dict__.keys(), Attacks.__dict__.values()):
        if a[:2] != '__':
            temp_dict['Attacks'][a] = [b]
    for c in temp_dict['Attacks']:
        if c[:2] != '__':
            temp_dict['Attacks'][c] = temp_dict['Attacks'][c].__dict__
    complete_dict[temp_dict['Name']] = temp_dict


with open('new_file.json', 'w+') as new_file:
    json.dump(complete_dict, new_file, indent = 4)
