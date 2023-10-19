from fractions import Fraction
import math
from numpy import array,degrees,arctan2,dot,cross
pointsA=[]
pointsB=[]
edgesA=[]
edgesB=[]

class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y
    def __eq__(self, other):
        if isinstance(other, Point):
            return self.x == other.x and self.y == other.y
        return False

class Line(object):
    def __init__(self,startPoint,endPoint,slope,idx):
        self.startPoint = startPoint
        self.endPoint = endPoint
        self.slope = slope
        self.idx = idx
    
    def __eq__(self, other):
        if isinstance(other, Line):
            # Compare startPoint, endPoint, and slope attributes
            return (self.startPoint == other.startPoint and
                    self.endPoint == other.endPoint and
                    self.slope == other.slope and 
                    self.idx == other.idx)
        return False
    
    def __hash__(self):
        return hash((self.startPoint, self.endPoint, self.slope,self.idx))
    
    def is_startPoint(self, point):
        return point.x == self.startPoint.x and point.y == self.startPoint.y

    def is_endPoint(self, point):
        return point.x == self.endPoint.x and point.y == self.endPoint.y

def left_or_right(segment,point):
    A = (segment.startPoint.x - segment.endPoint.x) * (segment.startPoint.y - point.y)
    B = (segment.startPoint.y - segment.endPoint.y) * (segment.startPoint.x - point.x)
    cross_product = (A) - (B)
    if cross_product > 0:
        return "left"
    elif cross_product < 0:
        return "right"
    else:
        return "parallel"

def tVectorFinder(p,edgesA,edgesB,cond1=True,cond2=False,l=None):
    if (cond2 == False):
        edgeA= next(filter(lambda e: e.is_startPoint(p)  , edgesA))
        edgeB= next(filter(lambda e: e.is_startPoint(p)  , edgesB))
        if(left_or_right(edgeA,edgeB.endPoint) == "left"):
            return (edgeB.startPoint.x - edgeB.endPoint.x, edgeB.startPoint.y - edgeB.endPoint.y),edgeA.startPoint
        elif ((left_or_right(edgeA,edgeB.endPoint) == "right")):
            return (edgeA.endPoint.x - edgeA.startPoint.x, edgeA.endPoint.y - edgeA.startPoint.y),edgeA.endPoint
        else:
            return (edgeB.startPoint.x - edgeB.endPoint.x, edgeB.startPoint.y - edgeB.endPoint.y),edgeA.startPoint
    else:   
        if (cond1):
            return(l.endPoint.x - p.x, l.endPoint.y - p.y),l.endPoint 
        else: 
            return(p.x - l.endPoint.x , p.y - l.endPoint.y),p
        
