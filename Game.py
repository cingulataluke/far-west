#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Ce fichier contient toutes les fonctions concernant la partie et le personnage joueur
"""

# importation des modules nécessaires :
# modules système
import sys

# ---------


def create(x, y, dirct):
    """créée le personnage joueur et donc une nouvelle partie"""

    g = dict()
    g["score"] = 0
    g["time"] = 0
    g["health"] = 5
    g["x"] = x
    g["y"] = y
    g["dirct"] = dirct

    return g


def getscore(g):
    return g["score"]


def setscore(g, new):
    g["score"] = new


def gettime(g):
    return g["time"]


def settime(g, new):
    g["time"] = new


def gethealth(g):
    return g["health"]


def sethealth(g, new):
    g["health"] = new


def getx(g):
    return g["x"]


def setx(g, new):
    g["x"] = new


def gety(g):
    return g["y"]


def sety(g, new):
    g["y"] = new


def getdirct(g):
    return g["dirct"]


def setdirct(g, new):
    g["dirct"] = new


def move(g, dirct):
    """fait avancer le personnage dans une direction choisie, si possible"""

    if dirct == "left":
        setdirct(g, dirct)

        oldx = getx(g)
        setx(g, oldx - 1)
        if g["x"] < 0:
            setx(g, oldx)

    elif dirct == "right":
        setdirct(g, dirct)

        oldx = getx(g)
        setx(g, oldx + 1)
        if g["x"] > 55:
            setx(g, oldx)

    else:
        print "erreur Game.move : valeur de dirct non prise en charge"


def jump(s):
    import Main

    if Main.onGround:
        Main.speed = s
        Main.player["y"] -= 1
        Main.onGround = False

    if Main.onRock:
        Main.speed = s
        Main.player["y"] -= 1
        Main.onRock = False


def shoot(g):
    import Bullet
    import Main

    dirct = getdirct(g)
    x = getx(g)
    y = gety(g)

    if dirct == "left":
        x -= 1
    elif dirct == "right":
        x += 1
    else:
        print "erreur Game.shoot : valeur de dirct non prise en charge"

    for r in Main.rocks:
        if not (r["x"] == x or r["x"] + 1 == x):
            return Bullet.create(x, y, dirct, "white", 2)


def addscore(g, added):
    score = getscore(g)
    setscore(g, score + added)


def getshot(g, bullet):
    import Main
    health = gethealth(g)
    sethealth(g, health - 1)
    Main.bulletremove(bullet)


def testover(g):
    health = gethealth(g)

    if health > 0:
        return False
    else:
        return True


def show(g):
    sys.stdout.write("\033[40m")  # fond noir
    sys.stdout.write("\033[37m")  # couleur (blanc)
    sys.stdout.write("\033[" + str(int(g["y"])) + ";" + str(int(g["x"])) + "H")
    sys.stdout.write("@")
    sys.stdout.write("\033[0m")


def showgui(g):
    print "Score : " + str(getscore(g))

    vies = ""
    i = 0
    while i < gethealth(g):
        vies += "❤ "
        i += 1
    print "Vies : " + vies

    print "Temps : " + str(gettime(g))
