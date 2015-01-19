'''
Created on 12/1/2015

@author: Iranid
'''
from datetime import datetime, timedelta,date
from tarifa import Tarifa
import sys
#from django.forms.formsets import TOTAL_FORM_COUNT

def main():
    fechaEntrada, fechaSalida, tasaDiurna, tasaNocturna = parseArg(sys.argv)
    
    try:
        fechaEntrada = datetime.strptime(fechaEntrada, "%Y-%m-%d %H:%M")
    
    except Exception as e1:
        print("Fecha de entrada inválida")
        sys.exit("El programa no puede continuar")
    
    try:
        fechaSalida = datetime.strptime(fechaSalida, "%Y-%m-%d %H:%M")
    
    except Exception as e2:
        print("Fecha de salida inválida")
        sys.exit("El programa no puede continuar")
    
    if tasaDiurna < 0:
        print("El monto de la tasa diurna no es válido")
        sys.exit()
        
    if tasaNocturna < 0:
        print("El monto de la tasa nocturna no es válido")
        sys.exit()
    
    tarifa = Tarifa(tasaDiurna, tasaNocturna)
    
    montoTotal = calculoMontoReserva(fechaEntrada, fechaSalida, tarifa)
    print("El monto total a pagar por la reserva es: ", montoTotal)
    
   
def parseArg(args):
    msg = "Error usando los argumentos de entrada: \nreservacion <fecha_entrada>, <fecha_salida>, <tasa_diurna>, <tasa_nocturna>"
    if len(args) != 5:
        print(msg)
        sys.exit(1)
    return args[1], args[2], float(args[3]), float(args[4])
    

def calculoMontoReserva(fechaEntrada, fechaSalida,tarifa):
    
    totalPagoReserva = 0
    
    #Determina si fecha de entrada es mayor a la fecha de entrada
    restaDias = fechaSalida - fechaEntrada
    
    assert(fechaSalida > fechaEntrada) ,"La fecha de entrada es mayor que la fecha de salida"
        
    assert(restaDias.total_seconds() >=(15*60) and restaDias.total_seconds() <= (72*60*60)), \
           "La reservación no cumple los límites de tiempo inferior y superior"
    
    masTasa = max(tarifa.getTasaDiurno(), tarifa.getTasaNocturno())
    
    fechaRevision = fechaEntrada
    while fechaRevision < fechaSalida:
        
        horaActual = fechaRevision.hour
        horaSiguiente = (horaActual + 1) % 24 
        horaSiguienteDT = fechaRevision.replace(hour = horaSiguiente) 
        
        if horaSiguienteDT > fechaSalida:
            horaSiguienteDT = fechaSalida
            horaSiguiente = horaSiguienteDT.hour
        print("\n")    
        print("hora actual y siguiente: ", horaActual, horaSiguiente)  
        print("rango analizado: ", fechaRevision.strftime("%H:%M"), " - ", horaSiguienteDT.strftime("%H:%M"))    
        
        periodoNocturno1 = list(range(0,6))
        if horaActual in periodoNocturno1:
            if horaSiguiente == 6 and horaSiguienteDT.minute != 0:
                totalPagoReserva += masTasa
            else:
                totalPagoReserva += tarifa.getTasaNocturno()
            
    
        
        periodoDiurno = list(range(6,18))
        if horaActual in periodoDiurno:
            if horaSiguiente == 18 and horaSiguienteDT.minute != 0:
                totalPagoReserva += masTasa
            else:
                totalPagoReserva += tarifa.getTasaDiurno()
            
        
        periodoNocturno2 = list(range(18, 24))
        if horaActual in periodoNocturno2:
            totalPagoReserva += tarifa.getTasaNocturno()
    
    
        fechaRevision = fechaRevision.replace(hour = horaSiguienteDT.hour, minute = horaSiguienteDT.minute)
        if fechaRevision.hour == 0:
            fechaRevision = fechaRevision + timedelta(days = 1)
            
        print("total acumulado: ", totalPagoReserva)
        print("nueva fecha y hora siguiente: ", fechaRevision, horaSiguiente)
    
    return totalPagoReserva
        
    
    
if __name__== "__main__":
    main()
