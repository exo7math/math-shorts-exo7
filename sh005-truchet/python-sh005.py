

from manim import *
import numpy as np

from config_shorts_exo7 import *

# Run times of each scene
run_time_1 = 3
run_time_2 = 3
run_time_3 = 4
run_time_4 = 3
run_time_5 = 3
run_time_6 = 4
run_time_7 = 5
run_time_between_scenes = 0.4


# Text
# font_shorts = "Times New Roman"
text_color = LIGHT_GRAY
Tex.set_default(color=text_color, font_size=24, tex_template=TexFontTemplates.libertine)
title_color = '0xffd43b'   # YELLOW4

# Colors
arc_col = 'white'
fill_col_1 = blue_exo7
fill_col_2 = red_exo7
fill_col_1_bis = TEAL_D
fill_col_2_bis = MAROON_E
edge_col = '0xAAAAAA'   # edge of the each boudary rectangle
no_fill_color = '0x777777'
vert_line_col = '0x1111dd'
hor_line_col = '0xdd1111'

# Truchet tiling


# Manim version
# Truchet tile: circle version
def truchet_tile_circle(P, c, arc=True, edge=False, fill=False, reverse=False):
    """ P center, c configuration """
    x, y = P
    r = 0.5 # radius

    if fill:
        col1, col2 = fill_col_1, fill_col_2
    else:
        col1, col2 = no_fill_color, no_fill_color

    if reverse:
        col1, col2 = col2, col1


    objects = []
    

    square = Square(side_length=1, fill_color=col2, fill_opacity=1, stroke_width=0).shift([0.5, 0.5, 0])
    objects.append(square)

    if c == 0:

        if fill:  
            arc1 = ArcPolygon([0,1,0], [0,1-r,0], [r,1,0], fill_color=col1, fill_opacity=1, stroke_width=0,  
                                        arc_config=[{'angle': 0, 'stroke_width': 0},
                                        {'radius': r, 'stroke_width': 0},
                                        {'angle': 0, 'stroke_width': 0}])
            arc2 = ArcPolygon([1,0,0], [1-r,0,0], [1,r,0], fill_color=col1, fill_opacity=1, stroke_width=0,   
                                        arc_config=[{'angle': 0, 'stroke_width': 0},
                                        {'radius': -r, 'stroke_width': 0},
                                        {'angle': 0, 'stroke_width': 0}])
            objects.append(arc1)
            objects.append(arc2)

        
        if arc:
            arc1 = Arc(start_angle=90*DEGREES, angle=90*DEGREES, radius=r, color=arc_col).shift([1, 0, 0])
            arc2 = Arc(start_angle=-90*DEGREES, angle=90*DEGREES, radius=r, color=arc_col).shift([0, 1, 0])
            objects.append(arc1)
            objects.append(arc2)
        
        
    elif c == 1:
        if fill:
            arc1 = ArcPolygon([0,0,0], [r,0,0], [0,r,0], fill_color=col1, fill_opacity=1, stroke_width=0,
                                    arc_config=[{'angle': 0, 'stroke_width': 0},
                                    {'radius': r, 'stroke_width': 0},
                                    {'angle': 0, 'stroke_width': 0}])  
            arc2 = ArcPolygon([1,1,0], [1-r,1,0], [1,1-r,0], fill_color=col1, fill_opacity=1, stroke_width=0,
                                    arc_config=[{'angle': 0, 'stroke_width': 0},
                                    {'radius': r, 'stroke_width': 0},
                                    {'angle': 0, 'stroke_width': 0}])
            objects.append(arc1)
            objects.append(arc2)

        if arc:
            arc1 = Arc(start_angle=0*DEGREES, angle=90*DEGREES, radius=r, color=arc_col).shift([0, 0, 0])
            arc2 = Arc(start_angle=180*DEGREES, angle=90*DEGREES, radius=r, color=arc_col).shift([1, 1, 0])
            objects.append(arc1)
            objects.append(arc2)

    if edge:
        square = Square(side_length=1, stroke_color=edge_col, stroke_width=4).shift([0.5, 0.5, 0])
        objects.append(square)

    return Group(*objects).shift([x, y, 0])


