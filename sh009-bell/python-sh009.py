from manim import *
import numpy as np

from config_shorts_exo7 import *


from galton_lib import *


np.random.seed(27) # seed


# Text
font_shorts = "Comic Neue"  # "Opens Sans"
text_color = red_exo7
# Tex.set_default(color=text_color, font_size=24, tex_template=TexFontTemplates.libertine)

# Colors
hex_col = GRAY_D
# hex_fillcol = 'black'
pin_col = GRAY_D
ball_col = TEAL_D
fill_col_1 = blue_exo7
fill_col_2 = red_exo7
fill_col_1_bis = TEAL_D
fill_col_2_bis = MAROON_E
graph_color = red_exo7

######### PROBABILITIES #########

N = 1000
n = 12  # Number of rows in the Galton board, with n+1 bins


####### GRAPHICS ########
ball_scale = 0.5  


# A ball
def ball_plot(x, y, ball_scale=1):
    """ Create a ball at position x, y """
    return Dot(color=ball_col, radius=0.16 * ball_scale).move_to([x, y, 0])

virtual_ball = ball_plot(0, 0, ball_scale=ball_scale)
ball_diameter = virtual_ball.width


# Hexagon figure
def hexagon_plot(x, y):
    """ Hexagon centered at x, y """
    r = 1/np.sqrt(3)
    hexagon = RegularPolygon(n=6, start_angle=PI/6, radius=r, color=hex_col, z_index=0).shift([x, y, 0])
    pin = Square(side_length=0.35, color=pin_col, fill_color=pin_col, fill_opacity=1, z_index=0).rotate(PI/4).move_to([x, y-r, 0])
    pinhexa = Group(pin)  # Group(hexagon, pin)
    return pinhexa


# Grid of hexagons
def grid_plot(n):
    """ Create a grid of hexagons with n rows """
    hexagons = Group()
    for i in range(n):
        for j in range(i+1):
            x, y = ij_to_xy(i, j)
            hexagon = hexagon_plot(x, y)
            hexagons.add(hexagon)
    return hexagons


def plot_trajectory(traj):
    """ Plot a trajectory as a series of line segments"""
    path = []
    for i in range(len(traj) - 1):
        x1, y1 = traj[i]
        x2, y2 = traj[i + 1]
        path.append(Line([x1, y1, 0], [x2, y2, 0], color=red_exo7))
    return Group(*path)


