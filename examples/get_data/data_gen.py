import pandas as pd
import numpy as np
import random
from datetime import datetime
import matplotlib.pyplot as plt


# create random numbers between a range and sort from highest to lowest

data_cols = ['Experimental Group', 'Subject_ID', 'Date', 'Diet Type', 'Blood Glucose Levels', 'Weight']

# diet type: Normal, high fat 
# normal glucose : 85 +/-  22.5
# high glucose: 152.4 +/- 15.3

norm_gluc = []
weight =[]
for i in range(150):
    r = random.triangular((60 + (i%5)*2),(100), (85.6 + i%5))
    norm_gluc.append(r)
    w = random.triangular(0.20 ,0.30 ,0.25)
    weight.append(w)

fat = []
high_gluc = []
for i in range(150):
    r = random.triangular(60, 170, 130)
    high_gluc.append(r)
    w = random.triangular(0.20, 0.60, 0.40)
    fat.append(w)
high_gluc = sorted(high_gluc)
fat = sorted(fat)


matrix = [[0 for x in range(len(data_cols))]for y in range(301)]
#for i in range(len(data_cols)):
    #matrix[0][i] = data_cols[i]

mice = {}
weights = {}
count = 0
for i in range(300):
    if i < 150:
        matrix[i][0] = 'Control'
        matrix[i][3] = 'Normal'
        matrix[i][4] = norm_gluc[i-1]
        matrix[i][1] = "Mouse" + str(i%5) 
        matrix[i][5] =  str(weight[i-1]) + ' g'
        if str(i%5) == str(4):
            count+=1
        
        if str(i%5) in mice:
            mice[str(i%5)].append(matrix[i][4])
            weights[str(i%5)].append(matrix[i][5])
        else:
            mice[str(i%5)] = [matrix[i][4]]
            weights[str(i%5)] = [matrix[i][5]]
        matrix[i][2] = str(int(i/6) + 1) + str(int(i/16)+1)+'2018'
    if i >= 150:
        matrix[i][0] = 'Experimental'
        matrix[i][3] = 'High'
        matrix[i][4] = high_gluc[i - 151]
        matrix[i][1] = "Mouse" + str(i%5 + 5) 
        matrix[i][5] = str(fat[i- 151]) +' g'
        if str(i%5+5) in mice:
            mice[str(i%5+5)].append(matrix[i][4])
            weights[str(i%5+5)].append(matrix[i][5])
        else:
            mice[str(i%5+5)] = [matrix[i][4]]
            weights[str(i%5+5)] = [matrix[i][5]]
        matrix[i][2] = str(int((i-151)/6) + 1) + str(int((i-151)/16)+1) + '2018'

temp = '\t'.join(data_cols)
print(temp)
np.savetxt('np.csv', matrix, delimiter=',', header=temp, fmt='%5s') 
print(mice)

"""
df1 = pd.DataFrame(data = matrix)
print(df1)
#print(df[0])
#df[5].plot()
#plt.show()
df1.to_csv('example_mouse_data1.csv', sep='\t')

# line plot session recorded vs blood glucose for each mouse

df = pd.DataFrame({'x': range(1,31), 'y0': mice[str(0)], 'y1': mice[str(1)], 'y2': mice[str(2)], 'y3': mice[str(3)],'y4':mice[str(4)] , 'y5':mice[str(5)] , 'y6':mice[str(6)], 'y7':mice[str(7)] , 'y8':mice[str(8)] , 'y9':mice[str(9)] })

plt.plot( 'x', 'y0', data=df, marker='o', markerfacecolor='blue', markersize=12, color='skyblue', linewidth=4)
plt.plot( 'x', 'y1', data=df, marker='o', markerfacecolor='blue', markersize=12, color='olive', linewidth=4)
plt.plot( 'x', 'y2', data=df, marker='', color='olive', linewidth=2)
plt.plot( 'x', 'y3', data=df, marker='', color='blue', linewidth=2, linestyle='dashed', label="toto")
plt.plot( 'x', 'y4', data=df, marker='', color='purple', linewidth=2, linestyle='dashed', label="toto")
plt.plot( 'x', 'y5', data=df, marker='', color='yellow', linewidth=2, linestyle='dashed', label="toto")
plt.plot( 'x', 'y6', data=df, marker='', color='red', linewidth=2, linestyle='dashed', label="toto")
plt.plot( 'x', 'y7', data=df, marker='', color='green', linewidth=2, linestyle='dashed', label="toto")
plt.plot( 'x', 'y8', data=df, marker='', color='pink', linewidth=2, linestyle='dashed', label="toto")
plt.plot( 'x', 'y9', data=df, marker='', color='orange', linewidth=2, linestyle='dashed', label="toto")
plt.show()



# avg weight vs. avg blood gluc levels per animal
print(mice)
print(weights)
a =[]
b = []
for k in mice:
    temp = map(int, mice[k])
    w = [x[:-3] for x in weights[k]]
    tempw = map(float, w)
    a.append(sum(temp)/float(len(temp)))
    b.append(sum(tempw)/float(len(tempw)))
plt.plot(np.array(a), np.array(b), marker='o', markersize=12, linestyle='', color='green')
plt.show()
controlbgl = []
controlw = []
expw = []
expbgl = []
for k in mice:
    if k > '5':
        temp = map(int, mice[k])
        w = [x[:-3] for x in weights[k]]
        tempw = map(float, w)
        controlbgl.append(sum(temp)/float(len(temp)))
        controlw.append(sum(tempw)/float(len(tempw)))
    else:
        temp = map(int, mice[k])
        w = [x[:-3] for x in weights[k]]
        tempw = map(float, w)
        expbgl.append(sum(temp)/float(len(temp)))
        expw.append(sum(tempw)/float(len(tempw)))
x = [(sum(controlbgl)/float(len(controlbgl))), (sum(expbgl)/float(len(expbgl)))]
y = [(sum(controlw)/float(len(controlw))), (sum(expw)/float(len(expw)))]
plt.plot(x,y, 'r+', markersize=20)
plt.show()

plt.bar()

plt.
"""
