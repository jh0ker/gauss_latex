# gauss.py
Solves a system of linear equations using the Gauss-Jordan algorithm and exports all steps to text or LaTeX code.

## Requirements:
Python 2.7 or higher

## Usage:

To show the help text:
```
./gauss.py -h
```

To do the thing:
```
./gauss.py "3.0;8;2" "2;-3/2;0"
```

To do the thing, but with LaTeX and ignoring steps that don't change the matrix (you probably want this):
```
./gauss.py "1;2;1;1;1;2" "-1;-2;-2;2;1;1" "2;4;3;-1;0;-1" "1;2;2;-2;1;1" -s --latex 
```
