# IFS 

import numpy as np
import random

import matplotlib.pyplot as plt
import matplotlib.animation as animation
import matplotlib.colors

# IFS

# Affine transformation
def transformation(x,y,a,b,c,d,e,f):
    xx = a*x + b*y + e
    yy = c*x + d*y + f
    return xx, yy
    

# Random choice (with probas)
def hasard(pliste):
    x = random.random()
    k = 0
    while k < len(pliste) and x > pliste[k]:
        x = x - pliste[k]
        k = k + 1
    if k >= len(pliste):
        k = k - 1
    return k
    

# Test    
#pliste = [0.25,0.5,0.25]
#for i in range(5):
#    print(hasard(pliste))


# Plot an IFS
# Input : a list of transformations and probas
# Each transformation is of the form [a,b,c,d,e,f,p]
def ifs(transfoliste, nbiter):
    pliste = [transfo[6] for transfo in transfoliste] # Les proba
    x=0; y=0 #x=random(); y=random()   # Point initial (au pif)
    listepoints = []
    for i in range(nbiter):                  # Itération
        k = hasard(pliste)                   # On choisit un tranfo au hasard
        # k = hasard_bis(len(pliste))
        transfo = (transfoliste[k])[0:6]     # Voici la transfo
        x,y = transformation(x, y, *transfo)   # L'image du point
        if i > 100:                          # On n'affiche pas les tous premiers points 
            listepoints.append((x, y))
    return listepoints
    
    
# La fougère
fougere = [
[0, 0,  0,  0.16,   0,  0,  0.01],
[0.85,  0.04,   -0.04,  0.85,   0,  1.60,   0.85],
[0.20,  -0.26,  0.23,   0.22,   0,  1.60,   0.07],
[-0.15, 0.28,   0.26,   0.24,   0,  0.44,   0.07]
]

Nmax = 200000
monifs = ifs(fougere, Nmax)

liste_x = [p[0] for p in monifs]
liste_y = [p[1] for p in monifs]


# Animation IFS


# Dimensions of the video
video_width_px = 1080
video_height_px = 1920

# Assuming a common DPI for video, adjust as needed
dpi = 100

# Calculate figure size in inches
fig_width_in = video_width_px / dpi
fig_height_in = video_height_px / dpi

# Frames per second
fps = 30

# Font
plt.rcParams["font.family"] = "Georgia", "Times New Roman", "DejaVu Serif", "Georgia", "serif", 
# plt.rcParams["font.family"] = "Liberation Sans" 

# Colors
# black_exo7 = (0.06,0.12,0.18)   # '#102030' 
black_exo7 = matplotlib.colors.to_rgb('#212529')  # GRAY9   
green_fern = '#00ff1a'
text_color = matplotlib.colors.to_rgb('#ECF0F1')    # OLD (0.5,0.5,0.5)


# Create a figure with specified size and a 2D axis
fig, ax = plt.subplots(figsize=(fig_width_in, fig_height_in))


plt.axis('off')
ax.set_xlim(-3, 3.5)
ax.set_ylim(-0.5, 12)
ax.set_aspect('equal')

fig.set_facecolor(black_exo7)
ax.set_facecolor(black_exo7)
plt.tight_layout()



def tempo(n):
    """ non linear tempo for displaying the points """
    m = int(0.6*n**2.0)
    if m > Nmax:
        print("Warning ! Not enough points to display")

    return m

xlift = -0.2  # horizontal translation
ylift = 0.5   # vertical translation
scat = ax.scatter(xlift+liste_x[0], ylift+liste_y[0], color=green_fern, s=0.25)
mytext = ax.text(-1.5, 10, '', ha='center', color=black_exo7, fontsize=30, weight='bold')

def update(frame):
    # for each frame, update the data stored on each artist.

    t = frame / fps 
    print(f"frame {frame} time {t:.2f}")

    # if frame > 450:  # stop animation, but keep the last frame
    #     return scat, mytext,

    x = liste_x[:tempo(frame)]
    y = liste_y[:tempo(frame)]
    x = [xlift+xi for xi in x]
    y = [ylift+yi for yi in y]
    # update the scatter plot:
    data = np.stack([x,y]).T
    scat.set_offsets(data)
    # Text with fading


    tfstart, tflong = 250, 75
    if tfstart <= frame < tfstart+tflong: 
        percent = (frame-tfstart)/tflong
        mycolor = (1-percent)*np.array(black_exo7) + percent*np.array(text_color)
        mytext.set_text("Barnsley fern")
        mytext.set_color(mycolor)

    if tfstart+tflong <= frame < tfstart+2*tflong: 
        percent = (frame-tfstart-tflong)/(tflong)
        mycolor = (1-percent**2)*np.array(text_color) + (percent**2)*np.array(black_exo7)
        mytext.set_text("Barnsley fern")
        mytext.set_color(mycolor)

    if frame >= tfstart+2*tflong:
        mytext.set_text("")
        mytext.set_color(black_exo7)

    # update the line plot:
    return scat, mytext, 


ani = animation.FuncAnimation(fig=fig, func=update, frames=540, interval=1, repeat=False)


ffmpeg_writer = animation.FFMpegWriter(fps=fps, bitrate=-1)
ani.save('video-nomusic-sh001.mp4', writer=ffmpeg_writer)

# plt.show()