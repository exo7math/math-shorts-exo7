from manim import *
from manim.opengl import *

import numpy as np

from config_shorts_exo7 import *

# Constants
# speed = 1

# LOW RESOLUTION 
# cylinder_resolution = (1, 5) 
# axes_resolution = 3   
# dot3d_resolution= (4, 4) 

# HIGH RESOLUTION (for final video)
cylinder_resolution = (1, 32) 
axes_resolution = 8 
dot3d_resolution= (8, 8) 


# point_trail_length = 100  # video low resolution
# point_trail_length = 200  # video medium resolution
point_trail_length = 400  # video high resolution


# Colors
point1_color = '0xe8590c' # ORANGE 8
point2_color = '0xfd7e14' # ORANGE 6
cylinder_color = '0xfff9db'  # YELLOW 0  '0xf1f3f5'  # GRAY 1
# point_color = RED
color_logo_meta = '0x007ef7'  # some blue of the logo
color_text_meta = color_logo_meta  # some blue of the logo
curve_color = color_logo_meta
color_arrows = '0x868e96' # GRAY 6
plane_color = '0xffa8a8' # RED 3  #'0xc0eb75' # LIM

text_color = LIGHT_GRAY

# Fonts
font_shorts = "Open Sans" # "Noto Sans"  # "Times New Roman"
Tex.set_default(color=text_color, font_size=24, tex_template=TexFontTemplates.biolinum)


theta_proj = 0  # angle of the projection plane
zscale = 0.7    # vertical scale


##### LISSAJOU CURVES IN 3D #####

# Lissajous curve in space
def lissajous_3Dcurve(t, n=2, z0=0):
    x = np.cos(t)
    y = np.sin(t)
    z = zscale * (z0+np.sin(n*t))
    return [x, y, z]


##### PROJECTION #####
def projection(x, y, z, theta=0):
    """" Projection to the vertical plane with polar angle theta """
    dot_product = x*np.cos(theta) + y*np.sin(theta)
    
    # Projection sur la droite
    xx = dot_product * np.cos(theta)
    yy = dot_product * np.sin(theta)
    zz = z
    return [xx, yy, zz]


def projection_lissajous(t, n=2):
    """ Projection of the Lissajous curve on the vertical plane """
    x, y, z = lissajous_3Dcurve(t, n)
    r = -1.5
    vx, vy = -r*np.sin(theta_proj), r*np.cos(theta_proj)
    xx, yy, zz = projection(x, y, z, theta=theta_proj)

    return xx+vx, yy+vy, zz


# projection plane
def compute_plane(theta=0):
    """ Computatin of a vertical plane with polar angle theta """

    width, height, r = 1.6, 1.2, -1.5
    xA, yA = width*np.cos(theta), width*np.sin(theta)
    vx, vy = -r*np.sin(theta), r*np.cos(theta)

    mypolygon = [ [xA+vx, yA+vy, -height], [xA+vx, yA+vy, height], 
                 [-xA+vx, -yA+vy, height], [-xA+vx, -yA+vy, -height] ]

    return mypolygon



#### FADING PATH ####

