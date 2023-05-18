#!/usr/bin/env python
# -*- coding: utf-8 -*-
import qrcode
img = qrcode.make("https://pezkdelivery.blogspot.com/2022/05/menu-pezk.html") # 2 de septiembre
f = open("pezk.png", "wb")
img.save(f)
f.close()
