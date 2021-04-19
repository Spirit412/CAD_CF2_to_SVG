import math
from typing import List

from svgwrite import *
from svgwrite.container import *
from svgwrite.utils import *
from svgwrite.drawing import *
from svgwrite.path import *
from svgwrite.shapes import *


def create_svg(svg_size_w, svg_size_h):
    svg_size_w = 500 * mm
    svg_size_h = 500 * mm
    dwg = Drawing('title.svg',
                  size=(svg_size_w, svg_size_h),
                  profile='tiny',
                  debug=True,
                  # viewBox="0 0 200 200"
                  # preserveAspectRatio="xMinYMin"

                  )
    defs_OnUP = Defs(id='defs_t')
    symbol_t = Symbol(id='OneUP')
    symbol_t.add(dwg.rect((20 * mm, 20 * mm), (50 * mm, 50 * mm),
                          fill=rgb(200, 0, 13, '%')))
    symbol_t.add(dwg.rect((50 * mm, 50 * mm), (100 * mm, 100 * mm),
                          fill=rgb(0, 80, 13, '%')))
    symbol_t.add(Circle(center=(50, 50), r=50))
    symbol_t.add(Ellipse(center=(150, 150), r=(20, 60), fill='green'))

    # L,2,1,0,83.935917,138.201819,83.935917,38.202019,0,0.000000
    # [4] - start X
    # [5] - start Y
    # [6] - End X
    # [7] - End Y
    # [2] - Layer / pen
    # [3] - Auxillery line type

    #
    # A, 2, 1, 0, -0.000000, -0.000000, 90.000000, -0.000000, 45.000000, -20.000000, +1, 0, 0.0000
    # A,2,1,0,83.935917,38.202019,78.935998,33.202453,78.936174,38.202196,-1,0,0.000000

    # /////// CPECIFICATION  ARC CF2
    # A, p, t, at, sx, sy, ex, ey, cx, cy, =/-1, nbridges, wbridges
    # A us the capital letter A.
    # P is the pointage in points (1/72 inches).
    # t is the common file linetype
    # at is the common file auxiliary linetype

    # sx, sy is the start coordinate of the arc.
    # ex, ey is the end coordinate of the arc.

    # nbridges is the number of bridges in the arc.
    # wbridges is the width of the bridges in the arc in mm.
    # //////// /////// CPECIFICATION  CF2

    # [4]   - start X   - the start coordinate of the arc. X
    # [5]   - start Y   - the start coordinate of the arc. Y
    # [6]   - End X   - the end coordinate of the arc X
    # [7]   - End Y   - the end coordinate of the arc Y
    # [8]   - Centre X
    # [9]   - Centre Y
    # [10]  - Direction of rotation
    # if ([4]==[6]) && ([5]==[7])) - Circle
    # else - Arc

    # https://zen.yandex.ru/media/id/5930862ad7d0a635f6556788/sintaksis-svg-path-illiustrirovannoe-rukovodstvo-5aa68af91410c30c8cd600cd
    # "M mx,my A rx,ry x-axis-rotation large-arc-flag, sweep-flag x,y"
    # "M 70,70 A75,55   45              0, 1 160,140"
    # M mx, my – координаты начальной точки дуги элипса
    # A rx, ry – радиусы дуги элипса
    # x - axis - rotation – угол поворота всей  дуги элипса относительно оси абцисс
    # large - arc - flag – параметр, отвечающий за вывод большей части    дуги, если( = 1) или
    # меньшей( = 0) части дуги
    # sweep - flag – отвечает за направление отрисовки дуги из начальной точки в
    # конечную точку.Если sweep - flag = 1, то дуга элипса будет отрисована по часовой
    # стрелке.При sweep - flag = 0 – против    часовой    стрелки.
    # x, y – координаты конечной точки дуги элипса

    coef = 3.779527559
    # 1mm ≅ 3.779527559px or user units
    # get_line = ['A', 2, 1, 0, -0.000000, -0.000000, 90.000000, -0.000000, 45.000000, -20.000000, '+1', 0, 0.0000]
    get_line_str = 'A,2,1,0,85.515169,20.840128,85.515169,20.840128,64.651336,7.066949,+1,0,0.000000'

    get_line = get_line_str.split(',')
    print('get_line', get_line)
    for i, val in enumerate(get_line, start=0):
        print(f'№ {i} => {val}')
    print(get_line)
    v1 = float(get_line[4]) * coef
    '''start X'''
    v2 = get_line[5] * coef
    '''start Y'''
    v3 = get_line[6] * coef
    '''End X'''
    v4 = get_line[7] * coef
    '''End Y'''
    v5 = get_line[8] * coef
    print(v5)
    '''Centre X'''
    v6 = get_line[9] * coef
    print(v6)
    '''Centre Y'''
    dirc = str(get_line[10])
    '''Direction of rotation'''
    layer = get_line[2]
    '''Layer / pen   - is the common file linetype'''
    auxLT = get_line[3]
    '''Auxillery line type   - the common file auxiliary linetype'''
    radius = find_radius(v1, v2, v5, v6)
    if '+' in dirc:
        dirc = 0
        print('dirc = 1')
    else:
        dirc = 1
        print('dirc = 0')

    if (v1 == v3) and (v2 == v4):
        symbol_t.add(Circle(center=(v5, v6), r=radius))
    else:
        dd = f"M{v1},{v2}a{radius},{radius},1,0,{dirc},{v3},{v4}"
        print(str(dd))
        w = dwg.path(d=str(dd), fill="none", stroke="black", stroke_width="20")
        symbol_t.add(w)

    defs_OnUP.add(symbol_t)
    dwg.add(defs_OnUP)
    dwg.add(Use(href='#OneUP', insert=(100 * mm, 100 * mm)))

    dwg.save()