# https://github.com/ManimCommunity/manim/issues/3854
TRAIL_LENGTH = config.frame_rate * 1.2  # Length of trail behind mercury
SCALE_FACTOR = 4                        # Manifold scaling factor
class FadingPath(VMobject):
    """
    Custom VMobject subclass to create a fading path trail.
    Contains an updater method to update each of its points.
    """

    def __init__(self,
                 traced_mobject: Mobject,
                 trail_length: int = TRAIL_LENGTH,
                 stroke_width: int = SCALE_FACTOR,
                 stroke_color: ManimColor = None,
                 **kwargs) -> None:
        super().__init__(**kwargs)
        if stroke_color is None:
            stroke_color = [PURE_BLUE, PINK]
        self.stroke_color = stroke_color
        self.stroke_width = stroke_width
        self.traced_mobject = traced_mobject
        self.trail_length = trail_length
        self.transparent_color = stroke_color[0] if isinstance(stroke_color, list) else stroke_color
        self.opaque_color = stroke_color[1] if isinstance(stroke_color, list) else stroke_color
        self.start_new_path(self.traced_mobject.get_center())
        self.add_updater(self.update_trace)

    def update_trace(self, mobj, dt):
        new_line = Line(self[-1].get_end(), self.traced_mobject.get_center())

        # calculate linear gradient function for opacity
        max_opacity = 1
        min_opacity = 0
        opacity_step = (max_opacity - min_opacity) / len(self)

        new_line.set_opacity(max_opacity)
        new_line.set_color(self.opaque_color)
        self.add(new_line)

        if len(self) > self.trail_length:
            for i, line in enumerate(self):
                if i in [0, 1]:
                    self.remove(line)

        for i, line in enumerate(self):
            # update opacity for each line in the path group
            new_opacity = min_opacity + i * opacity_step
            line.set_stroke(opacity=new_opacity)

            # update color of each line in the path group
            ratio = (i / len(self)) ** 2
            new_color = interpolate_color(self.transparent_color, self.opaque_color, ratio)
            line.set_color(new_color)


# fade out a scene
def fade_out(scene: Scene):
    animations = []
    for mobject in scene.mobjects:
        animations.append(FadeOut(mobject))
    scene.play(*animations, run_time=run_time_between_scenes)



#### SCENES ####

