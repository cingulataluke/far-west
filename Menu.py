#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Ce fichier contient toutes les fonctions permettant d'afficher et d'utiliser le menu
"""

# importation des modules nécessaires :
# modules système
import sys
import select
import termios
import tty

# variables globales
menu = None
old_settings = termios.tcgetattr(sys.stdin)

# ---------


def init():
    global menu

    tty.setcbreak(sys.stdin.fileno())  # interaction clavier

    menu = dict()

    menu["selected"] = "play"  # valeurs de selected : play ou quit
    menu["first"] = True  # si c'est la première fois qu'on créée le menu, on n'affiche pas le score et le temps

    fichier = open("menu.txt", "r")
    menu["str"] = fichier.read()
    fichier.close()

    return menu


def gameover():
    menu["selected"] = "play"
    menu["first"] = False

    fichier = open("menu2.txt", "r")
    menu["str"] = fichier.read()
    fichier.close()

    run()


def getselected(m):
    return m["selected"]


def setselected(m, new):
    m["selected"] = new


def getfirst(m):
    return m["first"]


def setfirst(m, new):
    m["first"] = new


def move():
    global menu

    k = sys.stdin.read(1)

    if k == "z":
        setselected(menu, "play")

    elif k == "s":
        setselected(menu, "quit")

    if k == "a":
        mselect()


def mselect():
    import Main
    global menu, old_settings

    if getselected(menu) == "play":
        Main.init()

    elif getselected(menu) == "quit":
        sys.stdout.write("\033[37m")
        sys.stdout.write("\033[40m")

        termios.tcsetattr(sys.stdin, termios.TCSADRAIN, old_settings)
        sys.exit()


def show():
    import Main
    import Game
    global menu

    # efface le terminal
    sys.stdout.write("\033[2J")
    sys.stdout.write("\033[1;1H")
    sys.stdout.write("\033[37m")

    sys.stdout.write(menu["str"])

    first = getfirst(menu)

    if not first:
        score = str(Game.getscore(Main.player))
        temps = str(Game.gettime(Main.player))

        sys.stdout.write("\033[3;9H")
        sys.stdout.write(score)
        sys.stdout.write("\033[5;9H")
        sys.stdout.write(temps)

    showcursor()

    sys.stdout.write("\033[37m")  # reset de la couleur
    sys.stdout.write("\033[40m")

    sys.stdout.write("\033[0;0H\n")  # reset curseur


def showcursor():
    global menu

    first = getfirst(menu)
    selected = getselected(menu)

    if first:
        if selected == "play":
            sys.stdout.write("\033[4;19H")
            sys.stdout.write(">")

        else:
            sys.stdout.write("\033[6;18H")
            sys.stdout.write(">")

    else:
        if selected == "play":
            sys.stdout.write("\033[7;7H")
            sys.stdout.write(">")

        else:
            sys.stdout.write("\033[9;7H")
            sys.stdout.write(">")


def run():
    show()

    while 1:
        if select.select([sys.stdin], [], [], 0) == ([sys.stdin], [], []):
            move()
            show()


def main():
    global menu

    menu = init()
    run()


# --------
# main()
