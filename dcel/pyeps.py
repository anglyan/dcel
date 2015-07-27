#! /usr/bin/env python
#Copyright 2008, Angel Yanguas-Gil

"""Crude ps and eps drawing of geometrical objects.

Geometrical objects are represented by PSClasses. These
are inserted in PSPlot, a container class with the
methods needed for saving the plots as ps and eps files.

Methods expects points passed as (x, y) pairs. 

"""


class PSPrimitive:
    """
    Abstract class containing basic PS commands.

    """

    def __init__(self, lc=[]):
        self.lc = []
    
    def __str__(self):
        return '\n'.join(self.lc)

    #State variables

    def create(self): pass
    
    def isplot(self): pass
    
    def istext(self): pass
        
    def isfilled(self): pass
    
    def isgroup(self): pass
    
    #Basic PS operations

    def newpath(self):
        return 'newpath'
    
    def lineto(self, x, y):
        return '%d %d lineto' % (x, y)
    
    def rlineto(self, x, y):
        return '%d %d rlineto' % (x, y)
    
    def arc(self, x, y, r, a1, a2):
        return '%d %d %d %d %d arc' %(x, y, r, a1, a2)
    
    def moveto(self, x, y):
        return '%d %d moveto' % (x, y)
    
    def stroke(self):
        return 'stroke'
    
    def gsave(self):
        return 'gsave'
    
    def grestore(self):
        return 'grestore'
    
    def fill(self):
        return 'fill'
    
    def setgray(self,x):
        return '%6.4f setgray' % x
    
    def setlinewidth(self, n):
        return '%d setlinewidth' % n
    
    def setdash(self,style):
        if style is 'dotted':
            s = '[1] 0 setdash'
        elif style is 'dashed':
            s = '[5] 0 setdash'
        return s
    
    def closepath(self):
        return 'closepath'


class PSLine(PSPrimitive):
    """Implements a straight line.

    Constructor keywords:
    p1, p2: 2D points.
    lwidth, lcolor and lstyles should contain PS values for
    width, color and linestyle.

    """
    def __init__(self, p1, p2, lwidth=1, lcolor=0, lstyle='full'):
        self.x1 = p1[0]
        self.y1 = p1[1]
        self.x2 = p2[0]
        self.y2 = p2[1]
        self.linecolor = lcolor
        self.linewidth = lwidth
        self.style = lstyle

        self.create()
    
    def create(self):
        self.lc = []
        self.lc.append(self.newpath())
        self.lc.append(self.moveto(self.x1, self.y1))
        self.lc.append(self.lineto(self.x2, self.y2))
        self.lc.append(self.setlinewidth(self.linewidth))
        self.lc.append(self.setgray(self.linecolor))
        if self.style is not 'full':
            self.lc.append(self.setdash(self.style))
        self.lc.append(self.stroke())

    def isplot(self):
        return True
     
    def istext(self):
        return False
    
    def isfilled(self):
        return False
    
    def isstroked(self):
        return True
    
    def isgroup(self):
        return False
    
class PSPolyline(PSPrimitive):
    """
    Implements a polyline.

    Constructor arguments:
    pl: list of points.
    lwidth, lcolor and lstyle should be PS values.

    """

    def __init__(self, pl, lwidth=1, lcolor=0, lstyle='full'):
        
        self.pl = pl
        self.np = len(pl)
        self.linecolor = lcolor
        self.linewidth = lwidth
        self.style = lstyle
        
        self.create()
    
    def create(self):
        self.lc = []
        self.lc.append(self.newpath())
        self.lc.append(self.moveto(self.pl[0][0], self.pl[0][1]))
        
        for p in self.pl[1:]:
            self.lc.append(self.lineto(p[0], p[1]))
        
        self.lc.append(self.setlinewidth(self.linewidth))
        self.lc.append(self.setgray(self.linecolor))
        if self.style is not 'full':
            self.lc.append(self.setdash(style))
        self.lc.append(self.stroke())

    def isplot(self):
        return True
     
    def istext(self):
        return False
    
    def isfilled(self):
        return False
    
    def isstroked(self):
        return True
    
    def isgroup(self):
        return False

