'''
Created on 12/1/2015

@author: Iranid
'''
from datetime import date,datetime, time, timedelta
import sys 
from tarifa import Tarifa
from django.forms.formsets import TOTAL_FORM_COUNT

def main():
    '''El cableado de datos es temporal '''
    parametro_fecha_entrada = "2014-01-01 16:30"
    parametro_fecha_salida = "2014-02-01 16:35"
    parametro_tasa_diurna = 45
    parametro_tasa_nocturna = 35
    
    try:
        fecha_entrada = datetime.strptime(parametro_fecha_entrada, "%Y-%m-%d %H:%M")
    
    except Exception as e1:
        print("Fecha de entrada inv�lida")
        sys.exit("El programa no puede continuar")
    
    try:
        fecha_salida = datetime.strptime(parametro_fecha_salida, "%Y-%m-%d %H:%M")
    
    except Exception as e2:
        print("Fecha de salida inv�lida")
        sys.exit("El programa no puede continuar")
    
    if parametro_tasa_diurna < 0:
        print("El monto de la tasa diurna no es v�lido")
        sys.exit()
        
    if parametro_tasa_nocturna < 0:
        print("El monto de la tasa nocturna no es v�lido")
        sys.exit()
    
    tarifa = Tarifa(parametro_tasa_diurna, parametro_tasa_nocturna)
    
    monto_total= calculo_monto_reserva(fecha_entrada, fecha_salida, tarifa)
    print("El monto total a pagar por la reserva es: ", monto_total)
    
    
    

def calculo_monto_reserva(fecha_entrada, fecha_salida,tarifa):
    
    total_pago_reserva = 0
    
    
    #Determina si fecha de entrada es mayor a la fecha de entrada
    restaDias = fecha_salida - fecha_entrada
    
    if restaDias.days < 0:
        print("La fecha de entrada es mayor que la fecha de salida")
        sys.exit()
        
    if restaDias.total_seconds() <(15*60) or restaDias.total_seconds() >(72*60*60):
        print("La reservaci�n no cumple los l�mites de tiempo inferior y superior")
        sys.exit()
    
    max_tasa = max(tarifa.__tasa_diurna, tarifa.__tasa_nocturna)
    
    fecha_revision = fecha_entrada
    while fecha_revision < fecha_salida:
        
        hora_actual = fecha_revision.hora
        hora_siguiente = (hora_actual + 1) % 24        
        
        periodo_nocturno1 = list(range(0,6))
        if hora_actual in periodo_nocturno1:
            if hora_siguiente == 6:
                total_pago_reserva += max_tasa
            else:
                total_pago_reserva += tarifa.__tasa_nocturna
            
    
        
        periodo_diurno = list(range(6,18))
        if hora_actual in periodo_diurno:
            if hora_siguiente == 18:
                total_pago_reserva += max_tasa
            else:
                total_pago_reserva += tarifa.__tasa_diurna
            
        
        periodo_nocturno2 = list(range(18, 24))
        if hora_actual in periodo_nocturno2:
            total_pago_reserva += tarifa.__tasa_nocturna
    
    
        fecha_revision = fecha_revision.replace(hour = hora_siguiente, minute = fecha_salida.minute)
        if fecha_revision.hour == 0:
            fecha_revision = fecha_revision + timedelta(days = 1)
    
    return total_pago_reserva
        
    
    
if __name__== "__main__":
    main()
