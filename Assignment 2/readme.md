# Assignment 2 - Introduction Into Artificial Intelligence (CS370)

## The assignment given:
![](https://i.imgur.com/xvT9KRf.png)

### Example Input:
```
1 2
-1 -2 3 4
-1 -3 4
2 3
-2 -4
0
```

### Example Output:
```
The Clauses: {1: [1, 2], 2: [-1, -2, 3, 4], 3: [-1, -3, 4], 4: [2, 3], 5: [-2, -4]}
Unique Atom List: [1, 2, 3, 4]
Single Atom List: (False, {})
Atoms: False - Clauses: {2: [3], 3: [-3]}
Atoms: {1: True, 2: True, 3: False, 4: False} - Clauses: {2: [3], 3: [-3]}
Atoms: False - Clauses: {2: [-2, 3, 4], 3: [-3, 4], 4: [2, 3], 5: [-2, -4]}
Atoms: {1: True, 2: False, 3: True, 4: True} - Clauses: {}
Atoms: {1: True, 2: False, 3: True, 4: True} - Clauses: {2: [-2, 3, 4], 3: [-3, 4], 4: [2, 3], 5: [-2, -4]}
Atoms: {1: True, 2: False, 3: True, 4: True} - Clauses: {1: [1, 2], 2: [-1, -2, 3, 4], 3: [-1, -3, 4], 4: [2, 3], 5: [-2, -4]}
Atoms: {1: True, 2: None, 3: None, 4: None} - Clauses: {1: [1, 2], 2: [-1, -2, 3, 4], 3: [-1, -3, 4], 4: [2, 3], 5: [-2, -4]}
DP Has Returned: {1: True, 2: False, 3: True, 4: True}
```

### To Run:
```
python assignment2.py input1.txt
```