import os

local_path = '.pp'
except_prefix = '\033[31m[error]: '


def save(saveName, data):
    pyprefs_dir = os.path.join(local_path, 'pyprefs')

    if not os.path.isdir(pyprefs_dir):
        os.makedirs(pyprefs_dir)

    file_path = os.path.join(pyprefs_dir, saveName + '.txt')

    with open(file_path, 'w') as pypfile:
        pypfile.write(str(data))
        return True


def load(saveName):
    pyprefs_dir = os.path.join(local_path, 'pyprefs')

    if not os.path.isdir(pyprefs_dir):
        os.makedirs(pyprefs_dir)

    file_path = os.path.join(pyprefs_dir, saveName + '.txt')

    if not os.path.isfile(file_path):
        print(except_prefix + f'Save {saveName} not found.')
        exit()

    with open(file_path, 'r') as pypfile:
        return pypfile.read()


def check(saveName):
    pyprefs_dir = os.path.join(local_path, 'pyprefs')
    file_path = os.path.join(pyprefs_dir, saveName + '.txt')

    return os.path.isfile(file_path)
