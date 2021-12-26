from os import read
import random
import time
from tkinter import *

resource = [0] * 4
# 0: Limestone Chip
# 1: Marble Chip
# 2: Apple
# 3: Gooseberry
resName = ["Limestone Chip", "Marble Chip", "Apple", "Gooseberry"]
logL = ["", "", "", "", ""]
health = 100.0
energy = 100.0
dead = 0

def saveFile():
    global resource
    nowTime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    record = open("record.txt", "w+")
    record.write(str(resource) + "\n")
    record.write(str(health) + ", " + str(energy) + ", " + str(dead) + "\n")
    record.write(nowTime)
    record.flush()
    record.close()
    logUpdate("File is successfully saved in " + nowTime + ".")

def loadFile():
    global resource, health, energy, dead
    record = open("record.txt", "r+")
    readRec = list(map(str, record.read().split("\n")))
    resource = list(map(int, readRec[0][1 : len(readRec[0]) - 1].split(", ")))
    health, energy, dead = map(float, readRec[1].split(", "))
    record.flush()
    record.close()
    logUpdate("File saved in " + readRec[2] + " is successfully loaded.")
    if dead == 1: die()

def restart():
    global resource, health, energy, dead
    resource = [0] * len(resource)
    health, energy, dead = 100, 100, 0

def tUpdate():
    global health, energy, dead
    
    for i in range(4):
        exec("res" + str(i) + "NS.set(str(resource[" + str(i) + "]))")
    logS.set("\n".join(logL))
    if dead == 0:
        hpS.set(str(int(health)))
        epS.set(str(int(energy)))
        healthRecv()
        energyRecv()
        rt.after(100, tUpdate)

def healthRecv():
    global health
    if health < 100: health += 0.1

def energyRecv():
    global energy
    if energy < 100: energy += 0.45

def die():
    global health, dead
    health = 0
    hpS.set("---")
    epS.set("---")
    logUpdate("You died.")
    exploreB.grid_forget()
    dead = 1
    return

def explore():
    global health, energy
    if energy < 10:
        logUpdate("You are too tired to explore.")
        return
    if random.randint(0, 99) < 5:
        logUpdate("You are hurt by thorns and got nothing.")
        logUpdate("HLTH −10, ENRG −10")
        if health > 10: health -= 10
        else: die()
        energy = energy - 20 if energy >= 20 else 0
        return
    energy -= 10
    incr = [
    int(random.randint(0, 99) < 70) * random.randint(4, 6),
    int(random.randint(0, 99) < 20) * random.randint(1, 5),
    int(random.randint(0, 99) < 40) * random.randint(0, 2),
    int(random.randint(0, 99) < 30) * random.randint(1, 10)]

    logInfo = ""
    for i in range(len(resource)):
        resource[i] += incr[i]
        if incr[i] > 0: logInfo += resName[i] + "+" + str(incr[i]) + ", "
    logInfo = logInfo[:len(logInfo) - 2]

    logUpdate("You explored" + (" and got nothing." if logInfo == "" else ":"))
    if logInfo != "": logUpdate(logInfo)

def logUpdate(newLog):
    global logL
    logL.append(newLog)
    logL = logL[1:]

rt = Tk()
rt.geometry("420x360")
rt.title("The Exploration")
rt.iconbitmap("wugicon.ico")

menubar = Menu(rt, tearoff=False)
fileMenu = Menu(menubar, tearoff=False)
menubar.add_cascade(label="File(F)", accelerator="F", menu=fileMenu)
menubar.add_cascade(label="Go(G)", accelerator="G")
menubar.add_cascade(label="Technologies(T)", accelerator="T")
menubar.add_cascade(label="Repositories(R)", accelerator="R")
menubar.add_cascade(label="Help(H)", accelerator="H")

fileMenu.add_cascade(label="Load", command=loadFile)
fileMenu.add_cascade(label="Save", command=saveFile)
fileMenu.add_cascade(label="Restart", command=restart)
fileMenu.add_cascade(label="Settings")

rt['menu'] = menubar
rt.bind("<Button-3>", lambda res: fileMenu.post(res.x_root, res.y_root))

speech = Label(rt, width=32, 
    text="You are a wanderer in a forest...", font=("Noto Sans Italic", 12), 
    anchor="nw", justify="left")
