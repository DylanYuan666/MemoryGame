import os

def game_fight(filename, data):
    with open(filename, 'w') as file:
        file.write(data)

def game_load(filename):
    if not os.path.exists(filename):
        return None
    with open(filename, 'r') as file:
        return file.read()
    