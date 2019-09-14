import numpy as np
import matplotlib.pyplot as plt


import curve_handler as p



CONTROL = np.array([[-12.73564, 9.03455],
[-26.77725, 15.89208],
[-42.12487, 20.57261],
[-15.34799, 4.57169],
[-31.72987, 6.85753],
[-49.14568, 6.85754],
[-38.09753, -1e-05],
[-67.92234, -11.10268],
[-89.47453, -33.30804],
[-21.44344, -22.31416],
[-32.16513, -53.33632],
[-32.16511, -93.06657],
[-2e-05, -39.83887],
[10.72167, -70.86103],
[32.16511, -93.06658],
[21.55219, -22.31397],
[51.377, -33.47106],
[89.47453, -33.47131],
[15.89191, 0.00025],
[30.9676, 1.95954],
[45.22709, 5.87789],
[14.36797, 3.91883],
[27.59321, 9.68786],
[39.67575, 17.30712]])
KNOTS = np.linspace(0,1,26)
KNOTS[ 1] = KNOTS[ 2] = KNOTS[ 0]
KNOTS[-3] = KNOTS[-2] = KNOTS[-1]

cd = p.CurveDesigner(d_vector=CONTROL,u_vector=KNOTS)
#cd(d_vector=CONTROL,u_vector=KNOTS)
# but we need many new points... hmmm... and then to plot them.
spline = cd.generateSpline(5000)
   
#Plot s(u) and control points using points generated by the deBoor-algorithm
cd.plot(spline, cd.d_vector, control = True)

basisspline = cd.splineFromBasisFunc(5000)

#Plot s(u) and control points using points generated by basis function multiplication and summation
cd.plot(basisspline, cd.d_vector, control = True)

