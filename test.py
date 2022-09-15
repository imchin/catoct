#!/usr/bin/python3

from trajectory import Trajectory
import numpy as np
import matplotlib.pyplot as plt


n = 3
N = 10
q_0 = np.random.rand(n,1)
q = np.random.rand(n,N)
v_max = [1]*n
a_max = [0.1]*n

# generate trajectory
traj = Trajectory()
traj.set_position(q)
traj.set_bound(v_max,a_max)
traj.time_optimal(q_0)

# evaluation
t = np.linspace(0,np.sum(traj.duration),1000)
q_t,v_t,a_t = traj.evaluate(t)

# visualization
fig,axs = plt.subplots(3)
axs[0].plot(t,q_t)
axs[0].plot(np.cumsum(traj.duration),traj.position,'r*',linewidth=1,markersize=10)
axs[1].plot(t,v_t)
axs[1].plot(np.cumsum(traj.duration),traj.velocity,'r*',linewidth=1,markersize=10)
axs[2].plot(t,a_t)
axs[2].plot(np.cumsum(traj.duration),traj.acceleration,'r*',linewidth=1,markersize=10)
plt.show()