# Truchet tile: square version
def truchet_tile_square(P, c, arc=True, edge=False, fill=False, reverse=False):
    """ P center, c configuration """
    x, y = P
    r = 0.5 # radius

    if fill:
        col1, col2 = fill_col_1_bis, fill_col_2_bis
    else:
        col1, col2 = no_fill_color, no_fill_color

    if reverse:
        col1, col2 = col2, col1


    objects = []
    

    square = Square(side_length=1, fill_color=col2, fill_opacity=1, stroke_width=0).shift([0.5, 0.5, 0])
    objects.append(square)

    if c == 0:
        arc1 = Polygon([0,1,0], [0,1-r,0], [r,1,0], fill_color=col1, fill_opacity=1, stroke_width=0)
        arc2 = Polygon([1,0,0], [1-r,0,0], [1,r,0], fill_color=col1, fill_opacity=1, stroke_width=0)
        objects.append(arc1)
        objects.append(arc2)

        
        # if arc:
        #     arc1 = Arc(start_angle=90*DEGREES, angle=90*DEGREES, radius=r, color=arc_col).shift([1, 0, 0])
        #     arc2 = Arc(start_angle=-90*DEGREES, angle=90*DEGREES, radius=r, color=arc_col).shift([0, 1, 0])
        #     objects.append(arc1)
        #     objects.append(arc2)
        
        
    elif c == 1:
        arc1 = Polygon([0,0,0], [r,0,0], [0,r,0], fill_color=col1, fill_opacity=1, stroke_width=0)  
        arc2 = Polygon([1,1,0], [1-r,1,0], [1,1-r,0], fill_color=col1, fill_opacity=1, stroke_width=0)
        objects.append(arc1)
        objects.append(arc2)

        # if arc:
        #     arc1 = Arc(start_angle=0*DEGREES, angle=90*DEGREES, radius=r, color=arc_col).shift([0, 0, 0])
        #     arc2 = Arc(start_angle=180*DEGREES, angle=90*DEGREES, radius=r, color=arc_col).shift([1, 1, 0])
        #     objects.append(arc1)
        #     objects.append(arc2)

    if edge:
        square = Square(side_length=1, stroke_color=edge_col, stroke_width=4).shift([0.5, 0.5, 0])
        objects.append(square)

    return Group(*objects).shift([x, y, 0])




def display_grid_tiles(Nx, Ny, func_tile=truchet_tile_circle, seed=1, edge=False, arc=True, boundary=True, grid=False, fill=False):

    # Random rotation
    np.random.seed(seed)
    alea = np.random.randint(2, size=(Nx, Ny))

    objects = []

    # boundary rectangle
    if boundary:
        square = Rectangle(width=Nx, height=Ny, color=edge_col).shift([Nx/2, Ny/2, 0])
        objects.append(square)

    for j in range(Ny):
        for i in range(Nx):
            P = (i, j)
            c = alea[i, j]

            if (c==0) and ((i+j) % 2 == 0):
                reverse = False
            elif (c==0) and ((i+j) % 2 == 1):
                reverse = True
            elif (c==1) and ((i+j) % 2 == 0):
                reverse = True
            elif (c==1) and ((i+j) % 2 == 1):
                reverse = False
            

            tile = func_tile(P, c, arc=arc, edge=edge, fill=fill, reverse=reverse)
            objects += tile


    if grid:    # grid
        for i in range(Nx+1):
            line = Line([i, 0, 0], [i, Ny, 0], stroke_color=edge_col)
            objects.append(line)
        for j in range(Ny+1):
            line = Line([0, j, 0], [Nx, j, 0], stroke_color=edge_col)
            objects.append(line)

    return VGroup(*objects)

# display_grid_tiles(10, 10, grid=True)
# display_grid_tiles(3, 3, grid=False, fill=['lavenderblush', 'lightgreen'])


############ Test 1 ############

def test1(scene : Scene):
    title = Text("Title").move_to([0,4,0])

    # ax = Axes(x_range = [-1, 2], y_range = [-1, 2], x_length=3, y_length=3)
    # P = Dot(point=[0,0,0])
    # scene.add(P)

    # tile = truchet_tile((0,0), 0)
    # ax.add(Square(side_length=1, stroke_width=2))

    tile1 = truchet_tile_circle((-2,1), 0, arc=True, fill=False, reverse=False)
    tile2 = truchet_tile_circle((1,1), 1, arc=True, fill=False, reverse=False)
    tile3 = truchet_tile_circle((-2,-1), 0, arc=False, fill=True, reverse=False)
    tile4 = truchet_tile_circle((1,-1), 1, arc=True, fill=True, reverse=False)   
    # display_one_tile()

    scene.add(title)  

    scene.add(tile1)
    scene.add(tile2)
    scene.add(tile3)
    scene.add(tile4)

    scene.wait(2)
    # scene.play()


############ Test 2 ############

