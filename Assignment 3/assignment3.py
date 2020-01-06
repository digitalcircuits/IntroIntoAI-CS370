import os
from os import path
import copy
from collections import defaultdict
import random as rn
import sys

def readGDrive(textfilename):
  if os.path.exists(textfilename) == False:
    print("ERROR: File Specified Does not Exist! Exiting...")
    exit()
  else:
      f = open(textfilename, "r")
      data = f.readlines()
      newData = []
      for i in data:
        #Remove all \n in lists
        newData.append(i.strip().replace(" ", "").split(","))
      for i in newData:
        ia = 0
        while ia < len(i):
          if (len(i) - 1) != ia:
            i[ia] = float(i[ia])
          else:
            i[ia] = i[ia]
          ia += 1
      return newData

def countCategoriesUniqueLetters(inputSet):
  #Checks to see what unique letters to be done
  uniqueLetters = {}
  for i in inputSet:
    for j in i:
      if isinstance(j, str) == True:
        if (j not in uniqueLetters):
          uniqueLetters[j] = 1
        else:
          uniqueLetters[j] = uniqueLetters[j] + 1
  return uniqueLetters

def calculateDistance(xVector, yVector):
  xVectorCopy = copy.deepcopy(xVector)
  yVectorCopy = copy.deepcopy(yVector)

  calcPlay = []
  Results = float(0.00)
  for a in range(len(xVector)):
    Results = Results + pow(xVectorCopy[a] - yVectorCopy[a], 2)
  return Results

def SubtractVectors(x, y):
  xPlay = copy.deepcopy(x)
  yPlay = copy.deepcopy(y)
  resPlay = [0.00] * len(xPlay)
  for i in range(len(xPlay)):
    resPlay[i] = xPlay[i] - yPlay[i]
  return resPlay

def AddVectors(x, y):
  xPlay = copy.deepcopy(x)
  yPlay = copy.deepcopy(y)
  resPlay = [0.00] * len(xPlay)
  for i in range(len(xPlay)):
    resPlay[i] = xPlay[i] + yPlay[i]
  return resPlay

def MultiplyVectors(x, y):
  xPlay = copy.deepcopy(x)
  yPlay = copy.deepcopy(y)
  resPlay = [0.00] * len(xPlay)
  for i in range(len(xPlay)):
    resPlay[i] = xPlay[i] * yPlay[i]
  return resPlay

def ListToDict(input):
  #Conver that List into Dictionary Format
  hardCopyInput = copy.deepcopy(input)
  getLetters = countCategoriesUniqueLetters(hardCopyInput)
  defaultDict = {}
  #Initialize the dictionary
  for keys, values in getLetters.items():
    defaultDict[keys] = 0
  #Now add the lines
  tempList = [] 
  for keys, values in getLetters.items():
    for i in hardCopyInput:
      if i[-1] == keys:
        tempList.append(i[:-1]) 
    defaultDict[keys] = copy.deepcopy(tempList)
    tempList.clear()
  return defaultDict

def GradRandomVectors(TrainingSet, TrainingSetDict):
  #Ran if Random is Set to True
  exemplarsTrainingSet = copy.deepcopy(TrainingSet)
  exemplarsTrainingSetDict = copy.deepcopy(TrainingSetDict)
  exemplarsPlay = {}
  minVal = 100 #If our minimum was 0, it would stay at 0, so we need to give it a large number
  maxVal = 0
  for a in exemplarsTrainingSetDict.items():
    for b in range(len(a[1][0])):
      for c in a[1]:
        if c[b] < minVal:
          minVal = c[b]
        if c[b] > maxVal:
          maxVal = c[b]
      tempList = []
      for i in range(len(a[1][0])):
        tempList.append(rn.uniform(minVal, maxVal))
      exemplarsPlay[a[0]] = tempList
  return exemplarsPlay

def GradInitialVectors(TrainingSet, TrainingSetDict):
  #Ran if Random is Set to False
  exemplarsTrainingSet = copy.deepcopy(TrainingSet)
  exemplarsTrainingSetDict = copy.deepcopy(TrainingSetDict)
  exemplarsPlay = {}
  for a in exemplarsTrainingSetDict.items():
    #a = ('a', [[1.0, 1.0, 2.0], [2.0, 1.0, 1.0], [2.0, 0.0, 1.0]])
    centroid = [0.00] * len(a[1][0])
    for vec in a[1]:
      centroid = AddVectors(centroid, vec)
    for index in range(len(centroid)):
      centroid[index] = centroid[index] / len(a[1])
    exemplarsPlay[a[0]] = centroid
  return exemplarsPlay

def computeAccuracy(TrainingSet, Exemplars):
  TrainingSetCopy = copy.deepcopy(TrainingSet)
  ExemplarsCopy = copy.deepcopy(Exemplars)
  TotalNumber = 0
  for p in TrainingSetCopy.items():
    TotalNumber += len(p[1])
  Correct = 0
  for a in TrainingSetCopy.items():
      for b in a[1]:
          Minimum = 100
          for exemplars in ExemplarsCopy.items():
              c = exemplars[1]
              if calculateDistance(b, c) < Minimum:
                  Minimum = calculateDistance(b, c)
                  CorrectVars = exemplars[0]
          if CorrectVars == a[0]:
              Correct = Correct + 1
  return (Correct + 0.0) / TotalNumber

