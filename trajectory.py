#!/usr/bin/python3

import numpy as np
from scipy.optimize import minimize

def get_Tqvac(T,q):
    a = 0.5
    if len(q[0])==3:
        A_1 = [2/(a*T[0]) ,2*(1-a)/T[0], 0]
        A_2 = [2/((1-a)*T[0]), 4/T[0]+4/T[1], 2/((1-a)*T[1])]
        A_3 = [0,2*(1-a)/T[1],2/(a*T[1])]
        A = np.array([A_1,A_2,A_3])
        
        b = [6*(q[:,1]-q[:,0])/(T[0]**2),6/(1-a)*((q[:,1]-q[:,0])/(T[0]**2)+(q[:,2]-q[:,1])/(T[1]**2)),6*(q[:,2]-q[:,1])/(T[1]**2)]
        v = np.concatenate((np.zeros((1,q.shape[0])),np.linalg.inv(A)@b,np.zeros((1,q.shape[0]))),0).T
        q_a1 = q[:,0]+v[:,1]/3*a*T[0]
        q_a2 = q[:,-1]-v[:,-2]/3*a*T[-1]
        q_a = np.concatenate((np.array([q[:,0]]).T,np.array([q_a1]).T,q[:,1:-1],np.array([q_a2]).T,np.array([q[:,-1]]).T),1)
        
        T_a = np.array([a*T[0],(1-a)*T[0],(1-a)*T[1],a*T[1]])

        d_1  = q_a[:,1:]-q_a[:,0:-1]-v[:,0:-1]*T_a
        d_2 = v[:,1:]-v[:,0:-1] 
        c_2 = 3/(T_a**2)*d_1-1/T_a*d_2
        a = 2*c_2
        c_0 = q_a[:,0:-1]
        c_1 = v[:,0:-1]
        d_1  = q_a[:,1:]-q_a[:,0:-1]-v[:,0:-1]*T_a
        d_2 = v[:,1:]-v[:,0:-1]
        c_2 = 3/(T_a**2)*d_1-1/T_a*d_2
        c_3 = -2/(T_a**3)*d_1+1/(T_a**2)*d_2
        c = (c_0,c_1,c_2,c_3)
    else:
        ud = 1/T
        ld = 1/T
        ud[0] = (1-a)/T[0]
        ld[0] = 1/(((1-a)**2)*T[0])
        ud[-1] = 1/(((1-a)**2)*T[-1])
        ld[-1] = (1-a)/T[-1]
        d = list()
        d.append(0)
        d.extend(2/T[0:-1]+2/T[1:])
        d.append(0)
        d = np.array(d)
        d[0] = 1/(a*T[0])
        d[1] = 2/((1-a)*T[0])+2/T[1]
        d[-2] = 2/T[-2]+2/((1-a)*T[-1])
        d[-1] = 1/(a*T[-1])
        A = np.diag(d)+np.diag(ld,-1)+np.diag(ud,1)
        b_1 = np.array([3/(T[0:-1]**2)]).T*(q[:,1:-1]-q[:,0:-2]).T
        b_2 = np.array([(3/(T[1:]**2))]).T*(q[:,2:]-q[:,1:-1]).T
        b = b_1+b_2
        b = np.concatenate((np.zeros((1,q.shape[0])),b,np.zeros((1,q.shape[0]))),0)
        b[0,:] = (3/(T[0]**2))*(q[:,1]-q[:,0])
        b[1,:] = (-3/(((1-a)*T[0])**2))*q[:,0]+3*(1/(((1-a)*T[0])**2)-1/(T[1]**2))*q[:,1]+(3/(T[1]**2))*q[:,2]
        b[-2,:] = (3/(((1-a)*T[-1])**2))*q[:,-1]+3*(1/(T[-2]**2)-1/(((1-a)*T[-1])**2))*q[:,-2]-(3/(T[-2]**2))*q[:,-3]
        b[-1,:] = (3/(T[-1]**2))*(q[:,-1]-q[:,-2])
        v = np.concatenate((np.zeros((1,q.shape[0])),np.linalg.inv(A)@b,np.zeros((1,q.shape[0]))),0).T
        q_a1 = q[:,0]+v[:,1]/3*a*T[0]
        q_a2 = q[:,-1]-v[:,-2]/3*a*T[-1]
        q_a = np.concatenate((np.array([q[:,0]]).T,np.array([q_a1]).T,q[:,1:-1],np.array([q_a2]).T,np.array([q[:,-1]]).T),1)
        T_a = list()
        T_a.append(a*T[0])
        T_a.append((1-a)*T[0])
        T_a.extend(T[1:-1])
        T_a.append((1-a)*T[-1])
        T_a.append(a*T[-1])
        T_a = np.array(T_a)
        d_1  = q_a[:,1:]-q_a[:,0:-1]-v[:,0:-1]*T_a
        d_2 = v[:,1:]-v[:,0:-1] 
        c_2 = 3/(T_a**2)*d_1-1/T_a*d_2
        a = 2*c_2
        c_0 = q_a[:,0:-1]
        c_1 = v[:,0:-1]
        d_1  = q_a[:,1:]-q_a[:,0:-1]-v[:,0:-1]*T_a
        d_2 = v[:,1:]-v[:,0:-1]
        c_2 = 3/(T_a**2)*d_1-1/T_a*d_2
        c_3 = -2/(T_a**3)*d_1+1/(T_a**2)*d_2
        c = (c_0,c_1,c_2,c_3)
    return T_a,q_a,v,a,c
