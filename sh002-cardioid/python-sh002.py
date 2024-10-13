from manim import *
import numpy as np

from config_shorts_exo7 import *

# Constants
speed1 = 1
speed2 = 2*speed1
pi = np.pi

# Colors
point1_color = '0x82c91e' # LIME 6
point2_color = '0xfd7e14' # ORANGE 6
line_color = LIGHT_GRAY
circle_color = GRAY
text_color = LIGHT_GRAY

# Fonts
font_shorts = "Open Sans" # "Noto Sans"  # "Times New Roman"

# Run times of each scene
run_time_1 = 4
run_time_2 = 4
# run_time_3 = 4
run_time_4 = 4
# run_time_5 = 10
# run_time_between_scenes = 0.2

# scale factor (1 = unit circle)
myscale = 1.8


# Usefull function
def cossin(t):
    return (myscale*np.cos(-pi/2+2*pi*t), myscale*np.sin(-pi/2+2*pi*t), 0)

# fade out a scene
def fade_out(scene: Scene):
    animations = []
    for mobject in scene.mobjects:
        animations.append(FadeOut(mobject))
    scene.play(*animations, run_time=run_time_between_scenes)

# Scene 1
def OnePoint(scene : Scene):
    title = Text("Point P: speed 1", color=text_color, font=font_shorts).scale(0.4).move_to([0,3,0])
    scene.add(title)

    circle = Circle(radius=1, color=circle_color).scale(myscale)
    P = Dot(color=point1_color).scale(1.2)
    scene.add(circle)
    scene.add(P)

    t_tracker = ValueTracker(0)
    P.add_updater(lambda x: x.move_to(cossin(speed1*t_tracker.get_value())))

    scene.play(t_tracker.animate.set_value(1), run_time=run_time_1, rate_func=linear) 
    # scene.wait()


# Scene 2
def OtherPoint(scene : Scene):
    title = Text("Point Q: speed 2", font=font_shorts, color=text_color).scale(0.4).move_to([0,3,0])
    scene.add(title)

    circle = Circle(radius=1, color=circle_color).scale(myscale)
    Q = Dot(color=point2_color).scale(1.2)
    scene.add(circle)
    scene.add(Q)

    t_tracker = ValueTracker(0)
    Q.add_updater(lambda x: x.move_to(cossin(speed2*t_tracker.get_value())))

    scene.play(t_tracker.animate.set_value(1), run_time=run_time_2, rate_func=linear)
    # scene.wait()


# Scene 3
def TwoPoints(scene : Scene):
    title = Text("Points P and Q", font=font_shorts, color=text_color).scale(0.4).move_to([0,3,0])
    scene.add(title)

    circle = Circle(radius=1, color=circle_color).scale(myscale)
    P = Dot(color=point1_color).scale(1.2)
    Q = Dot(color=point2_color).scale(1.2)
    scene.add(circle)
    scene.add(P)
    scene.add(Q)

    t_tracker = ValueTracker(0)
    P.add_updater(lambda x: x.move_to(cossin(speed1*t_tracker.get_value())))
    Q.add_updater(lambda x: x.move_to(cossin(speed2*t_tracker.get_value())))

    scene.play(t_tracker.animate.set_value(1), run_time=run_time_3, rate_func=linear)
    # scene.wait()


# Scene 4
def OneLine(scene : Scene):
    title = Text("Line between P and Q", font=font_shorts, color=text_color).scale(0.4).move_to([0,3,0])
    scene.add(title)

    circle = Circle(radius=1, color=circle_color).scale(myscale)
    P = Dot(color=point1_color).scale(1.2)
    Q = Dot(color=point2_color).scale(1.2)
    line = always_redraw(lambda: Line(start=P.get_center(), end=Q.get_center(), color=line_color))
    line.set_z_index(P.get_z_index()-1)
    scene.add(circle)
    scene.add(P)
    scene.add(Q)
    scene.add(line)


    t_tracker = ValueTracker(0)

    P.add_updater(lambda x: x.move_to(cossin(speed1*t_tracker.get_value())))
    Q.add_updater(lambda x: x.move_to(cossin(speed2*t_tracker.get_value())))

    scene.play(t_tracker.animate.set_value(1), run_time=run_time_4, rate_func=linear)
    # scene.wait()


# Scene 5 (and 6)
def AllLines(scene : Scene, Nlines=50, erase=False, with_title=True, total_time=2, wait_time=0):
    if with_title:
        title = Text("A  Cardioid", font=font_shorts, color=text_color).scale(0.4).move_to([0,3,0])
        scene.add(title)

    circle = Circle(radius=1, color=circle_color, stroke_width=3).scale(myscale)
    P = Dot(color=point1_color)
    Q = Dot(color=point2_color)
    
    line = always_redraw(lambda: Line(start=P.get_center(), end=Q.get_center(), color=line_color, stroke_width=3))
    line.set_z_index(P.get_z_index()-1)
    scene.add(circle)
    scene.add(P)
    scene.add(Q)
    scene.add(line)

    # delta_t = 0.1 # time between drawing a line between the two points
    # Nlines = 50 
    delta_t = 1/Nlines
    t_tracker = ValueTracker(0)
    end_t = delta_t

    for _ in range(Nlines):
        P.add_updater(lambda x: x.move_to(cossin(speed1*t_tracker.get_value())))
        Q.add_updater(lambda x: x.move_to(cossin(speed2*t_tracker.get_value())))        
        scene.play(t_tracker.animate.set_value(end_t), run_time=total_time*delta_t, rate_func=linear)
        trace_line = Line(start=P.get_center(), end=Q.get_center(), color=line_color, stroke_width=1)
        scene.add(trace_line)
        end_t += delta_t
    
    # scene.remove(P)
    # scene.remove(Q)

    if wait_time > 0:
        scene.play(FadeOut(P,Q), run_time=0.5)
        scene.wait(wait_time-0.5)


# Regroup all scenes in one
class Cardioid(Scene):
    def construct(self):
        scenes = [OnePoint, 
                  OtherPoint, 
                  # TwoPoints, 
                  OneLine, 
                  lambda s: AllLines(s, Nlines=50, with_title=False, total_time=3), 
                  lambda s: AllLines(s, Nlines=100, with_title=True, total_time=6, wait_time=3)]
        # scenes = [OnePoint, OtherPoint, TwoPoints, OneLine]
        # scenes = [OnePoint]
        for scene in scenes:
            scene(self)
            # fade_out(self)
            self.clear()

