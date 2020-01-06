import os
import copy
import re
from collections import defaultdict
import sys

def readGDrive(textfilename):
  f = open(textfilename, "r")
  data = f.readlines()[:-1]
  #Clean out the newlines
  newClause = {}
  ia = 0
  while ia < len(data):
    L = data[ia].strip("\n").split(" ")
    for i in range(len(L)):
      L[i] = int(L[i])
    newClause[ia+1] = L
    ia = ia + 1
  return newClause


def getNewAtomTrueFunc(V, Rnd, Pos, Status):
  #Set a Random or Specific Atom to Either True or False
  AtomsCopy = copy.deepcopy(V)
  if Rnd == True:
    for key in AtomsCopy:
      value = AtomsCopy[key]
      if value == None:
        AtomsCopy[key] = Status
        #print("About to return: " + str(AtomsCopy) + " and " + str(key))
        return AtomsCopy, key
  elif Rnd == False:
    AtomsCopy[Pos] = Status
    return AtomsCopy, int(Pos)

def AtomUnique(Info):
#Find Atoms in the Text File and Make a Unique List of Atoms
#Strips out any '-' since we want the Atoms, not their literals
  linecount = 0
  AtomList = []
  while linecount < len(Info):
    tempArray = Info[linecount+1]
    iae = 0
    while iae < len(tempArray):
      if tempArray[iae] < 0:
        liner = tempArray[iae] * -1
      else:
        liner = tempArray[iae]
      #print(str(liner))
      if liner not in AtomList:
        AtomList.append(liner)
      iae = iae + 1
    linecount = linecount + 1
  return AtomList

#For Part 3
def checkLiteralInClause(Clause):
  #Checks to see if theres a Atom with one Literal
  diction = {}
  dontAdd = []
  linecount = 0
  for key, val in Clause.items():
    tempArray = Clause[key]
    iae = 0
    while iae < len(tempArray):
      valueget = checkLiteralAtom(tempArray[iae])
      valueGetAsInt = int(valueget[0])
      if valueGetAsInt not in dontAdd:
        if valueGetAsInt not in diction.keys():
          diction[valueGetAsInt] = valueget[1]
        elif valueGetAsInt in diction.keys():
          if diction[valueGetAsInt] != valueget[1]:
            del diction[valueGetAsInt]
            dontAdd.append(valueGetAsInt)
      iae += 1
    linecount += 1
  if len(diction) > 0:
    return True, diction
  else:
    return False, diction

def HasSingletonClause(Clauses):
  #For Part 4
  #If S contains a clause with one literal, assign that atom to that clause
  singletonAtoms = {}
  SignSignal = False
  for ia in Clauses:
    if len(Clauses[ia]) == 1:
      atom, sign = checkLiteralAtom(Clauses[ia][0])
      AtomAdd = int(atom)
      singletonAtoms[AtomAdd] = sign
      SignSignal = True
  return SignSignal, singletonAtoms

def checkEmptyListString(Clauses):
#Checks for Empty Lists in a Dictionary, removes then, and reorganizes list
  ClauseCopy = copy.deepcopy(Clauses)
  gotRes = False
  i = 0
  a = 1
  while i < len(ClauseCopy):
    tempArray = ClauseCopy[i+1]
    if tempArray == [] or tempArray == None or len(tempArray) == 0:
      del ClauseCopy[i+1]
      gotRes = True
      for ip in sorted (ClauseCopy.keys()):
        ClauseCopy2[a] = ClauseCopy.get(ip)
        a += 1
    i += 1
  ClauseCopy = copy.deepcopy(ClauseCopy2)
  return gotRes, ClauseCopy

def checkLiteralAtom(Atom):
#check to see if an Atom is a Positive or Negative (Only Atom, not Clauses)
  AtomA = str(Atom)
  if AtomA[:1] == '-':
    return int(AtomA[1:]), False
  else:
    return int(AtomA), True

