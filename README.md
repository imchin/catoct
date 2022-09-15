# CATOCT: Continuous-Acceleraiton Time-Optimal Cubic Trajectory
This is suitable for fully-actuated robotics manipulator.

## Objective:
Given a sequence of (multiple-degree-of-freedom) via points in joint space and limits on the magnitude of both velocity and acceleration of each degree of freedom, 
the goal is to generate a piece-wise cubic trajectory that is time-optimal and satisfies both velocity and acceleration constraints. The trajectory must be 
continuous in position, velocity, and acceleration.

## Why not quintic trajectory ?:
The advantage of using polynomial trajectory is its easily-computed derivatives based on its fixed structure of coefficients and the monomials. 
A cubic trajectory consists of 4 coefficients. Only 4 boundary conditions and the duration of thetrajectory are required to compute the coefficients. Typically, this is done by assigning 
the initial position, the final position, the intial velocity, and the final velocity. The resultant cubic trajectory can be appended togeter to form a 
piece-wise cubic trajectory. Since the velocity can be arbitarily assigned, one can form a piece-wise cubic trajectory that gaurantee to be continuous in its velocity.
However, if the duration is arbitary, one cannot gaurantee the continuity in the acceleration.

One simple way to solve this is to use a quintic trajectory, which has 6 coefficients. In addition to the given position and velocity of the boundaries, the accceleration can be assigned as well. 
The resultant piece-wise quintic trajectory can now be conitnuous in its position, velocity, and accceleration. This implies that, in order to generate a piece-wise quintic trajectory,
one needs the followings.
* durations of each sub-trajectory
* position at each via points (including the initial one)
* velocity at each via points (including the initial one)
* acceleration at each via points (including the initial one)
Given the position of the via points, there are several questions about the rest of the parameters.
* Can the durations be any values? Can they be too small or too large ?
* Can the velocity be any values? Is there any way we can compute this automatically?
* Can the acceleration be any values? Can the actuators achieve the given acceleration? What happens to the acceleration between the via points?

The problem is that, for the quintic trajectory, one has to determine many unknowns. A feasible trajectory does exist, but it might require extensive tuning.
This is why "CATOCT:Continuous-Acceleration Time-Optimal Cubic Trajectory" is developed.

## Ideas behind CATOCT:
In reality, a sequence of via points in joint space are the only things given to the trajectory generator. Our goal is to automatically compute the optimal durations of each sub-trajectory 
as well as the velocity of each via point.
