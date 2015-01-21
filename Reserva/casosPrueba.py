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
class TestCalculoMontoReserva(unittest.TestCase):
    
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
    

    def testMinTiempo(self):
        nocturno = 2.00
        diurno = 4.00
        self.assertRaises(AssertionError, self.calcularMonto,"2014-01-01 01:00", "2014-01-01 01:14", diurno, nocturno)
    
    def testMaxTiempo(self):
        nocturno = 2.00
        diurno = 4.00
        self.assertRaises(AssertionError, self.calcularMonto,"2014-01-01 01:00", "2014-01-04 01:01", diurno, nocturno)
    
    def testMenorTiempo(self):
        nocturno = 999999.11
        diurno = 4088999.67
        monto = self.calcularMonto("2014-01-01 01:00","2014-01-01 01:15",diurno,nocturno)
        dosDecimales = Decimal(10) ** -2
        verificacion = Decimal(nocturno*1)
        self.assertEqual(monto.quantize(dosDecimales), verificacion.quantize(dosDecimales))
    
    def testMayorTiempoInexacto(self):
        nocturno = 456.33
        diurno = 22.45
        monto = self.calcularMonto("2014-01-01 01:20", "2014-01-04 01:20", diurno, nocturno)
        dosDecimales = Decimal(10) ** -2
        verificacion = Decimal((nocturno*11 + diurno*11 + max(nocturno,diurno)*2 )*3)
        self.assertEqual(monto.quantize(dosDecimales), verificacion.quantize(dosDecimales))
        
        
    def testMayorTiempoExacto(self):
        nocturno = 45.40
        diurno = 56.90
        monto = self.calcularMonto("2014-01-01 01:00", "2014-01-04 01:00",diurno, nocturno)
        dosDecimales = Decimal(10) ** -2
        verificacion = Decimal((nocturno*12 + diurno*12)*3)
        self.assertEqual(monto.quantize(dosDecimales), verificacion.quantize(dosDecimales))
               
    def testUnMinuto(self):
        nocturno = 2.00
        diurno = 4.00
        monto = self.calcularMonto("2014-01-01 01:00","2014-01-01 01:16",diurno,nocturno)
        dosDecimales = Decimal(10) ** -2
        verificacion = Decimal(nocturno*1)
        self.assertEqual(monto.quantize(dosDecimales), verificacion.quantize(dosDecimales))
          
    def testTransicionNocturnoDiurno(self):
        # Caso diurno > nocturno
        nocturno,diurno = 12.00, 34.00
        monto = self.calcularMonto("2014-01-01 05:01", "2014-01-01 6:01",diurno, nocturno)
        dosDecimales = Decimal(10) ** -2
        verificacion = Decimal(max(nocturno,diurno))
        self.assertEqual(monto.quantize(dosDecimales), verificacion.quantize(dosDecimales))
        
        # Caso nocturno > diurno
        nocturno = 14.00
        diurno = 6.00
        monto = self.calcularMonto("2014-01-01 05:01", "2014-01-01 6:01",diurno, nocturno)
        verificacion = Decimal(max(nocturno,diurno))
        self.assertEqual(monto.quantize(dosDecimales), verificacion.quantize(dosDecimales))
            
              
    def testTransicionDiurnoNocturno(self):
        # Caso diurno > nocturno
        nocturno = 2.00
        diurno = 11.15
        monto = self.calcularMonto("2014-01-01 17:01", "2014-01-01 18:01",diurno, nocturno)
        dosDecimales = Decimal(10) ** -2
        verificacion = Decimal(max(nocturno,diurno))
        self.assertEqual(monto.quantize(dosDecimales), verificacion.quantize(dosDecimales))
    
        # Caso nocturno > diurno
        nocturno = 17.10
        diurno = 3.25
        monto = self.calcularMonto("2014-01-01 17:01", "2014-01-01 18:01",diurno, nocturno)
        verificacion = Decimal(max(nocturno,diurno))
        self.assertEqual(monto.quantize(dosDecimales), verificacion.quantize(dosDecimales))
    
    
    def testTransicionADiurnoSinMaximo(self):
        nocturno = 40.35 # Caso diurno > nocturno
        diurno = 80.15
        monto = self.calcularMonto("2014-01-01 05:00", "2014-01-01 6:00",diurno, nocturno)
        dosDecimales = Decimal(10) ** -2
        verificacion = Decimal(nocturno)
        self.assertEqual(monto.quantize(dosDecimales), verificacion.quantize(dosDecimales))
        
        nocturno = 74.00 # Caso nocturno > diurno
        diurno = 10.80
        monto = self.calcularMonto("2014-01-01 05:00", "2014-01-01 6:00",diurno, nocturno)
        dosDecimales = Decimal(10) ** -2
        verificacion = Decimal(nocturno)
        self.assertEqual(monto.quantize(dosDecimales), verificacion.quantize(dosDecimales))
      
      
    def testTransicionANocturnoSinMaximo(self):
        nocturno = 40.35 # Caso diurno > nocturno
        diurno = 80.15
        monto = self.calcularMonto("2014-01-01 17:00", "2014-01-01 18:00",diurno,nocturno)
        dosDecimales = Decimal(10) ** -2
        verificacion = Decimal(diurno)
        self.assertEqual(monto.quantize(dosDecimales), verificacion.quantize(dosDecimales))
        
        nocturno = 74.00 # Caso nocturno > diurno
        diurno = 10.80
        monto = self.calcularMonto("2014-01-01 17:00", "2014-01-01 18:00",diurno,nocturno)
        dosDecimales = Decimal(10) ** -2
        verificacion = Decimal(diurno)
        self.assertEqual(monto.quantize(dosDecimales), verificacion.quantize(dosDecimales))
    

    def testMenorTiempoInexacto(self):
        nocturno = 8.34
        diurno = 999.11
        monto = self.calcularMonto("2014-01-01 17:59", "2014-01-01 18:14",diurno, nocturno)
        dosDecimales = Decimal(10) ** -2
        verificacion = Decimal(max(diurno, nocturno)*1)
        self.assertEqual(monto.quantize(dosDecimales), verificacion.quantize(dosDecimales))
       
    
    def testHoraDemasNocturno(self):
        nocturno = 8.34
        diurno = 999.11
        monto = self.calcularMonto("2014-01-01 20:00", "2014-01-01 21:01",diurno, nocturno)
        dosDecimales = Decimal(10) ** -2
        verificacion = Decimal(nocturno*2)
        self.assertEqual(monto.quantize(dosDecimales), verificacion.quantize(dosDecimales))
        
    
    def testHoraDemasDiurno(self):
        nocturno = 8.34
        diurno = 999.11
        monto = self.calcularMonto("2014-01-01 8:00", "2014-01-01 9:01",diurno,nocturno)
        dosDecimales = Decimal(10) ** -2
        verificacion = Decimal(diurno*2)
        self.assertEqual(monto.quantize(dosDecimales), verificacion.quantize(dosDecimales))
        
        
    def testHoraDemasConTransicionADiurno1(self):
        nocturno = 2
        diurno = 4
        dosDecimales = Decimal(10) ** -2
        monto = self.calcularMonto("2014-01-12 05:01", "2014-01-12 06:02",diurno, nocturno)
        verificacion = Decimal(max(nocturno, diurno)*1 + diurno *1)
        self.assertEqual(monto.quantize(dosDecimales), verificacion.quantize(dosDecimales))
        

    def testHoraDemasConTransicionANocturno1(self):
        nocturno = 34.67
        diurno = 222.34
        monto = self.calcularMonto("2014-01-01 17:01", "2014-01-01 18:02",diurno,nocturno)
        dosDecimales = Decimal(10) ** -2
        verificacion = Decimal(max(nocturno,diurno)*1  + nocturno*1)
        self.assertEqual(monto.quantize(dosDecimales), verificacion.quantize(dosDecimales))
        
    
    def testHoraDemasConTransicionADiurno2(self):
        nocturno = 7.00
        diurno = 5.00
        monto = self.calcularMonto("2014-01-01 5:00", "2014-01-01 6:01",diurno,nocturno)
        dosDecimales = Decimal(10) ** -2
        verificacion = Decimal(nocturno + diurno)
        self.assertEqual(monto.quantize(dosDecimales), verificacion.quantize(dosDecimales))
        
    
    def testHoraDemasConTransicionANocturno2(self):
        nocturno = 7.00
        diurno = 5.00
        monto = self.calcularMonto("2014-01-01 17:00", "2014-01-01 18:01",diurno,nocturno)
        dosDecimales = Decimal(10) ** -2
        verificacion = Decimal(nocturno + diurno)
        self.assertEqual(monto.quantize(dosDecimales), verificacion.quantize(dosDecimales))
    
    def testHoraMinimaConTransicionANocturno(self):
        nocturno = 13.00
        diurno = 7.00 
        monto = self.calcularMonto("2014-01-01 17:59", "2014-01-01 18:14",diurno,nocturno)
        dosDecimales = Decimal(10) ** -2
        verificacion = Decimal(max(nocturno,diurno))
        self.assertEqual(monto.quantize(dosDecimales), verificacion.quantize(dosDecimales)) 
        
    def testHoraMinimaConTransicionADiurno(self):
        nocturno = 13.00
        diurno = 7.00 
        monto = self.calcularMonto("2014-01-01 5:59", "2014-01-01 6:14",diurno,nocturno)
        dosDecimales = Decimal(10) ** -2
        verificacion = Decimal(max(nocturno,diurno))
        self.assertEqual(monto.quantize(dosDecimales), verificacion.quantize(dosDecimales)) 
          
    def testTarifaGratisDiurnoTiempoMin(self):
        nocturno = 99.99
        diurno = 0
        monto = self.calcularMonto("2014-01-01 7:00", "2014-01-01 7:15",diurno,nocturno)
        dosDecimales = Decimal(10) ** -2
        verificacion = Decimal(diurno)
        self.assertEqual(monto.quantize(dosDecimales), verificacion.quantize(dosDecimales))
        
    def testTarifaGratisNocturnoTiempoMin(self):
        nocturno = 0
        diurno = 99.99
        monto = self.calcularMonto("2014-01-01 7:00", "2014-01-01 7:15",diurno,nocturno)
        dosDecimales = Decimal(10) ** -2
        verificacion = Decimal(diurno)
        self.assertEqual(monto.quantize(dosDecimales), verificacion.quantize(dosDecimales))
        
if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()