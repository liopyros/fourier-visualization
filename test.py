import matplotlib
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.pyplot import figure
from matplotlib.animation import FuncAnimation, PillowWriter

time_period = 1
step_size = 50
plot_interval = np.pi * 2 / step_size
theta = 0
periodicity = 3
multiplier = 1 / 2
plot_divisor = 1 / 2
radius_multiplier = 4 / np.pi 
est_values = []
est_trace_y = []
est_trace_x = []
real_trace_y = []

links = []
size = int(input('Number of approximation terms: '))
for s in range(size):
    links.append(0)

poly = 64*size
t = np.linspace(0, 2*np.pi, poly+1)

coordinates = [0, 0]
temp_coordinates = [0, 0]

figure(figsize=(14,5), dpi=100)
writer = PillowWriter(fps=10)

def animate(i):
    global theta, periodicity, temp_coordinates, radius_largest, est_values, est_trace_y, est_trace_x, real_trace_y

    plt.cla()

    radius = radius_multiplier
    radius_largest = 0
    radius = radius_multiplier

    # plot the starting circle of link length 1
    x = radius*np.cos(t)
    y = radius*np.sin(t)
    plt.plot(x, y, color='#646464', linewidth=1)    

    for link in range(len(links)):        
        # the square wave approximation only uses odd "n" terms
        if (link+1) % 2 == 1:
            n = link + 1
            radius = radius_multiplier / n

            # plot the first link from the origin (0, 0)
            if link == 0:
                coordinates = [radius*np.cos(theta*multiplier), radius*np.sin(theta*multiplier)]
                plt.plot([0, coordinates[0]], [0, coordinates[1]], linewidth=3, color="black")  
            else:
                coordinates = [coordinates[0] + radius*np.cos(theta*multiplier*n), coordinates[1] + radius*np.sin(theta*multiplier*n)]
                plt.plot([temp_coordinates[0], coordinates[0]], [temp_coordinates[1], coordinates[1]], linewidth=3, color="black")  

                # plot the radius of each new link
                x = radius*np.cos(t)
                y = radius*np.sin(t)
                plt.plot(x + temp_coordinates[0], y + temp_coordinates[1], linewidth=1.5)
                plt.plot([0, 0], [5, 5], linewidth=1.5)

            temp_coordinates = coordinates
            radius_largest += radius 
    
    offset = np.pi
    t_values = []
    est_values.insert(0, float(coordinates[1]))

    if (theta*multiplier) <= (2*np.pi + plot_interval*plot_divisor):
        est_trace_y.append(coordinates[1])
        est_trace_x.append(coordinates[0])
    else:
        est_values.pop(len(est_values)-1)     

    for j in range(len(est_values)):
        t_values.append(offset + j*plot_interval*plot_divisor)
    
    real_trace_y.insert(0, float(1)) if np.sin(theta*multiplier) >= 0 else real_trace_y.insert(0, float(-1))
    
    if len(real_trace_y) > len(t_values):
        real_trace_y.pop(len(real_trace_y)-1)  
        
    theta += plot_interval    
    
    plt.plot(t_values, real_trace_y, linewidth=1, color="green")
    plt.plot(t_values, est_values, linewidth=2, color="blue")
    plt.plot(est_trace_x, est_trace_y, linewidth=1.5, color='#D3D3D3', zorder=0)
    plt.plot([offset, offset], [-5, 5], linewidth=2, color="blue")
    plt.plot([temp_coordinates[0], offset], [temp_coordinates[1], temp_coordinates[1]], linewidth=1.5, color="red", zorder=10)
    plt.gca().set_aspect('equal')
    plt.gca().set_autoscale_on(False)
    plt.xlim(-radius_largest-0.5, offset + 2*np.pi + 0.5)
    plt.ylim(-2, 2)

ani = FuncAnimation(plt.gcf(), animate, interval=time_period)

# # Save a gif of the animation
# ani.save(f'./gif/square_{size}.gif', writer=writer)

plt.show()

