# Get data from existing dataset
If you have an API Key, Lab and community proceed to the next step.

API Key:
1. Login to Scicrunch or create an account
2. Go to My Account -> API Keys
3. Generate an API Key or get the one under Key

Lab:
Use the publicly available lab, ODC-SCI Demo Laboratory, to retrieve an example dataset. 


## Import module and libraries to plot the data
```python

    from scicrunch.datasets import *
    import pandas as pd
    import numpy as np
    import matplotlib.pyplot as plt
```

## Make an Interface object to connect with the scicrunch server
Include your api key, the lab name and the community name.
```python
    dataset_id = '42'
    dataset_name = 'Example Analysis Dataset'
    lab_name = 'ODC-SCI Demo Laboratory'
    interface = datasets.Interface(
        "api_key",
        lab_name
    )
```

## Get the data from the Example Analysis Dataset
The data will be in the format of a list of dictionaries, each list entry is a seperate data entry, the dictionary contains the data corresponding to the data field
```python
    data = Interface.getdata(dataset_name)
    print(data)
```
## Get data fields
These correspond to what the data means and will be useful in analysis

```python
    info = Interface.getInfo(dataset_name)
    print(info)

    headers = []
    for i in info['fields']:
        headers.append(i)
    print(headers)
```

## Organize the data into a matrix with the columns as the data fields and the rows as seperate data entries
This will put the data into a DataFrame object from the pandas library. This will make it easier to make graphs and plots with.
```python
    matrix = [[0 for x in range(len(headers))]for y in range(len(data))]

    for d in range(len(data)):
        for h in range(len(headers)):
            matrix[d][h] = data[d][headers[h]]


    df1 = pd.DataFrame(data = matrix)

    w = headers.index("Weight")
    eG = headers.index("# Experimental Group")
    d = headers.index("Diet Type")
    bgl = headers.index("Blood Glucose Levels")
    sid = headers.index("Subject_ID")
    date = headers.index("Date")
    
```


# Organization of Data
Put data into dictionaries and lists by experimental group
```python
    groups = {}
    lines = {}
    for m in matrix:
        if m[sid] in lines:
            lines[m[sid]]['weight'].append(m[w][:-2])
            lines[m[sid]]['glucose'].append(m[bgl])
        else:
            lines[m[sid]] = {'weight': [m[w][:-2]], 'glucose': [m[bgl]]}
        if m[eG] in groups:
            if m[sid] not in groups[m[eG]]:
                groups[m[eG]].append(m[sid])
        else:
            groups[m[eG]] = [m[sid]]
```
# Plots
## Line Plot:
### Weight vs. Blood Glucose for each mouse 
One line for each mouse.
x-axis: Weight
y-axis: Blood Glucose Level
Control group has markers 'o'
Experimental group has '+' markers
```python
    for l in lines:
        if l in groups['Control']:
            plt.plot(lines[l]['weight'], lines[l]['glucose'], marker='o', markerfacecolor='red')
        else:
            plt.plot(lines[l]['weight'], lines[l]['glucose'], marker='+', markerfacecolor='blue')
    plt.show()


```

## Bar Graph
### Average Weight and Blood Glucose Levels for Each Experimental Group
```python
    c_weight = 0
    e_weight = 0
    c_gbl = 0
    e_gbl = 0

    for l in lines:
        if l in groups['Control']:
            c_weight = c_weight + sum(map(float, lines[l]['weight']))/float(len(lines[l]['weight']))
            c_gbl = c_gbl + sum(map(float, lines[l]['glucose']))/float(len(lines[l]['glucose']))
        else:
            e_weight = e_weight + sum(map(float, lines[l]['weight']))/float(len(lines[l]['weight']))
            e_gbl = e_gbl + sum(map(float, lines[l]['glucose']))/float(len(lines[l]['glucose']))

    c_weight = c_weight/len(groups['Control'])
    c_gbl = e_gbl/len(groups['Control'])
    e_weight = e_weight/len(groups['Experimental'])
    e_gbl = e_gbl/len(groups['Experimental'])

    bars = [c_weight, e_weight, c_gbl, e_gbl]
    labels = ['Control Weight', 'Experimental Weight', 'Control Blood Glucose Levels', 'Experimental Blood Glucose Levels']
    y_pos = np.arange(len(bars))
    plt.bar(y_pos, bars, align='center', alpha=0.5)
    plt.xticks(y_pos, labels)
    plt.ylabel('Quant')
    plt.show()

```

## Scatter Plot
### Average weight vs. Average Glucose for Each Mouse
```python
x = []
y = []
for l in lines:
    x.append(sum(map(float, lines[l]['weight']))/ float(len(lines[l]['weight'])))
    y.append(sum(map(float, lines[l]['glucose']))/ float(len(lines[l]['glucose'])))

plt.scatter(x, y)
plt.show()

```
