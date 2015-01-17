'''
Created on 12/1/2015

@author: Iranid
'''
from datetime import datetime, timedelta,date
from tarifa import Tarifa
import sys
#from django.forms.formsets import TOTAL_FORM_COUNT

def main():
    '''El cableado de datos es temporal '''
    parametro_fecha_entrada = "2014-01-01 16:30"
    parametro_fecha_salida = "2014-01-01 18:45"
    parametro_tasa_diurna = 45
    parametro_tasa_nocturna = 90
    
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
    
    monto_total = calculo_monto_reserva(fecha_entrada, fecha_salida, tarifa)
    print("El monto total a pagar por la reserva es: ", monto_total)
    
    
    

def calculo_monto_reserva(fecha_entrada, fecha_salida,tarifa):
    
    total_pago_reserva = 0
    
    #Determina si fecha de entrada es mayor a la fecha de entrada
    restaDias = fecha_salida - fecha_entrada
    
    assert(fecha_salida > fecha_entrada) ,"La fecha de entrada es mayor que la fecha de salida"
        
    assert(restaDias.total_seconds() >=(15*60) and restaDias.total_seconds() <= (72*60*60)), \
           "La reservación no cumple los límites de tiempo inferior y superior"
    
    max_tasa = max(tarifa.getTasaDiurno(), tarifa.getTasaNocturno())
    
    fecha_revision = fecha_entrada
    while fecha_revision < fecha_salida:
        
        hora_actual = fecha_revision.hour
        hora_siguiente = (hora_actual + 1) % 24 
        hora_siguiente_DT = fecha_revision.replace(hour = hora_siguiente) 
        
        if hora_siguiente_DT > fecha_salida:
            hora_siguiente_DT = fecha_salida
            hora_siguiente = hora_siguiente_DT.hour
        print("\n")    
        print("hora actual y siguiente: ", hora_actual, hora_siguiente)  
        print("rango analizado: ", fecha_revision.strftime("%H:%M"), " - ", hora_siguiente_DT.strftime("%H:%M"))    
        
        periodo_nocturno1 = list(range(0,6))
        if hora_actual in periodo_nocturno1:
            if hora_siguiente == 6 and hora_siguiente_DT.minute != 0:
                total_pago_reserva += max_tasa
            else:
                total_pago_reserva += tarifa.getTasaNocturno()
            
    
        
        periodo_diurno = list(range(6,18))
        if hora_actual in periodo_diurno:
            if hora_siguiente == 18 and hora_siguiente_DT.minute != 0:
                total_pago_reserva += max_tasa
            else:
                total_pago_reserva += tarifa.getTasaDiurno()
            
        
        periodo_nocturno2 = list(range(18, 24))
        if hora_actual in periodo_nocturno2:
            total_pago_reserva += tarifa.getTasaNocturno()
    
    
        fecha_revision = fecha_revision.replace(hour = hora_siguiente_DT.hour, minute = hora_siguiente_DT.minute)
        if fecha_revision.hour == 0:
            fecha_revision = fecha_revision + timedelta(days = 1)
            
        print("total acumulado: ", total_pago_reserva)
        print("nueva fecha y hora siguiente: ", fecha_revision, hora_siguiente)
    
    return total_pago_reserva
        
    
    
if __name__== "__main__":
    main()
