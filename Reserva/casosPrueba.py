'''
Created on 16/1/2015

@author: Jonnathan
'''
from reservacion import calculo_monto_reserva
from datetime import datetime
from tarifa import Tarifa
import unittest

diurno = 5     # Constantes que representan las tasas fijas
nocturno = 7

class TestHoras(unittest.TestCase):
    ''' Clase de prueba para las horas, La tasa es fija para cada prueba'''
    
    def setUp(self):
        self.tarifa = Tarifa(tasa_diurna=diurno,tasa_nocturna=nocturno) # Inicializacion de tasa Fija
    
    def calcularMonto(self,fecha_entrada,fecha_salida):
        fecha_entrada = datetime.strptime(fecha_entrada, "%Y-%m-%d %H:%M")
        fecha_salida = datetime.strptime(fecha_salida,"%Y-%m-%d %H:%M")
        return calculo_monto_reserva(fecha_entrada,fecha_salida,self.tarifa)
      
    def testMinTiempo(self):
        #Arreglar assertRaises
        self.assertRaises(AssertionError, self.calcularMonto("2014-01-01 01:00", "2014-01-01 01:14"))
    
    def testMaxTiempo(self):
        #Arreglar assertRaises 
        self.assertRaises(AssertionError, self.calcularMonto("2014-01-01 01:00", "2014-01-04 01:01"))
        
    def testMenorTiempo(self):
        monto = self.calcularMonto("2014-01-01 01:00","2014-01-01 01:15")
        self.assertEqual(monto, nocturno*1)
        
    def testMayorTiempoInexacto(self):
        monto = self.calcularMonto("2014-01-01 01:20", "2014-01-04 01:20")
        self.assertEqual(monto, (nocturno*11 + diurno*11 + max(nocturno,diurno)*2 )*3) 
    
    def testMayorTiempoExacto(self):
        monto = self.calcularMonto("2014-01-01 01:00", "2014-01-04 01:00")
        self.assertEqual(monto,(nocturno*12 + diurno*12)*3) 

    def testUnMinuto(self):
        monto = self.calcularMonto("2014-01-01 01:00","2014-01-01 01:16")
        self.assertEqual(monto, nocturno*1)
        
    def testTransiciones(self):
        monto = self.calcularMonto("2014-01-01 05:01", "2014-01-01 6:01")
        self.assertEqual(monto, max(nocturno,diurno))
        
        monto = self.calcularMonto("2014-01-01 17:01", "2014-01-01 18:01")
        self.assertEqual(monto, max(nocturno,diurno))
        
    def testTransicionSinMaximo(self):
        monto = self.calcularMonto("2014-01-01 05:00", "2014-01-01 6:00")
        self.assertEqual(monto, nocturno)
        monto = self.calcularMonto("2014-01-01 17:00", "2014-01-01 18:00")
        self.assertEqual(monto, diurno)
        
    def testHoraDemas(self):
        monto = self.calcularMonto("2014-01-01 20:00", "2014-01-01 21:01")
        self.assertEqual(monto, nocturno*2)
        monto = self.calcularMonto("2014-01-01 8:00", "2014-01-01 9:01")
        self.assertEqual(monto, diurno*2)
        
    def testHoraDemasConTransicion(self):
         #Recomendacion: Prueba cambiando valores de nocturno y diurno
        #Caso nocturno > diurno, diurno > nocturno (habria q cambiar la funcion)
        monto = self.calcularMonto("2014-01-01 5:01", "2014-01-01 6:02")
        self.assertEqual(monto, max(nocturno,diurno) + diurno)
        monto = self.calcularMonto("2014-01-01 17:01", "2014-01-01 18:02")
        self.assertEqual(monto, max(nocturno,diurno) + nocturno)
        
    def testHoraDemasConTransicion2(self):
        #Recomendacion: Prueba cambiando valores de nocturno y diurno
        #Caso nocturno > diurno, diurno > nocturno (habria q cambiar la funcion)
        monto = self.calcularMonto("2014-01-01 5:00", "2014-01-01 6:01")
        self.assertEqual(monto,nocturno + diurno)
        monto = self.calcularMonto("2014-01-01 17:00", "2014-01-01 18:01")
        self.assertEqual(monto,nocturno + diurno)
        
        
if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()