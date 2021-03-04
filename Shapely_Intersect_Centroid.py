# -*- coding: utf-8 -*-
"""
Created on Mon Mar  1 13:32:48 2021

@author: Tianyu
"""

import numpy as np
import pylab as pl
from matplotlib import collections as mc
import matplotlib.pyplot as plt
from shapely.geometry import Polygon
from shapely.geometry import Point
from shapely.geometry import LineString

############################################################
""" Flat Rectangle
# L: side length of rec
# theta: rotation of rec
# Xm, Ym: translation of rec
# a, b: width and length of sensor 
# I: Indentation distance
# Rs: sensor surface radius
"""
"""
L = 40; theta = -20*np.pi/180; Xm = 8; Ym = 25; a = 16; b = 35; I = 0.2; Rs = 14;

Obj1 = Point(L/2*np.cos(theta) - L/2*np.sin(theta) + Xm, L/2*np.sin(theta) + L/2*np.cos(theta) + Ym)
Obj2 = Point(-L/2*np.cos(theta) - L/2*np.sin(theta)+ Xm, -L/2*np.sin(theta) + L/2*np.cos(theta)+ Ym) 
Obj3 = Point(-L/2*np.cos(theta) + L/2*np.sin(theta)+ Xm, -L/2*np.sin(theta) - L/2*np.cos(theta)+ Ym)
Obj4 = Point(L/2*np.cos(theta) + L/2*np.sin(theta)+ Xm, L/2*np.sin(theta) - L/2*np.cos(theta)+ Ym)
Object = Polygon([(Obj1.x, Obj1.y), (Obj2.x, Obj2.y), (Obj3.x, Obj3.y), (Obj4.x, Obj4.y)])

Sen1 = Point(L/2, L/2)
Sen2 = Point(L/2 + a, L/2)
Sen3 = Point(L/2 + a, L/2 + b)
Sen4 = Point(L/2, L/2 + b)
Sensor = Polygon([(Sen1.x, Sen1.y), (Sen2.x, Sen2.y), (Sen3.x, Sen3.y), (Sen4.x, Sen4.y)])

if I < 2.489:
    D = 2*sqrt(2*Rs*I - I**2)
else:
    D = 16
# contact area of invisible plane
CA1 = Point((Sen1.x + Sen2.x)/2 - D/2, Sen1.y)
CA2 = Point((Sen1.x + Sen2.x)/2 + D/2, Sen1.y)
CA3 = Point((Sen3.x + Sen4.x)/2 + D/2, Sen3.y)
CA4 = Point((Sen3.x + Sen4.x)/2 - D/2, Sen3.y)
CA = Polygon([(CA1.x, CA1.y), (CA2.x, CA2.y), (CA3.x, CA3.y), (CA4.x, CA4.y)])

IT = Object.intersection(CA)
CT = IT.centroid


lines = [[(Obj1.x, Obj1.y), (Obj2.x, Obj2.y)], [(Obj2.x, Obj2.y), (Obj3.x, Obj3.y)], 
          [(Obj3.x, Obj3.y), (Obj4.x, Obj4.y)], [(Obj4.x, Obj4.y), (Obj1.x, Obj1.y)], 
          [(Sen1.x, Sen1.y),(Sen2.x, Sen2.y)], [(Sen2.x, Sen2.y), (Sen3.x, Sen3.y)], 
          [(Sen3.x, Sen3.y), (Sen4.x, Sen4.y)], [(Sen4.x, Sen4.y), (Sen1.x, Sen1.y)]]
lc = mc.LineCollection(lines, linewidths = 1)
# middle line of sensor
lines2 = [[(0.5*(Sen1.x+Sen2.x), 0.5*(Sen1.y + Sen2.y)), (0.5*(Sen3.x + Sen4.x), 0.5*(Sen3.y + Sen4.y))]]
lc2 = mc.LineCollection(lines2, linewidths = 1, linestyle = 'dashdot')
# contact area of the sensor
lines3 = [[(CA1.x, CA1.y), (CA4.x, CA4.y)], [(CA2.x, CA2.y), (CA3.x, CA3.y)]]
lc3 = mc.LineCollection(lines3, linewidths = 1, linestyle = 'dashed')

fig,ax = pl.subplots()
ax.add_collection(lc)
ax.add_collection(lc2)
ax.add_collection(lc3)
if CT.is_empty == False:
    ax.plot(CT.x, CT.y, 'o', color = 'black', markersize = 5)
ax.autoscale()
ax.margins(0.1)
ax.grid()
ax.set_aspect('equal', 'box')
"""
###################################################################
""" Flat Triangle
# R: inscribed circle radius
# theta: rotation of rec
# Xm, Ym: translation of rec
# a, b: width and length of sensor
# I: Indentation distance
# Rs: sensor surface radius"""
"""
R = 20; theta = -10*np.pi/180; Xm = 14; Ym = 20; a = 16; b = 35; I = 0.5; Rs = 14;

Obj1 = Point( - R*np.sin(theta) + Xm,  R*np.cos(theta) + Ym) 
Obj2 = Point(-1.5*R/sqrt(3)*np.cos(theta) - (-0.5*R)*np.sin(theta)+ Xm, -1.5*R/sqrt(3)*np.sin(theta) + (-0.5*R)*np.cos(theta)+ Ym) 
Obj3 = Point(1.5*R/sqrt(3)*np.cos(theta) - (-0.5*R)*np.sin(theta)+ Xm, 1.5*R/sqrt(3)*np.sin(theta) + (-0.5*R)*np.cos(theta)+ Ym)
Object = Polygon([(Obj1.x, Obj1.y), (Obj2.x, Obj2.y), (Obj3.x, Obj3.y)])

Sen1 = Point(0, R)
Sen2 = Point(a, R)
Sen3 = Point(a, R+b)
Sen4 = Point(0, R+b)
Sensor = Polygon([(Sen1.x, Sen1.y), (Sen2.x, Sen2.y), (Sen3.x, Sen3.y), (Sen4.x, Sen4.y)])

if I < 2.489:
    D = 2*sqrt(2*Rs*I - I**2)
else:
    D = 16
# contact area of invisible plane
CA1 = Point((Sen1.x + Sen2.x)/2 - D/2, Sen1.y)
CA2 = Point((Sen1.x + Sen2.x)/2 + D/2, Sen1.y)
CA3 = Point((Sen3.x + Sen4.x)/2 + D/2, Sen3.y)
CA4 = Point((Sen3.x + Sen4.x)/2 - D/2, Sen3.y)
CA = Polygon([(CA1.x, CA1.y), (CA2.x, CA2.y), (CA3.x, CA3.y), (CA4.x, CA4.y)])

IT = Object.intersection(CA)
CT = IT.centroid


lines = [[(Obj1.x, Obj1.y), (Obj2.x, Obj2.y)], [(Obj2.x, Obj2.y), (Obj3.x, Obj3.y)], 
          [(Obj3.x, Obj3.y), (Obj1.x, Obj1.y)], 
          [(Sen1.x, Sen1.y),(Sen2.x, Sen2.y)], [(Sen2.x, Sen2.y), (Sen3.x, Sen3.y)], 
          [(Sen3.x, Sen3.y), (Sen4.x, Sen4.y)], [(Sen4.x, Sen4.y), (Sen1.x, Sen1.y)]]
lc = mc.LineCollection(lines, linewidths = 1)
# middle line of sensor
lines2 = [[(0.5*(Sen1.x+Sen2.x), 0.5*(Sen1.y + Sen2.y)), (0.5*(Sen3.x + Sen4.x), 0.5*(Sen3.y + Sen4.y))]]
lc2 = mc.LineCollection(lines2, linewidths = 1, linestyle = 'dashdot')
# contact area of the sensor
lines3 = [[(CA1.x, CA1.y), (CA4.x, CA4.y)], [(CA2.x, CA2.y), (CA3.x, CA3.y)]]
lc3 = mc.LineCollection(lines3, linewidths = 1, linestyle = 'dashed')

fig,ax = pl.subplots()
ax.add_collection(lc)
ax.add_collection(lc2)
ax.add_collection(lc3)
if CT.is_empty == False:
    ax.plot(CT.x, CT.y, 'o', color = 'black', markersize = 5)
ax.autoscale()
ax.margins(0.1)
ax.grid()
ax.set_aspect('equal', 'box')
"""

