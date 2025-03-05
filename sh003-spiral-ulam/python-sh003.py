
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
import matplotlib.colors

from shorts_lib import new_figure, anim, generate_short
from shorts_lib import video_width_px, video_height_px, fig


# Font
plt.rcParams["font.family"] = "Liberation Sans" #, "Arial" #"DejaVu Sans"  #, "Times New Roman", "DejaVu Serif", "Georgia", "serif", 

# Colors
black_exo7 = '#212529'  # GRAY9   
color_integer = '#ced4da'  # GRAY 4   ## OLD '#adb5bd'  # GRAY5
edge_gray = '#495057'    # GRAY7

color_prime = '#d6336c'  # PINK7
color_not_prime = '#d0bfff' # VIOLET2 

text_color = 'lightgray'


# Crible d'Eratosthène
# retourne tous les nombres premiers de 1 à n
def eratosthene(n):
    liste_entiers = list(range(n+1))    # tous les entiers
    liste_entiers[1] = 0                # 1 n'est pas premier : on remplace l'indice par 0
    k = 2                               # on commence par les multiples de 2
    while k*k <= n:
        if liste_entiers[k] != 0:       # si le nombres n'est pas barrés
            i = k                       # les i sont les multiples de k
            while i <= n-k:
                i = i+k
                liste_entiers[i] = 0    # les muliples de k ne sont pas des nombres premiers           
        k = k +1    
    
    # liste_premiers = [k for k in liste_entiers if k !=0]  # on efface les zéros
    return liste_entiers[1:]


# Test
# n = 20
# print('Nombres premiers de 1 à %d par le crible d''Eratosthène :' %n)
# print(eratosthene(n))  


# function to plot out the ulam spiral 
# https://www.geeksforgeeks.org/the-ulam-spiral/
def make_spiral(arr): 
    """ Transform an array into a spiral """
    nrows, ncols= arr.shape 
    idx = np.arange(nrows*ncols).reshape(nrows,ncols)[::-1] 
    spiral_idx = [] 
    while idx.size: 
        spiral_idx.append(idx[0]) 
  
        # Remove the first row (the one we've 
        # just appended to spiral). 
        idx = idx[1:] 
  
        # Rotate the rest of the array anticlockwise 
        idx = idx.T[::-1] 
  
    # Make a flat array of indices spiralling  
    # into the array. 
    spiral_idx = np.hstack(spiral_idx) 
  
    # Index into a flattened version of our  
    # target array with spiral indices. 
    spiral = np.empty_like(arr) 
    spiral.flat[spiral_idx] = arr.flat[::-1] 
    return spiral 


def define_spiral(w):
    """ Define the spiral of numbers and primes """   
    
    # Array indexed from 1 to w*w
    global arr, spiarr, primes, arrprimes, spiprimes, spibool
    arr = np.arange(w*w).reshape(w,w) + 1
    # Spiraled array
    spiarr = make_spiral(arr)
    # print(spiarr)   

    # Primes
    primes = eratosthene(w*w)
    arrprimes = np.array(primes).reshape(w,w)
    spiprimes = make_spiral(arrprimes)
    spibool = spiprimes > 0
    return


def define_axis(size):
    global ax1
    ax1.clear()
    ax1.set_aspect('equal')
    ax1.set_xlim(-3, size+2)
    ax1.set_ylim(-3, size+2)
    ax1.set_axis_off()


# create a new figure and get the main axis
ax = new_figure()


size = 10
define_spiral(size)
# print(spiarr)

# define ax1 for local coordinates
offset = 0
ax1 = fig.add_axes([offset/video_width_px, offset/video_height_px, (video_width_px-2*offset)/video_width_px, (video_height_px-2*offset)/video_height_px])
define_axis(size)  

# colors
fig.set_facecolor(black_exo7)
ax.set_facecolor(black_exo7)
ax1.set_facecolor(black_exo7)

# # Part 1 : spiral of all integers (up to 100)

# steps = size**2
@anim(steps=100, start=0, end=4)
def part1(frame):
    ax.text(540, 1500, "A spiral of integers", fontsize=25, ha='center', weight='normal', color=text_color)
    n = frame + 1   
    i, j = np.where(spiarr == n)[0][0], np.where(spiarr == n)[1][0]
    # print(n,i,j)
    # rect = ax1.patch
    # rect.set_facecolor('lightgoldenrodyellow')
    ax1.add_patch(Rectangle((i-0.5, j-0.5), 1, 1, edgecolor=edge_gray, lw=2, facecolor=color_integer))
    ax1.text(i, j-0.02, spiarr[i,j], ha='center', va='center', color='black', fontsize=20)


