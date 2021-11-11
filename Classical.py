import numpy as np
import math
import matplotlib.pyplot as plt
import pandas as pd

a=1
x_input=50
y_input= 10
theta_input=-10
k1=-1
k2=-0.5
u_his=[]
y_his=[y_input]
x_his=[x_input]
theta_his=[theta_input]
while(1):
    print('This is %d iteration' % (a))
    output = k1*y_input + k2*theta_input
    y_input = y_input + 0.5 * 0.1 * math.sin(theta_input / 180 * math.pi)
    x_input = x_input + 0.5 * 0.1 * math.cos(theta_input / 180 * math.pi)
    theta_input = theta_input / 180 * math.pi + 0.5 * 0.1 * math.tan(output / 180 * math.pi) / 2.5
    theta_input = theta_input * 180 / math.pi
    y_his.append(y_input)
    x_his.append(x_input)
    theta_his.append(theta_input)
    u_his.append(output)
    a = a + 1
    if a == 3000:
        break
        pass

# 打印输出结果
fig=plt.figure(figsize=[9,9],num=0)
plt.plot(range(1,a+1),y_his)
plt.plot(range(1,a+1),theta_his)
plt.plot(range(1,a),u_his)
fig=plt.figure(figsize=[9,9],num=1)
plt.plot(x_his,y_his)
plt.show()
# dataframe_x=pd.DataFrame(x_his)
# dataframe_y=pd.DataFrame(y_his)
# dataframe_theta=pd.DataFrame(theta_his)
# dataframe_u=pd.DataFrame(u_his)
# dataframe_x.to_excel('x4.xlsx')
# dataframe_y.to_excel('y4.xlsx')
# dataframe_theta.to_excel('theta4.xlsx')
# dataframe_u.to_excel('u4.xlsx')