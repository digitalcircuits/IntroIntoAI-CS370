# Assignment 1 - Introduction Into Artificial Intelligence (CS370)

## The Assignment Given
![](https://i.imgur.com/TPDpxYB.png)

Basically put, we need to see how many dominos we can combine that produces the same string in the numerator & denominator. 

### Example Input:
```
python assignment1.py input1.txt
```


### Example Output:

```
Max Size Queue: 5
Max Depth: 50
Verbose Mode: True
Number of Dominos: 3

Dominos Listed:
D1  ->  ['bb', 'b']
D2  ->  ['a', 'aab']
D3  ->  ['abbba', 'bb']

Attempting Search...
A Solution Has Been Found!
Top: aabbbaabb
Bottom: aabbbaabb
[['bbbbbbabbba', 'bbbbb'], ['bbbbbbbb', 'bbbb']]
{"['', 'b']": 'D1', "['ab', '']": 'D2', "['', 'bb']": 'D1', "['baab', '']": 'D2', "['', 'a']": 'D3', "['', 'bbb']": 'D1', "['', 'abbba']": 'D3', "['b', '']": 'D2', "['', 'bbbb']": 'D1', "['', 'babbba']": 'D3'}
```