####################################################################

""" Flat Circle
# R: Radius of the circle
# Xm, Ym: translation of circle
# a, b: width and length of sensor 
# I: Indentation distance
# Rs: sensor surface radius """

"""
R = 20; Xm = -5; Ym = 10; a = 16; b = 35; I = 1.4; Rs = 14;

Object = Point(Xm, Ym).buffer(R)

Sen1 = Point(0, R)
Sen2 = Point(a, R)
Sen3 = Point(a, R + b)
Sen4 = Point(0, R + b)
Sensor = Polygon([(Sen1.x, Sen1.y), (Sen2.x, Sen2.y), (Sen3.x, Sen3.y), (Sen4.x, Sen4.y)])

if I < 2.489:
    D = 2*sqrt(2*Rs*I - I**2)
else:
    D = 16
# contact area of invisible plane
CA1 = Point((Sen1.x + Sen2.x)/2 - D/2, Sen1.y)
CA2 = Point((Sen1.x + Sen2.x)/2 + D/2, Sen1.y)
CA3 = Point((Sen3.x + Sen4.x)/2 + D/2, Sen3.y)
CA4 = Point((Sen3.x + Sen4.x)/2 - D/2, Sen3.y)
CA = Polygon([(CA1.x, CA1.y), (CA2.x, CA2.y), (CA3.x, CA3.y), (CA4.x, CA4.y)])

# intersection area
IT = Object.intersection(CA)
# center of the intersection area
CT = IT.centroid

lines = [[(Sen1.x, Sen1.y),(Sen2.x, Sen2.y)], [(Sen2.x, Sen2.y), (Sen3.x, Sen3.y)], 
          [(Sen3.x, Sen3.y), (Sen4.x, Sen4.y)], [(Sen4.x, Sen4.y), (Sen1.x, Sen1.y)]]
lc = mc.LineCollection(lines, linewidths = 1)
# middle line of sensor
lines2 = [[(0.5*(Sen1.x+Sen2.x), 0.5*(Sen1.y + Sen2.y)), (0.5*(Sen3.x + Sen4.x), 0.5*(Sen3.y + Sen4.y))]]
lc2 = mc.LineCollection(lines2, linewidths = 1, linestyle = 'dashdot')
# contact area of the sensor
lines3 = [[(CA1.x, CA1.y), (CA4.x, CA4.y)], [(CA2.x, CA2.y), (CA3.x, CA3.y)]]
lc3 = mc.LineCollection(lines3, linewidths = 1, linestyle = 'dashed')
circle = plt.Circle((Xm, Ym), R, color = 'blue', fill=False)

fig,ax = pl.subplots()
ax.add_collection(lc)
ax.add_collection(lc2)
ax.add_collection(lc3)
ax.add_patch(circle)
if CT.is_empty == False:
    ax.plot(CT.x, CT.y, 'o', color = 'black', markersize = 5)
ax.autoscale()
ax.margins(0.1)
ax.grid()
ax.set_aspect('equal', 'box')
"""