# Bin dimensions
bin_ball_width = 5 # width of the bin in ball's size
bin_ball_height = np.ceil(binomial_distribution(n, N, n//2)/bin_ball_width)+3  # Expected maximal height of the bin
# print(bin_height)

## The bins
bins_count = [0] * (n + 1)  # Initialize bins with 0 balls

space = 1    # space below the hexagons grid
bin_xy_width = np.sqrt(3) / 2    # real width of the bin
bin_xy_depth = ball_diameter * bin_ball_height   # real size of the bin



# The bins the receives the balls
def bins_plot(n):
    """ Create a bin figure with n+1 bins """
    bins = Group()

    for j in range(n+2):
        x, y = ij_to_xy(n, j)
        y += -space
        bins.add(Line([x-1/2, y, 0], [x-1/2, y - bin_xy_depth, 0], color=hex_col, z_index=0))

    x, y = ij_to_xy(n, 0)
    xx, yy = ij_to_xy(n, n)
    bins.add(Line([x-1/2, y-bin_xy_depth-space, 0], [xx+1/2, yy-bin_xy_depth-space, 0], color=hex_col, z_index=0))  # bottom line

    return bins



def create_spaced_title(text, font, color, letter_spacing=0.3, word_spacing=0.6):
    """Create a title with custom letter spacing"""
    words = text.split(" ")  # Split text into words
    
    title_group = VGroup()
    
    # Create all letters first to find the common baseline
    letter_objects = []
    for word in words:
        for letter in word:
            letter_obj = Text(letter, font=font, color=color)
            letter_objects.append(letter_obj)
    
    # Find the lowest bottom point to use as common baseline
    if letter_objects:
        baseline = min([letter.get_bottom()[1] for letter in letter_objects])
    else:
        baseline = 0
    
    x_pos = 0
    for word_index, word in enumerate(words):
        for letter in word:
            letter_obj = Text(letter, font=font, color=color)
            # Align all letters to the same baseline
            letter_obj.align_to([0, baseline, 0], DOWN)
            letter_obj.move_to([x_pos, letter_obj.get_center()[1], 0])
            title_group.add(letter_obj)
            x_pos += letter_obj.width + letter_spacing
        
        # Add extra space between words (except after the last word)
        if word_index < len(words) - 1:
            x_pos += word_spacing
    
    return title_group


################ Test 9 ############
def galton_scene(scene : Scene):
    # Create title with custom letter spacing
    title = create_spaced_title("The bell curve", font_shorts, text_color, 
                               letter_spacing=0.3, word_spacing=0.6).scale(1.3).move_to([0,-16.5,0])
    # scene.add(title)  

    scene.camera.frame.save_state()
    
    # Set initial camera to be more zoomed out
    scene.camera.frame.scale(0.8).move_to([0, 0.5, 0])

    # Hexagons
    hexagons = grid_plot(n)
    scene.add(hexagons)

    # Bins
    bins_fig = bins_plot(n)
    scene.add(bins_fig)

    t_tracker = ValueTracker(0)

    # Balls
    list_balls = VGroup()
    for k in range(N):
        list_balls.add(ball_plot(0, 0, ball_scale=ball_scale))

    list_full_traj_xy = full_trajectories(n, N, bin_width=bin_ball_width, ball_diameter=ball_diameter, space=space, depth=bin_xy_depth)

    # print("Plotted traj", list_full_traj_xy[0])
    # traj0 = plot_trajectory(list_full_traj_xy[0])
    # scene.add(traj0)

    list_func = []
    for k in range(N):
        # Progressive increase in ball appearance rate: starts slow, then accelerates
        mydelay = sum([0.3*1/(i**0.5) for i in range(1, k+1)])  # Delay for each ball
        list_func.append(lambda t, traj=list_full_traj_xy[k], delay=mydelay: function_path(t, traj, delay=delay))


    scene.add(list_balls)
    for k, ball in enumerate(list_balls):
        ball.add_updater(lambda x, func=list_func[k]: x.move_to(func(t_tracker.get_value())))


    total_time = 20  # 14
    
    scene.play( 
            t_tracker.animate(rate_func=rate_functions.ease_in_sine, run_time=21).set_value(total_time),
            scene.camera.frame.animate(rate_func=linear, run_time=16).scale(3).move_to(scene.camera.frame.get_center() + DOWN * 7),
            # run_time=21,  
            rate_func= rate_functions.ease_in_sine
        ) 
    
    # Plot the Gauss function

    x, y = ij_to_xy(n, 0)
    yshift = y - space - bin_xy_depth
    gauss_func = lambda x: normal_distribution(x, n, N)*ball_diameter/bin_ball_width
    gauss_graph = FunctionGraph(gauss_func, x_range=[0, n], color=graph_color, stroke_width=8).shift([-n/2, yshift, 0])
    scene.add(gauss_graph)
    scene.play(
        Create(gauss_graph),
        FadeIn(title),
        run_time=3,
        rate_func=linear
    )

    scene.wait(1)
    return


############ All scenes ############

# Fade out a scene
def fade_out(scene: Scene):
    animations = []
    for mobject in scene.mobjects:
        animations.append(FadeOut(mobject))
    scene.play(*animations, run_time=run_time_between_scenes)


# Regroup all scenes in one
class Galton(MovingCameraScene):
    def construct(self):
        scenes = [galton_scene]
        for scene in scenes:
            scene(self)
            # fade_out(self)
            self.clear()