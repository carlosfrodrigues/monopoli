#!/usr/bin/python
# -*- coding: utf-8 -*-

import getmono
import insertsql

obj = getmono.GetMono("Engenharia+Eletrônica+e+de+Computação", 2017)
lista = obj.monoList()
obj.download()

insertsql.getKeys(lista, "files/")

