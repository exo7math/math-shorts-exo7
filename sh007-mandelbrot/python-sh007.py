import numpy as np
import matplotlib.pyplot as plt
import mandelbrot as mand
import time     

# mand.linear_zoom(-0.64, -0.41, 0.02, 50, 10)


# Mandelbrot set with rounded path 
# Warning: points should be distinct


# Path

# points = [       
#          (-1, 0, 2.2),   
#         (-1, 0, 1.5),  # 2.2/1.5 = 1.4666
#         (-0.8, 0.1, 1),   # 1.5/1 = 1.5
#         (-0.7, 0.25, 0.3),  # 1/0.3 = 3.3333
#         (-0.62, 0.42, 0.1),    # 0.3/0.1 = 3
#         (-0.57, 0.50, 0.025),    # 0.1/0.025 = 4
#         (-0.55, 0.52500, 0.005),   # 0.025/0.005 = 5
#         (-0.54825,0.52930,0.0012), # 0.005/0.0012 = 4.1666
#         (-0.54824,0.52935,0.0003),  # 0.0012/0.0003 = 4
#         (-0.54823,0.52940,0.0001),  # 0.0003/0.0001 = 3
#         (-0.548206,0.529520,0.00001),  # 0.0001/0.00001 = 10
#         (-0.54820502,0.52952430,0.0000005)  # 0.00001/0.0000005 = 20
#         ]


points = [       
         (-1, 0, 2.2),   
        (-1, 0, 1.5),  # 2.2/1.5 = 1.4666
        (-0.8, 0.1, 0.9),   # 1.5/0.9 = 1.6666
        (-0.7, 0.25, 0.4),  # 0.9/0.4 = 2.25
        (-0.62, 0.42, 0.13),    # 0.4/0.13 = 3.0769
        (-0.57, 0.50, 0.035),    # 0.13/0.035 = 3.7142
        (-0.55, 0.52500, 0.008),   # 0.035/0.008 = 4.375
        (-0.54825,0.52930,0.0016), # 0.008/0.0016 = 5
        (-0.54824,0.52935,0.0003),  # 0.0016/0.0003 = 5.3333
        (-0.54823,0.52940,0.00005),  # 0.0003/0.00005 = 6
        (-0.548206,0.529520,0.00001),  # 0.00005/0.00001 = 5
        (-0.54820502,0.52952430,0.0000005)  # 0.00001/0.0000005 = 20
        ]

# Preliminary view
# mand.prelim_view(points, maxiter=1000)



# Movie

duration = 30
mand.fps = 60  
steps = duration*mand.fps

func_path = mand.round_linear_path(points, r=0.5) 
t = np.linspace(0, 1, steps)
path = func_path(t)

t0 = time.time()
mand.curved_zoom(path, maxiter=1000, steps=steps, name='video-mandelbrot-60fps.mp4')
t1 = time.time()
print(f'Total calculation time (in minuts): {(t1-t0)/60:.2f}')