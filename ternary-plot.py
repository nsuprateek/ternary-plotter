import os
import sys
import subprocess

os.chdir(os.path.dirname(os.path.abspath(__file__)))

# Only create the project environment when no virtual environment exists.
if sys.prefix == sys.base_prefix:
    venv_dir = ".venv"
    if not os.path.exists(venv_dir):
        print("Dependencies not installed, installing now")
        subprocess.check_call([sys.executable, "setup.py"])

    if os.name == "nt":  # if windows
        venv_python = os.path.join(venv_dir, "Scripts", "python.exe")
    else:
        venv_python = os.path.join(venv_dir, "bin", "python")

    subprocess.check_call([
        venv_python,
        os.path.abspath(__file__),
        *sys.argv[1:]
    ])
    sys.exit()
# ======== ARGUMENTS ============

import argparse

parser = argparse.ArgumentParser()

parser.add_argument(
    "-f", "--file",
    help="Input CSV file",
    default="data.csv"
)

parser.add_argument(
    "-s", "--size",
    help="Size of points on the plot",
    type=int,
    default=30
)

parser.add_argument(
    "--no-view",
    help="Don't show the final plot in a matplotlib viewer",
    action="store_false",
    dest="view"
)

args = parser.parse_args()

# ======== MAIN PROGRAM =========

import matplotlib.pyplot as plt
import mpltern
import pandas as pd

df = pd.read_csv(args.file, header=None)

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
ax.scatter(top, left, right, s=args.size)
filename = f"Ternary Plot ({labels.iloc[col['top']]}-{labels.iloc[col['left']]}-{labels.iloc[col['right']]}).png"
plt.savefig(filename)
print(f"Created {filename}")

if args.view:
    plt.show()