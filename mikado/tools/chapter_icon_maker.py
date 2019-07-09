#! -*- coding:utf-8 -*-

'''
Drawing Nice Geometric Shapes with Python
-----------------------------------------

I want to have nice looking "random" icons for things like chapter headings.
Sorta like cleaner gravatars

* should be able to draw a quartered large box, and populate each quadrant
  with blank or "something nice and geometrical".

Features:
   I define a large box, and within that 4 smaller ones can be calculated.
   Each box randomly chooses either
   "blank"
   or a curve, from diagonally opposite corners, linking to the centre
   curve is one of "straight", "wavy", "arc"
   and fill is any valid matplotlib color

Credits:
I saw this on someone's blog somewhere. I really cannot find the credit now
but I liked the nice quadrant / geometric look so I have attempted to recreate it.

Color:
see https://www.websitebuilderexpert.com/designing-websites/how-to-choose-color-for-your-website/ (v good)

https://jerichowriters.com/self-publish-book-amazon-kindle-kdp/#overview

'''
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Ellipse, PathPatch
import matplotlib.path
import matplotlib.colors
import random
import logging
log = logging.getLogger(__name__)
log.addHandler(logging.StreamHandler())
log.setLevel(logging.DEBUG)



def get_color(colortype='dominant'):
    """ """
    converter = matplotlib.colors.ColorConverter()
    colours = ['#f7d38b', '#e58bf7', '#8baff7']
    x = random.randint(0,2)
    return converter.to_rgba(colours[x], alpha=None)
    
def generate_ellipses():
    for i in range(10):
        
        plt = generate_ellipse()
        plt.savefig('images/ellipse_%s.png' % i, bbox_inches='tight')
    

def generate_ellipse():
    """This is a pretty and colourful way to generate a square ish image """
    NUM = 100

    ells = [Ellipse(xy=np.random.rand(2) * 10,
                    width=np.random.rand(), height=np.random.rand(),
                    angle=np.random.rand() * 360)
            for i in range(NUM)]

    fig, ax = plt.subplots(subplot_kw={'aspect': 'equal'})
    for e in ells:
        ax.add_artist(e)
        e.set_clip_box(ax.bbox)
        e.set_alpha(np.random.rand())
        e.set_facecolor(np.random.rand(3))

    ax.set_xlim(0, 10)
    ax.set_ylim(0, 10)

    plt.axis('off')
    return plt
    #plt.show()



def curve_in_box(BL, BR, TR, TL, curve='wavy', fill='none'):
    """
    I am drawing a curve from diagonally opposite corners of a box (square)
    and filling in one or other of the 'sides'.

    I a presuming square for now?
    # calc bezier control points as follows
    straight - striaght line bisecting into 2 triangles
    wavy     - two control points at mid point of each above triangles
    arc      - a single control point at same mid point.
    
    
    """
    Path = matplotlib.path.Path
    
    width = BR[0]-BL[0]
    height = TL[1]-BL[1]
    xorigin = BL[0]
    yorigin = BL[1]

    midpoint_top = (int(0.25*width)+xorigin, int(0.75*height)+yorigin)
    midpoint_right = (int(0.75*width)+xorigin, int(0.25*height)+yorigin)
    
    if curve == 'wavy':
        bc = Path([BL, TL, TR,
               midpoint_top, midpoint_right, BL, # CTRL CTRL ENDPOINT
                   BL],
                   [Path.MOVETO, Path.LINETO, Path.LINETO,
                    Path.CURVE4, Path.CURVE4, Path.CURVE4,
                    Path.CLOSEPOLY]
                   )
    elif curve == 'straight':
        bc = Path([BL, TL, TR,
                   BL, BL, BL,
                   BL],
                   [Path.MOVETO, Path.LINETO, Path.LINETO,
                    Path.CURVE4, Path.CURVE4, Path.CURVE4,
                    Path.CLOSEPOLY]
                   )
    elif curve == 'arc':
        bc = Path([BL, TL, TR,
                   TL, BL, #CONTROLPOINT ENDPOINT
                   BL],
                   [Path.MOVETO, Path.LINETO, Path.LINETO,
                    Path.CURVE3, Path.CURVE3,
                    Path.CLOSEPOLY]
                   )
    elif curve == 'none':
        bc = Path()
    else:
        raise RuntimeError("Bad curve value %s" % curve)
    
    pp = PathPatch(bc, fc=fill)
    return pp

def corners_from_origin(xyorigin, w,h):
    """ BL, BR, TR, TL 

    >>> corners_from_origin((0,0), 10,10)
    [(0, 0), (10, 0), (10, 10), (0, 10)]
  
    """
    return [ xyorigin,
             (xyorigin[0]+w, xyorigin[1]),
             (xyorigin[0]+w, xyorigin[1]+h),
             (xyorigin[0], xyorigin[1]+h)]
    
def getchoices():
    """choice is [type of curve, fill color] 
    type = none"""
    #weight the choices a bit
    curves = ['none', 'none', 'none', 'none', 'wavy', 'arc', 'straight']
    curve = curves[random.randint(0,len(curves)-1)]
    return [curve, get_color()]
            
def generate_boxes():
    """ 
    Two curves - pretty curve in the box
    curve that encloses some part of box like a pizza slice - oint at the centre point of all 4 boxes
    BL - Bottom Left etc
    CP - control point

"""
    #CONSTANTS
    quadrant_width = qw = 10
    quadrant_height = qh = 10
    EC = 'black'    
    
    fig = plt.figure(figsize=(1,1))
    plt.axes()
    origins = [(0,0), (qw,0), (qw,qh), (0,qh)]
    for i in range(4):
                            #origin, width, height, edge color, fill color
        sq1 = plt.Rectangle(origins[i], qw, qh, ec=EC, fc='none')
        plt.gca().add_patch(sq1)
        choices = getchoices() 
        log.info("CHoices are %s", str(choices))
        log.info("origin %s", repr(origins[i]))
        curve, fill = choices
        if curve != 'none':
            BL, BR, TR, TL = corners_from_origin(origins[i], qw, qh)
            pp = curve_in_box(BL, BR, TR, TL, curve=curve, fill=fill)
            plt.gca().add_patch(pp)
    plt.axis("scaled")
    plt.axis('off')
    return fig

def run():
    htmlfrag = ''
    for i in range(40):
        fig = generate_boxes()
        img = 'images/icon_%s.png' % i
        fig.savefig(img, bbox_inches='tight')
        htmlfrag += '<img src="{}">'.format(img)
    for i in range(10):
        htmlfrag += '<img src="images/ellipse_{}.png">'.format(i)
    html = "<html><body>{}</body></html>".format(htmlfrag)
    fo = open("foo.html", "w")
    fo.write(html)
    fo.close()
    
    
    
def test():
    import doctest
    doctest.testmod()

if __name__ == '__main__':
    #test()
    generate_ellipses()
    run()
