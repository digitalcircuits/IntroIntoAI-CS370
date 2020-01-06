import sys
import os
import queue
from collections import deque
from collections import namedtuple
import re

Domino = namedtuple("Domino", ['numerator', 'denominator'])
State = namedtuple("State", ['dominoesgroup', 'top', 'bottom', 'diff', 'difflet'])
        
def GoalStateReach(top, bottom):
    if top == bottom:
        diff = "same"
        difflet = "" 
    elif top.startswith(bottom):
        diff = "top"
        difflet = top[len(bottom):]
    elif bottom.startswith(top):
        diff = "bottom"
        difflet = bottom[len(top):]
    else:
        return False
    return [diff, difflet]

def BreadthFirstSearch(max_queue, num_dominos, dominoes, max_size):
    explored_dominoes = {}
    frontiereddominoes = []
    for name, dom in dominoes.items():
        PsChk = GoalStateReach(dom[0].strip(), dom[1].strip())
        if PsChk:
            frontiereddominoes.insert(0, [dom[0].strip(), dom[1].strip()])
            if PsChk[0] == "top":
                throwaway = ["", PsChk[1]]
                if repr(throwaway) not in explored_dominoes:
                    explored_dominoes.update({str(throwaway): name})
            elif PsChk[0] == "bottom":
                throwaway = [PsChk[1], ""]
                if repr(throwaway) not in explored_dominoes:
                    explored_dominoes.update({str(throwaway): name})
    while frontiereddominoes and len(frontiereddominoes) < max_queue:
        state = frontiereddominoes.pop()
        for name, dom in dominoes.items():
            okstates = re.findall(r"[a-z]+", str(state))
            PsChk = GoalStateReach(okstates[0].strip() + dom[0].strip(),okstates[1].strip() + dom[1].strip())
            if PsChk:
                if PsChk[0] == "top":
                    throwaway = ["", PsChk[1]]
                    if repr(throwaway) not in explored_dominoes:
                        frontiereddominoes.insert(0, [okstates[0] + dom[0], okstates[1] + dom[1]])
                        explored_dominoes[str(throwaway)] = name
                elif PsChk[0] == "bottom":
                    throwaway = [PsChk[1], ""]
                    if repr(throwaway) not in explored_dominoes:
                        frontiereddominoes.insert(0, [okstates[0] + dom[0], okstates[1] + dom[1]])
                        explored_dominoes[str(throwaway)] = name
                elif PsChk[0] == "same":
                    return ("Solution",okstates[0].strip() + dom[0].strip(),okstates[1].strip() + dom[1].strip(),frontiereddominoes,explored_dominoes)
    if not frontiereddominoes:
        return "No Solution has been found! All Frontier Dominos has been exhausted!"
    else:
        return DFS_with_limits(max_size, max_queue, frontiereddominoes, explored_dominoes, dominoes)


def DFS_with_limits(max, depth, frontiereddominoes, explored_dominoes, dominoes):
    #a.k.a itartive deepening
    for i in range(depth):
        state = frontiereddominoes.pop()
        resultr = DepthFirst(state, explored_dominoes, 0, i, dominoes)
        if resultr:
            if "soulution_found" == resultr[0]:
                return resultr
    return "Iterative Deepening Search Resulted Nothing"


def DepthFirst(ntcr, explored_dominoes, cycles, lmdep, dominoes):
    if cycles <= lmdep:
        for name, dom in dominoes.items():
            PsChk = GoalStateReach(ntcr[0].strip() + dom[0].strip(), ntcr[1].strip() + dom[1].strip())
            if PsChk:
                if PsChk[0] == "top":
                    throwaway = ["", PsChk[1]]
                    if repr(throwaway) not in explored_dominoes:
                        explored_dominoes[str(throwaway)] = name
                        return DepthFirst(throwaway, explored_dominoes, cycles + 1, lmdep, dominoes)
                elif PsChk[0] == "bottom":
                    throwaway = [PsChk[1], ""]
                    if repr(throwaway) not in explored_dominoes:
                        explored_dominoes[str(throwaway)] = name
                        return DepthFirst(throwaway, explored_dominoes, cycles + 1, lmdep, dominoes)
                elif PsChk[0] == "same":
                    return ("solution_found",ntcr[0].strip() + dom[0].strip(),ntcr[1].strip() + dom[1].strip(), explored_dominoes)
        if cycles == lmdep:
            return "No Solution Has Been Found In: " + str(cycles)
    else:
        return "Depth First Resulted Nothing With Current Settings"

def SearchArg(max_size_queue, domino_number, dominosInDict, max_depth):
    MSQ = max_size_queue
    DN = domino_number
    dND = dominosInDict
    MXD = max_depth
    Results = BreadthFirstSearch(MSQ, DN, dND, MXD)
    if Results[0] == 'Solution':
        print("A Solution Has Been Found!")
        iae = 0
        while iae < len(Results):
            if iae != 0:
                if iae == 1:
                    print("Top: " + Results[1])
                elif iae == 2:
                    print("Bottom: " + Results[2])
                else:
                    print(Results[iae])
            iae = iae+1
    else:
        print(Results)

  

def take_user_input(filename_arg):
    filename = filename_arg
    if os.path.exists(filename) == False:
      print("ERROR: The file '" + filename + "' does not exist, exiting...")
      quit()
    else:
      try:
        
        fp = open(filename, "r")
        fpL = fp.readlines()

        #Better way to initialize it, relies on the user having good input file
        max_size_queue = int(fpL[0])
        max_depth = int(fpL[1])
        #Change it to a bool -> Python does the work for you
        output_sequence_generated_flag = bool(fpL[2])
        domino_number = int(fpL[3])
        dominosFile = fpL[4: 4 + int(domino_number)]
      except:
        print("ERROR: Invalid Input in one of the files ")
        print(sys.exc_info())
        quit()

      return max_size_queue, max_depth, output_sequence_generated_flag, domino_number, dominosFile

def MakeDominoDict(dominosFile):
  dominoDict = {}
  for x in dominosFile:
    xSplitRes = x.split()
    dominoDict['D' + xSplitRes[0]] = [xSplitRes[1], xSplitRes[2]]
  return dominoDict

def main():
  max_size_queue, max_depth, output_sequence_generated_flag, domino_number, dominosFile = take_user_input(sys.argv[1])
  #Convert them into strings
  print("Max Size Queue: " + str(max_size_queue))
  print("Max Depth: " + str(max_depth))
  print("Verbose Mode: " + str(output_sequence_generated_flag))
  print("Number of Dominos: " + str(domino_number))
  print()
  dominosInDict = MakeDominoDict(dominosFile)
  print("Dominos Listed:")
  for key in dominosInDict:
	  print(key, ' -> ', dominosInDict[key])
  print()
  print("Attempting Search...")
  ans = SearchArg(
      max_size_queue, 
      domino_number, 
      dominosInDict, max_depth)

  
if sys.version_info[0] < 3:
  print()
  raise Exception("ERROR: This script was coded in Python 3(.7.4) and therefore may not work on lower versions. Please switch to Python 3(.7.4)")
elif len(sys.argv) < 2:
  print()
  print("ERROR: You must pass an input file as an argument, for example: python " + sys.argv[0] + " input1.txt - exiting...")
  print()
  quit()
else:
  main()