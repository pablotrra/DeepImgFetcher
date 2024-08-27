import os

def obtain_subdirs(dir):
    subdirs = [dir_name for dir_name in os.listdir(dir) if os.path.isdir(os.path.join(dir, dir_name))]
    return subdirs