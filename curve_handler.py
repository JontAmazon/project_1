# -*- coding: utf-8 -*-
import numpy as np
import matplotlib.pyplot as plt

'''QUESTIONS:'''
# 1. uu is selected correctly. But is dd? I guess so, but not sure...
#    EV TODO = try it differently. Does is work now/still?

'''TODO'''
# 1.

'''PROGRAM'''
class CurveDesigner(object):
    """Class to design 2D curves using cubic splines and control points, 
    as well as by fitting cubic splines through given data points."""

    def __init__(self, d_vector = None, u_vector = None, interpolation_points = None): #Constructor method for a CurveDesigner-object
        
        if d_vector is None:
            self.d_vector = np.array([[1, 4], [0.5, 6], [5, 4], [3, 12], [11, 14], 
                                            [8, 4], [12, 3], [11, 9], [15, 10], [17, 8]]) #Default control point-vector
        else:
            self.d_vector = d_vector
            
        if u_vector is None: 
            self.u_vector = np.array([0, 0, 0, 0, 1/8, 2/8, 3/8, 4/8, 5/8, 6/8, 1, 1, 1, 1]) #Default knot vector
        else:
            self.u_vector = u_vector
            
    
    def __call__(self, d_vector = None, u_vector = None): #Method for using a created CurveDesigner-instance
        
        if d_vector is not None: 
            self.d_vector = d_vector

        if u_vector is not None: 
            self.u_vector = u_vector
            
    def generateSpline(self, n):
        ''' This funktion takes in control points (d_vector) and node points 
        (u_vector) and returns the cubic spline for those points using the 
        deBoor method for cubic splines
        
        n determines the "resolution" of the spline
        
        '''

        self.u = np.linspace(min(self.u_vector)+0.001,max(self.u_vector)-0.001,n)  # generate n- long vector of u-values to generate spline
        spline = np.empty([2,n])
        
        #This for-loop can probably be replaced with vector operations 
        for j in range(0,n):
            i = int(self.u_vector.searchsorted([self.u[j]]))   # finds the "hot interval"
            uu = self.u_vector[i-3:i+3] #extracts the relevant 
            dd = self.d_vector[i-3:i+1]   
            S_u = self.deBoor(dd,uu,self.u[j]) # generate the S value for our current u. 
            spline[:,j] = S_u  # add the the point to the spline vector
        return spline
    
    
    
    def deBoor(self, dd, ui, u, blossom = False):
        """"Calculates new points s(u) on a curve using the De Boor algorithm.
        dd: [d_(I-2), ..., d_(I+1)] : control points for our hot interval
        uu: [u_(I-2), ..., u_(I+3)] : node points for our 
        u: parameter for generating a new point."""
        uu2, uu1, u0, u1, u2, u3 = ui
        
        a21 = (u1-u)/(u1-uu2)
        a31 = (u2-u)/(u2-uu1)
        a41 = (u3-u)/(u3-u0)
        d21 = a21*dd[0] + (1-a21)*dd[1]
        d31 = a31*dd[1] + (1-a31)*dd[2]
        d41 = a41*dd[2] + (1-a41)*dd[3]
        
        a32 = (u1-u)/(u1-uu1)
        a42 = (u2-u)/(u2-u0)
        d32 = a32*d21 + (1-a32)*d31
        d42 = a42*d31 + (1-a42)*d41
        
        a43 = (u1-u)/(u1-u0)
        d43 = a43*d32 + (1-a43)*d42
        
        #If blossom is set to True, return the wanted blossoms and control point for u_blossom
        #instead of the spline point
        if blossom:
            blossoms1 = d21, d31, d41 #Defines the first iteration blossom points d[u, u_{I-1}, u_I], d[u, u_I, u_{I + 1}] and d[u, u_{I+1}, u_{I+2}]
            blossoms2 = d32, d42 #Defines the second iteration blossom points d[u, u, u_I] 
            control_point = dd[0] #Defines the control point
            return blossoms1, blossoms2, control_point, d43
        
        return d43
        
    def basis_func(self, j):
        def N(u,j,k):
            if(k==0):
                if(self.u_vector[j]==self.u_vector[j-1]):
                    return 0
                if((self.u_vector[j-1]<=u) and (u<self.u_vector[j])):
                    return 1
                return 0
            #Prevent out of bounds and divide by zero.
            if j==0:
                if (self.u_vector[j+k]-self.u_vector[j]):
                    return (self.u_vector[j+k]-u)/(self.u_vector[j+k]-self.u_vector[j])*N(u,j+1,k-1)
                else:
                    return 0
            
            if (j+1)==(len(self.u_vector)-2):
                if (self.u_vector[j+k-1]-self.u_vector[j-1]):
                    return (u-self.u_vector[j-1])/(self.u_vector[j+k-1]-self.u_vector[j-1])*N(u,j,k-1)    
                else:
                    return 0

            #Not out of bounds, check if divide by zero
            if ((self.u_vector[j+k-1]-self.u_vector[j-1]) and (self.u_vector[j+k]-self.u_vector[j])):
                return (u-self.u_vector[j-1])/(self.u_vector[j+k-1]-self.u_vector[j-1])*N(u,j,k-1) \
                        +(self.u_vector[j+k]-u)/(self.u_vector[j+k]-self.u_vector[j])*N(u,j+1,k-1)
            
            if ((self.u_vector[j+k-1]-self.u_vector[j-1]) and not (self.u_vector[j+k]-self.u_vector[j])):
                return (u-self.u_vector[j-1])/(self.u_vector[j+k-1]-self.u_vector[j-1])*N(u,j,k-1)
            
            if ((self.u_vector[j+k]-self.u_vector[j]) and not (self.u_vector[j+k-1]-self.u_vector[j-1])):
                return (self.u_vector[j+k]-u)/(self.u_vector[j+k]-self.u_vector[j])*N(u,j+1,k-1)
        
        def evaluate_N(u):
            return N(u,j,3) 
        return evaluate_N
    
    def plot(self, spline, d_vector, control = False, blossom = False, blossoms1 = None, blossoms2= None, control_point = None, d43 = None):
        s1 = spline[0,:]        # generate the x-coordinates for the spline
        s2 = spline[1,:]        # generate the y-coordniates for the spline

        d0, d1 = zip(*d_vector) #Separates the x- and y-values for the control points
        
        if control:
            plt.plot(d0, d1, color = 'r', linewidth = 0.3) #Plot line inbetween control points
            plt.plot(d0, d1, 'bo', color = 'r') #Plot the control points
         
        plt.plot(s1,s2) #Plots the spline 
        
        if blossom:
