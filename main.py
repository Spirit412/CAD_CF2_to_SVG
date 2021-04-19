import os

import options

from cf2_measure import Cf2


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
            print(cutter)
    else:
        print('список пуст')
        # cutter = Cf2(cf2)
        # print (cutter)


def main():
    list_cf2(os.path.normpath(str(options.opt_dir())))


if __name__ == '__main__':
    main()
