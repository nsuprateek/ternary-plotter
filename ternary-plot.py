import matplotlib.pyplot as plt
import mpltern
import pandas as pd


df = pd.read_csv("data.csv", header=None)

# Get 1st row (i.e. top, left right)
headers = df.iloc[0]
# Map column names to index
col = {name: idx for idx, name in enumerate(headers)}

# Get 2nd row
labels = df.iloc[1]
# top, left, right = df['top'].values, df['left'].values, df['right'].values
# top, left, right = df[['top', 'left', 'right']].to_numpy().T
data = df.iloc[2:]


values = data.iloc[:, [col["top"], col["left"], col["right"]]].astype(float)

# Normalise
values = values.div(values.sum(axis=1), axis=0) * 100 # axis=1 means sum of row

top = values.iloc[:, 0]
left = values.iloc[:, 1]
right = values.iloc[:, 2]

ax = plt.subplot(projection="ternary", ternary_sum=100.0)
ax.set_tlabel(labels.iloc[col["top"]])
ax.set_llabel(labels.iloc[col["left"]])
ax.set_rlabel(labels.iloc[col["right"]])

ax.grid()
ax.scatter(top, left, right, s=30)
plt.savefig('Ternary Graph.png')
plt.show()