class PSCircle(PSPrimitive):
    """
    Implements a circle.

    Constructor arguments:
    center: 2D point with the center of the circle
    rad: radius of the circle

    """

    def __init__(self, center, rad, lwidth=1, lcolor=0,
        lstyle='full', bcolor=1):
        self.c = center
        self.rad = rad
        self.linecolor = lcolor
        self.linewidth = lwidth
        self.style = lstyle
        self.bgcolor = bcolor
        
        self.create()
    
    def create(self):
        self.lc=[]
        self.lc.append(self.newpath())
        self.lc.append(self.moveto(self.c[0] + self.rad, self.c[1]))
        self.lc.append(self.arc(self.c[0], self.c[1], self.rad, 0, 360))
        if self.bgcolor is not 1:
            self.lc.append(self.gsave())
        self.lc.append(self.setlinewidth(self.linewidth))
        self.lc.append(self.setgray(self.linecolor))
        if self.style is not 'full':
            self.lc.append(self.setdash(style))
        self.lc.append(self.stroke())
        if self.bgcolor is not 1:
            self.lc.append(self.grestore())
            self.lc.append(self.setgray(self.bgcolor))
            self.lc.append(self.fill())

    def isplot(self):
        return True
     
    def istext(self):
        return False
    
    def isfilled(self):
        return False
    
    def isstroked(self):
        return True
    
    def isgroup(self):
        return False


class PSPolygon(PSPrimitive):
    """
    Implements a closed polygon.

    Constructor arguments:
    pl: list of points

    """

    def __init__(self, pl, lwidth=1, lcolor=0, lstyle='full', bcolor=1):
        self.pl = pl
        self.np = len(pl)
        self.linecolor = lcolor
        self.linewidth = lwidth
        self.style = lstyle
        self.bgcolor = bcolor
        
        self.create()
    
    def create(self):
        self.lc = []
        self.lc.append(self.newpath())
        self.lc.append(self.moveto(self.pl[0][0], self.pl[0][1]))
        
        for p in self.pl[1:]:
            self.lc.append(self.lineto(p[0], p[1]))
        self.lc.append(self.closepath())
        if self.bgcolor is not 1:
            self.lc.append(self.gsave())
        self.lc.append(self.setlinewidth(self.linewidth))
        self.lc.append(self.setgray(self.linecolor))
        if self.style is not 'full':
            self.lc.append(self.setdash(style))
        self.lc.append(self.stroke())
        if self.bgcolor is not 1:
            self.lc.append(self.grestore())
            self.lc.append(self.setgray(self.bgcolor))
            self.lc.append(self.fill())

    def isplot(self):
        return True
     
    def istext(self):
        return False
    
    def isfilled(self):
        return False
    
    def isstroked(self):
        return True
    
    def isgroup(self):
        return False


class PSClip(PSPrimitive):
    """
    Implements a polyline clipping boundary.

    Constructor arguments:
    pl: is a list with the points that define the clipping boundary.
    
    """    
    
    def __init__(self, pl):
        self.pl = pl

        self.create()
    
    def create(self):
        self.lc = []
        self.lc.append(self.newpath())
        self.lc.append(self.moveto(self.pl[0][0], self.pl[0][1]))
        for p in self.pl[1:]:
            self.lc.append(self.lineto(p[0], p[1]))
        self.lc.append(self.closepath())
        self.lc.append("clip")

    def isplot(self):
        return False
     
    def istext(self):
        return False
    
    def isfilled(self):
        return False
    
    def isstroked(self):
        return False
    
    def isgroup(self):
        return False


class PSPlot(PSPrimitive):
    """
    Container of PSPrimitives.
    
    It methods allow the creation of PS and EPS plots.
    Constructor argument:
    pslist: list of PSPrimitive objects.

    """
    
    def __init__(self, pslist):
        """A list of PSPrimitive objects is passed to PSPlot"""
        self.plist = pslist
        self.bounds = None
        self.create()

    def append(self, psobject):
        self.plist.append(psobject)
        self.create()

    def extend(self, pslist):
        self.plist.extend(pslist)
        self.create()
    
    def create(self):
        self.lc=[]
        self.lc.append(self.psstart())
        if self.bounds is not None:
            self.lc.append(self.bounds.__str__())
        for psel in self.plist:
            self.lc.append(psel.__str__())
        self.lc.append(self.psend())
    
    def psstart(self):
        return '%!'
    
    def setbound(self, clip):
        self.bounds = clip
        
    def psend(self):
        return 'showpage'
    
    def save(self, filename):
        """
        Saves the object as a PS image
        """
        f = open(filename, 'w')
        f.write(str(self) + '\n')
        
    def saveeps(self, filename):
        """
        Saves the object as an EPS image
        """
        if self.bounds is None:
            print "bounding box needed"
        else:
            xmin, xmax, ymin, ymax = 10000, -10000, 10000, -10000
            for p in self.bounds.pl:
                xmin = min(xmin, p[0])
                ymin = min(ymin, p[1])
                xmax = max(xmax, p[0])
                ymax = max(ymax, p[1])
            
            epshead = []
            epshead.append("%!PS-Adobe-3.0 EPSF-3.0")
            epshead.append("%%%%BoundingBox: %d %d %d %d" % 
                (xmin, ymin, xmax, ymax))
            epsfile = epshead
            epsfile.extend(self.lc[1:-1])
            f = open(filename, 'w')
            f.write('\n'.join(epsfile) + '\n')
            f.close()
            

