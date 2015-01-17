'''
Created on 16/1/2015

@author: Jonnathan
'''
from reservacion import calculo_monto_reserva
from datetime import datetime
from tarifa import Tarifa
import unittest

class TestHoras(unittest.TestCase):
    
    def setUp(self):
        self.tarifa = Tarifa(tasa_diurna=30,tasa_nocturna=40)
    
    def testMenorMinimo(self):
        fecha_entrada = self.obtenerFecha("2014-01-01 01:00")
        fecha_salida = self.obtenerFecha("2014-01-01 01:14")
        self.assertRaises(AssertionError, calculo_monto_reserva(fecha_entrada, fecha_salida, self.tarifa))
        
    def testMinimoMinutos(self):
        fecha_entrada = self.obtenerFecha("2014-01-01 01:00")
        fecha_salida = self.obtenerFecha("2014-01-01 01:15")
        monto = calculo_monto_reserva(fecha_entrada, fecha_salida, self.tarifa)
        self.assertEqual(monto, self.tarifa.getTasaNocturno())
        
    def testUnMinuto(self):
        fecha_entrada = self.obtenerFecha("2014-01-01 01:00")
        fecha_salida = self.obtenerFecha("2014-01-01 01:16")
        tarifa = Tarifa(30,30)
        monto = calculo_monto_reserva(fecha_entrada, fecha_salida, tarifa)
        self.assertEqual(monto, self.tarifa.getTasaDiurno())
    
    def obtenerFecha(self,fecha):
        fecha = datetime.strptime(fecha, "%Y-%m-%d %H:%M")
        return fecha;   

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()