'''
Created on 16/1/2015

@author: Jonnathan
'''
from reservacion import calculo_monto_reserva
from datetime import datetime
from tarifa import Tarifa
import unittest

class TestHoras(unittest.TestCase):
    ''' Clase de prueba para las horas, La tasa es fija para cada prueba'''
       
    def calcularMonto(self,fecha_entrada,fecha_salida,diurno,nocturno):
        fecha_entrada = datetime.strptime(fecha_entrada, "%Y-%m-%d %H:%M")
        fecha_salida = datetime.strptime(fecha_salida,"%Y-%m-%d %H:%M")
        tarifa = Tarifa(tasa_diurna=diurno,tasa_nocturna=nocturno)
        return calculo_monto_reserva(fecha_entrada,fecha_salida,tarifa)
     
        
    def testMinTiempo(self):
        #Arreglar assertRaises
        diurno,nocturno = 7,5
        self.assertRaises(AssertionError, self.calcularMonto("2014-01-01 01:00", "2014-01-01 01:14",diurno,nocturno))
    
    def testMaxTiempo(self):
        #Arreglar assertRaises
        diurno,nocturno = 7,5 
        self.assertRaises(AssertionError, self.calcularMonto("2014-01-01 01:00", "2014-01-04 01:01",diurno,nocturno))
        
    def testMenorTiempo(self):
        diurno,nocturno = 7,5 
        monto = self.calcularMonto("2014-01-01 01:00","2014-01-01 01:15",diurno,nocturno)
        self.assertEqual(monto, nocturno*1)
        
    def testMayorTiempoInexacto(self):
        diurno,nocturno = 7,5 
        monto = self.calcularMonto("2014-01-01 01:20", "2014-01-04 01:20",diurno,nocturno)
        self.assertEqual(monto, (nocturno*11 + diurno*11 + max(nocturno,diurno)*2 )*3) 
    
    def testMayorTiempoExacto(self):
        #Revisar caso de prueba (La hora diurna Aplica de 6:00 a 18:00 (inclusive)
        # Transicion Entre hora 17:00 y hora 18:00 se esta cobrando la tasa nocturna (deberia ser la diurna)
        diurno,nocturno = 7,5 
        monto = self.calcularMonto("2014-01-01 01:00", "2014-01-04 01:00",diurno,nocturno)
        self.assertEqual(monto,(nocturno*12 + diurno*12)*3) 
             
    def testUnMinuto(self):
        diurno,nocturno = 7,5 
        monto = self.calcularMonto("2014-01-01 01:00","2014-01-01 01:16",diurno,nocturno)
        self.assertEqual(monto, nocturno*1)
        
if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()