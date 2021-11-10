#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Ce fichier contient toutes les fonctions concernant les balles
"""

# importation des modules nécessaires :
# modules système
import sys

# ---------


def create(x, y, dirct, color, speed):
    b = dict()

    b["x"] = x
    b["y"] = y
    b["dirct"] = dirct
    b["color"] = color
    b["speed"] = speed

    return b


def getx(b):
    return b["x"]


def setx(b, new):
    b["x"] = new


def gety(b):
    return b["y"]


def sety(b, new):
    b["y"] = new


def getdirct(b):
    return b["dirct"]


def setdirct(b, new):
    b["dirct"] = new


def getcolor(b):
    return b["color"]


def setcolor(b, new):
    b["color"] = new


def getspeed(b):
    return b["speed"]


def setspeed(b, new):
    b["speed"] = new


def move(b):
    dirct = getdirct(b)
    # speed = getspeed(b)

    if dirct == "left":
        setdirct(b, dirct)
        oldx = getx(b)

        # setx(b, int(oldx - speed))
        setx(b, oldx - 1)

    elif dirct == "right":
        setdirct(b, dirct)
        oldx = getx(b)

        # setx(b, int(oldx + speed))
        setx(b, oldx + 1)


def live(b):
    import Main
    import Enemy
    import Game

    if b in Main.bullets:
        move(b)  # faire avancer la balle

        x = getx(b)
        if x < 0 or x > 56:
            Main.bulletremove(b)  # faire disparaitre la balle si elle sort du jeu

        color = getcolor(b)

        for e in Main.enemies:  # vérifie si la balle a touché un ennemi
            if Main.testcollision(e, b) and Main.testcollisiony(e, b) and color == "white":  # est-ce une balle alliée ?
                Enemy.getshot(e, b)
        for i in Main.rocks:
            if (Main.testcollision(b, i) or getx(b) == i["x"] + 1) and gety(b) > 10:
                Main.bulletremove(b)  # détection des collisions avec les rochers

        if Main.testcollision(Main.player, b) and Main.testcollisiony(Main.player, b) and color == "red":
            Game.getshot(Main.player, b)


def show(b):
    sys.stdout.write("\033[40m")  # fond noir

    color = getcolor(b)
    if color == "red":
        sys.stdout.write("\033[31m")  # couleur (rouge) = balle ennemie
    elif color == "white":
        sys.stdout.write("\033[37m")  # couleur (blanc) = balle joueur

    sys.stdout.write("\033[" + str(b["y"]) + ";" + str(b["x"]) + "H")
    sys.stdout.write("-")
    sys.stdout.write("\033[0m")
