from experta import Fact
from se_diagnostico_respiratorio import EvaluacionClinica
from se_diagnostico_respiratorio import Sintomas, Examenes, FactoresRiesgo
from complementos_funcionalidades import orden_claves

motor = EvaluacionClinica()
motor.declare(Sintomas(oxg=91))
motor.declare(Sintomas(fiebre=39), Sintomas(tos='tos productiva'), Examenes(pcr=50))
motor.declare(Examenes(radiografia='condensación'))
motor.declare(Sintomas(tos='tos seca'), Sintomas(fiebre=37), Examenes(pcr=9))
motor.declare(Sintomas(frec_resp=25), FactoresRiesgo(edad=25))
motor.declare(Sintomas(dolor_pecho='sí'), Sintomas(tos='tos productiva'))
motor.declare(FactoresRiesgo(edad=65), FactoresRiesgo(comorbilidad=1))
motor.declare(Examenes(radiografia='infiltrado'), Examenes(pcr=30))
motor.declare(FactoresRiesgo(expo_reciente='sí'), Sintomas(fiebre=38))
motor.declare(Sintomas(oxg=93))
motor.declare(FactoresRiesgo(comorbilidad=2), Sintomas(fiebre=38))
motor.declare(Examenes(pcr=15), Sintomas(tos='tos productiva'))
motor.declare(Examenes(radiografia='normal'), Sintomas(fiebre=37))
motor.declare(Sintomas(frec_resp=30))
motor.declare(Sintomas(dolor_pecho='sí'), Sintomas(oxg=94))
motor.declare(FactoresRiesgo(edad=11))
motor.declare(Examenes(pcr=100))
motor.declare(Sintomas(duracion_tos=22))
motor.declare(Sintomas(fiebre=38), Examenes(pcr=15))
motor.declare(FactoresRiesgo(expo_reciente_tipo='brote comunitario'))
motor.declare(Examenes(radiografia='empeoramiento'), Examenes(radiografia_tiempo=55))
motor.declare(Sintomas(oxg=96), Sintomas(sintomas='leves'))
motor.declare(Sintomas(tos='tos espesa'), Sintomas(fiebre=38.5))
motor.declare(FactoresRiesgo(comorbilidad=0), FactoresRiesgo(edad=45), Examenes(pcr=9))
motor.declare(Sintomas(dolor_pecho='severo'))
motor.declare(Sintomas(frec_resp_cambio='normal'), Sintomas(frec_resp_tiempo=36))
motor.declare(Examenes(pcr_aumento=51), Examenes(pcr_tiempo_aumento=45))
motor.declare(Sintomas(duracion_fiebre=6))
motor.declare(FactoresRiesgo(expo_reciente='no'), Examenes(radiografia='normal'))
motor.declare(Fact(activar=1))
motor.run()

resultados = motor.resultados_diagnostico
datos_paciente = motor.datos_paciente
"""
for regla, contenido in resultados.items():
    print(f'Regla: {regla}\nResultado: {contenido[0]}\nRecomendación: {contenido[1]}\n')

contador = 1
for clave, valor in datos_paciente.items():
    print(f'{contador}. Clave: {clave}          Valor: {valor}')
    contador += 1
print("")
datos_ordenados = {clave: datos_paciente[clave] for clave in orden_claves if clave in datos_paciente}
contador = 1
for clave, valor in datos_ordenados.items():
    print(f'{contador}. Clave: {clave}          Valor: {valor}')
    contador += 1
"""
