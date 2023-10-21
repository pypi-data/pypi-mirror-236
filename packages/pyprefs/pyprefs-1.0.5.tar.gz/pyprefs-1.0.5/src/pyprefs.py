from os import path, mkdir

local_path = 'C:\\Program Files\\mc-corp\\'
except_prefix = '\033[31m[error]: '

def save(saveName, data):
    if not path.isdir(local_path + 'pyprefs'):
        mkdir(local_path)
        mkdir(local_path + 'pyprefs')

    with open(local_path + 'pyprefs\\' + saveName + '.txt', 'w') as pypfile:
        pypfile.write(str(data))
        pypfile.close()
        return True


def load(saveName):
    if not path.isdir(local_path + 'pyprefs'):
        mkdir(local_path)
        mkdir(local_path + 'pyprefs')
    if not path.isfile(local_path + 'pyprefs\\' + saveName + '.txt'):
        print(except_prefix + f'Save {saveName} not found.')
        exit()

    with open(local_path + 'pyprefs\\' + saveName + '.txt', 'r') as pypfile:
        return pypfile.read()

def check(saveName):
    if path.isfile(local_path + 'pyprefs\\' + saveName + '.txt'):
        return True
    else:
        return False