######################################################################

""" edge
# L: length of the edge 
# Xm, Ym: translation of circle
# a, b: width and length of sensor 
# I: Indentation distance
# Rs: sensor surface radius"""
"""
L = 40; theta = -20*np.pi/180; Xm = 10; Ym = 25; a = 16; b = 35; I = 1.5; Rs = 14;

Obj1 = Point(-L/2*np.sin(theta) + Xm, L/2*np.cos(theta) + Ym)
Obj2 = Point(L/2*np.sin(theta) + Xm, -L/2*np.cos(theta) + Ym) 
Object = LineString([(Obj1.x, Obj1.y), (Obj2.x, Obj2.y)])

Sen1 = Point(0, L/2)
Sen2 = Point(a, L/2)
Sen3 = Point(a, L/2 + b)
Sen4 = Point(0, L/2 + b)
Sensor = Polygon([(Sen1.x, Sen1.y), (Sen2.x, Sen2.y), (Sen3.x, Sen3.y), (Sen4.x, Sen4.y)])

if I < 2.489:
    D = 2*sqrt(2*Rs*I - I**2)
else:
    D = 16
# contact area of invisible plane
CA1 = Point((Sen1.x + Sen2.x)/2 - D/2, Sen1.y)
CA2 = Point((Sen1.x + Sen2.x)/2 + D/2, Sen1.y)
CA3 = Point((Sen3.x + Sen4.x)/2 + D/2, Sen3.y)
CA4 = Point((Sen3.x + Sen4.x)/2 - D/2, Sen3.y)
CA = Polygon([(CA1.x, CA1.y), (CA2.x, CA2.y), (CA3.x, CA3.y), (CA4.x, CA4.y)])

IT = Object.intersection(CA)
CT = IT.centroid


lines = [[(Obj1.x, Obj1.y), (Obj2.x, Obj2.y)],
          [(Sen1.x, Sen1.y),(Sen2.x, Sen2.y)], [(Sen2.x, Sen2.y), (Sen3.x, Sen3.y)], 
          [(Sen3.x, Sen3.y), (Sen4.x, Sen4.y)], [(Sen4.x, Sen4.y), (Sen1.x, Sen1.y)]]
lc = mc.LineCollection(lines, linewidths = 1)
# middle line of sensor
lines2 = [[(0.5*(Sen1.x+Sen2.x), 0.5*(Sen1.y + Sen2.y)), (0.5*(Sen3.x + Sen4.x), 0.5*(Sen3.y + Sen4.y))]]
lc2 = mc.LineCollection(lines2, linewidths = 1, linestyle = 'dashdot')
# contact area of the sensor
lines3 = [[(CA1.x, CA1.y), (CA4.x, CA4.y)], [(CA2.x, CA2.y), (CA3.x, CA3.y)]]
lc3 = mc.LineCollection(lines3, linewidths = 1, linestyle = 'dashed')

fig,ax = pl.subplots()
ax.add_collection(lc)
ax.add_collection(lc2)
ax.add_collection(lc3)
if CT.is_empty == False:
    ax.plot(CT.x, CT.y, 'o', color = 'black', markersize = 5)
ax.autoscale()
ax.margins(0.1)
ax.grid()
ax.set_aspect('equal', 'box')
"""
#############################################################
""" Ball Tip
# R: Radius of the tip surface
# Rt: Radius of the tip cylinder
# Xm, Ym: translation of the tip
# a, b: width and length of sensor 
# Rs: sensor surface radius"""

