import pandas as pd
import numpy as np
from geopy.distance import geodesic
import matplotlib.pyplot as plt
import functions as fun




"""
plot utilizzo degli waypoint
"""



df_bubble=pd.read_csv("../data/df_to_plot.csv")
df_bubble.rename(columns={'astext(k.coords)':'coor'},inplace=True)
df_bubble


#calcola le frequenze degli waypoint
waypoint=fun.frequency(df_bubble,"sid")
waypoint
N=len(waypoint)

coor_dict={}
for i in range(df_bubble.shape[0]):
    key=df_bubble.iloc[i]["sid"]
    if key not in coor_dict:
        coor_dict[key]=df_bubble.iloc[i]["coor"]

coor_dict
#vettore x
x=np.zeros(N)
y=np.zeros(N)
z=np.zeros(N)
i=0
for key in waypoint:
    c=fun.coord(coor_dict[key])
    x[i]=c[0]
    y[i]=c[1]
    z[i]=waypoint[key]
    i=i+1
z

plt.scatter(x, y, s=z*0.1, alpha=0.5)
plt.scatter(50.037753, 8.560964,color="red")
plt.show()





plt.figure(figsize=(20,15))
for i in range(coord_traj.shape[0]):
    plt.plot(coordinate_x[i,:],coordinate_y[i,:],linewidth=num_percorsi[i]/10,label = "trajectory"+str(i))
plt.scatter(50.037753, 8.560964,color="red")

plt.savefig("plot/traj_1.png")