def total_time(T):
    return np.sum(T)
def nonlcon(T,q,v_max,a_max):
    T_a,q_a,v,a,c = get_Tqvac(T,q)
    min_v = np.array([v_max]).T+v
    max_v = np.array([v_max]).T-v
    min_a = np.array([a_max]).T+a
    max_a = np.array([a_max]).T-a
    return np.reshape(np.concatenate((max_v,min_v,max_a,min_a),1),2*v.size+2*a.size)

class Trajectory():
    def __init__(self):
        self.dof = 0
        self.num_via_point = 0
        self.position = []
        self.velocity = []
        self.acceleration = []
        self.duration = []
        self.initial_time = []
        self.v_max = []
        self.a_max = []
        c_0 = []
        c_1 = []
        c_2 = []
        c_3 = []
        c = [c_0,c_1,c_2,c_3]
        self.coefficient = c
        self.isOptimal = False
    def _compute_initial_time(self):
        initial_time = []
        initial_time.append(0)
        initial_time.extend(np.cumsum(self.duration)[:-1].tolist())
        return initial_time
    def set_position(self,position):
        self.position = np.array(position)
        self.dof = self.position.shape[0]
        self.num_via_point = self.position.shape[1]
        self.duration = np.ones(self.num_via_point).tolist()
        self.initial_time = self._compute_initial_time()
        self.isOptimal = False
    def set_bound(self,v_max,a_max):
        if (len(v_max)==self.dof) & (len(a_max)==self.dof):
            self.v_max = v_max
            self.a_max = a_max
        else:
            print('the given boundaries have different dimension from the DOF.')
    def oneViaPoint(self,q_0):
        a = 1/3
        q_N = self.position
        dq = q_N-q_0
        T_v = 1.5/(1-a)*np.amax(np.absolute(dq)/self.v_max)
        T_a = np.math.sqrt(6/(1-a)*np.amax(np.absolute(dq)/self.a_max))
        T_N = np.amax((T_v,T_a))
        T_min = [a*T_N,(1-2*a)*T_N,a*T_N]
        self.isOptimal = True
        self.position = [(q_0+(a**2)/(1-a)*dq).T[0].tolist(),(q_N-(a**2)/(1-a)*dq).T[0].tolist(),(q_N).T[0].tolist()]
        self.velocity = [(3*a/(1-a)*dq/T_N).T[0].tolist(),(3*a/(1-a)*dq/T_N).T[0].tolist(),(np.zeros(q_0.shape)).T[0].tolist()]
        self.acceleration = [(6/(1-a)*dq/(T_N**2)).T[0].tolist(),(-6/(1-a)*dq/(T_N**2)).T[0].tolist(),(np.zeros(q_0.shape)).T[0].tolist()]
        c_0 = np.concatenate((q_0,q_0+(a**2)/(1-a)*dq,q_N-(a**2)/(1-a)*dq),1)
        c_1 = np.concatenate((np.zeros(q_0.shape),3*a/(1-a)*dq/T_N,3*a/(1-a)*dq/T_N),1)
        c_2 = np.concatenate((np.zeros(q_0.shape),3/(1-a)*dq/(T_N**2),-3/(1-a)*dq/(T_N**2)),1)
        c_3 = np.concatenate((1/(a*(1-a))*dq/(T_N**3),-2/((1-2*a)*(1-a))*dq/(T_N**3),1/(a*(1-a))*dq/(T_N**3)),1)
        self.coefficient = [c_0,c_1,c_2,c_3]
        self.duration = T_min
        self.initial_time = self._compute_initial_time()
    def time_optimal(self,q_0):
        if len(self.position[0])<=1:
            self.oneViaPoint(q_0)
        else: 
            via_points = np.concatenate((q_0,self.position),1)
            cons = lambda T : nonlcon(T,via_points,self.v_max,self.a_max)
            ineq_cons = {'type': 'ineq','fun' : cons}
            T_min = minimize(total_time,np.ones((1,self.num_via_point)),method='SLSQP',constraints=[ineq_cons])
            T_a,q_a,v,a,c = get_Tqvac(T_min.x,via_points)
            self.isOptimal = True
            self.position = q_a[:,1:].T.tolist()
            self.velocity = v[:,1:].T.tolist()
            self.acceleration = np.concatenate((a[:,1:],np.zeros((self.dof,1))),1).T.tolist()
            self.coefficient = c
            self.duration = T_a.tolist()
            self.initial_time = self._compute_initial_time()
    def evaluate(self,t_vec):
        bin = np.digitize(t_vec,self.initial_time)-1
        position = []
        velocity = []
        acceleration = []
        for i in range(len(t_vec)):
            tau = t_vec[i]-self.initial_time[bin[i]]
            q = np.zeros((self.dof,1))
            v = np.zeros((self.dof,1))
            a = np.zeros((self.dof,1))
            c = self.coefficient
            q = c[0][:,bin[i]]+c[1][:,bin[i]]*(tau)+c[2][:,bin[i]]*(tau**2)+c[3][:,bin[i]]*(tau**3)
            v = c[1][:,bin[i]]+2*c[2][:,bin[i]]*(tau)+3*c[3][:,bin[i]]*(tau**2)
            a = 2*c[2][:,bin[i]]+6*c[3][:,bin[i]]*(tau)
            position.append(q.tolist())
            velocity.append(v.tolist())
            acceleration.append(a.tolist())
        return position,velocity,acceleration