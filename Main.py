#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Merci à G. Desmeulles et Q. Carlier dont le programme Saucer a servi d'inspiration et d'exemple pour de nombreuses
parties de ce code.

Fichier principal du programme

BUGS CONNUS :
-> crashs aléatoires
   - origine : collision des balles
   - raison : ???

"""

# importation des modules nécessaires :
# modules système
import random
import sys
import time
import select
import termios

# modules du projet
import Menu
import Game
import Enemy
import Terrain
import Bullet

# variables globales
old_settings = termios.tcgetattr(sys.stdin)
timeStep = 0.007
terrain = None
rocks = []
player = None
enemies = []
bullets = []
enemycounter = 0
speed = 0
acceleration = 1
onGround = False
onRock = False
onEnemy = False

# ---------


def enemyinit(num):
    for i in range(num):
        rangex = random.randint(0, 55)
        while 16 <= rangex <= 45:
            rangex = random.randint(0, 55)
        if rangex <= 16:
            dirct = "right"
        else:
            dirct = "left"
        enemies.append(Enemy.create(rangex, 12, dirct))


def enemyremove(enemy):
    enemies.remove(enemy)


def bulletremove(bullet):
    bullets.remove(bullet)


def init():
    # initialisation de la partie

    global timeStep, terrain, rocks, player, enemies

    terrain = Terrain.create("terrain.txt")  # génération du terrain

    player = Game.create(30, 12, "right")  # création du perso joueur en position(30,12) tourné vers la droite
    enemyinit(5)  # création de 5 ennemis

    i = 0  # empêche que les rochers se crééent là où il y a des ennemis
    toremove = False
    while i < 2:
        rocks.append(Terrain.createrocks("rock.txt"))  # génération des rochers
        for r in rocks:
            for e in enemies:
                if testcollision(r, e) or r["x"]+1 == e["x"]:
                    toremove = True
            if toremove:
                rocks.remove(r)
        i += 1

    run()


def testcollision(o, e):
    if o['x'] == e['x']:
        return True
    else:
        return False


def testcollisiony(o, e):
    if o['y'] == e['y']:
        return True
    else:
        return False


def run():
    # boucle de simulation

    global timeStep

    counter = 0

    while 1:
        counter += 1

        if counter == 10:  # les interactions et l'affichage n'ont lieu qu'une fois sur 10
            interact()
            show()
            counter = 0

        time.sleep(timeStep)


def show():
    # rafraichissement de l'affichage

    global terrain, player, enemies, bullets

    # efface le terminal
    sys.stdout.write("\033[1;1H")
    sys.stdout.write("\033[2J")

    if not Game.testover(player):

        # afficher tous les éléments
        Game.showgui(player)
        Game.show(player)
        Terrain.show(terrain, rocks)

        for e in enemies:
            Enemy.show(e)

        for b in bullets:
            Bullet.show(b)

        sys.stdout.write("\033[37m")  # reset de la couleur
        sys.stdout.write("\033[40m")

        sys.stdout.write("\033[0;0H\n")  # reset curseur


def isdata():
    return select.select([sys.stdin], [], [], 0) == ([sys.stdin], [], [])


def interact():
    global player, terrain, enemycounter, speed, acceleration, onGround, onRock, onEnemy

    speed -= acceleration
    y = Game.gety(player)
    y -= speed

    overrock = False
    for r in rocks:  # vérifie la collision avec un rocher
        if testcollision(player, r) or Game.getx(player) == r["x"]+1:
            overrock = True

    overenemy = False
    for e in enemies:
        if testcollision(player, e):
            overenemy = True

    if overrock and Game.gety(player) > 10:
        onRock = True

    if overenemy and Game.gety(player) > 11:
        onEnemy = True

    if not overrock:
        onRock = False

    if not overenemy:
        onEnemy = False

    if not overrock and not overenemy and y > 12:
        onGround = True

    if onGround:
        y = 12
    if onRock:
        y = 10
    if onEnemy:
        y = 11

    Game.sety(player, y)

    if isdata():
        k = sys.stdin.read(1)

        if k == 'z':  # touche du haut
            Game.jump(3)

        if k == 'q':
            Game.move(player, "left")
            for i in enemies:
                if testcollision(player, i) and onGround:
                    Game.move(player, "right")  # détection des collisions avec les ennemis
            for i in rocks:
                if (testcollision(player, i) or Game.getx(player) == i["x"]+1) and onGround:
                    Game.move(player, "right")  # détection des collisions avec les rochers

        elif k == 'd':
            Game.move(player, "right")
            for i in enemies:
                if testcollision(player, i) and onGround:
                    Game.move(player, "left")  # détection des collisions avec les ennemis
            for i in rocks:
                if (testcollision(player, i) or Game.getx(player) == i["x"]+1) and onGround:
                    Game.move(player, "left")  # détection des collisions avec les rochers

        if k == 's':
            bullets.append(Game.shoot(player))

        if k == "a":
            Menu.gameover()

        while isdata():
            sys.stdin.read(1)

    enemycounter += 1
    if enemycounter == 2:
        player["time"] += 1
        for e in enemies:
            Enemy.live(e)
        enemycounter = 0

    for b in bullets:
        Bullet.live(b)

    if len(enemies) < 3:  # s'il n'y a plus assez d'ennemis, on en rajoute
        cote = random.randint(0, 2)
        if cote == 0:
            enemies.append(Enemy.create(1, 12, "right"))
        else:
            enemies.append(Enemy.create(55, 12, "left"))

    if Game.testover(player):
        Menu.gameover()


def main():
    Menu.main()


# ---------

main()