#            if blossoms1 is not None and control_point is not None and d43 is not None:
            b1 = np.array(blossoms1)
            plt.plot(b1[:, 0], b1[:, 1], color = 'g', linewidth = 1) #Plot a line between the first blossom points in green.
            plt.plot(b1[:,0], b1[:,1], 'bo', color = 'g') #Plot the first iteration blossom points in green.
            b2 = np.array(blossoms2)
            plt.plot(b2[:, 0], b2[:, 1], color = 'y', linewidth = 1) #Plot a line between the second iteration blossom points in yellow.
            plt.plot(b2[:,0], b2[:,1], 'bo', color = 'y') #Plot the second iteration blossom points in yellow.
            plt.plot(control_point[0], control_point[1], 'bo', color = 'm') #Highlight the control point in magenta.
            plt.plot(d43[0], d43[1], 'bo', color = 'b') #Plot the given spline point in blue.
        
        plt.show()
        
    def splineFromBasisFunc(self, n):
        #This function evaluates S(u) for each u using the basis functions 
        #given from basis_func
        
        #Create empty list for storing L basis functions
        Ni = (len(self.u_vector)-2)*[None]
        
        #Create the basis functions for each value j (each possible hot interval) and store them in a list
        for j in range(len(self.u_vector)-2):
            Ni[j] = self.basis_func(j)
            
        #Use the control points and the basis functions to create s(u)
        
        self.u = np.linspace(min(self.u_vector)+0.001,max(self.u_vector)-0.001,n)  #Generate n-vector of u-values to generate spline
        Spline = np.empty([2,n]) #Create empty vector for filling with points on the spline
        
        #For each u in the u-vector, compute the spline and insert into spline vector
        for j in range(0,n):
            i = int(self.u_vector.searchsorted([self.u[j]])) #Find the "hot interval"
            
            dd = self.d_vector[i-3:i+1] #Extract the useful values of d_i from i = I - 2 to i = I + 1
            Nfuncs = Ni[i-3:i+1] #Extract the useful values of N^3_i from i = I - 2 to i = I + 1
            
            #Generate the spline for our current u by summing the products of each d_i with its corresponding N^3_i
            S_u = np.empty([])
            for p in range(len(dd)):
                Nval = Nfuncs[p](self.u[j])
                S_u = S_u + dd[p, :]*Nval
                
            Spline[:,j] = S_u  # add the the point to the spline vector   
        return Spline
    
    def generateBlossoms(self, u_blossom):
        i = int(self.u_vector.searchsorted(u_blossom)) #Find the "hot interval" for u_blossom
        uu = self.u_vector[i-3:i+3] #Extract the relevant interval of knot points  
        dd = self.d_vector[i-3:i+1] #Extract the relevant interval of control points
        blossoms1, blossoms2, control_point, d43 = self.deBoor(dd,uu, u_blossom, blossom = True) #Generate the blossoms and control point for u_blossom
        return blossoms1, blossoms2, control_point, d43
        
"""
#Blossom recursion.
cd = CurveDesigner()

#Find the "hot interval".
u = 0.01 # om man börjar u- på noll så kommer uu bli tomt set så frågan är hur vi ska välja första u
i = int(cd.u_vector.searchsorted([u])) #6 for u=0.3.

#Select the six relevant u's and the four relevant d's.
uu = cd.u_vector[i-3:i+3] #
dd = cd.d_vector[i-4:i]                                                            # Correct?

new_u = cd.deBoor(dd, uu, u)
# but we need many new points... hmmm... and then to plot them.
spline = cd.generateSpline(50)
   
#Plot s(u) and control points using points generated by the deBoor-algorithm
cd.plot(spline, cd.d_vector, control = True)

basisspline = cd.splineFromBasisFunc(50)

#Plot s(u) and control points using points generated by basis function multiplication and summation
cd.plot(basisspline, cd.d_vector, control = True)
"""

