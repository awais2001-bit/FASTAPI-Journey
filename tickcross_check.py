tick = 0
cross = 0
answers = [
    "c", "t", "t", "t", "t", "t", "t", "t", "t", "t",
    "c", "c", "t", "c", "c", "c", "t", "t", "t", "t",
    "t", "t", "c", "t", "t", "c", "c", "t", "c", "t",
    "t", "t", "t", "t", "c", "c", "t", "c", "t", "t",
    "c", "t", "c", "t", "t", "c", "t", "t", "t", "t",
    "t", "t", "t", "t", "t", "t", "t", "t", "t", "t",
    "t", "t", "t", "t", "t", "t", "t", "t", "t", "t",
    "t", "t", "t", "t", "t", "t", "c", "c", "c", "c",
    "c", "c", "c", "c", "c", "c", "c", "c", "c", "c",
    "c", "c", "c", "c", "c", "c", "c", "c", "c", "c"
]
for i in range(0,74):
    if i<=24 and answers[i]=="c":
        cross +=1
    elif i<=50 and answers[i]=="t":
        tick +=1
    elif i<=74 and answers[i]=="c":
        cross +=1
print("cross:", cross)
print("tick:", tick)
print(len(answers))

