from manim import *
import numpy as np

from config_shorts_exo7 import *

# Constants
speed1 = 1
speed2 = 2*speed1
pi = np.pi

# Colors
point_color = '0x1098ad' # CYAN7
line_color = '0xe03131' # RED8
text_color = LIGHT_GRAY

Dot.set_default(color=point_color)

# Fonts
# font_shorts = "Times New Roman"
Tex.set_default(color=text_color, font_size=24, tex_template=TexFontTemplates.libertine)

# Run times of each scene
run_time_1 = 3
run_time_2 = 3
run_time_3 = 4
run_time_4 = 5
run_time_between_scenes = 0.2

# scale factor (1 = unit circle)


## Lagrange interpolation

# Elementary Lagrange polynomial
def L(x, i, A):
    p = 1
    for j in range(len(A)):
        if j != i:
            p *= (x-A[j])/(A[i]-A[j])
    return p

# Lagrange interpolation polynomial
def lagrange(x, points):
    # A = list of abscissas
    A = [P[0] for P in points]
    # B = list of ordinates
    B = [P[1] for P in points]
    polynom = 0
    for i in range(len(A)):
        polynom += B[i]*L(x, i, A)
    return polynom


# Scene 1: a line through two points
def graphe1(scene : Scene):
    title = Tex(r"Through two points passes a line").move_to([0,3,0])
    subtitle = Tex(r"$f(x) = ax + b$").move_to([0,2.5,0])

    ax = Axes(x_range = (-3, 3), y_range = (-2, 5), x_length=6, y_length=7)
    # ax.add_coordinates()

    tracker = ValueTracker(0)

    def t():
        return tracker.get_value()
    
    def point1(s):
        return -2, 0

    def point2(s):
        return 2, 0+2*s


    P1 = Dot(ax.coords_to_point(*point1(0)))
    P2 = Dot(ax.coords_to_point(*point2(0)))
    P2.add_updater(lambda x: x.move_to(ax.coords_to_point(*point2(t()))))


    global f1   # will be used in the next scene
    f1 = lambda x: lagrange(x, [point1(t()), point2(t())])


    graph = always_redraw(lambda: ax.plot(f1, color=line_color))

    scene.add(graph)
    scene.add(P1, P2)
    scene.add(title)  
    scene.add(subtitle)
    scene.play(tracker.animate(run_time=run_time_1).set_value(1))  


# Scene 2: a parabola through three points
def graphe2(scene : Scene):
    title = Tex(r"Through three points passes a parabola").move_to([0,3,0])
    subtitle = Tex(r"$f(x) = ax^2 + bx + c$").move_to([0,2.5,0])

    ax = Axes(x_range = (-3, 3), y_range = (-2, 5), x_length=6, y_length=7)

    tracker = ValueTracker(0)

    def t():
        return tracker.get_value()
    
    # x2, y2 = 0, f1(0)  # new point on the preceding line 
    # print(y2) # -> y2 = 1

    def point1(s):
        return -2, 0
    
    def point2(s):
        return 0, 1+2*s
    
    def point3(s):
        return 2, 2
    

    P1 = Dot(ax.coords_to_point(*point1(0)))
    P2 = Dot(ax.coords_to_point(*point2(0)))  # new point
    P3 = Dot(ax.coords_to_point(*point3(0)))
    P2.add_updater(lambda x: x.move_to(ax.coords_to_point(*point2(t()))))

    global f2
    f2 = lambda x: lagrange(x, [point1(t()), point2(t()), point3(t())])
    graph = always_redraw(lambda: ax.plot(f2, color=line_color))

    scene.add(graph)
    scene.add(P1, P3)
    scene.play(Create(P2))
    scene.add(title)  
    scene.add(subtitle)

    scene.play(tracker.animate(run_time=run_time_2).set_value(1))
    scene.play(tracker.animate(run_time=run_time_2).set_value(-1))