def closestExemp(Exemplars, Point):
  pointPlay = copy.deepcopy(Point)
  exemplarPlay = copy.deepcopy(Exemplars)
  minVal = 100
  #print("My Point: " + str(pointPlay))
  #print("My et: " + str(exemplarPlay))
  for a in exemplarPlay.items():
    b = a[1]
    calculateDistanceResults = calculateDistance(b, pointPlay)
    if calculateDistanceResults < minVal:
      minVal = calculateDistanceResults
      Results = a[0]
  return Results

#MAIN FUNCTION
def gradDescent(TrainingSet, TrainingSetDict, stepSize, epsilon, M, randomVal, verboseMode):
  #Initialize Vectors
  exemplarVectors = {}
  if randomVal == True:
    exemplarVectors = GradRandomVectors(TrainingSet, TrainingSetDict)
  elif randomVal == False:
    exemplarVectors = GradInitialVectors(TrainingSet, TrainingSetDict)
  #print(exemplarVectors)
  previousCost = 1000000000000000000000 
  previousAccuracy = computeAccuracy(TrainingSetDict, exemplarVectors)
  n = {}
  iteration = -1
  TotalCost = 0.00
  while True:
    iteration += 1
    TotalCost = 0.00
    for items in TrainingSetDict.items():
      variable = items[0]
      n[variable] = [0.00] * len(items[1][0])
    for items in TrainingSetDict.items():
      category = items[0]
      g_v = exemplarVectors[category]
      for y in items[1]:
        closest_w = closestExemp(exemplarVectors, y) #maybe incorrect - w
        g_w = exemplarVectors[closest_w]
        if closest_w != category:
          try:
            Cost = calculateDistance(g_v, y) - calculateDistance(y, g_w)
          except Exception as e:
            print("ERROR: " + str(y))
            return 0,0
          if Cost < M:
            n[category] = AddVectors(n[category], SubtractVectors(y, g_v))#n_v
            n[closest_w] = AddVectors(n[closest_w], SubtractVectors(g_w, y))
            TotalCost += Cost
        else:
          TotalCost += M
    if verboseMode == True:
      print("Accuracy is: " + str(previousAccuracy) + " on Iteration: " + str(iteration))
      print("Total Cost: " + str(TotalCost) + " - and previous cost: " + str(previousCost))
      print()
      
    if TotalCost < epsilon:
      return exemplarVectors, previousAccuracy
    if TotalCost > (1-epsilon)*previousCost:
      return exemplarVectors, previousAccuracy
    
    h = {}
    for items in TrainingSetDict.items():
      v = items[0]
      g_v = exemplarVectors[v]
      h[v] = AddVectors(g_v, MultiplyVectors(n[v], [stepSize]*len(n[v])))

    NewAccuracy = computeAccuracy(TrainingSetDict, h)
    if NewAccuracy < previousAccuracy:
      return exemplarVectors, previousAccuracy
    
    for items in TrainingSetDict.items():
      v = items[0]
      exemplarVectors[v] = h[v]
    
    previousCost = TotalCost
    previousAccuracy = NewAccuracy

def main(input, stepSizeValue, epsilonValue, M, restarts, verbose):
  #Fetch the Input File
  inputFile = readGDrive(input)
  #Convert it Into a Dictionary
  TextLineDictFormat = ListToDict(inputFile)

  #Set a Best Value
  BestValue = 0.00

  #Set the Range of Restarts
  for i in range(int(restarts)):
    if i == 0:
      #We dont restart on the first run
      randomVal = False
    else:
      randomVal = True
    #Run the Function [Convert all Inputs as Floats]
    Exemplars, Results = gradDescent(TrainingSet = inputFile, 
                          TrainingSetDict = TextLineDictFormat, 
                          stepSize = float(stepSizeValue),
                          epsilon=float(epsilonValue),
                          M=M,
                          randomVal=randomVal,
                          verboseMode=verbose
                          )
    
    #Replace Best Value with out Results and Repeat the Restart
    if Results > BestValue:
      BestValue = Results
    #Verbose Mode
    if verbose == True:
      #Add +1 to i since we start at 0
      print("----We are on run number: " + str(i+1) + "------")
      print("Our Exemplars So Far:")
      print(Exemplars)
      #Debug Print
      print("Accuracy: " + str(Results))
      print("Best Value So Far: " + str(BestValue))
      print()
  print()
  print("Best Accuracy: " + str(BestValue))


if sys.version_info[0] < 3:
    raise Exception("ERROR: This Script was written with Python 3 and therefore must run on Python 3. Exiting Now")
    exit()
else:
    inputFile = str(sys.argv[1])
    stepSizeValue = float(sys.argv[2])
    epsilonValue = float(sys.argv[3])
    M = float(sys.argv[4])
    restarts = int(sys.argv[5])
    verbose = bool(sys.argv[6])
    
    print("Just to confirm, these are your settings:")
    print("Filename: " + str(inputFile))
    print("Step Size Value: " + str(stepSizeValue))
    print("Epsilon Value: " + str(epsilonValue))
    print("M: " + str(M))
    print("Restarts: " + str(restarts))
    print("Verbose Mode: " + str(verbose))
    print()
    print("If this is good, press [y]. Otherwise, Cntrl+C to cancel")
    prompt = input('=> ').lower()
    if prompt == 'y':
        main(input=inputFile, stepSizeValue=stepSizeValue, epsilonValue=epsilonValue, M=M, restarts=restarts, verbose=verbose)
    else:
        print("Alternative key pressed. Cancelling")