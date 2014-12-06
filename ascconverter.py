#!/usr/bin/env python
# *-* coding: iso-8859-1 *-*

import sys
import os

filePath = "Dict/TOEFL.txt"
fichier = open(filePath, "rb")
content = fichier.read().decode("utf-8")
fichier.close()

fichierTemp = open("Dict/TOEFLASC.txt", "w")
fichierTemp.write(content.encode("ASCII", 'ignore'))
fichierTemp.close()