def feasibleTV(polygonA,polygonB,edgesA,edgesB,vector,pointList):
    for point in pointList:
        translateV = Line(point[4],Point(point[4].x + vector[0],point[4].y + vector[1]),(((point[4].y + vector[1]) - point[4].y)/((point[4].x + vector[0]) - point[4].x)) if (point[4].x + vector[0] - point[4].x) != 0 else None,1)
        p = [point[4].x,point[4].y]
        if (polygonA.__contains__(p) and polygonB.__contains__(p)):
            startEA= next(filter(lambda e: e.is_startPoint(point[4]), edgesA))
            endEA= next(filter(lambda e: e.is_endPoint(point[4]), edgesA))
            startEB= next(filter(lambda e: e.is_startPoint(point[4]), edgesB))
            endEB= next(filter(lambda e: e.is_endPoint(point[4]), edgesB))
            angleEA = angle_finder(endEA,startEA)
            angleEB = angle_finder(endEB,startEB)
            bStartsize = (startEB.endPoint.x - startEB.startPoint.x, startEB.endPoint.y - startEB.startPoint.y)
            bEndsize = (endEB.endPoint.x - endEB.startPoint.x, endEB.endPoint.y - endEB.startPoint.y)
            mirrorSEB = Line(startEB.startPoint,Point(startEB.startPoint.x - bStartsize[0],startEB.startPoint.y - bStartsize[1]),startEB.slope,1)
            mirrorEEB = Line(Point(endEB.endPoint.x + bEndsize[0],endEB.endPoint.y + bEndsize[1]),endEB.endPoint,endEB.slope,1)
            bound1 = None
            bound2 = None
            if (angleEA < 180 and angleEB < 180):
                if (left_or_right(startEA,mirrorSEB.endPoint) == "left"):
                    bound1 = startEA
                else: 
                    bound1 = mirrorSEB
                if (left_or_right(endEA,mirrorEEB.startPoint) == "left"):
                    bound2 = endEA
                else:
                    bound2 = mirrorEEB
                if ((left_or_right(bound1,translateV.endPoint) == "left") and (left_or_right(bound2,translateV.endPoint) == "left")):
                    return False
                else:
                    pass
            elif (angleEA > 180 and angleEB < 180):
                if (left_or_right(startEA,mirrorSEB.endPoint) == "left"):
                    bound1 = startEA
                else: 
                    bound1 = mirrorSEB
                if (left_or_right(endEA,mirrorEEB.startPoint) == "left"):
                    bound2 = endEA
                else:
                    bound2 = mirrorEEB
                if (((left_or_right(bound1,translateV.endPoint) == "right") or (left_or_right(bound1,translateV.endPoint) == "parallel")) and ((left_or_right(bound2,translateV.endPoint) == "right") or (left_or_right(bound2,translateV.endPoint) == "parallel"))):
                    pass
                else:
                    return False
            elif (angleEB > 180 and angleEA < 180):
                if (left_or_right(startEA,mirrorSEB.endPoint) == "left"):
                    bound1 = startEA
                else: 
                    bound1 = mirrorSEB
                if (left_or_right(endEA,mirrorEEB.startPoint) == "left"):
                    bound2 = endEA
                else:
                    bound2 = mirrorEEB
                if (((left_or_right(bound1,translateV.endPoint) == "right") or (left_or_right(bound1,translateV.endPoint) == "parallel")) and ((left_or_right(bound2,translateV.endPoint) == "right") or (left_or_right(bound2,translateV.endPoint) == "parallel"))):
                    pass
                else:
                    return False
        elif (polygonA.__contains__(p)):
            Tvec = tVectorFinder(point[4],edgesA,edgesB,False,True,point[1])[0]
            pTvec = Line(point[4],Point(point[4].x + Tvec[0],point[4].y + Tvec[1]),(((point[4].y + Tvec[1]) - point[4].y)/((point[4].x + Tvec[0]) - point[4].x)) if ((point[4].x + Tvec[0]) - point[4].x) != 0 else None,1)
            if ((left_or_right(pTvec,translateV.endPoint) == "right") or (left_or_right(pTvec,translateV.endPoint) == "parallel")):
                pass
            else:
                return False
        else:
            Tvec = tVectorFinder(point[4],edgesA,edgesB,True,True,point[1])[0]
            pTvec = Line(point[4],Point(point[4].x + Tvec[0],point[4].y + Tvec[1]),(((point[4].y + Tvec[1]) - point[4].y)/((point[4].x + Tvec[0]) - point[4].x)) if ((point[4].x + Tvec[0]) - point[4].x) != 0 else None,1)
            if ((left_or_right(pTvec,translateV.endPoint) == "right") or (left_or_right(pTvec,translateV.endPoint) == "parallel")):
                pass
            else:
                return False
            
def find_intersection(line1,line2):
    x1 = Fraction(line1.startPoint.x)
    y1 = Fraction(line1.startPoint.y)
    x2 = Fraction(line1.endPoint.x)
    y2 = Fraction(line1.endPoint.y)
    x3 = Fraction(line2.startPoint.x)
    y3 = Fraction(line2.startPoint.y)
    x4 = Fraction(line2.endPoint.x)
    y4 = Fraction(line2.endPoint.y)
    cross_product = (x2 - x1) * (y4 - y3) - (y2 - y1) * (x4 - x3)

    if cross_product == 0:
        return None

    t1 = ((x4 - x3) * (y1 - y3) - (y4 - y3) * (x1 - x3)) / cross_product
    t2 = ((x2 - x1) * (y1 - y3) - (y2 - y1) * (x1 - x3)) / cross_product

    if 0 <= t1 <= 1 and 0 <= t2 <= 1:
        intersection_x = x1 + t1 * (x2 - x1)
        intersection_y = y1 + t1 * (y2 - y1)
        return Point(intersection_x,intersection_y)

    return None

