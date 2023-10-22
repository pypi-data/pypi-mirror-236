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
    pyprefs_dir = os.path.join(local_path, 'pyprefs\\')
    file_path = os.path.join(pyprefs_dir, saveName + '.txt')

    return os.path.isfile(file_path)

def remove(saveName):
    pyprefs_dir = os.path.join(local_path, 'pyprefs\\')
    file_path = pyprefs_dir + saveName + '.txt'
    print(file_path)
    if os.path.isfile(file_path):
        os.remove(pyprefs_dir + saveName + '.txt')
    else:
        print(except_prefix + f'Save {saveName} not found.')

def removeAll(debug=False):
    pyprefs_dir = os.path.join(local_path, 'pyprefs')

    if os.path.isdir(pyprefs_dir):
        for file in os.listdir(pyprefs_dir):
            file_path = os.path.join(pyprefs_dir, file)
            if os.path.isfile(file_path):
                os.remove(file_path)
        os.rmdir(pyprefs_dir)
        return True
    else:
        if debug:
            print(except_prefix + 'Saves not found.')
        return False