# @anim(steps=1, start=4, end=4.5)
# def pause1(frame):
#     pass


# part 2 : highlited primes up to 100

@anim(steps=100, start=4.5, end=10.5)
def part2(frame):
    ax.text(540, 1500, "Color prime numbers", fontsize=25, ha='center', weight='normal', color=text_color)
    if frame == 0:
        define_axis(size)
        for n in range(1, size**2+1):    
            i, j = np.where(spiarr == n)[0][0], np.where(spiarr == n)[1][0]
            ax1.add_patch(Rectangle((i-0.5, j-0.5), 1, 1, edgecolor=edge_gray, lw=2, facecolor=color_integer))
            ax1.text(i, j-0.02, spiarr[i,j], ha='center', va='center', color='black', fontsize=20)        



    n = frame + 1
    i, j = np.where(spiarr == n)[0][0], np.where(spiarr == n)[1][0]
    if n in primes:
        ax1.add_patch(Rectangle((i-0.5, j-0.5), 1, 1, edgecolor=edge_gray, lw=2, facecolor=color_prime))
        ax1.text(i, j-0.04, spiarr[i,j], ha='center', va='center', color='white', fontsize=20, weight='bold') 
    else:
        ax1.add_patch(Rectangle((i-0.5, j-0.5), 1, 1, edgecolor=edge_gray, lw=2, facecolor=color_not_prime))
        ax1.text(i, j-0.02, spiarr[i,j], ha='center', va='center', color='gray', fontsize=20)

# part 3 : only primes up to 400

@anim(steps=400, start=11, end=17)
def part3(frame):
    ax.text(540, 1500, "Prime numbers up to 400", fontsize=25, ha='center', weight='normal', color=text_color)
    size = 20
    if frame == 0:
        define_spiral(size)
        define_axis(size)

    n = frame + 1
    for m in range(max(1,n-3), min(n+3, size**2)+1):
        i, j = np.where(spiarr == m)[0][0], np.where(spiarr == m)[1][0]
        if m in primes:
            ax1.add_patch(Rectangle((i-0.5, j-0.5), 1, 1, edgecolor=edge_gray, facecolor=color_prime))
            ax1.text(i, j-0.02, spiarr[i,j], ha='center', va='center', color='white', fontsize=12, weight='normal') 
        else:
            ax1.add_patch(Rectangle((i-0.5, j-0.5), 1, 1, edgecolor=edge_gray, facecolor=color_not_prime))

    # i, j = np.where(spiarr == n)[0][0], np.where(spiarr == n)[1][0]
    # if n in primes:
    #     ax1.add_patch(Rectangle((i-0.5, j-0.5), 1, 1, edgecolor='white', facecolor='firebrick'))
    #     ax1.text(i, j, spiarr[i,j], ha='center', va='center', color='black', fontsize=10, weight='bold') 
    # else:
    #     ax1.add_patch(Rectangle((i-0.5, j-0.5), 1, 1, edgecolor='white', facecolor='lightgray'))


def soft_function(t):
    """f : [0,1] -> [0,1]"""
    # return 1 - pow(1 - t, 2)
    return t*t

# part 4 : primes up to 1000^2 : size = 1000
@anim(steps=1800, start=19, end=34)
def part4(frame, steps):
    ax.text(540, 1600, "Prime numbers up to 100 000", fontsize=25, ha='center', weight='normal', color=text_color)
    ci, cj = np.where(spiarr == 1)[0][0], np.where(spiarr == 1)[1][0]  # center (value 1)
    global ax1
    size = 333
    if frame == 0:
        define_spiral(size)
        define_axis(size+30)
        mycmap = matplotlib.colors.ListedColormap([color_not_prime, color_prime])
        ax1.matshow(spibool, cmap=mycmap)
        # ax1.add_patch(Rectangle((ci-0.5, cj-0.5), 1, 1, edgecolor=, facecolor='black'))
    
    # s = 0.5*frame * size/steps
    t = max(0.01, frame / steps)
    s = 0.5 * soft_function(t) * size
    ax1.set_xlim(ci-s, ci+s)
    ax1.set_ylim(cj-s, cj+s)
    

@anim(steps=1, start=34, end=35)
def pause4(frame):
    pass   


# generate the short with the animations
mylength = 35    # total is 35 seconds
myfps = 60       # production: fps = 60; at least 30 to print all integers
myframes = myfps*mylength
generate_short('video-nomusic-sh003.mp4', frames=myframes, length=mylength)

