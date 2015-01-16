'''
Created on 16/1/2015

@author: Jonnathan
'''
import unittest
from reservacion import calculo_monto_reserva
from tarifa import Tarifa
import datetime

class Test(unittest.TestCase):

    def testHoraCercana(self):
        entrada = datetime.datetime(year=2015,month=1,day=13,hour=14,minute=10)
        salida = datetime.datetime(year=2015, month=1, day=13, hour=14,minute=20)
        tarifa = Tarifa(30,30)
        monto = calculo_monto_reserva(entrada, salida, tarifa)
        
    def testMinimoMinutos(self):
        entrada = datetime.datetime(year=2015,month=1,day=13,hour=14,minute=10)
        salida = datetime.datetime(year=2015, month=1, day=13, hour=14,minute=25)
        tarifa = Tarifa(30,30)
        monto = calculo_monto_reserva(entrada, salida, tarifa)
        
    def testUnMinuto(self):
        entrada = datetime.datetime(year=2015,month=1,day=13,hour=14,minute=10)
        salida = datetime.datetime(year=2015, month=1, day=13, hour=14,minute=26)
        tarifa = Tarifa(30,30)
        monto = calculo_monto_reserva(entrada, salida, tarifa)
        self.assertEqual(monto, 30)

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()