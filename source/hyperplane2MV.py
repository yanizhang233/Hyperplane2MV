import numpy as np
from nonlinearity import sigma, relu
from config import Symbols
from sigmaConstruct import sigmaConstruct, sigmaConstruct_agu

class hyperplane2MV:
    def __init__(self, xcords, ycords): #input: xcoordinates, ycoordinates of the breakpoints
        self.xcords = xcords
        self.ycords = ycords

    def findLinPieces(self):
        self.LinPieces = {} #dictionary of linear pieces, key = pi,  value = [[x_1,x_2], slope, intercept] where [x_1, x_2] is the interval of the linear piece
        for i in range(len(self.xcords)-1):
            slope = round((self.ycords[i+1] - self.ycords[i]) / (self.xcords[i+1] - self.xcords[i]))
            intercept = round(self.ycords[i] - slope * self.xcords[i])
            self.LinPieces[f'p{i}'] = [[self.xcords[i], self.xcords[i+1]], slope, intercept]

    def findMeetPoints(self): #find the meet points of each pair of linear pieces
        self.MeetPoints = {} #dictionary of meet points, key = (pi, pj), value = [x, y] where (pi, pj) is the pair of linear pieces. At the left of x, pi is above pj, at the right of x, pi is below pj
        for i in range(len(self.LinPieces)-1):
            for j in range(i+1, len(self.LinPieces)):
                if self.LinPieces[f'p{i}'][1] == self.LinPieces[f'p{j}'][1]: #if the slopes are the same, then the lines are parallel, compare the intercepts
                    if self.LinPieces[f'p{i}'][2] > self.LinPieces[f'p{j}'][2]:
                        self.MeetPoints[(f'p{i}', f'p{j}')] = [float('inf'), float('inf')]
                    else:
                        self.MeetPoints[(f'p{j}', f'p{i}')] = [float('inf'), float('inf')]
                    continue

                x = (self.LinPieces[f'p{j}'][2] - self.LinPieces[f'p{i}'][2]) / (self.LinPieces[f'p{i}'][1] - self.LinPieces[f'p{j}'][1])
                y = self.LinPieces[f'p{i}'][1] * x + self.LinPieces[f'p{i}'][2]
                x = round(x * (2 ** len(self.LinPieces))) / (2 ** len(self.LinPieces))
                y = round(y * (2 ** len(self.LinPieces))) / (2 ** len(self.LinPieces))
                if self.LinPieces[f'p{i}'][1] < self.LinPieces[f'p{j}'][1]:
                    self.MeetPoints[(f'p{i}', f'p{j}')] = [x, y]
                else:
                    self.MeetPoints[(f'p{j}', f'p{i}')] = [x, y]

    def MinMax(self): #perform min-max representation
        self.MinMaxs = {} # on each linear region, find max
        for i in range(len(self.xcords)-1):
            curLin = f'p{i}'
            curLinRegion = self.LinPieces[curLin]
            aboveCur = []  # list of linear pieces above the current linear piece
            belowCur = [] #list of linear pieces below the current linear piece

            for key in self.MeetPoints:
                if key[0] == curLin:
                    if self.MeetPoints[key][0] >= curLinRegion[0][1]:
                        belowCur.append(key[1])
                    if self.MeetPoints[key][0] <= curLinRegion[0][0]:
                        aboveCur.append(key[1])
                if key[1] == curLin:
                    if self.MeetPoints[key][0] <= curLinRegion[0][0]:
                        belowCur.append(key[0])
                    if self.MeetPoints[key][0] >= curLinRegion[0][1]:
                        aboveCur.append(key[0])
            self.MinMaxs[curLin] = [aboveCur, belowCur]







    def convert(self, method): #extract an mv term from each linear region
        self.MVs = {} #dictionary of MV terms, key = pi, value = 'MV term'
        if method == 'R&R':
            for key in self.LinPieces:
                curLin = key
                curMV = sigmaConstruct(self.LinPieces[curLin][1], self.LinPieces[curLin][2])
                self.MVs[curLin] = curMV
        elif method == 'aguzzoli':
            for key in self.LinPieces:
                curLin = key
                curMV = sigmaConstruct_agu(self.LinPieces[curLin][1], self.LinPieces[curLin][2])
                self.MVs[curLin] = curMV

    def compose(self):
        #first compose according to min max
        self.minmax = []
        for key in self.MinMaxs:
            maxs = Symbols.VEE.join(self.MinMaxs[key][1])
            if len(maxs) > 0:
                maxs = f"({maxs}{Symbols.VEE}{key})"
            else:
                maxs = key
            self.minmax.append(maxs)
        overallMVp = Symbols.WEDGE.join(self.minmax)
        self.overallMVp = overallMVp

        overallMV = overallMVp
        #replace all linear pieces by the associated MV terms
        for key in self.LinPieces:
            overallMV = overallMV.replace(key, f"({self.MVs[key]})")
        self.overallMV = overallMV
    def extract(self, method):
        self.findLinPieces()
        self.findMeetPoints()
        self.MinMax()
        self.convert(method)
        self.compose()







'''
xcords = [0, 0.25, 0.5, 0.75, 1]
ycords = [0, 1, 0, 1, 0]
test = hyperplane2MV(xcords, ycords)
test.findLinPieces()

test.findMeetPoints()
test.MinMax()
test.extract()
test.compose()
'''


