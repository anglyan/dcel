#!/usr/bin/env python
#Copyright Angel Yanguas-Gil, 2008.

"""

xygraph implements a 2D map formed by undirected edges between
vertices.
"""

__author__ = "Angel Yanguas-Gil"

import math as m

import iodata as tok
import pyeps as ps


class Xygraph:
    """Represents a set of vertices connected by undirected edges.
    The vertices are stored in a list of coordinates, while
    the edges are stored as a pair of indices (i,j) of the vertices
    list.
    """

    def __init__(self, vl=[], el=[]):
        """Creates the 2D graph formed by a list of vertices (x,y)
        and a list of indices (i,j)
        """
        self.vl = vl
        self.el = el
        if self.vl != []:
            self.minmax()

    def minmax(self):
        """Determines the boundary box of the vertices in the graph"""
        vx = [v[0] for v in self.vl]
        vy = [v[1] for v in self.vl]
        self.xmax, self.xmin = max(vx), min(vx)
        self.ymax, self.ymin = max(vy), min(vy)

    def clip(self, clipbox):
        """Trims the vertex and edge list of elements that lie
        outside a clipping box [(xmin,xmax),(ymin,ymax)]"""
        pmin, pmax = clipbox
        ind = []
        vlt = []
        #Direct elimination of out of bounds edges and vertices
        for i in range(len(self.vl)):
            if self.vl[i][0] < pmin[0] or self.vl[i][1] < pmin[1] or \
                self.vl[i][0] > pmax[0] or self.vl[i][1] > pmax[1]:
                ind.append(i)
            else:
                vlt.append(self.vl[i])
        elt = filter((lambda x:(x[0] not in ind) and (x[1] not in ind)),
            self.el) 
        li = filter((lambda x: x not in ind),range(len(self.vl)))
        #We rename the indices in the trimmed edge list
        lf = range(len(self.vl) - len(ind))
        equiv = {}
        for i in range(len(li)):
            if li[i] != lf[i]:
                equiv[li[i]] = lf[i]

        for i in range(len(elt)):
            if elt[i][0] in equiv:
                x = equiv[elt[i][0]]
            else:
                x = elt[i][0]
            if elt[i][1] in equiv:
                y = equiv[elt[i][1]]
            else:
                y = elt[i][1]
            elt[i] = (x,y)
        
        self.vl = vlt
        self.el = elt
        self.minmax()

    def load(self, filename):
        """loads a xygraph from filename. The structure of the
        file should be that given by save method.
        """

        data = tok.filetosheet(filename)
        if data is not None:
            nv = data[0][0]
            self.vl = data[1:nv+1]
            self.el = data[nv+1:]
            self.minmax()

    def save(self, filename):
        """saves a xygraph to filename"""
        file = open(filename,'w')
        file.write("%d\n" % len(self.vl))
        for v in self.vl:
            file.write("%f %f\n" % (v[0], v[1]))
        for e in self.el:
            file.write("%d %d\n" % e)
        file.close()

    def saveplot(self, filename=None, res=512):
        """
        Creates a PS representation of the xygraph. Saves
        the plot as an EPS file is filename is provided.
        """
        canvas = []
        offset = 50
        dx = self.xmax - self.xmin
        dy = self.ymax - self.ymin
        dl = max(dx, dy)
        r = float(res) / dl
        for i, j in self.el:
            x0 = int(r*(self.vl[i][0] - self.xmin)) + offset
            y0 = int(r*(self.vl[i][1] - self.ymin)) + offset
            x1 = int(r*(self.vl[j][0] - self.xmin)) + offset
            y1 = int(r*(self.vl[j][1] - self.ymin)) + offset
            canvas.append(ps.PSLine((x0,y0), (x1,y1)))
        up = res + 2*offset
        right = res + 2*offset
        fb = offset
        fu = res + offset
        frame = ps.PSPolygon([(fb, fb), (fu, fb), \
            (fu, fu), (fb, fu)], 1)
        canvas.append(frame)

        plot = ps.PSPlot(canvas)
        bound = ps.PSClip([(0, 0), (0, right),
            (up, 0), (up, right)])
        plot.setbound(bound)
        if filename is not None:
            plot.saveeps(filename)
        return plot

if __name__=='__main__':
    import sys
    g = Xygraph()
    if len(sys.argv) < 2:
        print "Use: xygraph filename"
    else:
        g.load(sys.argv[1])
        g.saveplot("newplot.eps")

