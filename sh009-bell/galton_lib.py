# Galton board simulation

import numpy as np
import matplotlib.pyplot as plt
from math import comb


# GALTON BOARD SIMULATION

# A board with n rows and N ballswith n+1 bins  follwing one by one

# A ball is modelized by its trajectory  wich is a list of j=column values (being unsaid that that each step the ball from on row)

###### THEORETICAL TRAJECTORY ######

# Integer coordinates to hexagon grid coordinates
def ij_to_xy(i, j):
    """ Convert i, j to x, y coordinates for hexagon grid """
    x = j - i // 2 - (i % 2) / 2   # offset for odd rows
    y = -i * np.sqrt(3) / 2
    return x, y + 4



def ball_trajectory(n):
    """ Generate a random trajectory for a ball in n+1 bins """
    trajectory = [0]  # Start at the first bin
    for i in range(n):
        if np.random.rand() < 0.5:
            # Ball falls to the right
            trajectory.append(trajectory[-1] + 1)
        else:
            # Ball falls to the left
            trajectory.append(trajectory[-1])
    return trajectory

# Test
# for _ in range(5):
#     print(ball_trajectory(4))  # Example trajectory for 10 bins


def ball_path(trajectory):
    """ Convert a ball trajectory to a path for plotting """
    n = len(trajectory) - 1  # Number of rows
    path = []
    for i in range(n + 1):
        x, y = ij_to_xy(i, trajectory[i])   
        path.append((x, y))  # Offset y to fit the grid
    return path


def function_path(t, path, delay=0):
    """
    For t in [delay+0, delay+1], returns [x, y, 0] interpolated along the path.
    """
    
    n = len(path) - 1

    if t < delay:
        return np.array([path[0][0], path[0][1], 0])
    
    t = t - delay

    if t >= 1:    # return last position
        return np.array([path[-1][0], path[-1][1], 0])

    idx = t * n
    i = int(np.floor(idx))
    j = min(i + 1, n)
    alpha = idx - i
    x = (1 - alpha) * path[i][0] + alpha * path[j][0]
    y = (1 - alpha) * path[i][1] + alpha * path[j][1]
    return np.array([x, y, 0])


####### GRAPHICS TRAJECTORY ########

def trajij_to_trajxy(trajectory):
    trajxy = []
    for i, j in enumerate(trajectory):
        x, y = ij_to_xy(i, j)
        trajxy.append((x,y))
    return trajxy


##### FINAL BINS PLOT ######

def final_position(list_trajectory, n, N):
    """For each ball, return (bin_index, stacking_index)"""
    bin_counts = [0] * (n+1)
    final_pos = []
    for traj in list_trajectory:
        bin_index = traj[-1]
        stacking_index = bin_counts[bin_index]
        final_pos.append((bin_index, stacking_index))
        bin_counts[bin_index] += 1
    return final_pos


def final_xy_position(final_pos, n, N, bin_width=3, ball_diameter=1, space=0, depth=0):
    """For each ball, compute its (x, y, bin_index) position in the bin."""
    final_xy = []
    
    for bin_index, stacking_index in final_pos:
        # Use the same hexagonal grid coordinates as the trajectory to avoid horizontal jumps
        x, y = ij_to_xy(n, bin_index)
        
        # Spread balls horizontally in the bin
        x = x + ((stacking_index % bin_width) - bin_width/2 + 0.5) * ball_diameter
        
        # Calculate the layer (row) this ball is in - first balls go to bottom (layer 0)
        layer = stacking_index // bin_width
        
        # Position: bottom of bin + layer height (first balls at bottom)
        final_y = y - space - depth + layer * ball_diameter
        final_xy.append((x, final_y, bin_index))
    return final_xy


###### FULL TRAJECTORIES: ALL BALLS FROM TOP TO BIN #########

def full_trajectories(n, N, bin_width=3, ball_diameter=1, space=0, depth=0):
    """Return a list of full trajectories for all balls."""

    # N trajectories down to the grid
    list_traj_ij = [ball_trajectory(n) for k in range(N)]
    # print(list_traj_ij[0])

    # Convert the first part of the trajectories from (i, j) to (x, y)
    list_traj_xy = [trajij_to_trajxy(traj) for traj in  list_traj_ij]
    # print(list_traj_xy[0])

    # Final positions in bins (as an index and stacking index)
    final_pos = final_position(list_traj_ij, n, N)
    # print(" final position:", final_pos[0])

    # Convert final positions to (x, y, bin_index)
    final_xy = final_xy_position(final_pos, n, N, bin_width, ball_diameter, space, depth)
    # print(final_xy[0])

    # Create a full trajectory for each ball
    list_full_traj_xy = []
    for i in range(N):
        full_traj_xy = list_traj_xy[i].copy()
        x, y, bin_index = final_xy[i]
        full_traj_xy.append((x, y))

        list_full_traj_xy.append(full_traj_xy)

    # print(list_full_traj_xy[0])

    return list_full_traj_xy


######## PROBABILITIES #########

def binomial_distribution(n, N, k):
    """ Calculate the binomial distribution for n+1 bins at position k """
    p = 1/2  # Probability of falling left or right
    
    # Binomial coefficient
    coeff =comb(n, k)
    
    # Binomial probability mass function
    y = coeff * (p ** k) * ((1 - p) ** (n - k))
    
    return y * N  # Scale by the number of balls N



def normal_distribution(x, n, N):
    """ Calculate the normal distribution for n+1 bins at position x """
    mu = n/2
    sigma = np.sqrt(n/4)
    y = 1/(sigma * np.sqrt(2 * np.pi)) * np.exp( - (x - mu)**2 / (2 * sigma**2) )

    return y * N  # Scale by the number of balls N

