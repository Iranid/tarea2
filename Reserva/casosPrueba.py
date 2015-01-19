'''
Created on 16/1/2015

@author: Jonnathan
'''
from reservacion import calculoMontoReserva
from datetime import datetime
from tarifa import Tarifa
from decimal import *
import unittest

'''
diurno = 5
nocturno =  999.11
diurno = Decimal(diurno)    # Constantes que representan las tasas fijas
nocturno = Decimal(nocturno)
'''


class TestHoras(unittest.TestCase):
    ''' Clase de prueba para las horas, La tasa es fija para cada prueba'''
    '''
    def setUp(self):
        self.tarifa = Tarifa(tasa_diurna=diurno,tasa_nocturna=nocturno) # Inicializacion de tasa Fija
    '''
    
    def calcularMonto(self,fecha_entrada,fecha_salida,diurno, nocturno):
        tarifa = Tarifa(diurno, nocturno)
        fecha_entrada = datetime.strptime(fecha_entrada, "%Y-%m-%d %H:%M")
        fecha_salida = datetime.strptime(fecha_salida,"%Y-%m-%d %H:%M")
        return calculoMontoReserva(fecha_entrada,fecha_salida,tarifa)
      
    def testMinTiempo(self):
        nocturno = 2
        diurno = 4
        self.assertRaises(AssertionError, lambda: self.calcularMonto("2014-01-01 01:00", "2014-01-01 01:14", diurno, nocturno))
    
    def testMaxTiempo(self):
        nocturno = 2
        diurno = 4
        self.assertRaises(AssertionError, lambda: self.calcularMonto("2014-01-01 01:00", "2014-01-04 01:01", diurno, nocturno))
        
    def testMenorTiempo(self):
        nocturno = 999.11
        diurno = 40.67
        monto = self.calcularMonto("2014-01-01 01:00","2014-01-01 01:15",diurno,nocturno)
        self.assertEqual(float(monto), nocturno*1)
        
    def testMayorTiempoInexacto(self):
        nocturno = 456.33
        diurno = 22.45
        monto = self.calcularMonto("2014-01-01 01:20", "2014-01-04 01:20", diurno, nocturno)
        self.assertEqual(float(monto), (nocturno*11 + diurno*11 + max(nocturno,diurno)*2 )*3)

    def testMayorTiempoExacto(self):
        nocturno = 2.00
        diurno = 56.90
        monto = self.calcularMonto("2014-01-01 01:00", "2014-01-04 01:00",diurno, nocturno)
        self.assertEqual(float(format(monto,'.2f')), float(format((nocturno*12 + diurno*12)*3,'.2f')))
                 
    def testUnMinuto(self):
        nocturno = 2
        diurno = 4
        monto = self.calcularMonto("2014-01-01 01:00","2014-01-01 01:16",diurno,nocturno)
        self.assertEqual(float(monto), nocturno*1)
        
    def testTransicionMasUnMinuto(self):
        nocturno = 2
        diurno = 4
        monto = self.calcularMonto("2014-01-12 05:01", "2014-01-12 06:02",diurno, nocturno)
        self.assertEqual(float(monto), (max(nocturno, diurno)*1 + diurno *1))

        
    def testMenorTiempoInexacto(self):
        nocturno = 2
        diurno = 4
        monto = self.calcularMonto("2014-01-01 17:59", "2014-01-01 18:14",diurno, nocturno)
        self.assertEqual(float(monto), max(diurno, nocturno)*1)
     
    
        
if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()