# Scene 1 : with a projection plane
def Scene1(scene : ThreeDScene):

    ##### TEXTS #####
    title = Text("Lissajous curves", color=text_color, font=font_shorts).scale(0.4).move_to([0,4.5,0])
    scene.add_fixed_in_frame_mobjects(title)
    # scene.play(Write(title))

    # Equations in Latex
    eq1 = Tex(r"$\left\{\begin{array}{l} x(t) \ = \ \cos\,(t) \\ y(t) \ = \ \sin\,(t) \\ z(t) \ = \  \sin\,(n t)\end{array}\right.$", color=text_color).scale(1).move_to([-1.5, -3.5, 0])
    eq2 = Tex(r"$n=2$", color=text_color).scale(1).move_to([1, -3.1, 0])
    eq3 = Tex(r"the ", r"Meta", r" logo", color=text_color).scale(1.1).move_to([1, -3.5, 0])
    eq3.set_color_by_tex("Meta", color_text_meta) 
    # eq4 = Tex(r"$n=3$", color=text_color).scale(1).move_to([1, -3.5, 0])

    eqn3 = Tex(r"$n=3$", color=text_color).scale(1).move_to([-2.5, 3, 0])
    eqn4 = Tex(r"$n=4$", color=text_color).scale(1).move_to([-2.5, 0, 0])
    eqn5 = Tex(r"$n=5$", color=text_color).scale(1).move_to([-2.5, -3.5, 0])    


    ##### AXES #####


    x_arrow = Arrow3D(start=np.array([-1.1, 0, 0]),
        end=np.array([1.4, 0, 0]),
        resolution=axes_resolution, thickness=0.007, height=0.15, base_radius=0.04, color=color_arrows)

    y_arrow = Arrow3D(start=np.array([0, -1.1, 0]),
                end=np.array([0, 1.4, 0]),
                resolution=axes_resolution, thickness=0.007, height=0.15, base_radius=0.04, color=color_arrows)

    z_arrow = Arrow3D(start=np.array([0, 0, -1.1]),
                end=np.array([0, 0, 1.3]),
                resolution=axes_resolution, thickness=0.007, height=0.15, base_radius=0.04, color=color_arrows)

    # 3D axes (slow)
    scene.add(x_arrow, y_arrow, z_arrow)


    ##### CAMERA #####

    # zoom out so we see the axes
    scene.set_camera_orientation(phi=20 * DEGREES, theta=-2 * DEGREES, zoom=0.75)

    # built-in updater which begins camera rotation
    scene.begin_ambient_camera_rotation(rate=0.15)
    # scene.begin_ambient_camera_rotation(rate=0.15, about="theta")




    ##### PLANE #####

    # Plane for the projection
    plane = Polygon(*compute_plane(theta_proj), 
                    color=plane_color, fill_opacity=0.3, stroke_opacity=0)
    scene.add(plane)

    ##### CYLINDER ##### 

    epsilon = 0.0
    cylinder = Cylinder(radius=1-epsilon, height=2.0, fill_opacity=0.3, stroke_opacity=0, 
                        checkerboard_colors=False, show_ends=False, resolution=cylinder_resolution)
    cylinder.set_color(cylinder_color)

    scene.add(cylinder)


    ##### POINTS #####

    # 3D variant of the Dot() object
    P = Dot3D(color=point1_color, resolution=dot3d_resolution).scale(0.6)    
    scene.add(P)

    PP = Dot3D(color=point2_color, resolution=dot3d_resolution).scale(0.4)
    scene.add(PP)  

    t_tracker = ValueTracker(0)
    # n_tracker = ValueTracker(2)

    P.add_updater(lambda x: x.move_to(lissajous_3Dcurve(t_tracker.get_value(), n=2)))
    PP.add_updater(lambda x: x.move_to(projection_lissajous(t_tracker.get_value(), n=2)))

    ##### CURVES #####
    Q = FadingPath(P, trail_length=point_trail_length, stroke_color=[DARK_BLUE, LIGHT_PINK], stroke_width=4)
    scene.add(Q)

    QQ = FadingPath(PP, trail_length=point_trail_length, stroke_color=[DARK_BLUE, LIGHT_PINK], stroke_width=3)
    scene.add(QQ)
    
    phi, theta, focal_distance, gamma, zoom = scene.camera.get_value_trackers()

   ##### RUN TIMES #####
    speed = 0.25
    runt1 = 4   # 4
    runt2 = 3   # 3
    runt3 = 4   # 4
    runt4 = 4   # 3
    runt51 = 3
    runt52 = 3.5

    sc1 = True
    sc2 = True
    sc3 = True
    sc4 = True
    sc5 = True

    ##### SCENE 1 : BEGIN #####
    if sc1:
        scene.play( 
                    phi.animate.set_value(75*DEGREES),
                    zoom.animate.set_value(1.7),
                    t_tracker.animate.set_value(speed*runt1*2*PI),
                    run_time=runt1, 
                    rate_func=linear
                ) 
    

    ##### SCENE 2 : EQUATION #####
    if sc2:
        scene.add_fixed_in_frame_mobjects(eq1)

        # scene 2.1: the text fade in
        scene.play( 
                    FadeIn(eq1),
                    t_tracker.animate.increment_value(speed*1*2*PI), 
                    run_time=1, 
                    rate_func=linear
                )
        
        # scene 2.2: the curve 
        scene.play( 
                    t_tracker.animate.increment_value(speed*(runt2-1)*2*PI), 
                    run_time=runt2-1, 
                    rate_func=linear
                )        


    ##### SCENE 3 : META TEXT #####
    if sc3:
        scene.add_fixed_in_frame_mobjects(eq2)
        scene.add_fixed_in_frame_mobjects(eq3)    

        # scene 3.1: the text fade in
        scene.play( 
                    FadeIn(eq2),
                    FadeIn(eq3),
                    t_tracker.animate.increment_value(speed*1*2*PI),
                    run_time=1,
                    rate_func=linear
                )
        
        # scene 3.2: the curve
        scene.play(
                    LaggedStart(              # LONG COMPUTATIONS
                        FadeOut(x_arrow, y_arrow, z_arrow),
                        FadeOut(cylinder),
                        FadeOut(Q),
                        lag_ratio=0.20
                    ),
                    FadeOut(P),
                    t_tracker.animate.increment_value(speed*(runt3-1)*2*PI),
                    run_time=runt3-1, 
                    rate_func=linear
                )


    scene.remove(P,Q)        
    scene.remove(cylinder)
    scene.remove(x_arrow, y_arrow, z_arrow)
    
    scene.begin_ambient_camera_rotation(rate=-0.15)
    
    ##### SCENE 4 : end of n=2  #####
    if sc4:

        scene.play( LaggedStart(
                        FadeOut(eq1, eq2, plane),
                        # FadeOut(eq3),               
                        lag_ratio=0.5
                    ),
                    t_tracker.animate.increment_value(speed*runt4*2*PI),
                    run_time=runt4, 
                    rate_func=linear
                ) 

        scene.play(
                    FadeOut(eq3), 
                    t_tracker.animate.increment_value(speed*0.5*2*PI),
                    run_time=0.5,
                    rate_func=linear
                )

    scene.remove(plane)
    scene.remove(eq1, eq2, eq3)
    scene.remove(PP, QQ)



    # ##### SCENE 5 : n=3, 4, 5 #####

    scene.begin_ambient_camera_rotation(rate=0.15)

    t_tracker = ValueTracker(0)  

    P3 = Dot3D(color=point1_color, resolution=dot3d_resolution).scale(0.5) 
    P3.add_updater(lambda x: x.move_to(lissajous_3Dcurve(t_tracker.get_value(), n=3, z0=3)))
    Q3 = FadingPath(P3, trail_length=point_trail_length, stroke_color=[DARK_BLUE, LIGHT_PINK], stroke_width=4)

    P4 = Dot3D(color=point1_color, resolution=dot3d_resolution).scale(0.5)    
    P4.add_updater(lambda x: x.move_to(lissajous_3Dcurve(t_tracker.get_value(), n=4, z0=0)))
    Q4 = FadingPath(P4, trail_length=point_trail_length, stroke_color=[DARK_BLUE, LIGHT_PINK], stroke_width=4)

    P5 = Dot3D(color=point1_color, resolution=dot3d_resolution).scale(0.5)    
    P5.add_updater(lambda x: x.move_to(lissajous_3Dcurve(t_tracker.get_value(), n=5, z0=-3.5)))
    Q5 = FadingPath(P5, trail_length=point_trail_length, stroke_color=[DARK_BLUE, LIGHT_PINK], stroke_width=4)


    if sc5:
        scene.add(P3)   
        scene.add(Q3)
        scene.add_fixed_in_frame_mobjects(eqn3)
        scene.play(  
                    Add(eqn3),
                    t_tracker.animate.increment_value(speed*runt51*2*PI),
                    zoom.animate.set_value(1.5),
                    run_time=runt51, 
                    rate_func=linear
                )  
        
        # # n = 4
        scene.add(P4)
        scene.add(Q4)
        scene.add_fixed_in_frame_mobjects(eqn4)
        scene.play( 
                    Add(eqn4),
                    t_tracker.animate.increment_value(speed*runt51*2*PI),
                    zoom.animate.set_value(1.3),
                    run_time=runt51, 
                    rate_func=linear
                )  

        # n = 5
        scene.add(P5)
        scene.add(Q5)
        scene.add_fixed_in_frame_mobjects(eqn5)
        scene.play( 
                    Add(eqn5),
                    t_tracker.animate.increment_value(speed*runt51*2*PI),
                    run_time=runt51, 
                    rate_func=linear
                )  
        
        scene.play( 
                    FadeOut(eqn3, eqn4, eqn5),
                    t_tracker.animate.increment_value(speed*1*2*PI),
                    run_time=1, 
                    rate_func=linear
                ) 
                 
        scene.play( 
                    t_tracker.animate.increment_value(speed*runt52*2*PI),
                    run_time=runt52, 
                    rate_func=linear
                ) 
        



# Regroup all scenes in one
class Lissajous(ThreeDScene):
    def construct(self):
        scenes = [Scene1]
        for scene in scenes:
            scene(self)
            # fade_out(self)
            self.clear()

