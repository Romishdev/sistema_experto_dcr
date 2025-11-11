from experta import Fact, KnowledgeEngine, Rule, MATCH, TEST
from señales_alarmas import alarmas


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

    @Rule(Sintomas(oxg=MATCH.sat_oxg), TEST(lambda sat_oxg: sat_oxg < 92), salience=30)
    def saturacion_oxigeno(self): #Regla N°1
        resultado = 'Hipoxemia (bajo nivel de oxígeno en la sangre)'
        recomendacion = 'Derivar a Urgencias para evaluación y administración de oxígeno'

        self.senales_alarma.append('R01')
        print("Resultado: ", resultado)
        print("Recomendacion: ", recomendacion)

    @Rule(Sintomas(fiebre=MATCH.fiebre), Sintomas(tos='tos productiva'), Examenes(pcr=MATCH.pcr),
          TEST(lambda fiebre, pcr: fiebre >= 38.5 and pcr >= 50), salience=29)
    def sospecha_neumonia(self): #Regla N°2
        resultado = 'Probable infección respiratoria bacteriana (neumonía)'
        recomendacion = 'Evaluación médica inmediata para confirmación diagnóstica (radiografía de tórax, examen físico) e inicio de antibióticos según indicación médica'
        print(resultado)
        print(recomendacion)

    @Rule(Examenes(radiografia='condensación'), salience=28)
    def resultados_radiografia(self): #Regla N°3
        resultado = 'Sospecha de neumonía'
        recomendacion = 'Derivar a Urgencias si presenta signos de gravedad. Mientras tanto, mantener reposo, hidratación adecuada y control de fiebre. No automedicarse'
        print(resultado)

    @Rule(Sintomas(tos='tos seca'), Sintomas(fiebre=MATCH.fiebre), Examenes(pcr=MATCH.pcr),
          TEST(lambda fiebre, pcr: fiebre < 38 and pcr < 10), salience=27)
    def resfriado(self): #Regla N°4
        resultado = 'Resfriado probable'
        recomendacion = 'Reposo, hidratación, control sintomático y sin antibióticos'
        print(resultado)

    @Rule(Sintomas(frec_resp=MATCH.frec_resp), FactoresRiesgo(edad=MATCH.edad),
          TEST(lambda frec_resp, edad: frec_resp > 24 and 20 <= edad <= 64), salience=26)
    def resultados_frecuencia_respiratoria(self): #Regla N°5
        resultado = 'Aquipnea (signo de posible dificultad respiratoria)'
        recomendacion = 'Derivar a Urgencias si se asocia a hipoxemia o fiebre alta'
        print(resultado)

    @Rule(Sintomas(dolor_pecho='sí'), Sintomas(tos='tos productiva'), salience=25)
    def resultados_sintomas(self): #Regla N°6
        resultado = 'Descartar neumonía u otras complicaciones (pleuritis, derrame pleural, absceso pulmonar).'
        recomendacion = 'Derivar a Urgencias si hay fiebre, dificultad respiratoria o dolor torácico intenso.'
        print(resultado)

    @Rule(FactoresRiesgo(edad=MATCH.edad), FactoresRiesgo(comorbilidad=MATCH.comb),
          TEST(lambda edad, comb: edad >= 65 and comb >= 1), salience=24)
    def resultados_factores_riesgo(self): #Regla N°7
        resultado = 'Mayor riesgo de evolución desfavorable ante infección respiratoria'
        recomendacion = 'Derivar precozmente a Urgencias o valoración médica prioritaria, aun si los síntomas son leves. Mantener vigilancia estrecha, hidratación y control de temperatura'
        print(resultado)

    @Rule(Examenes(radiografia='infiltrado'), Examenes(pcr=MATCH.pcr), TEST(lambda pcr: pcr >= 30), salience=23)
    def sospecha_neumonia_2(self): #Regla N°8
        resultado = 'Neumonía posible'
        recomendacion = 'Derivar para evaluación médica y confirmación diagnóstica. Mantener hidratación, reposo y control de fiebre.'
        print(resultado)

    @Rule(FactoresRiesgo(expo_reciente='sí'), Sintomas(fiebre=MATCH.fiebre), TEST(lambda fiebre: fiebre >= 38), salience=22)
    def pruebas_virulogicas(self): #Regla N°9
        resultado = 'Sospecha de infección respiratoria viral'
        recomendacion = 'Considerar pruebas virológicas (influenza, SARS-CoV-2 u otras). Indicar aislamiento preventivo y manejo sintomático mientras se confirman los resultados.'
        print(resultado)

    @Rule(Sintomas(oxg=MATCH.sat_oxg), TEST(lambda sat_oxg: 92 <= sat_oxg <= 94), salience=21)
    def saturacion_oxigeno_2(self): #Regla N°10
        resultado = 'Hipoxemia leve'
        recomendacion = 'Indicar oximetría domiciliaria y seguimiento clínico en 48 horas'
        print(resultado)

    @Rule(FactoresRiesgo(comorbilidad=MATCH.comb), Sintomas(fiebre=MATCH.fiebre),
          TEST(lambda comb, fiebre: comb >= 2 and fiebre >= 38), salience=20)
    def resultados_evaluacion(self): #Regla N°11
        resultado = 'Alto riesgo clínico'
        recomendacion = 'Bajo umbral de derivación a Urgencias. Evaluar de forma prioritaria, con control de signos vitales y oximetría'
        print(resultado)

    @Rule(Examenes(pcr=MATCH.pcr), Sintomas(tos='tos productiva'), TEST(lambda pcr: 10 <= pcr <= 29), salience=19)
    def sospecha_bronquitis(self): #Regla N°12
        resultado = 'Posible bronquitis aguda'
        recomendacion = 'Tratamiento sintomático y control evolutivo'
        print(resultado)

    @Rule(Examenes(radiografia='normal'), Sintomas(fiebre=MATCH.fiebre), TEST(lambda fiebre: fiebre < 38), salience=18)
    def cuadro_respiratorio(self): #Regla N°13
        resultado = 'Cuadro respiratorio leve (viral o inespecífico)'
        recomendacion = 'Manejo sintomático: reposo, hidratación, control de fiebre o malestar con paracetamol o ibuprofeno si es necesario'
        print(resultado)

    @Rule(Sintomas(frec_resp=MATCH.frec_resp), TEST(lambda frec_resp: frec_resp >= 30), salience=17)
    def resultados_frecuencia_respiratoria_2(self): #Regla N°14
        resultado = 'Dificultad respiratoria severa'
        recomendacion = 'Derivar de inmediato a Urgencias para valoración y manejo. Controlar SatO₂ y signos vitales durante el traslado si es posible'

        self.senales_alarma.append('R14')
        print(resultado)

    @Rule(Sintomas(dolor_pecho='sí'), Sintomas(oxg=MATCH.sat_oxg), TEST(lambda sat_oxg: sat_oxg < 95), salience=16)
    def resultados_sintomas_2(self): #Regla N°15
        resultado = 'Posible compromiso respiratorio o cardiovascular'
        recomendacion = 'Solicitar ECG y enzimas cardíacas (troponina, CK-MB) para descartar origen cardíaco. Derivar si sospecha de origen cardíaco'
        print(resultado)

    @Rule(FactoresRiesgo(edad=MATCH.edad), TEST(lambda edad: edad < 12), salience=15)
    def ajustar_umbrales_frec_resp(self): #Regla N°16
        resultado = 'Aplicar umbrales pediátricos de frecuencia respiratoria'
        recomendacion = ('Ajustar umbrales de frecuencia respiratoria según edad:\n'
                         '< 2 meses → > 60 rpm\n2–12 meses → > 50 rpm\n1–5 años → > 40 rpm\n6–11 años → > 30 rpm\n'
                         'Derivar a Urgencias si frec. resp. supera el umbral o hay signos de dificultad respiratoria')
        print(resultado)

    @Rule(Examenes(pcr=MATCH.pcr), TEST(lambda pcr: pcr >= 100), salience=14)
    def resultados_examenes(self): #Regla N°17
        resultado = 'Inflamación/infección severa (alta sospecha bacteriana)'
        recomendacion = ('Derivar de inmediato a Urgencias para evaluación médica urgente y manejo hospitalario. '
                         'Requiere estudios complementarios (radiografía, hemograma, cultivo) y posible inicio de antibióticos intravenosos')

        self.senales_alarma.append('R17')
        print(resultado)

    @Rule(Sintomas(duracion_tos=MATCH.duracion_tos), TEST(lambda duracion_tos: duracion_tos > 21), salience=13)
    def descartar_causas_cronicas(self): #Regla N°18
        resultado = 'Sospecha de tuberculosis u otras causas crónicas (bronquitis crónica, asma, EPOC, reflujo, etc.)'
        recomendacion = ('Solicitar baciloscopía o prueba de tuberculosis según protocolo local. '
                         'Considerar radiografía de tórax y evaluación médica especializada. '
                         'Mantener medidas de aislamiento respiratorio hasta descartar TB')
        print(resultado)

    @Rule(Sintomas(fiebre=MATCH.fiebre), Examenes(pcr=MATCH.pcr),
          TEST(lambda fiebre, pcr: 37.5 <= fiebre <= 38.4 and 10 <= pcr <= 20), salience=12)
    def monitorizar(self): #Regla N°19
        resultado = 'Cuadro leve, posible infección viral o en evolución'
        recomendacion = 'Monitorizar evolución durante 48–72 horas. Indicar hidratación, reposo y control de fiebre. Reevaluar evolución'
        print(resultado)

    @Rule(FactoresRiesgo(expo_reciente='brote comunitario'), salience=11)
    def realizar_pruebas(self): #Regla N°20
        resultado = 'Riesgo de infección respiratoria contagiosa o epidémica'
        recomendacion = 'Solicitar pruebas etiológicas, aislamiento preventivo y seguimiento según resultados'
        print(resultado)

    @Rule(Examenes(radiografia='empeora'), Examenes(radiografia_tiempo=MATCH.rad_tiempo),
          TEST(lambda rad_tiempo: 48 <= rad_tiempo <= 72), salience=10)
    def revalorar_medicamentos(self): #Regla N°21
        resultado = 'Falta de respuesta o progresión de la infección pulmonar'
        recomendacion = ('Reevaluar antibióticos, descartar complicaciones y ajustar manejo'
                         'Considerar nuevos estudios microbiológicos y evaluación por especialista')
        print(resultado)

    @Rule(Sintomas(oxg=MATCH.sat_oxg), Sintomas(sintomas='leves'),
          TEST(lambda sat_oxg: sat_oxg >= 96), salience=9)
    def cuadro_respiratorio_sincompromiso(self): #Regla N°22
        resultado = 'Cuadro leve, sin hipoxemia'
        recomendacion = 'Manejo domiciliario con control de síntomas (hidratación, antitérmicos si fiebre).'
        print(resultado)

    @Rule(Sintomas(tos='tos espesa'), Sintomas(fiebre=MATCH.fiebre),
          TEST(lambda fiebre: fiebre > 38), salience=8)
    def valorar_bacteriana(self): #Regla N°23
        resultado = 'Posible etiología bacteriana'
        recomendacion = 'Valorar causa bacteriana; posible inicio antibiótico según evolución'
        print(resultado)

    @Rule(FactoresRiesgo(comorbilidad=MATCH.comb), FactoresRiesgo(edad=MATCH.edad), Examenes(pcr=MATCH.pcr),
          TEST(lambda comb, edad, pcr: comb == 0 and edad < 50 and pcr < 10), salience=7)
    def posible_resfriado(self): #Regla N°24
        resultado = 'Resfriado probable'
        recomendacion = 'Manejo sintomático (hidratación, reposo, analgésicos/antitérmicos si es necesario).'
        print(resultado)

    @Rule(Sintomas(dolor_pecho='severo'), salience=6)
    def descartar_causas_graves(self): #Regla N°25
        resultado = 'Dolor torácico severo'
        recomendacion = ('Descartar causas graves (TEP, neumotórax). '
                         'Derivar a Urgencias para evaluación inmediata y estudios complementarios (ECG, Rx, dímero D, TAC según caso)')
        self.senales_alarma.append('R25')
        print(resultado)

    @Rule(Sintomas(frec_resp_cambio='normal'), Sintomas(frec_resp_tiempo=MATCH.tiempo),
          TEST(lambda tiempo: tiempo <= 48), salience=5)
    def cambio_frec_resp(self): #Regla N°26
        resultado = 'Evolución favorable'
        recomendacion = 'Continuar manejo actual y seguimiento clínico'
        print(resultado)

    @Rule(Examenes(pcr_aumento=MATCH.pcr_aum), Examenes(pcr_tiempo_aumento=MATCH.tiempo),
          TEST(lambda pcr_aum, tiempo: pcr_aum > 50 and tiempo <= 48), salience=4)
    def aumento_pcr(self): #Regla N°27
        resultado = 'Empeoramiento o respuesta inadecuada al tratamiento'
        recomendacion = 'Escalar evaluación: repetir examen clínico, considerar estudios de imagen o cultivo. Revalorar necesidad de antibióticos o derivación'
        print(resultado)

    @Rule(Sintomas(duracion_fiebre=MATCH.tiempo_fiebre), TEST(lambda tiempo_fiebre: tiempo_fiebre > 5), salience=3)
    def fiebre_persistente(self): #Regla N°28
        resultado = 'Cuadro prolongado; posible complicación o etiología alternativa'
        recomendacion = 'Ampliar estudios diagnósticos (laboratorio, imagen, cultivos según sospecha). Evaluar necesidad de derivación o ajuste terapéutico'
        print(resultado)

    @Rule(FactoresRiesgo(expo_reciente='no'), Examenes(radiografia='normal'), salience=2)
    def infeccion_viral(self): #Regla N°29
        resultado = 'Probable infección viral leve'
        recomendacion = 'Manejo sintomático: reposo, hidratación, control de fiebre o malestar'
        print(resultado)

    @Rule(Fact(senales_alarma=MATCH.num), TEST(lambda num: num > 1), salience=1)
    def multiples_alarmas(self): #Regla N°30
        senal_alarma = self.senales_alarma[0]
        for regla in range(1, len(self.senales_alarma)):
            senal_alarma = senal_alarma + '_' + self.senales_alarma[regla]

        resultado = alarmas[senal_alarma][0]
        recomendacion = alarmas[senal_alarma][1]
        print(resultado)
        print(recomendacion)

    @Rule(Fact(activar=1), salience=0)
    def regla_aux(self):
        self.declare(Fact(senales_alarma=len(self.senales_alarma)))
