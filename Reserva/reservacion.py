'''
Created on 12/1/2015

@author: Iranid
'''
from datetime import date,datetime, time
import sys 
from tarifa import Tarifa

def main():
    '''El cableado de datos es temporal '''
    parametro_fecha_entrada = "2014-01-01 16:30"
    parametro_fecha_salida = "2014-02-01 16:35"
    parametro_tasa_diurna = 45
    parametro_tasa_nocturna = 35
    
    try:
        fecha_entrada = datetime.strptime(parametro_fecha_entrada, "%Y-%m-%d %H:%M")
    
    except Exception as e1:
        print("Fecha de entrada inválida")
        sys.exit("El programa no puede continuar")
    
    try:
        fecha_salida = datetime.strptime(parametro_fecha_salida, "%Y-%m-%d %H:%M")
    
    except Exception as e2:
        print("Fecha de salida inválida")
        sys.exit("El programa no puede continuar")
    
    if parametro_tasa_diurna < 0:
        print("El monto de la tasa diurna no es válido")
        sys.exit()
        
    if parametro_tasa_nocturna < 0:
        print("El monto de la tasa nocturna no es válido")
        sys.exit()
    
    tarifa = Tarifa(parametro_tasa_diurna, parametro_tasa_nocturna)

def calculo_monto_reserva(self, fecha_entrada, fecha_salida,tarifa):
    
    #Determina si fecha de entrada es mayor a la fecha de entrada
    restaDias = fecha_salida - fecha_entrada
    
    if restaDias.days < 0:
        print("La fecha de entrada es mayor que la fecha de salida")
        
    if restaDias.total_seconds() <(15*60) and restaDias.seconds >(72*60*60):
        print("La reservación no cumple los límites de tiempo inferior y superior")
    
    
    
    
if __name__== "__main__":
    main()
