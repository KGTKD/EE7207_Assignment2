import numpy as np
import math
import skfuzzy as fuzz
import skfuzzy.control as ctrl
import matplotlib.pyplot as plt
import pandas as pd

#定义范围
y_range = np.arange(-100,101,1,np.float32)
theta_range = np.arange(-180,181,1,np.float32)
u_range = np.arange(-30,31,1,np.float32)

# 创建模糊控制变量
y = ctrl.Antecedent(y_range, 'vertical position')
theta = ctrl.Antecedent(theta_range, 'angle of truck')
u = ctrl.Consequent(u_range, 'steering angle')

# 定义模糊集和其隶属度函数
y['BE']=fuzz.trapmf(y_range,[-100,-100,-40,-12.5])
y['BC']=fuzz.trimf(y_range,[-20,-10,0])
y['CE']=fuzz.trimf(y_range,[-6,0,6])
y['AC']=fuzz.trimf(y_range,[0,10,20])
y['AB']=fuzz.trapmf(y_range,[12.5,40,100,100])

theta['BO']=fuzz.trapmf(theta_range,[-180,-180,-120,-80])
theta['BR']=fuzz.trimf(theta_range,[-100,-65,-30])
theta['BH']=fuzz.trimf(theta_range,[-50,-25,0])
theta['HZ']=fuzz.trimf(theta_range,[-18,-0,18])
theta['AH']=fuzz.trimf(theta_range,[0,25,50])
theta['AR']=fuzz.trimf(theta_range,[30,65,100])
theta['AO']=fuzz.trapmf(theta_range,[80,120,180,180])

u['NB']=fuzz.trimf(u_range,[-30,-30,-16])
u['NM']=fuzz.trimf(u_range,[-25,-15,-5])
u['NS']=fuzz.trimf(u_range,[-12,-6,0])
u['ZE']=fuzz.trimf(u_range,[-5,-0,5])
u['PS']=fuzz.trimf(u_range,[0,6,12])
u['PM']=fuzz.trimf(u_range,[5,15,25])
u['PB']=fuzz.trimf(u_range,[16,30,30])

# 质心解模糊方式
u.defuzzify_method='centroid'

#输出规则
rule_PB=ctrl.Rule(antecedent=((y['BE'] & theta['BO'])|(y['BE'] & theta['BR'])|(y['BE'] & theta['BH'])
                              |(y['BC'] & theta['BO'])|(y['BC'] & theta['BR'])),
                  consequent=u['PB'],label='rule_PB')
rule_PM=ctrl.Rule(antecedent=((y['BE'] & theta['HZ'])|(y['BE'] & theta['AH'])
                              |(y['BC'] & theta['BH'])|(y['BC'] & theta['HZ'])
                              |(y['CE'] & theta['BO'])|(y['CE'] & theta['BR'])
                              |(y['AC'] & theta['BO'])),
                  consequent=u['PM'],label='rule_PM')
rule_PS=ctrl.Rule(antecedent=((y['BE'] & theta['AR'])|(y['BC'] & theta['AH'])|(y['CE'] & theta['BH'])
                              |(y['AC'] & theta['BR'])|(y['AB'] & theta['BO'])),
                  consequent=u['PS'],label='rule_PS')
rule_ZE=ctrl.Rule(antecedent=((y['CE'] & theta['HZ'])),
                  consequent=u['ZE'],label='rule_ZE')
rule_NS=ctrl.Rule(antecedent=((y['BE'] & theta['AO'])|(y['BC'] & theta['AR'])|(y['CE'] & theta['AH'])
                              |(y['AC'] & theta['BH'])|(y['AB'] & theta['BR'])),
                  consequent=u['NS'],label='rule_NS')
rule_NM=ctrl.Rule(antecedent=((y['AB'] & theta['BH'])|(y['AB'] & theta['HZ'])
                              |(y['AC'] & theta['HZ'])|(y['AC'] & theta['AH'])
                              |(y['CE'] & theta['AR'])|(y['CE'] & theta['AO'])
                              |(y['BC'] & theta['AO'])),
                  consequent=u['NM'],label='rule_NM')
rule_NB=ctrl.Rule(antecedent=((y['AB'] & theta['AH'])|(y['AB'] & theta['AR'])|(y['AB'] & theta['AO'])
                              |(y['AC'] & theta['AR'])|(y['AC'] & theta['AO'])),
                  consequent=u['NB'],label='rule_NB')

# 系统和运行环境初始化
system = ctrl.ControlSystem(rules=[rule_PB, rule_PM, rule_PS, rule_ZE, rule_NS, rule_NM, rule_NB])
sim = ctrl.ControlSystemSimulation(system)

#尝试
a=1
x_input=50
y_input=10
theta_input=-10
u_his=[]
x_his=[x_input]
y_his=[y_input]
theta_his=[theta_input]
# sim.input['vertical position'] = y_input
# sim.input['angle of truck'] = theta_input
# sim.compute()  # 运行系统
# output = sim.output['steering angle']
# print((output))
# y_input = y_input + 0.5 * 0.1 * math.sin(theta_input / 180 * math.pi)
# theta_input = theta_input + 0.5*0.1*math.tan(output/180*math.pi)/2.5
# print(y_input)
# print(theta_input)
while(1):
    print('This is %d iteration'%(a))
    sim.input['vertical position'] = y_input
    sim.input['angle of truck'] = theta_input
    sim.compute()  # 运行系统
    output = sim.output['steering angle']
    y_input = y_input + 0.5 * 0.1 * math.sin(theta_input / 180 * math.pi)
    x_input = x_input + 0.5 * 0.1 * math.cos(theta_input / 180 * math.pi)
    theta_input = theta_input/ 180 * math.pi + 0.5*0.1*math.tan(output/180*math.pi)/2.5
    theta_input = theta_input*180/math.pi
    y_his.append(y_input)
    x_his.append(x_input)
    theta_his.append(theta_input)
    u_his.append(output)
    a=a+1
    if a==3000:
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
dataframe_x=pd.DataFrame(x_his)
dataframe_y=pd.DataFrame(y_his)
dataframe_theta=pd.DataFrame(theta_his)
dataframe_u=pd.DataFrame(u_his)
dataframe_x.to_excel('x.xlsx')
dataframe_y.to_excel('y.xlsx')
dataframe_theta.to_excel('theta.xlsx')
dataframe_u.to_excel('u.xlsx')