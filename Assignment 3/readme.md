# Assignment 3 - Introduction Into Artificial Intelligence (CS370)

## The assignment given:

![](https://i.imgur.com/0qBS9uG.png)

### Example Input:
```
1,1,2,a
2,1,1,a
2,0,1,a
0,2,1,b
3,2,0,b
3,3,0,c
0,3,0,c
3,2,1,c
0,3,3,c
```

Each line is a centroid with an assigned category that must be calculated using the equation as described in the picture.

### Example Output:
```
 Iteration:0
1.667, 0.667, 1.333
1.500, 2.000, 0.500
1.500, 2.750, 1.000
Accuracy 0.8889  

 Iteration:1
1.667, 0.667, 1.333
1.350, 2.000, 0.450
1.650, 2.675, 1.000
Accuracy 0.8889  
Converged. Accuracy = 0.8889  

Best Accuracy: 0.89 
```

## Requirements

* Python 3 (tested on Python 3.7.4)

## To run

```
python assignment3.py <inputfile> <step size value> <epsilon value> <M> <number of restarts> <verbose mode>

python assignment3.py test2.txt 0.01 0.01 5 10 True

```