def angle_finder(line1,line2):
    A = array([float(line1.startPoint.x), float(line1.startPoint.y)])
    B = array([float(line1.endPoint.x), float(line1.endPoint.y)])
    C = array([float(line2.startPoint.x), float(line2.startPoint.y)])
    D = array([float(line2.endPoint.x), float(line2.endPoint.y)])

    AB = B - A
    CD = D - C

    dot_product = dot(AB, CD)
    cross_product = cross(AB, CD)

    theta = arctan2(cross_product, dot_product)

    theta_degrees = degrees(theta)

    if theta_degrees < 0:
        theta_degrees += 360.0

    return theta_degrees

def vector_angle(line):
    vector_x = float(line[0])
    vector_y = float(line[1])

    angle_rad = math.atan2(vector_y, vector_x)
    if angle_rad < 0:
        angle_rad += 2 * math.pi

    angle_deg = math.degrees(angle_rad)
    return angle_deg
def lowest_key(polygon):
    lowest_key = min((point[1], point[0]) for point in polygon)
    lowest_key_points = next(filter(lambda point: (point[1], point[0]) == lowest_key, polygon))
    return lowest_key_points

def highest_key(polygon):
    highest_key = max((point[1], point[0]) for point in polygon)
    highest_key_points = next(filter(lambda point: (point[1], point[0]) == highest_key, polygon))
    return highest_key_points


def rotate_point(point,angle):
    x = point.x
    y = point.y
    alpha = math.radians(angle)
    x_rotated = x * math.cos(alpha) + y * math.sin(alpha)
    y_rotated = -x * math.sin(alpha) + y * math.cos(alpha)
    return (y_rotated)

def bounding(edge, tVector):
    if ((edge.slope == None or edge.slope == 0) or (tVector.slope == 0 or tVector.slope == None)):
        return True
    elif((min(edge.startPoint.x,edge.endPoint.x) <= max(tVector.startPoint.x,tVector.endPoint.x) and max(edge.startPoint.x,edge.endPoint.x) >= min(tVector.startPoint.x,tVector.endPoint.x) and
        min(edge.startPoint.y,edge.endPoint.y) <= max(tVector.startPoint.y,tVector.endPoint.y) and max(edge.startPoint.y,edge.endPoint.y) >= min(tVector.startPoint.y,tVector.endPoint.y))):
        return True
    else:
        return False

def distance(vector,point):

    temp1 = point.x - vector.endPoint.x
    temp2 = point.y - vector.endPoint.y
    result = math.sqrt(temp1**2 + temp2**2)
    return result


ntv=None
def trimmer(Points,filteredEdges,translateVector):
    global ntv
    ntv = translateVector
    for point in Points:
        tVec=((Line(Point(point[0],point[1]),Point(point[0] + ntv[0],point[1] + ntv[1]),
        (((point[1] + ntv[1] - point[1]))/((point[0] + ntv[0]) - point[0])) if ((point[0] + ntv[0]) - point[0]) != 0 else None,1)))
        for edge in filteredEdges:
            if bounding(tVec,edge):
                intersect = find_intersection(tVec,edge)
                if (intersect is not None):
                    if (not(edge.is_startPoint(intersect) or edge.is_endPoint(intersect)) or ((edge.is_startPoint(intersect) or edge.is_endPoint(intersect)) and (not(tVec.is_startPoint(intersect)) and not(tVec.is_endPoint(intersect))))):
                        if(not(tVec.is_startPoint(intersect) and  left_or_right(edge,tVec.endPoint)=="right") and (intersect.x != (tVec.startPoint.x + translateVector[0]) or intersect.y != (tVec.startPoint.y + translateVector[1]))):
                            ntv= ((intersect.x - tVec.startPoint.x), (intersect.y - tVec.startPoint.y))
                            trimmer(Points,filteredEdges,ntv)
                            break
    return ntv



