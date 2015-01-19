'''
Created on 16/1/2015

@author: Jonnathan
'''
from reservacion import calculoMontoReserva
from datetime import datetime
from tarifa import Tarifa
from decimal import  *
import unittest



class TestHoras(unittest.TestCase):
    
    
    
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
        nocturno = 999999.11
        diurno = 4088999.67
        TWOPLACES = Decimal(10) ** -2
        monto = self.calcularMonto("2014-01-01 01:00","2014-01-01 01:15",diurno,nocturno)
        verificacion = (nocturno*1)
        self.assertEqual(Decimal(monto).quantize(TWOPLACES), Decimal(verificacion).quantize(TWOPLACES))
        print(Decimal(monto).quantize(TWOPLACES))
        print(Decimal(verificacion).quantize(TWOPLACES))
        
    def testMayorTiempoInexacto(self):
        nocturno = 456.33
        diurno = 22.45
        TWOPLACES = Decimal(10) ** -2
        monto = self.calcularMonto("2014-01-01 01:20", "2014-01-04 01:20", diurno, nocturno)
        verificacion = ((nocturno*11 + diurno*11 + max(nocturno,diurno)*2 )*3)
        self.assertEqual(Decimal(monto).quantize(TWOPLACES), Decimal(verificacion).quantize(TWOPLACES))
        print(Decimal(monto).quantize(TWOPLACES))
        print(Decimal(verificacion).quantize(TWOPLACES))
        

    def testMayorTiempoExacto(self):
        nocturno = 263.00
        diurno = 56.90
        TWOPLACES = Decimal(10) ** -2
        monto = self.calcularMonto("2014-01-01 01:00", "2014-01-04 01:00",diurno, nocturno)
        verificacion = Decimal((nocturno*12 + diurno*12)*3)
        self.assertEqual(Decimal(monto).quantize(TWOPLACES), Decimal(verificacion).quantize(TWOPLACES))
        print(Decimal(monto).quantize(TWOPLACES))
        print(Decimal(verificacion).quantize(TWOPLACES))
        
                 
    def testUnMinuto(self):
        nocturno = 2.00
        diurno = 4.00
        TWOPLACES = Decimal(10) ** -2
        monto = self.calcularMonto("2014-01-01 01:00","2014-01-01 01:16",diurno,nocturno)
        verificacion = Decimal(nocturno*1)
        self.assertEqual(Decimal(monto).quantize(TWOPLACES), Decimal(verificacion).quantize(TWOPLACES))
        print(Decimal(monto).quantize(TWOPLACES))
        print(Decimal(verificacion).quantize(TWOPLACES))
        
    def testTransicionMasUnMinuto(self):
        nocturno = 2
        diurno = 4
        TWOPLACES = Decimal(10) ** -2
        monto = self.calcularMonto("2014-01-12 05:01", "2014-01-12 06:02",diurno, nocturno)
        verificacion = Decimal(max(nocturno, diurno)*1 + diurno *1)
        self.assertEqual(Decimal(monto).quantize(TWOPLACES), Decimal(verificacion).quantize(TWOPLACES))
        print(Decimal(monto).quantize(TWOPLACES))
        print(Decimal(verificacion).quantize(TWOPLACES))

        
    def testMenorTiempoInexacto(self):
        nocturno = 8.34
        diurno = 999.11
        TWOPLACES = Decimal(10) ** -2
        monto = self.calcularMonto("2014-01-01 17:59", "2014-01-01 18:14",diurno, nocturno)
        verificacion = Decimal(max(diurno, nocturno)*1)
        self.assertEqual(Decimal(monto).quantize(TWOPLACES), Decimal(verificacion).quantize(TWOPLACES))
        print(Decimal(monto).quantize(TWOPLACES))
        print(Decimal(verificacion).quantize(TWOPLACES))
     
    
        
if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()