speech.grid(row=10, column=0, columnspan=2, sticky=W)

hpImg = PhotoImage(file="proj/health.png")
hpIc = Label(rt, width=16, 
    image=hpImg, 
    anchor="nw", justify="left")
hpIc.grid(row=10, column=2, sticky=E)

hpS = StringVar(value=str(int(health)))
hpN = Label(rt, width=3, 
    textvariable=hpS, font=("System", 16), fg="red", 
    anchor="nw", justify="left")
hpN.grid(row=10, column=3, sticky=W)

epImg = PhotoImage(file="proj/energy.png")
epIc = Label(rt, width=16, 
    image=epImg, 
    anchor="nw", justify="left")
epIc.grid(row=11, column=2, sticky=E)

epS = StringVar(value=str(int(energy)))
epN = Label(rt, width=3, 
    textvariable=epS, font=("System", 16), fg="green", 
    anchor="nw", justify="left")
epN.grid(row=11, column=3, sticky=W)



res0Img = PhotoImage(file="proj/minerals/limestone_chip.png")
res0Ic = Label(rt, width=32, 
    image=res0Img, 
    anchor="nw", justify="left")
res0Ic.grid(row=30, column=0, sticky=W)

res0Name = Label(rt, width=16, 
    text="Limestone Chips", font=("Noto Sans", 12), 
    anchor="nw", justify="left")
res0Name.grid(row=30, column=1, sticky=W)

res0NS = StringVar(value=str(resource[0]))
res0N = Label(rt, width=3, 
    textvariable=res0NS, font=("System", 16), 
    anchor="nw", justify="left")
res0N.grid(row=30, column=2, sticky=W)


res1Img = PhotoImage(file="proj/minerals/marble_chip.png")
res1Ic = Label(rt, width=32, 
    image=res1Img, 
    anchor="nw", justify="left")
res1Ic.grid(row=31, column=0, sticky=W)

res1Name = Label(rt, width=16, 
    text="Marble Chips", font=("Noto Sans", 12), 
    anchor="nw", justify="left")
res1Name.grid(row=31, column=1, sticky=W)

res1NS = StringVar(value=str(resource[1]))
res1N = Label(rt, width=3, 
    textvariable=res1NS, font=("System", 16), 
    anchor="nw", justify="left")
res1N.grid(row=31, column=2, sticky=W)


res2Img = PhotoImage(file="proj/plants/apple.png")
res2Ic = Label(rt, width=32, 
    image=res2Img, 
    anchor="nw", justify="left")
res2Ic.grid(row=32, column=0, sticky=W)


res2Name = Label(rt, width=16, 
    text="Apples", font=("Noto Sans", 12), 
    anchor="nw", justify="left")
res2Name.grid(row=32, column=1, sticky=W)


res2NS = StringVar(value=str(resource[1]))
res2N = Label(rt, width=3, 
    textvariable=res2NS, font=("System", 16), 
    anchor="nw", justify="left")
res2N.grid(row=32, column=2, sticky=W)


res3Img = PhotoImage(file="proj/plants/gooseberry.png")
res3Ic = Label(rt, width=32, 
    image=res3Img, 
    anchor="nw", justify="left")
res3Ic.grid(row=33, column=0, sticky=W)

res3Name = Label(rt, width=16, 
    text="Gooseberries", font=("Noto Sans", 12), 
    anchor="nw", justify="left")
res3Name.grid(row=33, column=1, sticky=W)

res3NS = StringVar(value=str(resource[1]))
res3N = Label(rt, width=3, 
    textvariable=res3NS, font=("System", 16), 
    anchor="nw", justify="left")
res3N.grid(row=33, column=2, sticky=W)


exploreB = Button(rt, width=8, height=2, 
    text="Explore\n(−10 ENRG)", command=explore, font=("Noto Sans", 10))
exploreB.grid(row=60, column=0, columnspan=2, sticky=W)


logS = StringVar(value="\n".join(logL))
logC = Label(rt, width=50, 
    textvariable=logS, font=("System", 12), 
    anchor="nw", justify="left", background="White")
logC.grid(row=90, column=0, columnspan=5, sticky=S)

tUpdate()
loadFile()

rt.update()
rt.mainloop()