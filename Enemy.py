#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Ce fichier contient toutes les fonctions gérant les ennemis
"""

# importation des modules nécessaires :
# modules système
import random
import sys

# ---------


def create(x, y, dirct):
    e = dict()

    # vie des ennemis en P2
    e["x"] = x
    e["y"] = y
    e["dirct"] = dirct
    e["health"] = 2

    return e


def getx(e):
    return e["x"]


def setx(e, new):
    e["x"] = new


def gety(e):
    return e["y"]


def sety(e, new):
    e["y"] = new


def getdirct(e):
    return e["dirct"]


def setdirct(e, new):
    e["dirct"] = new


def gethealth(e):
    return e["health"]


def sethealth(e, new):
    e["health"] = new


def move(e, dirct):
    """fait avancer l'ennemi dans une dirctection choisie, si possible"""

    if dirct == "left":
        setdirct(e, dirct)

        oldx = getx(e)
        setx(e, oldx - 1)
        if e["x"] < 1:
            setx(e, oldx)

    else:
        setdirct(e, dirct)

        oldx = getx(e)
        setx(e, oldx + 1)
        if e["x"] > 55:
            setx(e, oldx)


def shoot(e):
    import Bullet
    import Game
    import Main

    x = getx(e)
    y = gety(e)

    if Game.getx(Main.player) <= getx(e):
        dirct = "left"
        x -= 1
    else:
        dirct = "right"
        x += 1

    for r in Main.rocks:
        if not (r["x"] == x or r["x"] + 1 == x):
            return Bullet.create(x, y, dirct, "red", 1)


def getshot(e, bullet):
    import Main
    import Game

    Main.bulletremove(bullet)

    health = gethealth(e)
    sethealth(e, health - 1)

    if health == 0:
        Main.enemyremove(e)
        Game.addscore(Main.player, 100)


def live(e):
    import Main
    import Game

    action = random.randint(0, 100)
    Main.enemies.remove(e)  # pour ne pas que les ennemis collisionnent avec eux-mêmes

    if 1 <= action <= 35:
        if Game.getx(Main.player) <= getx(e):
            move(e, "left")

            if Main.testcollision(Main.player, e) and Main.player["y"] == 12:
                move(e, "right")  # détection des collisions avec le joueur
            for i in Main.enemies:
                if Main.testcollision(i, e):
                    move(e, "right")  # détection des collisions avec les autres ennemis
            for i in Main.rocks:
                if Main.testcollision(e, i) or getx(e) == i["x"] + 1:
                    move(e, "right")  # détection des collisions avec les rochers

        elif Game.getx(Main.player) > getx(e):
            move(e, "right")

            if Main.testcollision(Main.player, e) and Main.player["y"] == 12:
                move(e, "left")  # détection des collisions avec le joueur
            for i in Main.enemies:
                if Main.testcollision(i, e):
                    move(e, "left")  # détection des collisions avec les autres ennemis
            for i in Main.rocks:
                if Main.testcollision(e, i) or getx(e) == i["x"] + 1:
                    move(e, "left")  # détection des collisions avec les rochers

    elif 36 <= action <= 60:
        if Game.getx(Main.player) >= getx(e):
            move(e, "left")

            if Main.testcollision(Main.player, e) and Main.player["y"] == 12:
                move(e, "right")  # détection des collisions avec le joueur
            for i in Main.enemies:
                if Main.testcollision(i, e):
                    move(e, "right")  # détection des collisions avec les autres ennemis
            for i in Main.rocks:
                if Main.testcollision(e, i) or getx(e) == i["x"]+1:
                    move(e, "right")  # détection des collisions avec les rochers

        elif Game.getx(Main.player) < getx(e):
            move(e, "right")

            if Main.testcollision(Main.player, e) and Main.player["y"] == 12:
                move(e, "left")  # détection des collisions avec le joueur
            for i in Main.enemies:
                if Main.testcollision(i, e):
                    move(e, "left")  # détection des collisions avec les autres ennemis
            for i in Main.rocks:
                if Main.testcollision(e, i) or getx(e) == i["x"]+1:
                    move(e, "left")  # détection des collisions avec les rochers

    elif 61 <= action <= 66:
        Main.bullets.append(shoot(e))

    Main.enemies.append(e)


def show(e):
    sys.stdout.write("\033[40m")  # fond noir
    sys.stdout.write("\033[31m")  # couleur (rouge)
    sys.stdout.write("\033[" + str(e["y"]) + ";" + str(e["x"]) + "H")
    sys.stdout.write("o")
    sys.stdout.write("\033[0m")