R = 13; Rt = 15/2; Xm = 10; Ym = Rt + 15; a = 16; b = 35; I = 1.5; Rs = 14;

if Xm < 0 or Xm > a:
    print("X position out of range")
if Ym < Rt or Ym > Rt+b:
    print("Y position out of range")

Object = Point(Xm, Ym).buffer(R)

Sen1 = Point(0, Rt)
Sen2 = Point(a, Rt)
Sen3 = Point(a, Rt + b)
Sen4 = Point(0, Rt + b)
Sensor = Polygon([(Sen1.x, Sen1.y), (Sen2.x, Sen2.y), (Sen3.x, Sen3.y), (Sen4.x, Sen4.y)])

CT = Point(Xm + R/(R+Rs)*(a/2-Xm),Ym)

lines = [[(Sen1.x, Sen1.y),(Sen2.x, Sen2.y)], [(Sen2.x, Sen2.y), (Sen3.x, Sen3.y)], 
          [(Sen3.x, Sen3.y), (Sen4.x, Sen4.y)], [(Sen4.x, Sen4.y), (Sen1.x, Sen1.y)]]
lc = mc.LineCollection(lines, linewidths = 1)
# middle line of sensor
lines2 = [[(0.5*(Sen1.x+Sen2.x), 0.5*(Sen1.y + Sen2.y)), (0.5*(Sen3.x + Sen4.x), 0.5*(Sen3.y + Sen4.y))]]
lc2 = mc.LineCollection(lines2, linewidths = 1, linestyle = 'dashdot')
circle = plt.Circle((Xm, Ym), Rt, color = 'blue', fill=False)

fig,ax = pl.subplots()
ax.add_collection(lc)
ax.add_collection(lc2)
ax.add_patch(circle)
ax.plot(CT.x, CT.y, 'o', color = 'black', markersize = 5)
ax.autoscale()
ax.margins(0.1)
ax.grid()
ax.set_aspect('equal', 'box')