def boundry(polygon,edges,vector):
    angle = vector_angle(vector)

    rotated_points =[]

    for point in polygon:
        rotated_points.append(rotate_point(Point(point[0],point[1]),angle))

    minVal = polygon[rotated_points.index(min(rotated_points))]
    maxVal = polygon[rotated_points.index(max(rotated_points))]
    seg1 = Line(Point(minVal[0],minVal[1]),Point(minVal[0] + vector[0],minVal[1] + vector[1]),0,1)
    seg2 = Line(Point(maxVal[0],maxVal[1]),Point(maxVal[0] + vector[0],maxVal[1] + vector[1]),0,1)
    filtered_edges = []
    for edge in edges:
        if(not 
           ((((left_or_right(seg1,edge.startPoint) == "left") and (left_or_right(seg1,edge.endPoint) == "left")) and ((left_or_right(seg2,edge.startPoint) == "left") and (left_or_right(seg2,edge.endPoint) == "left"))) 
           or
           (((left_or_right(seg1,edge.startPoint) == "right") and (left_or_right(seg1,edge.endPoint) == "right")) and ((left_or_right(seg2,edge.startPoint) == "right") and (left_or_right(seg2,edge.endPoint) == "right")))
           )):
            filtered_edges.append(edge)
    return filtered_edges

def is_point_on_segment(point,line):
    min_y=min(line.startPoint.y,line.endPoint.y)
    max_y=max(line.startPoint.y,line.endPoint.y)
    min_x=min(line.startPoint.x,line.endPoint.x)
    max_x=max(line.startPoint.x,line.endPoint.x)
    if left_or_right(line,point) == "parallel":
        if ((point.x >= min_x)and(point.x <= max_x) and (point.y >= min_y) and (point.y <= max_y)):
            return point
        else:
            return None

def trimFun(polygonM,filteredES,translateV,p):
    tVectors = []
    infos= []
    intersection = None
    for point in polygonM:
        tVectors.append((Line(Point(point[0],point[1]),Point(point[0] + translateV[0],point[1] + translateV[1]),
        (((point[1] + translateV[1] - point[1]))/((point[0] + translateV[0]) - point[0])) if ((point[0] + translateV[0]) - point[0]) != 0 else None,1)))
    for i,point1 in enumerate(polygonM):
        tVector=Point(point1[0],point1[1])
        for j,edge in enumerate(filteredES):
            intersection = is_point_on_segment(tVector,edge)
            if intersection is not None:
                nTv =translateV
                if (edge.is_startPoint(intersection)):
                    infos.append([Point(polygonM[i][0], polygonM[i][1]),filteredES[j],p,False,intersection,i,edge.idx])
                elif (edge.is_endPoint(intersection)):
                    infos.append([Point(polygonM[i][0], polygonM[i][1]),filteredES[j],p,False,intersection,i,edge.idx])
                else:
                    infos.append([Point(polygonM[i][0], polygonM[i][1]),edge,p,True,intersection,i,edge.idx])

    return (infos)

