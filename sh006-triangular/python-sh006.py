

from manim import *
import numpy as np

from config_shorts_exo7 import *

# Run times of each scene
run_time_1 = 3
run_time_2 = 3
run_time_3 = 4
run_time_4 = 3
run_time_between_scenes = 0.4

# Colors
arrow_col = GRAY
grid_color_1 = '0x66a80f'  # LIME 8
grid_color_2 = '0xf08c00'  # YELLOW 8
grid_color_3 = '0x099268'  # TEAL 8 
# grid_color_3 = '0xab9a08'  # mix of YELLOW 8 and LIME 8
# grid_color_3 = '0xb29e05'  # mix of YELLOW 8 and LIME 8


# Text
# font_shorts = "Times New Roman"
text_color = LIGHT_GRAY

Tex.set_default(color=text_color, font_size=24, tex_template=TexFontTemplates.libertine)

# 
Line.set_default(stroke_width=2.5)

# Scale
myscale = 0.25

############ Rectangle ############

def rectangle(n, dashed=False, color=WHITE):
    objects = []

    if not dashed:
        line1 = Line([0,0,0], [0,n,0], color=color)
        line2 = Line([1,0,0], [1,n,0], color=color)
    else:
        line1 = DashedLine([0,0,0], [0,n,0], color=color)
        line2 = DashedLine([1,0,0], [1,n,0], color=color)

    objects.append(line1)
    objects.append(line2)

    for i in range(n+1):
        if not dashed:
            line = Line([0,i,0], [1,i,0], color=color)
        else:
            line = DashedLine([0,i,0], [1,i,0], color=color)
        objects.append(line)

    group = Group(*objects)
    # group.set_x(0)
    # group.set_y(0)
    # group.set_z(0)

    return group


def grid(n, color=WHITE):
    objects = []

    for i in range(n+2):
        line1 = Line([0,i,0], [n,i,0], color=color)
        objects.append(line1)
    for j in range(n+1):
        line2 = Line([j,0,0], [j,n+1,0], color=color)
        objects.append(line2)

    group = Group(*objects)
    return group



############ Scene 1 ############

def scene1(scene : Scene):
    title = Tex(r"Sum of the first integers").move_to([0,3.6,0])
    scene.add(title)

    bottom = []
    figs = []

    i = 1        
    rect = rectangle(i, dashed=False, color=grid_color_1).scale(myscale).move_to([myscale*(4+i),myscale*i/2-1,0])
    bottom.append(rect)
    fig = Tex(r"$1$").scale(1.0).move_to([myscale*i-2.5,-1.8,0])
    figs.append(fig)
    scene.add(rect)
    scene.play(rect.animate.move_to([myscale*i-2.5,myscale*i/2-1,0]), 
                FadeIn(fig, rate_func=rate_functions.ease_in_quart),
                run_time=1)
    
    i = 2
    rect = rectangle(i, dashed=False, color=grid_color_1).scale(myscale).move_to([myscale*(4+i),myscale*i/2-1,0])
    bottom.append(rect)
    fig = Tex(r"$2$").scale(1.0).move_to([myscale*i-2.5,-1.8,0])
    figs.append(fig)
    scene.add(rect)
    scene.play(rect.animate.move_to([myscale*i-2.5,myscale*i/2-1,0]), 
                FadeIn(fig, rate_func=rate_functions.ease_in_quart),
                run_time=1)

    i = 3
    rect = rectangle(i, dashed=False, color=grid_color_1).scale(myscale).move_to([myscale*(4+i),myscale*i/2-1,0])
    bottom.append(rect)
    fig = Tex(r"$3$").scale(1.0).move_to([myscale*i-2.5,-1.8,0])
    figs.append(fig)
    scene.add(rect)
    scene.play(rect.animate.move_to([myscale*i-2.5,myscale*i/2-1,0]), 
                FadeIn(fig, rate_func=rate_functions.ease_in_quart),
                run_time=1)

    i = 4
    rect = rectangle(i, dashed=False, color=grid_color_1).scale(myscale).move_to([myscale*(4+i),myscale*i/2-1,0])
    bottom.append(rect)
    # fig = Tex(r"$\cdots$").scale(1.0).move_to([myscale*i-2.5,myscale*i/2-1,0])
    # figs.append(fig)
    scene.add(rect)
    scene.play(rect.animate.move_to([myscale*i-2.5,myscale*i/2-1,0]), 
                # FadeIn(fig),
                run_time=1)

    i = 5
    rect = rectangle(i, dashed=False, color=grid_color_1).scale(myscale).move_to([myscale*(4+i),myscale*i/2-1,0])
    bottom.append(rect)
    fig = Tex(r"$\cdots$").scale(1.0).move_to([myscale*i-2.5,-1.8,0])
    figs.append(fig)
    scene.add(rect)
    scene.play(rect.animate.move_to([myscale*i-2.5,myscale*i/2-1,0]), 
                FadeIn(fig),
                run_time=1)

    i = 6
    rect = rectangle(i, dashed=False, color=grid_color_1).scale(myscale).move_to([myscale*(4+i),myscale*i/2-1,0])
    bottom.append(rect)
    # fig = Tex(r"$6$").scale(1.0).move_to([myscale*i-2.5,myscale*i/2-1,0])
    # figs.append(fig)
    scene.add(rect)
    scene.play(rect.animate.move_to([myscale*i-2.5,myscale*i/2-1,0]), 
                # FadeIn(fig),
                run_time=1)

    i = 7
    rect = rectangle(i, dashed=False, color=grid_color_1).scale(myscale).move_to([myscale*(4+i),myscale*i/2-1,0])
    bottom.append(rect)
    fig = Tex(r"$n$").scale(1.0).move_to([myscale*i-2.5,-1.8,0])
    figs.append(fig)
    scene.add(rect)
    scene.play(rect.animate.move_to([myscale*i-2.5,myscale*i/2-1,0]), 
                FadeIn(fig, rate_func=rate_functions.ease_in_quart),
                run_time=1)

    global gbottom
    gbottom = Group(*bottom)

    plus = []
    i = 1.5
    fig  = Tex(r"$+$").scale(0.9).move_to([myscale*i-2.5,-1.8,0])
    plus.append(fig)

    i = 2.5
    fig = Tex(r"$+$").scale(0.9).move_to([myscale*i-2.5,-1.8,0])
    plus.append(fig)

    i = 3.75
    fig = Tex(r"$+$").scale(0.9).move_to([myscale*i-2.5,-1.8,0])
    plus.append(fig)

    i = 6.25   
    fig = Tex(r"$+$").scale(0.9).move_to([myscale*i-2.5,-1.8,0])
    plus.append(fig)

    global gplus
    gplus = Group(*plus)
    scene.play(FadeIn(gplus), run_time=1)

    global gfigs
    gfigs = Group(*figs)

    scene.wait(1)

    