def propagate(S, V):
  #Delete Either Clause if satisfied or Literal from a Clause if opposite
  #Input is the Atom (V) were working with & List of Clauses
  #If Atom with correct value in clause true, remove that clause entirely
  #If Atom with correct value has atom opposite literal, remove only that atom
  #if 3 or 4 hit, propogate
  #For every atom we have in a clause, 
 
  #if False not in V.values() and True not in V.values():
  #  return False
  #else:    
  VWork = copy.deepcopy(V)
  SWork = copy.deepcopy(S)
  SWorkToCount = copy.deepcopy(SWork)
  for key,val in SWorkToCount.items():
    tempArray = SWorkToCount[key]
    for atomInClause in tempArray:
      AtomWorkWith = atomInClause
      AtomWorkWithStr = str(AtomWorkWith)
      t = checkLiteralAtom(AtomWorkWithStr)
      AtomCheckValue = t[1]
      AtomInDict = V[t[0]]
      if AtomInDict != None:
        if AtomCheckValue == AtomInDict and key in SWork:
          del SWork[key]
        elif AtomCheckValue != AtomInDict:
          SWork[key].remove(AtomWorkWith)
  return SWork

def DP(ATOMS, S):
  V = {}
  iae = 0
  for key in ATOMS:
    V[key] = None
  return DPHelper(ATOMS, S, V)

#S = Clauses
#V = {1: True, 2: UNBOUND, ...}
def DPHelper(ATOMS, S, V):
  goodLoop = True 
  while goodLoop == True:
    propWent = False
    #Part 1
    if len(S) == 0:
      print("Atoms: " + str(V) + " - Clauses: " + str(S))
      return V
    #Part 2
    for key, val in S.items():
      if S[key] == []:
        return False
    #Part 3
    P3Res = checkLiteralInClause(S)
    if P3Res[0] == True:
      for key,val in P3Res[1].items():
        V[key] = val
      propWent = True
    #Part 4
    P4Res = HasSingletonClause(S)
    if P4Res[0] == True:
      for key,val in P4Res[1].items():
        V[key] = val
      propWent = True
    #Part 5
    if propWent == True:
      S = propagate(S, V)
    else:
      goodLoop = False
    #Part 6
    if len(S) == 0:
      print("Atoms: " + str(V) + " - Clauses: " + str(S))
      return V
    SCopy = copy.deepcopy(S)
    VCopy = copy.deepcopy(V)
    for key,val in VCopy.items():
      if VCopy[key] == None:
        RunRes = getNewAtomTrueFunc(VCopy, True, None, True)
    VCopy = RunRes[0]
    PosUsed = RunRes[1]
    SCopy = propagate(SCopy, VCopy)
    VNEW = DPHelper(ATOMS, SCopy, VCopy)
    print("Atoms: " + str(VNEW) + " - Clauses: " + str(S))
    if VNEW == False:
      SCopy2 = copy.deepcopy(S)
      VCopy2 = copy.deepcopy(V)
      NewVCopy = getNewAtomTrueFunc(VCopy2, False, PosUsed, False)[0]
      SCopy2 = propagate(SCopy2, NewVCopy)
      VNEW2 = DPHelper(ATOMS, SCopy2, NewVCopy)
      if VNEW2 == False:
        print("Atoms: " + str(NewVCopy) + " - Clauses: " + str(S))
        return False
      else:
        print("Atoms: " + str(NewVCopy) + " - Clauses: " + str(S))
        return VNEW2
    else:
      print("Atoms: " + str(VCopy) + " - Clauses: " + str(S))
      return VNEW


def main(inputFile):
  dataRead = readGDrive(inputFile)
  print("The Clauses: " + str(dataRead))
  uniqueAtomList = AtomUnique(dataRead)
  print("Unique Atom List: " + str(uniqueAtomList))
  print("Single Atom List: " + str(checkLiteralInClause(dataRead)))
  print("DP Has Returned: " + str(DP(uniqueAtomList, dataRead)))


if sys.version_info[0] < 3:
  print()
  raise Exception("ERROR: This script was coded in Python 3(.7.4) and therefore may not work on lower versions. Please switch to Python 3(.7.4)")
elif len(sys.argv) < 2:
  print()
  print("ERROR: You must pass an input file as an argument, for example: python " + sys.argv[0] + " input1.txt - exiting...")
  print()
  quit()
else:
  main(sys.argv[1])