# Scene 3: a cubic through four points
def graphe3(scene : Scene):
    title = Tex(r"Through four points passes a cubic").move_to([0,3,0])
    subtitle = Tex(r"$f(x) = ax^3 + bx^2 + cx + d$").move_to([0,2.5,0])

    ax = Axes(x_range = (-3, 3), y_range = (-2, 5), x_length=6, y_length=7)

    tracker = ValueTracker(0)

    def t():
        return tracker.get_value()
    
    # x3, y3 = 1, f2(1)  # new point on the preceding parabola
    # print("==========", y3)  # -> y3 = 0
    
    # A = [-2+0.4*t, 0, 1, 2]
    # B = [0, -1-t, 0+2*t, 2]

    def point1(s):
        return -2+0.4*s, 0

    def point2(s):
        return 0, -1-s

    def point3(s):
        return 1, 0+2*s

    def point4(s):
        return 2, 2

    P1 = Dot(ax.coords_to_point(*point1(0)))
    P2 = Dot(ax.coords_to_point(*point2(0)))
    P3 = Dot(ax.coords_to_point(*point3(0)))  # new point on the preceding parabola
    P4 = Dot(ax.coords_to_point(*point4(0)))

    P1.add_updater(lambda x: x.move_to(ax.coords_to_point(*point1(t()))))
    P2.add_updater(lambda x: x.move_to(ax.coords_to_point(*point2(t()))))
    P3.add_updater(lambda x: x.move_to(ax.coords_to_point(*point3(t()))))


    global f3
    f3 = lambda x: lagrange(x, [point1(t()), point2(t()), point3(t()), point4(t())])
    # graph = always_redraw(lambda: ax.plot(f3, color=line_color, x_range=[-2.5, 2.4]))
    graph = always_redraw(lambda: ax.plot(f3, color=line_color))


    scene.add(graph)
    scene.add(P1, P2, P4)
    scene.play(Create(P3))
    scene.add(title)   
    scene.add(subtitle)

    scene.play(tracker.animate(run_time=run_time_3).set_value(0.45))
    scene.play(tracker.animate(run_time=run_time_3).set_value(-1))


# Scene 4: a polynomial of degree n through n+1 points
def graphe4(scene : Scene):
    title = Tex(r"Through $n+1$ points \\ passes a polynomial curve of degree $n$").move_to([0,3,0])
    subtitle = Tex(r"$f(x) = a_nx^n+a_{n-1}x^{n-1}+ \cdots + a_1x + a_0$").move_to([0,2.5,0])

    ax = Axes(x_range = (-3, 3), y_range = (-2, 5), x_length=6, y_length=7)

    tracker = ValueTracker(0)

    def t():
        return tracker.get_value()
    
    # x2, y2 = -1.5, f3(-1.5)  # new point on the preceding graph
    # print("==========", y2)  # -> y2 = 3.5464572192513373

    # x3, y3 = -0.7, f3(-0.7)  # new point on the preceding graph
    # print("==========", y3)  # -> y3 = 2.349772727272727  
    
    # A = [-2.4, -1.5, -0.7, 0, 1, 2]
    # B = [0, 3.546, 2.350, 0, -2, 2]

    def point1(s):
        return -2.4, 0
    
    def point2(s):
        return -1.5, 3.546 -1.10*s

    def point3(s):
        return -0.7, 2.350 -2.0*s

    def point4(s):
        return 0+0.2*s, 0+2.0*s

    def point5(s):
        return 1, -2+5.0*s
    
    def point6(s):
        return 2, 2 - 5*s

    P1 = Dot(ax.coords_to_point(*point1(0)))
    P2 = Dot(ax.coords_to_point(*point2(0)))
    P3 = Dot(ax.coords_to_point(*point3(0)))
    P4 = Dot(ax.coords_to_point(*point4(0)))
    P5 = Dot(ax.coords_to_point(*point5(0)))
    P6 = Dot(ax.coords_to_point(*point6(0)))

    P1.add_updater(lambda x: x.move_to(ax.coords_to_point(*point1(t()))))
    P2.add_updater(lambda x: x.move_to(ax.coords_to_point(*point2(t()))))
    P3.add_updater(lambda x: x.move_to(ax.coords_to_point(*point3(t()))))
    P4.add_updater(lambda x: x.move_to(ax.coords_to_point(*point4(t()))))
    P5.add_updater(lambda x: x.move_to(ax.coords_to_point(*point5(t()))))
    P6.add_updater(lambda x: x.move_to(ax.coords_to_point(*point6(t()))))


    ax.add_updater

 
    # global f4
    f4 = lambda x: lagrange(x, [point1(t()), point2(t()), point3(t()), point4(t()), point5(t()), point6(t())])

    graph = always_redraw(lambda: ax.plot(f4, color=line_color))

    scene.add(graph)
    scene.add(P1, P4, P5, P6)
    scene.play(Create(P2), Create(P3))

    scene.play(tracker.animate(run_time=run_time_4).set_value(1))

    scene.add(title)   
    scene.add(subtitle)

    scene.play(tracker.animate(run_time=run_time_4).set_value(0.6)) 
    # scene.play(tracker.animate(run_time=run_time_4).set_value(-1)) 




# Fade out a scene
def fade_out(scene: Scene):
    animations = []
    for mobject in scene.mobjects:
        animations.append(FadeOut(mobject))
    scene.play(*animations, run_time=run_time_between_scenes)


# Regroup all scenes in one
class Lagrange(Scene):
    def construct(self):
        scenes = [graphe1, graphe2, graphe3, graphe4]
        # scenes = [graphe1, graphe2, graphe3]
        for scene in scenes:
            scene(self)
            # fade_out(self)
            self.clear()

