import random
from collections import deque

def pop(gloves: deque, element):
    if element in gloves: gloves.remove(element)
    return deque

def calculate():
    gloves = deque([], 44)
    for _ in range(20): gloves.append("w")
    for _ in range(24): gloves.append("b")
    random.shuffle(gloves)
    
    while len(gloves) != 1:
        vals = [random.choice(gloves), random.choice(gloves)]
        if   not "w" in gloves: gloves.remove("b")
        elif not "b" in gloves: gloves.remove("w")
        else:
            if vals[0] == vals[1]:
                gloves = pop(gloves, "b")
                gloves = pop(gloves, "b")
                #gloves.extend(0)
            else:
                gloves = pop(gloves, "w")
                gloves = pop(gloves, "w")
                #gloves.extend("b")
    return gloves[0]

def main():    
    result = calculate()
    if result == "b":   print("Осталась черная перчатка!")
    elif result == "w": print("Осталась белая перчатка!")

main()