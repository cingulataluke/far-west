#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Ce fichier contient toutes les fonctions permettant de générer le sol et les rochers (obstacles)
"""

# importation des modules nécessaires :
# modules système
import random
import sys

# ---------


def create(placeholder):
    """créée le terrain (plat en P1)"""
    t = dict()

    fichier = open(placeholder, "r")
    t["str"] = fichier.read()
    fichier.close()
    t["grid"] = t["str"].splitlines()

    return t


def createrocks(rock):
    """créée un obstacle"""
    r = dict()

    fichier = open(rock, "r")
    r["str"] = fichier.read()
    fichier.close()
    r["grid"] = r["str"].splitlines()
    r["x"] = random.randint(16, 28) or random.randint(32, 45)

    return r


def show(t, r):
    sys.stdout.write("\033[1;1H")
    sys.stdout.write("\033[40m")  # fond noir
    sys.stdout.write("\033[33m")  # terrain jaune

    sys.stdout.write(t["str"])  # affiche le terrain

    for i in r:
        sys.stdout.write("\033[11" + ";" + str(i["x"]) + "H")
        sys.stdout.write(i["grid"][0])  # affiche les rochers
        sys.stdout.write("\033[12" + ";" + str(i["x"]) + "H")
        sys.stdout.write(i["grid"][1])
