import math

def modificar_por_lb(diccionario_jugador):
    diccionario_jugador['stats']['potencia'] += 1000
    diccionario_jugador['stats']['tecnica'] += 1000
    diccionario_jugador['stats']['rapidez'] += 1000

    if diccionario_jugador['otros']['lb'] == 'Todo (Atacante)':
        diccionario_jugador['stats']['regate'] += 1000
        diccionario_jugador['stats']['remate'] += 1000
        diccionario_jugador['stats']['pase'] += 1000
        diccionario_jugador['stats']['entrada'] += 1000
        diccionario_jugador['stats']['intercepcion'] += 1000

    elif diccionario_jugador['otros']['lb'] == 'Todo (Defensor)':
        diccionario_jugador['stats']['regate'] += 1000
        diccionario_jugador['stats']['remate'] += 1000
        diccionario_jugador['stats']['pase'] += 1000
        diccionario_jugador['stats']['entrada'] += 1000
        diccionario_jugador['stats']['bloqueo'] += 1000

    elif diccionario_jugador['otros']['lb'] == 'Ataque':
        diccionario_jugador['stats']['regate'] += 1000
        diccionario_jugador['stats']['remate'] += 1000
        diccionario_jugador['stats']['pase'] += 1000

    elif diccionario_jugador['otros']['lb'] == 'Defensa':
        diccionario_jugador['stats']['entrada'] += 1000
        diccionario_jugador['stats']['bloqueo'] += 1000
        diccionario_jugador['stats']['intercepcion'] += 1000

def modificar_por_bb4(diccionario_jugador):
    diccionario_jugador['stats']['potencia'] += 2400
    diccionario_jugador['stats']['tecnica'] += 2400
    diccionario_jugador['stats']['rapidez'] += 2400
    diccionario_jugador['stats']['regate'] += 1200
    diccionario_jugador['stats']['remate'] += 1200
    diccionario_jugador['stats']['pase'] += 1200
    diccionario_jugador['stats']['entrada'] += 1200
    diccionario_jugador['stats']['bloqueo'] += 1200
    diccionario_jugador['stats']['intercepcion'] += 1200

def calcular_fuerza_tecnicas(diccionario_jugador):
    
    #A todas las tecnicas, la multiplico por el aumento de potencia y por el extra que puedan tener
    for i in diccionario_jugador['tecnicas']:
        diccionario_jugador['tecnicas'][i] = math.ceil(math.ceil(diccionario_jugador['tecnicas'][i]*diccionario_jugador['otros']['potencia'])*diccionario_jugador['extras'][i])

def calcular_stats_visuales(diccionario_jugador, multiplicador_equipo):
    stat_final_regate = math.ceil(diccionario_jugador['stats']['regate'] * diccionario_jugador['exStats']['regate'] * multiplicador_equipo) + math.ceil(math.ceil(diccionario_jugador['stats']['rapidez'] * multiplicador_equipo)/2)
    stat_final_remate = math.ceil(diccionario_jugador['stats']['remate'] * diccionario_jugador['exStats']['remate'] * multiplicador_equipo) + math.ceil(math.ceil(diccionario_jugador['stats']['potencia'] * multiplicador_equipo)/2)
    stat_final_pase = math.ceil(diccionario_jugador['stats']['pase'] * diccionario_jugador['exStats']['pase'] * multiplicador_equipo) + math.ceil(math.ceil(diccionario_jugador['stats']['tecnica'] * multiplicador_equipo)/2)
    stat_final_entrada = math.ceil(diccionario_jugador['stats']['entrada'] * diccionario_jugador['exStats']['entrada'] * multiplicador_equipo) + math.ceil(math.ceil(diccionario_jugador['stats']['rapidez'] * multiplicador_equipo)/2)
    stat_final_bloqueo = math.ceil(diccionario_jugador['stats']['bloqueo'] * diccionario_jugador['exStats']['bloqueo'] * multiplicador_equipo) + math.ceil(math.ceil(diccionario_jugador['stats']['potencia'] * multiplicador_equipo)/2)
    stat_final_intercepcion = math.ceil(diccionario_jugador['stats']['intercepcion'] * diccionario_jugador['exStats']['intercepcion'] * multiplicador_equipo) + math.ceil(math.ceil(diccionario_jugador['stats']['tecnica'] * multiplicador_equipo)/2)
    stats_final = {'regate': stat_final_regate, 'remate': stat_final_remate, 'pase': stat_final_pase, 'entrada': stat_final_entrada, 'bloqueo': stat_final_bloqueo, 'intercepcion': stat_final_intercepcion}
    return stats_final

def calcular_stat_duelo(diccionario_jugador, stats_visuales):
    pass

def analizar_jugador(progress, diccionario_jugador):

    #---------------------------trabajo sobre las stats base----------------------------------------------------------------------
    #sumo los parametros del bb4
    if diccionario_jugador['otros']['bb4'] == True:
        modificar_por_bb4(diccionario_jugador)
    
    #sumo los parametros del lb
    if diccionario_jugador['otros']['lb'] == 'Nada':
        pass
    else:
        modificar_por_lb(diccionario_jugador)
    #---------------------------------trabajo sobre las tecnicas-------------------------------------------------------------
    calcular_fuerza_tecnicas(diccionario_jugador)
    
    #---------------------------------trabajo con ts y statsup---------------------------------------------------------------
    multiplicador_equipo = diccionario_jugador['otros']['ts']*(diccionario_jugador['otros']['bond']+diccionario_jugador['otros']['parametros']-1)

    stats_visual_final = calcular_stats_visuales(diccionario_jugador, multiplicador_equipo)
    #---------------------------------trabajo con las tecnicas---------------------------------------------------------------    

    diccionario_mostrar = {'statsVisuales': stats_visual_final}
    return diccionario_mostrar