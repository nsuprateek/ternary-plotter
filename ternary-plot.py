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
    "-ps", "--point-size",
    help="Size of points on the plot",
    type=int,
    default=30,
    dest="point_size"
)

parser.add_argument(
    "-ls", "--label-size",
    help="Size of labels",
    type=int,
    default=14,
    dest="label_size"
)

parser.add_argument(
    "--no-view",
    help="Don't show the final plot in a matplotlib viewer",
    action="store_false",
    dest="view"
)

parser.add_argument(
    "-g", "--show-grid",
    help="Show grid lines",
    action="store_true",
    dest="grid"
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
def clean_string(string):
    return (
        string
        .replace('$', '')
        .replace('{', '')
        .replace('}', '')
        .replace('_', '')
        .replace('^', '')
    )

# top, left, right = df['top'].values, df['left'].values, df['right'].values
# top, left, right = df[['top', 'left', 'right']].to_numpy().T
data = df.iloc[2:]


values = data.iloc[:, [col["top"], col["left"], col["right"]]].astype(float)

# Normalise
# ternary_sum auto normalises - this is unnecessary
# values = values.div(values.sum(axis=1), axis=0) * 100 # axis=1 means sum of row

top = values.iloc[:, 0]
left = values.iloc[:, 1]
right = values.iloc[:, 2]

ax = plt.subplot(projection="ternary", ternary_sum=100.0)
ax.set_tlabel(labels.iloc[col["top"]], fontsize=args.label_size)
ax.set_llabel(labels.iloc[col["left"]], fontsize=args.label_size)
ax.set_rlabel(labels.iloc[col["right"]], fontsize=args.label_size)

ax.grid(args.grid)

# ax.tick_params(labelrotation='horizontal')
ax.tick_params(length=0, label1On=False, label2On=False)

ax.taxis.set_label_rotation_mode("horizontal")
ax.laxis.set_label_rotation_mode("horizontal")
ax.raxis.set_label_rotation_mode("horizontal")

ax.scatter(top, left, right, s=args.point_size)

# Remove mathtext formatting before saving
labels = labels.map(clean_string)
filename = f"{labels.iloc[col['top']]} {labels.iloc[col['left']]} {labels.iloc[col['right']]}.png"

from pathlib import Path

output_dir = Path("Ternary Figures")
output_dir.mkdir(parents=True, exist_ok=True)

output_path = output_dir / filename

plt.savefig(output_path)
print(f"Saved {filename} to {output_path}")

if args.view:
    plt.show()
