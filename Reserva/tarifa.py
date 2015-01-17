'''
Created on 12/1/2015

@author: Iranid
'''

'''Clase Tarifa que se encarga del manejo 
de la tasa diurna y la tasa nocturna 
''' 

from decimal import *

class Tarifa:
        
    def __init__(self,tasa_diurna, tasa_nocturna):
        self.__tasa_diurna = Decimal(tasa_diurna)
        self.__tasa_nocturna = Decimal(tasa_nocturna)

    def getTasaNocturno(self):
        return self.__tasa_nocturna
    
    def getTasaDiurno(self):
        return self.__tasa_diurna
    
#tarifa = Tarifa(29.5,40.5)
#print(tarifa.getnocturno())   