def NFP(polygonA,polygonB):
    polygonB2=polygonB[:]
    a_RefPoint = lowest_key(polygonA)
    b_highPoint = highest_key(polygonB)
    diff_vec = (b_highPoint[0]-a_RefPoint[0], b_highPoint[1] - a_RefPoint[1])
    polygonB2= [[x - diff_vec[0], y - diff_vec[1]] for x,y in polygonB2]
    y=0
    nfp = []
    x=(None,None)
    wCond = lowest_key(polygonB2)
    point = Point(a_RefPoint[0],a_RefPoint[1])
    edgesA = [Line(Point(a[0],a[1]),Point(b[0],b[1]),((b[1] - a[1])/(b[0] - a[0])) if (b[0] - a[0]) != 0 else None,idx)  for idx, (a, b) in enumerate(zip(polygonA, polygonA[1:] + [polygonA[0]]))] 
    edgesB = [Line(Point(a[0],a[1]),Point(b[0],b[1]),((b[1] - a[1])/(b[0] - a[0])) if (b[0] - a[0]) != 0 else None,idx)  for idx, (a, b) in enumerate(zip(polygonB2, polygonB2[1:] + [polygonB2[0]]))] 

    nextTv =  tVectorFinder(point,edgesA,edgesB)[0]
    edgeA= next(filter(lambda e: e.is_startPoint(point)  , edgesA))
    edgeB= next(filter(lambda e: e.is_startPoint(point)  , edgesB))
    p = Point(point.x + nextTv[0],point.y + nextTv[1])
    if(edgeA.is_endPoint(p)):
        next_info = [point,edgeA,True,False,p,polygonA.index([point.x,point.y])]
    else:
        next_info = [point,edgeB,False,False,p,polygonB2.index([point.x,point.y])]



    cEdgesList = set()
    while (((x[0] != wCond[0]) or(x[1] != wCond[1]) or y <2)):
        edgesB = [Line(Point(a[0],a[1]),Point(b[0],b[1]),((b[1] - a[1])/(b[0] - a[0])) if (b[0] - a[0]) != 0 else None,idx)  for idx, (a, b) in enumerate(zip(polygonB2, polygonB2[1:] + [polygonB2[0]]))] 

        filteredEdgesA = boundry(polygonB2,edgesA,nextTv)
        filteredEdgesB = boundry(polygonA,edgesB,(-nextTv[0],-nextTv[1]))
        t1 = trimmer(polygonB2,filteredEdgesA,nextTv)
        t2 = trimmer(polygonA,filteredEdgesB,(-t1[0],-t1[1]))

        if((-t2[0],-t2[1]) == nextTv):
            if(next_info[3]):
                if (next_info[2]):
                    cEdgesList.add(next_info[1].idx)
            else:
                if (next_info[2]):
                    edgeA= next(filter(lambda e: e.is_startPoint(point)  , edgesA))
                    edgeB= next(filter(lambda e: e.is_startPoint(point)  , edgesB))
                    p = Point(point.x + -t2[0],point.y + -t2[1])
                    if(edgeA.is_endPoint(p)):
                        cEdgesList.add(edgeA.idx)
                else:
                    edgeA= next(filter(lambda e: e.is_startPoint(point)  , edgesA))
                    edgeB= next(filter(lambda e: e.is_startPoint(point)  , edgesB))
                    p = Point(point.x + -t2[0],point.y + -t2[1])
                    if(edgeA.is_endPoint(p)):
                        cEdgesList.add(edgeA.idx)

        polygonB2 = [[x + (-t2[0]), y + (-t2[1])] for x, y in polygonB2]
        trim1 = trimFun(polygonB2,filteredEdgesA,(-t2[0],-t2[1]),True)
        edgesB2 = [Line(Point(a[0],a[1]),Point(b[0],b[1]),((b[1] - a[1])/(b[0] - a[0])) if (b[0] - a[0]) != 0 else None,idx)  for idx, (a, b) in enumerate(zip(polygonB2, polygonB2[1:] + [polygonB2[0]]))]
        filteredEdgesB2 = boundry(polygonA,edgesB2,(-t2[0],-t2[1]))


        trim2 = trimFun(polygonA,filteredEdgesB2,t2,False)
        vecList = []
        nfp.append(lowest_key(polygonB2))

        idealTV=[]
        trimResults = trim1 + trim2

        for i,info in enumerate(trimResults):
            possibleNextVector = tVectorFinder(info[4],edgesA,edgesB2,info[2],info[3],info[1])[0]
            vecList.append(possibleNextVector)

        
        for j,vector in enumerate(vecList):
            if(feasibleTV(polygonA,polygonB2,edgesA,edgesB2,vector,trimResults) == False):
                pass
            else:
                idealTV.append((vector,trimResults[j][4],trimResults[j]))
        
        distanceL = []
        for l in idealTV:
            tvec = Line(point,Point(point.x + (-t2[0]/2),point.y + (-t2[1]/2)),5,1)
            distanceL.append(distance(tvec,l[1]))
        index = distanceL.index(min(distanceL))
        next_info = idealTV[index][2]
        nextTv = idealTV[index][0]
        point = idealTV[index][1]
        x = nfp[-1]
        y += 1

    return [(x[0],x[1]) for x in nfp]