import math
from re import split
import options
import os
import pathlib
import fileinput
from pydantic import BaseModel, Field, root_validator, condecimal
from svgwrite import *
from svgwrite.container import *
from svgwrite.utils import *
from svgwrite.drawing import *
from svgwrite.shapes import *
from config import settings


class Cf2(object):
    EXT = ".cf2"
    COEFFICIENT = 20.8346456  # 1mm ≅ 2,8346456px in to Adobe Illustrator
    LENG = 0
    FILE_NAME = ""

    def __init__(self, cutter: str):
        self.LENG = len(cutter)
        self.FILE_NAME = cutter.split('.')[0]

        # while str(self.FILE_NAME).endswith(".cf2"):
        #     # pass
        #     self.cutter = self.cutter[:-4]
        # else:
        path = os.path.normpath(settings.CF2_DIR)
        dir = os.path.join(path, self.FILE_NAME + self.EXT)

        with open(dir, 'r') as f:
            file_contents = f.read()

        # f = open(dir, 'r')
        # file_contents = f.read()
        # f.close()
        for line in file_contents.splitlines():

            if line.startswith('UR,'):
                UR1, UR2 = ''.join(line.split(',')[1]), ''.join(line.split(',')[2])
                UR1, UR2 = float(UR1), float(UR2)
            elif line.startswith('LL,'):
                LL1, LL2 = ''.join(line.split(',')[1]), ''.join(line.split(',')[2])
                LL1, LL2 = float(LL1), float(LL2)
        if abs(LL1) == 0:
            self.width = UR1
        if abs(LL2) == 0:
            self.height = UR2
        if LL1 < 0:
            if UR1 > LL1:
                self.width = abs(LL1) + abs(UR1)
        if LL1 > 0:
            if UR1 > LL1:
                self.width = UR1 - LL1
        if LL2 < 0:
            if UR2 > LL2:
                self.height = abs(LL2) + abs(UR2)
        if LL2 > 0:
            if UR2 > LL2:
                self.height = UR2 - LL2
        if self.width == 0 or self.height == 0:
            return "ERROR, 0"

        """Create SVG file"""
        svg_size_w = self.width * mm
        svg_size_h = self.height * mm
        colors = ['grey', 'black', 'red', 'green', 'blue']
        dwg = Drawing(self.FILE_NAME + '.svg',
                      size=(svg_size_w, svg_size_h),
                      profile='full'
                      )
        defs_OnUP = Defs(id='defs_t')
        symbol_t = Symbol(id='OneUP')

        block_driwing = []
        START, END = 'SUB', 'END'
        inblock = False
        for line in fileinput.input(files=dir, mode='r'):
            line = line.rstrip()
            if inblock:
                if END in line:
                    inblock = False
                else:
                    # print(line)
                    line = line.split(',')
                    line_type = int(line[2])
                    stroke_width = 5
                    '''
                    linetype (cut/erese/perf/dim/bleed) = color line
                    '''
                    if line[0] == 'L':
                        v1 = float(line[4]) * self.COEFFICIENT
                        '''start X'''
                        v2 = float(line[5]) * self.COEFFICIENT
                        '''start Y'''
                        v3 = float(line[6]) * self.COEFFICIENT
                        '''End X'''
                        v4 = float(line[7]) * self.COEFFICIENT
                        '''End Y'''
                        symbol_t.add(
                            (Line(start=(v1, v2), end=(v3, v4), stroke=colors[line_type], stroke_width=stroke_width)))
                        # symbol_t.add(dwg.line(start=(v1, v2),
                        #                       end=(v3, v4), stroke="red", stroke_width="5"))
                    elif line[0] == 'A':
                        v1 = float(line[4]) * self.COEFFICIENT
                        '''start X'''
                        v2 = float(line[5]) * self.COEFFICIENT
                        '''start Y'''
                        v3 = float(line[6]) * self.COEFFICIENT
                        '''End X'''
                        v4 = float(line[7]) * self.COEFFICIENT
                        '''End Y'''
                        v5 = float(line[8]) * self.COEFFICIENT
                        '''Centre X'''
                        v6 = float(line[9]) * self.COEFFICIENT
                        '''Centre Y'''
                        dirc = str(line[10])
                        '''Direction of rotation'''
                        auxLT = line[3]
                        '''Auxillery line type   - the common file auxiliary linetype'''
                        radius = self.find_radius(v1, v2, v5, v6)
                        if '+' in dirc:
                            dirc = 1
                        else:
                            dirc = 0

                        if (v1 == v3) and (v2 == v4):
                            symbol_t.add(Circle(center=(v5, v6),
                                                r=radius,
                                                fill="none",
                                                stroke=colors[line_type],
                                                stroke_width=stroke_width))
                        else:
                            dd = f"M{v1},{v2}A{radius},{radius},1,0,{dirc},{v3},{v4}"
                            # print(str(dd))
                            w = dwg.path(d=str(dd), fill="none", stroke=colors[line_type], stroke_width=stroke_width)
                            symbol_t.add(w)
                    elif line[0] == 'T':
                        print('TEXT')

            elif START in line:  # not in block
                print(line)
                inblock = True
        print(' /////// ')

        defs_OnUP.add(symbol_t)
        dwg.add(defs_OnUP)
        dwg.add(Use(href='#OneUP', insert=(5 * mm, 5 * mm)))
        dwg.save()

    def __repr__(self):
        return ("{:s}.cf2 > {:s}".format(self.FILE_NAME, self.measures()))
        # return ("{:s}.cf2 > {:s}\nCutter: {:s}\nMeasures: {:s}\nWidth: {:d}\nHeight: {:d}".format(self.cutter, self.measures(), self.cutter, self.measures(), self.width, self.height))
        # return "".join((cutter,".cf2 > ",measures,"\nCutter: ",cutter,"\nMeasures: ",measures,"\nWidth: ",str(width),"\nHeight: ",str(height)))

    def find_radius(self, abs_X: float, abs_Y: float, xc: float, yc: float):
        return math.sqrt(pow(xc - abs_X, 2) + pow(yc - abs_Y, 2))

    def measures(self):
        return str(self.width) + 'x' + str(self.height)

    def _width(self):
        return self.width

    def _height(self):
        return self.height

    def _cutter(self):
        if str(self.FILE_NAME).endswith(".cf2"):
            return self.FILE_NAME[:-4]
        else:
            return self.FILE_NAME
