'''
Created on 16/1/2015

@author: Jonnathan
'''
from reservacion import calculoMontoReserva
from datetime import datetime
from tarifa import Tarifa
from decimal import  *
import unittest


'''
Casos de prueba para la funcion calculoMontoReserva
'''
class TestHoras(unittest.TestCase):
    
    '''
    Inicializa los argumentos de la funcion calculoMontoReserva
    y la ejecuta para obtener el valor de una reserva
    
    @param fechaEntrada     Fecha de entrada de la reserva
    @param fechaSalida      Fecha de salida de la reserva
    @param diurno           Tasa cobrada en horario diurno
    @param nocturno         Tasa cobrada en horario nocturno
    
    @return Decimal         Monto calculado de la reserva
    '''
    def calcularMonto(self,fechaEntrada,fechaSalida,diurno, nocturno):
        tarifa = Tarifa(diurno, nocturno)
        fechaEntrada = datetime.strptime(fechaEntrada, "%Y-%m-%d %H:%M")
        fechaSalida = datetime.strptime(fechaSalida,"%Y-%m-%d %H:%M")
        return calculoMontoReserva(fechaEntrada,fechaSalida,tarifa)
    
    
    '''
    Prueba que la funcion no permita una reserva con una duracion menor a 15 minutos
    '''
    def testMinTiempo(self):
        nocturno = 2
        diurno = 4
        self.assertRaises(AssertionError, lambda: self.calcularMonto("2014-01-01 01:00", "2014-01-01 01:14", diurno, nocturno))
    
    
    '''
    Prueba que la funcion no permita una reserva con una duracion mayor a 72 horas
    '''
    def testMaxTiempo(self):
        nocturno = 2
        diurno = 4
        self.assertRaises(AssertionError, lambda: self.calcularMonto("2014-01-01 01:00", "2014-01-04 01:01", diurno, nocturno))
    
    
    '''
    Prueba una reserva con la duracion mas peque;a posible, es decir, una duracion de 15 minutos
    '''
    def testMenorTiempo(self):
        nocturno = 999999.11
        diurno = 4088999.67
        TWOPLACES = Decimal(10) ** -2
        monto = self.calcularMonto("2014-01-01 01:00","2014-01-01 01:15",diurno,nocturno)
        verificacion = Decimal(nocturno*1)
        self.assertEqual(monto.quantize(TWOPLACES), verificacion.quantize(TWOPLACES))
        print(monto.quantize(TWOPLACES))
        print(verificacion.quantize(TWOPLACES))
    
    
    '''
    Prueba una reserva de varios días donde se producen reiteradamente transiciones de horario diurno/nocturno
    '''
    def testMayorTiempoInexacto(self):
        nocturno = 456.33
        diurno = 22.45
        TWOPLACES = Decimal(10) ** -2
        monto = self.calcularMonto("2014-01-01 01:20", "2014-01-04 01:20", diurno, nocturno)
        verificacion = Decimal((nocturno*11 + diurno*11 + max(nocturno,diurno)*2 )*3)
        self.assertEqual(monto.quantize(TWOPLACES), verificacion.quantize(TWOPLACES))
        print(monto.quantize(TWOPLACES))
        print(verificacion.quantize(TWOPLACES))
        
    
    '''
    Prueba una reserva de varios días donde no se producen transiciones de horario diurno/nocturno
    '''
    def testMayorTiempoExacto(self):
        nocturno = 263.00
        diurno = 56.90
        TWOPLACES = Decimal(10) ** -2
        monto = self.calcularMonto("2014-01-01 01:00", "2014-01-04 01:00",diurno, nocturno)
        verificacion = Decimal((nocturno*12 + diurno*12)*3)
        self.assertEqual(monto.quantize(TWOPLACES), verificacion.quantize(TWOPLACES))
        print(monto.quantize(TWOPLACES))
        print(verificacion.quantize(TWOPLACES))
        
    
    '''
    Prueba una reserva donde la última hora cuantificable abarca sólo 1 minuto
    '''           
    def testUnMinuto(self):
        nocturno = 2.00
        diurno = 4.00
        TWOPLACES = Decimal(10) ** -2
        monto = self.calcularMonto("2014-01-01 01:00","2014-01-01 01:16",diurno,nocturno)
        verificacion = Decimal(nocturno*1)
        self.assertEqual(monto.quantize(TWOPLACES), verificacion.quantize(TWOPLACES))
        print(monto.quantize(TWOPLACES))
        print(verificacion.quantize(TWOPLACES))
    
    
    def testTransicionNocturnoDiurno(self):
        nocturno = 2.00
        diurno = 4.00
        TWOPLACES = Decimal(10) ** -2
        monto = self.calcularMonto("2014-01-01 05:01", "2014-01-01 6:01",diurno, nocturno)
        verificacion = Decimal(max(nocturno,diurno))
        self.assertEqual(monto.quantize(TWOPLACES), verificacion.quantize(TWOPLACES))
        
    
    def testTransicionDiurnoNocturno(self):
        nocturno = 2.00
        diurno = 4.00
        TWOPLACES = Decimal(10) ** -2
        monto = self.calcularMonto("2014-01-01 17:01", "2014-01-01 18:01",diurno, nocturno)
        verificacion = Decimal(max(nocturno,diurno))
        self.assertEqual(monto.quantize(TWOPLACES), verificacion.quantize(TWOPLACES))
    
    
    def testTransicionADiurnoSinMaximo(self):
        nocturno = 2.00
        diurno = 4.00
        TWOPLACES = Decimal(10) ** -2
        monto = self.calcularMonto("2014-01-01 05:00", "2014-01-01 6:00",diurno, nocturno)
        verificacion = Decimal(nocturno)
        self.assertEqual(monto.quantize(TWOPLACES), verificacion.quantize(TWOPLACES))
    
    
    def testTransicionANocturnoSinMaximo(self):
        nocturno = 2.00
        diurno = 4.00
        TWOPLACES = Decimal(10) ** -2
        monto = self.calcularMonto("2014-01-01 17:00", "2014-01-01 18:00",diurno,nocturno)
        verificacion = Decimal(diurno)
        self.assertEqual(monto.quantize(TWOPLACES), verificacion.quantize(TWOPLACES))
    
    
    
    '''
    Prueba una reserva donde se produce una transicion de horario 
    y la duración de la misma es el mínimo tiempo posible (15 minutos)
    '''  
    def testMenorTiempoInexacto(self):
        nocturno = 8.34
        diurno = 999.11
        TWOPLACES = Decimal(10) ** -2
        monto = self.calcularMonto("2014-01-01 17:59", "2014-01-01 18:14",diurno, nocturno)
        verificacion = Decimal(max(diurno, nocturno)*1)
        self.assertEqual(monto.quantize(TWOPLACES), verificacion.quantize(TWOPLACES))
        print(monto.quantize(TWOPLACES))
        print(verificacion.quantize(TWOPLACES))
    
    
    def testHoraDemasNocturno(self):
        nocturno = 8.34
        diurno = 999.11
        TWOPLACES = Decimal(10) ** -2
        monto = self.calcularMonto("2014-01-01 20:00", "2014-01-01 21:01",diurno, nocturno)
        verificacion = Decimal(nocturno*2)
        self.assertEqual(monto.quantize(TWOPLACES), verificacion.quantize(TWOPLACES))
        
    
    def testHoraDemasDiurno(self):
        nocturno = 8.34
        diurno = 999.11
        TWOPLACES = Decimal(10) ** -2
        monto = self.calcularMonto("2014-01-01 8:00", "2014-01-01 9:01",diurno,nocturno)
        verificacion = Decimal(diurno*2)
        self.assertEqual(monto.quantize(TWOPLACES), verificacion.quantize(TWOPLACES))
        
    
    
    '''
    Prueba una reserva donde se produce una transicion de horario 
    y luego de la transicion la siguiente hora a cobrar tiene sólo un minuto 
    ''' 
    def testHoraDemasConTransicionANocturno(self):
        nocturno = 2
        diurno = 4
        TWOPLACES = Decimal(10) ** -2
        monto = self.calcularMonto("2014-01-12 05:01", "2014-01-12 06:02",diurno, nocturno)
        verificacion = Decimal(max(nocturno, diurno)*1 + diurno *1)
        self.assertEqual(monto.quantize(TWOPLACES), verificacion.quantize(TWOPLACES))
        print(monto.quantize(TWOPLACES))
        print(verificacion.quantize(TWOPLACES))

    
    def testHoraDemasConTransicionADiurno(self):
        nocturno = 34.67
        diurno = 222.34
        TWOPLACES = Decimal(10) ** -2
        monto = self.calcularMonto("2014-01-01 17:01", "2014-01-01 18:02",diurno,nocturno)
        verificacion = Decimal(max(nocturno,diurno)*1  + nocturno*1)
        self.assertEqual(monto.quantize(TWOPLACES), verificacion.quantize(TWOPLACES))
        print(monto.quantize(TWOPLACES))
        print(verificacion.quantize(TWOPLACES))
    
    
    def testHoraDemasConTransicionANocturno2(self):
        #Recomendacion: Prueba cambiando valores de nocturno y diurno
        #Caso nocturno > diurno, diurno > nocturno (habria q cambiar la funcion)
        nocturno = 2
        diurno = 4
        TWOPLACES = Decimal(10) ** -2
        monto = self.calcularMonto("2014-01-01 5:00", "2014-01-01 6:01",diurno,nocturno)
        verificacion = Decimal(nocturno + diurno)
        self.assertEqual(monto.quantize(TWOPLACES), verificacion.quantize(TWOPLACES))
        
    
    def testHoraDemasConTransicionADiurno2(self):
        #Recomendacion: Prueba cambiando valores de nocturno y diurno
        #Caso nocturno > diurno, diurno > nocturno (habria q cambiar la funcion)
        nocturno = 2
        diurno = 4
        TWOPLACES = Decimal(10) ** -2
        monto = self.calcularMonto("2014-01-01 17:00", "2014-01-01 18:01",diurno,nocturno)
        verificacion = Decimal(nocturno + diurno)
        self.assertEqual(monto.quantize(TWOPLACES), verificacion.quantize(TWOPLACES))
        
    
    
    
        
if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()