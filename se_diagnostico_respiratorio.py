from experta import Fact, KnowledgeEngine, Rule, MATCH, TEST, AS
from complementos_funcionalidades import alarmas


class Sintomas(Fact):
    """Diagnostico del Paciente"""
    pass


class Examenes(Fact):
    """Diagnostico del Paciente"""
    pass


class FactoresRiesgo(Fact):
    """Diagnostico del Paciente"""
    pass


class EvaluacionClinica(KnowledgeEngine):
    def __init__(self):
        super().__init__()
        self.senales_alarma = []
        self.resultados_diagnostico = {}
        self.datos_paciente = {}
        self.titulo_datos_paciente = {}

    def ejecutar_reglas(self, datos):
        self.declare(Sintomas(oxg=datos['sat_oxg']))
        self.declare(Sintomas(fiebre=datos['temperatura']), Sintomas(tos=datos['tos']), Examenes(pcr=datos['pcr']))
        self.declare(Examenes(radiografia=datos['radiografia']))
        self.declare(Sintomas(tos=datos['tos']), Sintomas(fiebre=datos['temperatura']), Examenes(pcr=datos['pcr']))
        self.declare(Sintomas(frec_resp=datos['frec_resp']), FactoresRiesgo(edad=datos['edad']))
        self.declare(Sintomas(dolor_pecho=datos['dolor_pecho']), Sintomas(tos=datos['tos']))
        self.declare(FactoresRiesgo(edad=datos['edad']), FactoresRiesgo(comorbilidad=datos['comorbilidad']))
        self.declare(Examenes(radiografia=datos['radiografia']), Examenes(pcr=datos['pcr']))
        self.declare(FactoresRiesgo(expo_reciente=datos['exp_reciente']), Sintomas(fiebre=datos['temperatura']))
        self.declare(Sintomas(oxg=datos['sat_oxg']))
        self.declare(FactoresRiesgo(comorbilidad=datos['comorbilidad']), Sintomas(fiebre=datos['temperatura']))
        self.declare(Examenes(pcr=datos['pcr']), Sintomas(tos=datos['tos']))
        self.declare(Examenes(radiografia=datos['radiografia']), Sintomas(fiebre=datos['temperatura']))
        self.declare(Sintomas(frec_resp=datos['frec_resp']))
        self.declare(Sintomas(dolor_pecho=datos['dolor_pecho']), Sintomas(oxg=datos['sat_oxg']))
        self.declare(FactoresRiesgo(edad=datos['edad']))
        self.declare(Examenes(pcr=datos['pcr']))
        self.declare(Sintomas(duracion_tos=datos['duracion_tos']))
        self.declare(Sintomas(fiebre=datos['temperatura']), Examenes(pcr=datos['pcr']))
        if datos['exp_reciente'] == 'sí' and 'tipo_expo' in datos:
            self.declare(FactoresRiesgo(expo_reciente_tipo=datos['tipo_expo']))
        self.declare(Examenes(radiografia=datos['cambio_radiografia']), Examenes(radiografia_tiempo=datos['tiempo_cambio_radiografia']))
        self.declare(Sintomas(oxg=datos['sat_oxg']), Sintomas(sintomas=datos['sintomas']))
        self.declare(Sintomas(tos=datos['tos']), Sintomas(fiebre=datos['temperatura']))
        self.declare(FactoresRiesgo(comorbilidad=datos['comorbilidad']), FactoresRiesgo(edad=datos['edad']), Examenes(pcr=datos['pcr']))
        self.declare(Sintomas(dolor_pecho=datos['dolor_pecho']))
        self.declare(Sintomas(frec_resp_cambio=datos['cambio_frec_resp']), Sintomas(frec_resp_tiempo=datos['duracion_cambio_frecresp']))
        self.declare(Examenes(pcr_aumento=datos['aumento_pcr']), Examenes(pcr_tiempo_aumento=datos['tiempo_aum_pcr']))
        self.declare(Sintomas(duracion_fiebre=datos['duracion_fiebre']))
        self.declare(FactoresRiesgo(expo_reciente=datos['exp_reciente']), Examenes(radiografia=datos['radiografia']))
        self.declare(Fact(activar=1))
        self.run()

        return self.resultados_diagnostico, self.datos_paciente, self.titulo_datos_paciente

    @Rule(Sintomas(oxg=MATCH.sat_oxg), TEST(lambda sat_oxg: sat_oxg < 92), salience=30)
    def saturacion_oxigeno(self, sat_oxg): #Regla N°1
        resultado = 'Hipoxemia (bajo nivel de oxígeno en la sangre)'
        recomendacion = 'Derivar a Urgencias para evaluación y administración de oxígeno'
        self.resultados_diagnostico['R01'] = [resultado, recomendacion]
        self.senales_alarma.append('R01')
        self.datos_paciente.setdefault('oxigeno', f'{sat_oxg}%')
        self.titulo_datos_paciente.setdefault('oxigeno', 'Saturación de O2')

    @Rule(Sintomas(fiebre=MATCH.fiebre), AS.tosp << Sintomas(tos='tos productiva'), Examenes(pcr=MATCH.pcr),
          TEST(lambda fiebre, pcr: fiebre >= 38.5 and pcr >= 50), salience=29)
    def sospecha_neumonia(self, fiebre, tosp, pcr): #Regla N°2
        resultado = 'Probable infección respiratoria bacteriana (neumonía)'
        recomendacion = 'Evaluación médica inmediata para confirmación diagnóstica (radiografía de tórax, examen físico) e inicio de antibióticos según indicación médica'
        self.resultados_diagnostico['R02'] = [resultado, recomendacion]
        self.datos_paciente.setdefault('fiebre', f'{fiebre} °C')
        self.datos_paciente.setdefault('tos', tosp['tos'])
        self.datos_paciente.setdefault('pcr', f'{pcr} mg/L')
        self.titulo_datos_paciente.setdefault('fiebre', 'Fiebre')
        self.titulo_datos_paciente.setdefault('tos', tosp['Tos'])
        self.titulo_datos_paciente.setdefault('pcr', 'Proteína C Reactiva')

    @Rule(AS.rad << Examenes(radiografia='condensación'), salience=28)
    def resultados_radiografia(self, rad): #Regla N°3
        resultado = 'Sospecha de neumonía'
        recomendacion = 'Derivar a Urgencias si presenta signos de gravedad. Mientras tanto, mantener reposo, hidratación adecuada y control de fiebre. No automedicarse'
        self.resultados_diagnostico['R03'] = [resultado, recomendacion]
        self.datos_paciente.setdefault('radiografia', rad['radiografia'])
        self.titulo_datos_paciente.setdefault('radiografia', 'Radiografía')

    @Rule(AS.tosp << Sintomas(tos='tos seca'), Sintomas(fiebre=MATCH.fiebre), Examenes(pcr=MATCH.pcr),
          TEST(lambda fiebre, pcr: fiebre < 38 and pcr < 10), salience=27)
    def resfriado(self, tosp, fiebre, pcr): #Regla N°4
        resultado = 'Resfriado probable'
        recomendacion = 'Reposo, hidratación, control sintomático y sin antibióticos'
        self.resultados_diagnostico['R04'] = [resultado, recomendacion]
        self.datos_paciente.setdefault('tos', tosp['tos'])
        self.datos_paciente.setdefault('fiebre', f'{fiebre} °C')
        self.datos_paciente.setdefault('pcr', f'{pcr} mg/L')
        self.titulo_datos_paciente.setdefault('tos', 'Tos')
        self.titulo_datos_paciente.setdefault('fiebre', 'Fiebre')
        self.titulo_datos_paciente.setdefault('pcr', 'Proteína C Reactiva')

    @Rule(Sintomas(frec_resp=MATCH.frec_resp), FactoresRiesgo(edad=MATCH.edad),
          TEST(lambda frec_resp, edad: frec_resp > 24 and 20 <= edad <= 64), salience=26)
    def resultados_frecuencia_respiratoria(self, frec_resp, edad): #Regla N°5
        resultado = 'Aquipnea (signo de posible dificultad respiratoria)'
        recomendacion = 'Derivar a Urgencias si se asocia a hipoxemia o fiebre alta'
        self.resultados_diagnostico['R05'] = [resultado, recomendacion]
        self.datos_paciente.setdefault('frec_resp', f'{frec_resp} rpm')
        self.datos_paciente.setdefault('edad', f'{edad} años')
        self.titulo_datos_paciente.setdefault('frec_resp', 'Frecuencia respiratoria')
        self.titulo_datos_paciente.setdefault('edad', 'Edad')

    @Rule(AS.dolorpecho << Sintomas(dolor_pecho='sí'), AS.tosp << Sintomas(tos='tos productiva'), salience=25)
    def resultados_sintomas(self, dolorpecho, tosp): #Regla N°6
        resultado = 'Descartar neumonía u otras complicaciones (pleuritis, derrame pleural, absceso pulmonar).'
        recomendacion = 'Derivar a Urgencias si hay fiebre, dificultad respiratoria o dolor torácico intenso.'
        self.resultados_diagnostico['R06'] = [resultado, recomendacion]
        self.datos_paciente.setdefault('dolorpecho', dolorpecho['dolor_pecho'])
        self.datos_paciente.setdefault('tos', tosp['tos'])
        self.titulo_datos_paciente.setdefault('dolorpecho', 'Dolor en el Pecho')
        self.titulo_datos_paciente.setdefault('tos', 'Tos')

    @Rule(FactoresRiesgo(edad=MATCH.edad), FactoresRiesgo(comorbilidad=MATCH.comb),
          TEST(lambda edad, comb: edad >= 65 and comb >= 1), salience=24)
    def resultados_factores_riesgo(self, edad, comb): #Regla N°7
        resultado = 'Mayor riesgo de evolución desfavorable ante infección respiratoria'
        recomendacion = 'Derivar precozmente a Urgencias o valoración médica prioritaria, aun si los síntomas son leves. Mantener vigilancia estrecha, hidratación y control de temperatura'
        self.resultados_diagnostico['R07'] = [resultado, recomendacion]
        self.datos_paciente.setdefault('edad', f'{edad} años')
        self.datos_paciente.setdefault('comb', comb)
        self.titulo_datos_paciente.setdefault('edad', 'Edad')
        self.titulo_datos_paciente.setdefault('comb', 'Comorbilidades')

    @Rule(AS.rad << Examenes(radiografia='infiltrado'), Examenes(pcr=MATCH.pcr), TEST(lambda pcr: pcr >= 30), salience=23)
    def sospecha_neumonia_2(self, rad, pcr): #Regla N°8
        resultado = 'Neumonía posible'
        recomendacion = 'Derivar para evaluación médica y confirmación diagnóstica. Mantener hidratación, reposo y control de fiebre.'
        self.resultados_diagnostico['R08'] = [resultado, recomendacion]
        self.datos_paciente.setdefault('radiografia', rad['radiografia'])
        self.datos_paciente.setdefault('pcr', f'{pcr} mg/L')
        self.titulo_datos_paciente.setdefault('radiografia', 'Radiografía')
        self.titulo_datos_paciente.setdefault('pcr', 'Proteína C Reactiva')

    @Rule(AS.exprec << FactoresRiesgo(expo_reciente='sí'), Sintomas(fiebre=MATCH.fiebre), TEST(lambda fiebre: fiebre >= 38), salience=22)
    def pruebas_virulogicas(self, exprec, fiebre): #Regla N°9
        resultado = 'Sospecha de infección respiratoria viral'
        recomendacion = 'Considerar pruebas virológicas (influenza, SARS-CoV-2 u otras). Indicar aislamiento preventivo y manejo sintomático mientras se confirman los resultados.'
        self.resultados_diagnostico['R09'] = [resultado, recomendacion]
        self.datos_paciente.setdefault('expo_reciente', exprec['expo_reciente'])
        self.datos_paciente.setdefault('fiebre', f'{fiebre} °C')
        self.titulo_datos_paciente.setdefault('expo_reciente', 'Exposición reciente')
        self.titulo_datos_paciente.setdefault('fiebre', 'Fiebre')

    @Rule(Sintomas(oxg=MATCH.sat_oxg), TEST(lambda sat_oxg: 92 <= sat_oxg <= 94), salience=21)
    def saturacion_oxigeno_2(self, sat_oxg): #Regla N°10
        resultado = 'Hipoxemia leve'
        recomendacion = 'Indicar oximetría domiciliaria y seguimiento clínico en 48 horas'
        self.resultados_diagnostico['R10'] = [resultado, recomendacion]
        self.datos_paciente.setdefault('oxigeno', f'{sat_oxg}%')
        self.titulo_datos_paciente.setdefault('oxigeno', 'Saturación de O2')

    @Rule(FactoresRiesgo(comorbilidad=MATCH.comb), Sintomas(fiebre=MATCH.fiebre),
          TEST(lambda comb, fiebre: comb >= 2 and fiebre >= 38), salience=20)
    def resultados_evaluacion(self, comb, fiebre): #Regla N°11
        resultado = 'Alto riesgo clínico'
        recomendacion = 'Bajo umbral de derivación a Urgencias. Evaluar de forma prioritaria, con control de signos vitales y oximetría'
        self.resultados_diagnostico['R11'] = [resultado, recomendacion]
        self.datos_paciente.setdefault('comb', comb)
        self.datos_paciente.setdefault('fiebre', f'{fiebre} °C')
        self.titulo_datos_paciente.setdefault('comb', 'Comorbilidades')
        self.titulo_datos_paciente.setdefault('fiebre', 'Fiebre')

    @Rule(Examenes(pcr=MATCH.pcr), AS.tosp << Sintomas(tos='tos productiva'), TEST(lambda pcr: 10 <= pcr <= 29), salience=19)
    def sospecha_bronquitis(self, pcr, tosp): #Regla N°12
        resultado = 'Posible bronquitis aguda'
        recomendacion = 'Tratamiento sintomático y control evolutivo'
        self.resultados_diagnostico['R12'] = [resultado, recomendacion]
        self.datos_paciente.setdefault('pcr', f'{pcr} mg/L')
        self.datos_paciente.setdefault('tos', tosp['tos'])
        self.titulo_datos_paciente.setdefault('pcr', 'Proteína C Reactiva')
        self.titulo_datos_paciente.setdefault('tos', 'Tos')

    @Rule(AS.rad << Examenes(radiografia='normal'), Sintomas(fiebre=MATCH.fiebre), TEST(lambda fiebre: fiebre < 38), salience=18)
    def cuadro_respiratorio(self, rad, fiebre): #Regla N°13
        resultado = 'Cuadro respiratorio leve (viral o inespecífico)'
        recomendacion = 'Manejo sintomático: reposo, hidratación, control de fiebre o malestar con paracetamol o ibuprofeno si es necesario'
        self.resultados_diagnostico['R13'] = [resultado, recomendacion]
        self.datos_paciente.setdefault('radiografia', rad['radiografia'])
        self.datos_paciente.setdefault('fiebre', f'{fiebre} °C')
        self.titulo_datos_paciente.setdefault('radiografia', 'Radiografía')
        self.titulo_datos_paciente.setdefault('fiebre', 'Fiebre')

    @Rule(Sintomas(frec_resp=MATCH.frec_resp), TEST(lambda frec_resp: frec_resp >= 30), salience=17)
    def resultados_frecuencia_respiratoria_2(self, frec_resp): #Regla N°14
        resultado = 'Dificultad respiratoria severa'
        recomendacion = 'Derivar de inmediato a Urgencias para valoración y manejo. Controlar SatO₂ y signos vitales durante el traslado si es posible'
        self.resultados_diagnostico['R14'] = [resultado, recomendacion]
        self.senales_alarma.append('R14')
        self.datos_paciente.setdefault('frec_resp', f'{frec_resp} rpm')
        self.titulo_datos_paciente.setdefault('frec_resp', 'Frecuencia respiratoria')

    @Rule(AS.dolorpecho << Sintomas(dolor_pecho='sí'), Sintomas(oxg=MATCH.sat_oxg), TEST(lambda sat_oxg: sat_oxg < 95), salience=16)
    def resultados_sintomas_2(self, dolorpecho, sat_oxg): #Regla N°15
        resultado = 'Posible compromiso respiratorio o cardiovascular'
        recomendacion = 'Solicitar ECG y enzimas cardíacas (troponina, CK-MB) para descartar origen cardíaco. Derivar si sospecha de origen cardíaco'
        self.resultados_diagnostico['R15'] = [resultado, recomendacion]
        self.datos_paciente.setdefault('dolorpecho', dolorpecho['dolor_pecho'])
        self.datos_paciente.setdefault('oxigeno', f'{sat_oxg}%')
        self.titulo_datos_paciente.setdefault('dolorpecho', 'Dolor en el pecho')
        self.titulo_datos_paciente.setdefault('oxigeno', 'Saturación de O2')

    @Rule(FactoresRiesgo(edad=MATCH.edad), TEST(lambda edad: edad < 12), salience=15)
    def ajustar_umbrales_frec_resp(self, edad): #Regla N°16
        resultado = 'Aplicar umbrales pediátricos de frecuencia respiratoria'
        recomendacion = ('Ajustar umbrales de frecuencia respiratoria según edad:\n'
                         '< 2 meses → > 60 rpm\n2–12 meses → > 50 rpm\n1–5 años → > 40 rpm\n6–11 años → > 30 rpm\n'
                         'Derivar a Urgencias si frec. resp. supera el umbral o hay signos de dificultad respiratoria')
        self.resultados_diagnostico['R16'] = [resultado, recomendacion]
        self.datos_paciente.setdefault('edad', f'{edad} años')
        self.titulo_datos_paciente.setdefault('edad', 'Edad')

    @Rule(Examenes(pcr=MATCH.pcr), TEST(lambda pcr: pcr >= 100), salience=14)
    def resultados_examenes(self, pcr): #Regla N°17
        resultado = 'Inflamación/infección severa (alta sospecha bacteriana)'
        recomendacion = ('Derivar de inmediato a Urgencias para evaluación médica urgente y manejo hospitalario. '
                         'Requiere estudios complementarios (radiografía, hemograma, cultivo) y posible inicio de antibióticos intravenosos')
        self.resultados_diagnostico['R17'] = [resultado, recomendacion]
        self.senales_alarma.append('R17')
        self.datos_paciente.setdefault('pcr', f'{pcr} mg/L')
        self.titulo_datos_paciente.setdefault('pcr', 'Proteína C Reactiva')

    @Rule(Sintomas(duracion_tos=MATCH.duracion_tos), TEST(lambda duracion_tos: duracion_tos > 21), salience=13)
    def descartar_causas_cronicas(self, duracion_tos): #Regla N°18
        resultado = 'Sospecha de tuberculosis u otras causas crónicas (bronquitis crónica, asma, EPOC, reflujo, etc.)'
        recomendacion = ('Solicitar baciloscopía o prueba de tuberculosis según protocolo local. '
                         'Considerar radiografía de tórax y evaluación médica especializada. '
                         'Mantener medidas de aislamiento respiratorio hasta descartar TB')
        self.resultados_diagnostico['R18'] = [resultado, recomendacion]
        self.datos_paciente.setdefault('duracion_tos', f'{duracion_tos} días')
        self.titulo_datos_paciente.setdefault('duracion_tos', 'Duración de la tos')

    @Rule(Sintomas(fiebre=MATCH.fiebre), Examenes(pcr=MATCH.pcr),
          TEST(lambda fiebre, pcr: 37.5 <= fiebre <= 38.4 and 10 <= pcr <= 20), salience=12)
    def monitorizar(self, fiebre, pcr): #Regla N°19
        resultado = 'Cuadro leve, posible infección viral o en evolución'
        recomendacion = 'Monitorizar evolución durante 48–72 horas. Indicar hidratación, reposo y control de fiebre. Reevaluar evolución'
        self.resultados_diagnostico['R19'] = [resultado, recomendacion]
        self.datos_paciente.setdefault('fiebre', f'{fiebre} °C')
        self.datos_paciente.setdefault('pcr', f'{pcr} mg/L')
        self.titulo_datos_paciente.setdefault('fiebre', 'Fiebre')
        self.titulo_datos_paciente.setdefault('pcr', 'Proteína C Reactiva')

    @Rule(AS.exprec << FactoresRiesgo(expo_reciente_tipo='brote comunitario'), salience=11)
    def realizar_pruebas(self, exprec): #Regla N°20
        resultado = 'Riesgo de infección respiratoria contagiosa o epidémica'
        recomendacion = 'Solicitar pruebas etiológicas, aislamiento preventivo y seguimiento según resultados'
        self.resultados_diagnostico['R20'] = [resultado, recomendacion]
        self.datos_paciente.setdefault('expo_reciente_tipo', exprec['expo_reciente_tipo'])
        self.titulo_datos_paciente.setdefault('expo_reciente_tipo', 'Tipo de exposición')

    @Rule(AS.rad << Examenes(radiografia='Empeoramiento'), Examenes(radiografia_tiempo=MATCH.rad_tiempo),
          TEST(lambda rad_tiempo: 48 <= rad_tiempo <= 72), salience=10)
    def revalorar_medicamentos(self, rad, rad_tiempo): #Regla N°21
        resultado = 'Falta de respuesta o progresión de la infección pulmonar'
        recomendacion = ('Reevaluar antibióticos, descartar complicaciones y ajustar manejo'
                         'Considerar nuevos estudios microbiológicos y evaluación por especialista')
        self.resultados_diagnostico['R21'] = [resultado, recomendacion]
        self.datos_paciente.setdefault('radiografia', rad['radiografia'])
        self.datos_paciente.setdefault('rad_tiempo', f'{rad_tiempo} horas')
        self.titulo_datos_paciente.setdefault('radiografia', 'Radiografía')
        self.titulo_datos_paciente.setdefault('rad_tiempo', 'Tiempo de Empeoramiento')

    @Rule(Sintomas(oxg=MATCH.sat_oxg), AS.sints << Sintomas(sintomas='leves'),
          TEST(lambda sat_oxg: sat_oxg >= 96), salience=9)
    def cuadro_respiratorio_sincompromiso(self, sat_oxg, sints): #Regla N°22
        resultado = 'Cuadro leve, sin hipoxemia'
        recomendacion = 'Manejo domiciliario con control de síntomas (hidratación, antitérmicos si fiebre).'
        self.resultados_diagnostico['R22'] = [resultado, recomendacion]
        self.datos_paciente.setdefault('oxigeno', f'{sat_oxg}%')
        self.datos_paciente.setdefault('sintomas', sints['sintomas'])
        self.titulo_datos_paciente.setdefault('oxigeno', 'Saturación de O2')
        self.titulo_datos_paciente.setdefault('sintomas', 'Sintomas')

    @Rule(AS.tosp << Sintomas(tos='tos espesa'), Sintomas(fiebre=MATCH.fiebre),
          TEST(lambda fiebre: fiebre > 38), salience=8)
    def valorar_bacteriana(self, tosp, fiebre): #Regla N°23
        resultado = 'Posible etiología bacteriana'
        recomendacion = 'Valorar causa bacteriana; posible inicio antibiótico según evolución'
        self.resultados_diagnostico['R23'] = [resultado, recomendacion]
        self.datos_paciente.setdefault('tos', tosp['tos'])
        self.datos_paciente.setdefault('fiebre', f'{fiebre} °C')
        self.titulo_datos_paciente.setdefault('tos', 'Tos')
        self.titulo_datos_paciente.setdefault('fiebre', 'Fiebre')

    @Rule(FactoresRiesgo(comorbilidad=MATCH.comb), FactoresRiesgo(edad=MATCH.edad), Examenes(pcr=MATCH.pcr),
          TEST(lambda comb, edad, pcr: comb == 0 and edad < 50 and pcr < 10), salience=7)
    def posible_resfriado(self, comb, edad, pcr): #Regla N°24
        resultado = 'Resfriado probable'
        recomendacion = 'Manejo sintomático (hidratación, reposo, analgésicos/antitérmicos si es necesario).'
        self.resultados_diagnostico['R24'] = [resultado, recomendacion]
        self.datos_paciente.setdefault('comb', comb)
        self.datos_paciente.setdefault('edad', f'{edad} años')
        self.datos_paciente.setdefault('pcr', f'{pcr} mg/L')
        self.titulo_datos_paciente.setdefault('comb', 'Comorbilidades')
        self.titulo_datos_paciente.setdefault('edad', 'Edad')
        self.titulo_datos_paciente.setdefault('pcr', 'Proteína C Reactiva')

    @Rule(AS.dolorpecho << Sintomas(dolor_pecho='severo'), salience=6)
    def descartar_causas_graves(self, dolorpecho): #Regla N°25
        resultado = 'Dolor torácico severo'
        recomendacion = ('Descartar causas graves (TEP, neumotórax). '
                         'Derivar a Urgencias para evaluación inmediata y estudios complementarios (ECG, Rx, dímero D, TAC según caso)')
        self.resultados_diagnostico['R25'] = [resultado, recomendacion]
        self.senales_alarma.append('R25')
        self.datos_paciente.setdefault('dolorpecho', dolorpecho['dolor_pecho'])
        self.titulo_datos_paciente.setdefault('dolorpecho', 'Dolor de pecho')

    @Rule(AS.frecresp_c << Sintomas(frec_resp_cambio='normal'), Sintomas(frec_resp_tiempo=MATCH.tiempo),
          TEST(lambda tiempo: tiempo <= 48), salience=5)
    def cambio_frec_resp(self, frecresp_c, tiempo): #Regla N°26
        resultado = 'Evolución favorable'
        recomendacion = 'Continuar manejo actual y seguimiento clínico'
        self.resultados_diagnostico['R26'] = [resultado, recomendacion]
        self.datos_paciente.setdefault('frecresp_c', frecresp_c['frec_resp_cambio'])
        self.datos_paciente.setdefault('frecresp_c_tiempo', f'{tiempo} horas')
        self.titulo_datos_paciente.setdefault('frecresp_c', 'Cambio en la frecuencia respiratoria')
        self.titulo_datos_paciente.setdefault('frecresp_c_tiempo', 'Tiempo del cambio')

    @Rule(Examenes(pcr_aumento=MATCH.pcr_aum), Examenes(pcr_tiempo_aumento=MATCH.tiempo),
          TEST(lambda pcr_aum, tiempo: pcr_aum > 50 and tiempo <= 48), salience=4)
    def aumento_pcr(self, pcr_aum, tiempo): #Regla N°27
        resultado = 'Empeoramiento o respuesta inadecuada al tratamiento'
        recomendacion = 'Escalar evaluación: repetir examen clínico, considerar estudios de imagen o cultivo. Revalorar necesidad de antibióticos o derivación'
        self.resultados_diagnostico['R27'] = [resultado, recomendacion]
        self.datos_paciente.setdefault('pcr_aum', f'{pcr_aum}%')
        self.datos_paciente.setdefault('pcr_aum_tiempo', f'{tiempo} horas')
        self.titulo_datos_paciente.setdefault('pcr_aum', 'Aumento de la Proteína C Reactiva')
        self.titulo_datos_paciente.setdefault('pcr_aum_tiempo', 'Tiempo del aumento del PCR')

    @Rule(Sintomas(duracion_fiebre=MATCH.tiempo_fiebre), TEST(lambda tiempo_fiebre: tiempo_fiebre > 5), salience=3)
    def fiebre_persistente(self, tiempo_fiebre): #Regla N°28
        resultado = 'Cuadro prolongado; posible complicación o etiología alternativa'
        recomendacion = 'Ampliar estudios diagnósticos (laboratorio, imagen, cultivos según sospecha). Evaluar necesidad de derivación o ajuste terapéutico'
        self.resultados_diagnostico['R28'] = [resultado, recomendacion]
        self.datos_paciente.setdefault('duracion_fiebre', f'{tiempo_fiebre} días')
        self.titulo_datos_paciente.setdefault('duracion_fiebre', 'Duración de la fiebre')

    @Rule(AS.exprec << FactoresRiesgo(expo_reciente='no'), AS.rad << Examenes(radiografia='normal'), salience=2)
    def infeccion_viral(self, exprec, rad): #Regla N°29
        resultado = 'Probable infección viral leve'
        recomendacion = 'Manejo sintomático: reposo, hidratación, control de fiebre o malestar'
        self.resultados_diagnostico['R29'] = [resultado, recomendacion]
        self.datos_paciente.setdefault('expo_reciente', exprec['expo_reciente'])
        self.datos_paciente.setdefault('radiografia', rad['radiografia'])
        self.titulo_datos_paciente.setdefault('expo_reciente', 'Exposición reciente')
        self.titulo_datos_paciente.setdefault('radiografia', 'Radiografía')

    @Rule(Fact(senales_alarma=MATCH.num), TEST(lambda num: num > 1), salience=1)
    def multiples_alarmas(self, num): #Regla N°30
        senal_alarma = self.senales_alarma[0]
        for regla in range(1, len(self.senales_alarma)):
            senal_alarma = senal_alarma + '_' + self.senales_alarma[regla]

        resultado = alarmas[senal_alarma][0]
        recomendacion = alarmas[senal_alarma][1]
        self.resultados_diagnostico['R30'] = [resultado, recomendacion]
        self.datos_paciente.setdefault('senales_alarma', num)
        self.titulo_datos_paciente.setdefault('senales_alarma', 'Señales de Alarma')

    @Rule(Fact(activar=1), salience=0)
    def regla_aux(self):
        self.declare(Fact(senales_alarma=len(self.senales_alarma)))
