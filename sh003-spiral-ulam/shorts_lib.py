# short.py imports the necessary modules and defines the functions to generate the short.
import matplotlib.pyplot as plt
import matplotlib.animation as animation

# inspect is used to check the arguments of the decorated functions 
import inspect

# fig is a global variable that will be used to store the figure
fig = None
# ax is a global variable that will be used to store the main axis
ax = None

# Dimensions of the video
video_width_px = 1080
video_height_px = 1920
# Assuming a common DPI for video, adjust as needed
# this has no real effect on the video quality, only on the figure size/line width/text size
dpi = 128    

# Calculate figure size in inches
fig_width_in = video_width_px / dpi
fig_height_in = video_height_px / dpi

# Create a figure with specified size and a 2D axis
fig, ax = plt.subplots(figsize=(fig_width_in, fig_height_in))

# new_figure create and init a new figure 
# and return the main axis with dimensions 1080 x 1920
def new_figure():
    global ax
    return ax

def reset_axis():
    global ax
    ax.clear()
    ax.set_position([0, 0, 1, 1])  # This sets the axes position to cover the whole figure area
    ax.set_aspect('equal')
    ax.set_xlim(0, video_width_px)
    ax.set_ylim(0, video_height_px)
    ax.set_axis_off()

# animations is a global variable that will be used to store the animations
# each animation is a dictionary with the following keys:
# - animation: the function that generates the animation, that takes a parameter i.
# - start: the time in seconds when the animation starts.
# - end: the time in seconds when the animation ends.
# - fps: the frames per second of this animation.
# - before: a boolean that indicates if the first frame of the animation should be displayed before the animation starts.
# - keep: a boolean that indicates if the last frame of the animation should be kept after the animation ends.
# - last: the last frame of the animation.
animations = []

# amim is a decorator that adds the animation to the list of animations
def anim(steps=100, start=0, end=1, before=False, keep=False, **kwargs):
    def decorator(a):
        params = inspect.signature(a).parameters
        # if a hase more then one parameter, passe the extra parameters to the animation function
        if len(params) > 1:
            args = kwargs.copy()
            # append steps, start, end, before, keep to the kwargs
            args['steps'] = steps
            args['start'] = start
            args['end'] = end
            args['before'] = before
            args['keep'] = keep
            # keep in **args only the parameters that are in the signature
            args = {k: v for k, v in args.items() if k in params}
            # create the new anim function that takes only one parameter
            anim = lambda i: a(i, **args)
        else:
            anim = a
        animations.append({
            'animation': anim, # the function that generates the animation
            'start': start, # start time in seconds
            'end': end, # end time in seconds
            'fps': steps / (end - start), # frames per second
            'before': before, # if the first frame should be displayed before the animation starts
            'keep': keep, # if the last frame should be kept after the animation ends
            'last': steps-1, # the last frame of the animation
        }) 
    return decorator

# generate_short generate the short with the animations
#of length seconds in mp4 format with the given name
def generate_short(name, frames=100, length=5, extra_args=None):
    # Calculate the frames per second of the video
    fps = frames / length

    def animate(i):
        # clear the figure
        reset_axis()
        # Calculate the time in seconds corresponding to the frame i
        t = i / fps 
        print(f"frame {i} time {t:.2f}")
        # loop aver all the animations
        for a in animations:
            # if the time is in the range of the animation
            if t >= a['start'] and t < a['end']:
                # calculate the animation frame
                j = int((t - a['start'])*a['fps'])
                a['animation'](j)
            elif t < a['start'] and a['before']:
                a['animation'](0)
            elif t >= a['end'] and a['keep']:
                a['animation'](a['last'])

    # Call the animator
    ani = animation.FuncAnimation(fig, animate, frames=frames+1, repeat=False)

    # Save the animation if name is not None or empty
    if name:
        # add mp4 if no '.' in name
        if '.' not in name:
            name += '.mp4'
        ani.save(name, fps=fps, dpi=dpi, extra_args=extra_args)
    else:
        plt.show()
        plt.close()


# logo size 
logo_width = 200
offset = 20
# axl ia an axis to draw the logo
axl = fig.add_axes([offset/1080, (1920-offset-logo_width)/1920, logo_width/1080, logo_width/1920])
axl.set_aspect('equal')
axl.set_xlim(0, logo_width)
axl.set_ylim(0, logo_width)

def reset_logo():
    global axl
    axl.clear()
    axl.set_axis_off()

reset_logo()

# draw the logo
# @anim(steps=50, start=0, end=1, keep=True)
# def logo(i, **anim_args):
#     reset_logo()
#     # read the logo from a file logo/exo7anim-00XX.png where XX is i in 2 digits
#     axl.imshow(plt.imread(f"logo/exo7anim-00{i+1:02d}.png"))