def find_radius(absX: float, absY: float, xc: float, yc: float):
    return math.sqrt(pow(xc - absX, 2) + pow(yc - absY, 2))


# def find_Ang_Rad(absX: float, absY: float, xc: float, yc: float, dirc: int):
#     global radius
#     radius = 0
#     '''
#     absX - start X
#     absY - start Y
#     xc - Centre X
#     yc - Centre Y
#     dirc - Direction ofrotation
#     '''
#     # rtnAng - Var used to RETURN Angle of movement
#     # radius - Global used to return RADIUS
#     rx = absX - xc
#     ry = absY - yc
#
#     if rx == 0:
#         rad = abs(ry)
#         if ry > 0:
#             rtnAng = 90
#         else:
#             rtnAng = 270
#         radius = rad
#         return rtnAng
#     # (rx = 0)
#
#     if ry == 0:
#         rad = abs(rx)
#         if rx > 0:
#             rtnAng = 0
#         else:
#             rtnAng = 180
#         radius = rad
#         return rtnAng
#
#     rad = (abs(rx) * abs(rx)) + (abs(ry) * abs(ry))
#     rad = math.sqrt(rad)
#     radius = rad
#
#     if (rx > 0) and (ry > 0):
#         aplus = 0
#         wrx = rx
#         wry = rx
#         # (rx > 0 And ry > 0)
#     if (rx < 0) and (ry > 0):
#         aplus = 90
#         wrx = ry
#         wry = rx
#         # (rx < 0 And ry > 0)
#     if (rx > 0) and (ry < 0):
#         aplus = 270
#         wrx = ry
#         wry = rx
#
#     rtnAng = abs(wry) / abs(wrx)
#     rtnAng = math.atan(rtnAng)
#     rtnAng = (rtnAng / math.pi) * 100
#     rtnAng = rtnAng + aplus
#     if (rtnAng > 360):
#         rtnAng = rtnAng - 360
#     return rtnAng


if __name__ == '__main__':
    create_svg(500, 500)