############ Scene 2 ############

def scene2(scene : Scene):

    global gtop
    gtop = gbottom.copy()
    gtop.set_color(grid_color_2)

    global text_factor, text_paranth1, text_paranth2
    text_factor = Tex(r"2", color=grid_color_2).scale(1.5).move_to([-2.55,-1.8,0])
    text_paranth1 = Tex(r"(").scale(1.0).move_to([-2.37,-1.8,0])
    text_paranth2 = Tex(r")").scale(1.0).move_to([-0.57,-1.8,0])


    scene.play(gtop.animate.shift([3,0,0]), 
               Write(text_factor),
            #    text_factor.animate.scale(1.5),               
               FadeIn(text_paranth1),
               FadeIn(text_paranth2),
               run_time=2, 
               rat_func=rate_functions.ease_in_sine)

    scene.play(Rotate(gtop, PI, about_point=[0,0.5,0]), 
               text_factor.animate.scale(1/1.5),
               run_time=2, rate_func=linear)

    scene.play(gtop.animate.move_to([-1.5,0.13,0]), 
               text_factor.animate.set_color(text_color),               
               run_time=1, rate_func=rate_functions.ease_out_sine)

    scene.wait(2)


############ Scene 3 ############

def scene3(scene : Scene):

    ggrid = grid(7, color=grid_color_3).scale(myscale).move_to([-1.5,0.0,0])

    scene.play(ggrid.animate.shift([3.0,0,0]), run_time=2)

    
    arr1 = DoubleArrow([0,-1,0],[7.5,-1,0], color=arrow_col, stroke_width=2, tip_length=0.1).scale(myscale).move_to([1.50,-1.15,0])
    arr2 = DoubleArrow([-1,0,0],[-1,8.5,0], color=arrow_col, stroke_width=2, tip_length=0.1).scale(myscale).move_to([0.5,0.0,0])
    text1 = Tex(r"$n$", color=text_color).scale(0.75).move_to([1.5,-1.3,0])
    text2 = Tex(r"$n+1$", color=text_color).scale(0.75).move_to([0.2,0.0,0])
    global garrow
    garrow = Group(arr1, arr2, text1, text2)

    global text_egal, text_result
    text_egal = Tex(r"$=$").scale(1.3).move_to([0.3,-1.8,0])
    text_result = Tex(r"$n(n+1)$").scale(1.0).move_to([1.55,-1.8,0])

    scene.play(FadeIn(arr1), 
               FadeIn(text1),
               FadeIn(arr2),
               FadeIn(text2),
               run_time=1.5)
    
    scene.play(FadeIn(text_egal),
                FadeIn(text_result),
                run_time=1.5)
        
    scene.wait(1)


############ Scene 4 ############

def scene4(scene : Scene):

    # text_new_result = Tex(r"$\displaystyle \frac{n(n+1)}{2}$").scale(1.0).move_to([1.55,-2.0,0])

    # scene.play(FadeOut(text_paranth1),
    #             FadeOut(text_paranth2),
    #             # text_factor.move_to([1.5,-2.2,0]),
    #             FadeOut(text_factor),
    #             FadeOut(text_result),
    #             FadeIn(text_new_result),
    #             run_time=1)
    
    formula = Tex(r"$\displaystyle 1+2+3+\cdots+n \  = \  \frac{n(n+1)}{2}$").scale(1.3).move_to([-0.2,-3,0])

    scene.play(Write((formula)), run_time=4)

    scene.play(FadeOut(*gfigs),
               FadeOut(*gplus),
               FadeOut(*garrow),
               FadeOut(text_factor, text_paranth1, text_paranth2, text_egal, text_result))
    
    scene.wait(3)




############ All scenes ############

# Fade out a scene
def fade_out(scene: Scene):
    animations = []
    for mobject in scene.mobjects:
        animations.append(FadeOut(mobject))
    scene.play(*animations, run_time=run_time_between_scenes)


# Regroup all scenes in one
class Triangular(Scene):
    def construct(self):
        scenes = [scene1, scene2, scene3, scene4]
        # scenes = [scene1, scene2, scene3]
        for scene in scenes:
            scene(self)
            # fade_out(self)
            # self.clear()