'''
Created on 12/1/2015

@author: Iranid
'''

'''Clase Tarifa que se encarga del manejo 
de la tasa diurna y la tasa nocturna 
''' 

from decimal import *

class Tarifa:
        
    _tasa_diurna = 0
    _tasa_nocturna = 0
    
    def __init__(self,tasa_diurna, tasa_nocturna):
        self._tasa_diurna = Decimal(tasa_diurna)
        self._tasa_nocturna = Decimal(tasa_nocturna)

    def getnocturno(self):
        return self._tasa_nocturna
    
    def getdiurno(self):
        return self._tasa_diurna
    
tarifa = Tarifa(29.5,40.5)
#print(tarifa.getnocturno())   