def test2(scene : Scene):
    title = Text("Title").move_to([0,4,0])
    
    Nx, Ny = 5, 5
    tiles = display_grid_tiles(Nx, Ny, arc=True, grid=True, fill=False).shift([-Nx/2, -Ny/2, 0]).scale(5/Nx)
    
    scene.add(title)
    scene.add(tiles)
    scene.wait(2)


############ Test 3 ############

def test3(scene : Scene):
    title = Text("Title").move_to([0,4,0])
    
    Nx, Ny = 7, 7
    tiles = display_grid_tiles(Nx, Ny, func_tile=truchet_tile_square, seed=5, arc=True, grid=True, fill=True).shift([-Nx/2, -Ny/2, 0]).scale(5/Nx)
    
    scene.add(title)
    scene.add(tiles)
    scene.wait(2)


############ Scene 1 ############

def scene1(scene : Scene):
    title = Text("Two tiles", color=title_color).scale(0.4).move_to([0,3.5,0])

    tile1 = truchet_tile_circle((-1.75,1.5), 0, arc=True, edge=True, fill=False, reverse=False)
    tile2 = tile1.copy()

    tile3 = tile1.copy().shift([2.5,0,0])

    arc = CurvedArrow(start_point=np.array([2,-2,0]),end_point=np.array([-2,2,0]), stroke_width=4, color=edge_col).scale(0.3).move_to([1.75,2.5,0])
    degree = Text("90°", color=edge_col).scale(0.25).move_to([2.25,3,0])


    scene.add(title)  

    scene.play(FadeIn(tile1))
    scene.add(tile1)
    scene.add(tile2)
    scene.play(Transform(tile1, tile3))
    scene.remove(tile1)

    scene.play(Rotate(tile3, angle=PI/2),
               FadeIn(arc),
               FadeIn(degree),
               run_time=2,
               rate_func=linear)  

    scene.wait(1)


############ Scene 2 ############
def scene2(scene : Scene):
    title = Text("and pick tiles at random", color=title_color).scale(0.25).move_to([0,0,0])

    scene.add(title)  
    
    Nx, Ny = 4, 4
    tiles = display_grid_tiles(Nx, Ny, seed=1, arc=True, edge=True, boundary=False, grid=False, fill=False).shift([-Nx/2, -Ny/2-2, 0]).scale(3/Nx)

    i = 0
    for tile in tiles:
        if i % 4 == 0:
            scene.wait(0.20)

        scene.add(tile)

        i += 1

    scene.wait(1.5)


 ############ Scene 3 ############

def scene3(scene : Scene):
    title = Text("This is called a Truchet tiling", color=title_color).scale(0.3).move_to([0,3.5,0])

    scene.add(title)  
    
    Nx, Ny = 10, 10
    tiles = display_grid_tiles(Nx, Ny, seed=2, arc=True, edge=False, boundary=False, grid=False, fill=False).shift([-Nx/2, -Ny/2, 0]).scale(5/Nx)

    i = 0
    for tile in tiles:
        if i % 3 == 0:
            scene.wait(0.07)

        scene.add(tile)

        i += 1    
    # scene.play(Create(tiles),run_time=run_time_2)

    scene.wait(2)   




############ Scene 4 ############

def scene4(scene : Scene):

    Nx, Ny = 12, 12
    tiles = display_grid_tiles(Nx, Ny, seed=4, arc=False, edge=False, boundary=False, grid=False, fill=True).shift([-Nx/2, -Ny/2, 0]).scale(5/Nx)

    i = 0
    for tile in tiles:
        if i % 3 == 0:
            scene.wait(0.045)

        scene.add(tile)

        i += 1  

    scene.wait(2)  

############ Scene 5 ############

def scene5(scene : Scene):


    Nx, Ny = 25, 25
    tiles = display_grid_tiles(Nx, Ny, func_tile=truchet_tile_square, seed=7, arc=False, edge=False, boundary=False, grid=False, fill=True).shift([-Nx/2, -Ny/2, 0]).scale(5/Nx)
    # scene.play(FadeIn(tiles), run_time=0.1)   

    i = 0
    for tile in tiles:
        if i % (3*Nx) == 0:
            scene.wait(0.17)

        scene.add(tile)

        i += 1  

    scene.wait(2)  
       

############ All scenes ############

# Fade out a scene
def fade_out(scene: Scene):
    animations = []
    for mobject in scene.mobjects:
        animations.append(FadeOut(mobject))
    scene.play(*animations, run_time=run_time_between_scenes)


# Regroup all scenes in one
class Truchet(Scene):
    def construct(self):
        scene1(self)
        scene2(self)  
        self.clear()  
        scene3(self)    
        self.clear()
        scene4(self)    
        self.clear()
        scene5(self)    

 