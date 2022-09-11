import os

from config import settings

from cf2_to_svg import Cf2


def list_cf2(cf2):
    path = cf2
    path_cf2 = []
    list_dir_cf2 = os.listdir(path)
    if list_dir_cf2:
        for item in list_dir_cf2:
            if item.endswith(".cf2"):
                path_cf2.append(item)
        for item in path_cf2:
            cutter = Cf2(str(item))
            print("- "*20)
            print(cutter.LENG)
            print("- "*20)
            print(cutter)
    else:
        print('список пуст')


def main():
    print(settings.ROOT_DIR)
    print(settings.CF2_DIR)
    list_cf2(os.path.normpath(str(settings.CF2_DIR)))


if __name__ == '__main__':
    main()
