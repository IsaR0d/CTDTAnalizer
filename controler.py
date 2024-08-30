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
    tecnicas_final = {}
    #A todas las tecnicas, la multiplico por el aumento de potencia y por el extra que puedan tener
    for i in diccionario_jugador['tecnicas']:
        multiplicador_balones_aire = 0
        if i == 'alto' or i == 'bajo':
            if diccionario_jugador['otros']['cabeceo'] == 'Muy Bueno' or diccionario_jugador['otros']['volea'] == 'Muy Bueno':
                multiplicador_balones_aire = 0.25
            elif diccionario_jugador['otros']['cabeceo'] == 'Bueno' or diccionario_jugador['otros']['volea'] == 'Bueno':
                multiplicador_balones_aire = 0.125
            
        tecnicas_final[i] = ((diccionario_jugador['tecnicas'][i] + multiplicador_balones_aire) *((diccionario_jugador['otros']['potencia'])+diccionario_jugador['extras'][i]-1))
        print(diccionario_jugador['tecnicas'][i], multiplicador_balones_aire, diccionario_jugador['otros']['potencia'], diccionario_jugador['extras'][i], tecnicas_final[i])
    if diccionario_jugador['otros']['volea'] == 'Muy Bueno':
        tecnicas_final['bloqueoBajo'] = (diccionario_jugador['tecnicas']['bloqueo']+0.25)*((diccionario_jugador['otros']['potencia'])+diccionario_jugador['extras']['bloqueo']-1)
    elif diccionario_jugador['otros']['volea'] == 'Bueno':
        tecnicas_final['bloqueoBajo'] = (diccionario_jugador['tecnicas']['bloqueo']+0.125)*((diccionario_jugador['otros']['potencia'])+diccionario_jugador['extras']['bloqueo']-1)
    else:
        tecnicas_final['bloqueoBajo'] = tecnicas_final['bloqueo']
    if diccionario_jugador['otros']['cabeceo'] == 'Muy Bueno':
        tecnicas_final['bloqueoAlto'] = (diccionario_jugador['tecnicas']['bloqueo']+0.25)*((diccionario_jugador['otros']['potencia'])+diccionario_jugador['extras']['bloqueo']-1)
    elif diccionario_jugador['otros']['cabeceo'] == 'Bueno':
        tecnicas_final['bloqueoAlto'] = (diccionario_jugador['tecnicas']['bloqueo']+0.125)*((diccionario_jugador['otros']['potencia'])+diccionario_jugador['extras']['bloqueo']-1)
    else:
        tecnicas_final['bloqueoAlto'] = tecnicas_final['bloqueo']
    return tecnicas_final

def calcular_stats_visuales(diccionario_jugador, multiplicador_equipo, multiplicador_color):
    stat_final_regate = math.ceil(diccionario_jugador['stats']['regate'] * multiplicador_color * diccionario_jugador['exStats']['regate'] * multiplicador_equipo) + ((diccionario_jugador['stats']['rapidez']* multiplicador_color * multiplicador_equipo)/2)
    stat_final_remate = math.ceil(diccionario_jugador['stats']['remate']* multiplicador_color * diccionario_jugador['exStats']['remate'] * multiplicador_equipo) + ((diccionario_jugador['stats']['potencia']* multiplicador_color * multiplicador_equipo)/2)
    stat_final_pase = math.ceil(diccionario_jugador['stats']['pase']* multiplicador_color * diccionario_jugador['exStats']['pase'] * multiplicador_equipo) + ((diccionario_jugador['stats']['tecnica']* multiplicador_color * multiplicador_equipo)/2)
    stat_final_entrada = math.ceil(diccionario_jugador['stats']['entrada']* multiplicador_color * diccionario_jugador['exStats']['entrada'] * multiplicador_equipo) + ((diccionario_jugador['stats']['rapidez']* multiplicador_color * multiplicador_equipo)/2)
    stat_final_bloqueo = math.ceil(diccionario_jugador['stats']['bloqueo']* multiplicador_color * diccionario_jugador['exStats']['bloqueo'] * multiplicador_equipo) + ((diccionario_jugador['stats']['potencia']* multiplicador_color * multiplicador_equipo)/2)
    stat_final_intercepcion = math.ceil(diccionario_jugador['stats']['intercepcion']* multiplicador_color * diccionario_jugador['exStats']['intercepcion'] * multiplicador_equipo) + ((diccionario_jugador['stats']['tecnica']* multiplicador_color * multiplicador_equipo)/2)
    stats_final = {'regate': stat_final_regate, 'remate': stat_final_remate, 'pase': stat_final_pase, 'entrada': stat_final_entrada, 'bloqueo': stat_final_bloqueo, 'intercepcion': stat_final_intercepcion}
    return stats_final

def calcular_stat_duelo(diccionario_jugador, multiplicador_equipo, tecnicas_final):
    multiplicador_color = 1
    if diccionario_jugador['otros']['color'] == True:
        multiplicador_color = 1.25
    stats_sin_tecnica = calcular_stats_visuales(diccionario_jugador, multiplicador_equipo , multiplicador_color)
    print(stats_sin_tecnica)
    print(tecnicas_final)
    reg_stat_duelo = math.ceil(stats_sin_tecnica['regate']*(tecnicas_final['regate']/100))
    rem_stat_duelo = math.ceil(stats_sin_tecnica['remate']*(tecnicas_final['remate']/100))
    pase_stat_duelo = math.ceil(stats_sin_tecnica['pase']*(tecnicas_final['pase']/100))
    ent_stat_duelo = math.ceil(stats_sin_tecnica['entrada']*(tecnicas_final['entrada']/100))
    blo_stat_duelo = math.ceil(stats_sin_tecnica['bloqueo']*(tecnicas_final['bloqueo']/100))
    int_stat_duelo = math.ceil(stats_sin_tecnica['intercepcion']*(tecnicas_final['intercepcion']/100))
    cab_stat_duelo = math.ceil(stats_sin_tecnica['remate']*(tecnicas_final['alto']/100))
    vol_stat_duelo = math.ceil(stats_sin_tecnica['remate']*(tecnicas_final['bajo']/100))
    balto_stat_duelo = math.ceil(stats_sin_tecnica['bloqueo']*(tecnicas_final['bloqueoAlto']/100))
    bbajo_stat_duelo = math.ceil(stats_sin_tecnica['bloqueo']*(tecnicas_final['bloqueoBajo']/100))
    print(reg_stat_duelo, rem_stat_duelo, pase_stat_duelo, ent_stat_duelo, blo_stat_duelo, int_stat_duelo, cab_stat_duelo, vol_stat_duelo, balto_stat_duelo, bbajo_stat_duelo)
    stats_duelo = {'regate': reg_stat_duelo, 'remate': rem_stat_duelo, 'pase': pase_stat_duelo, 'entrada': ent_stat_duelo, 'bloqueo': blo_stat_duelo, 'intercepcion': int_stat_duelo, 'cabeceo': cab_stat_duelo, 'volea': vol_stat_duelo, 'bloqueoAlto': balto_stat_duelo, 'bloqueoBajo': bbajo_stat_duelo}
    return stats_duelo


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
    tecnicas_final = calcular_fuerza_tecnicas(diccionario_jugador)
    
    #---------------------------------trabajo con ts y statsup---------------------------------------------------------------
    multiplicador_equipo = diccionario_jugador['otros']['ts']*(diccionario_jugador['otros']['bond']+diccionario_jugador['otros']['parametros']-1)

    stats_visual_final = calcular_stats_visuales(diccionario_jugador, multiplicador_equipo, 1)
    #---------------------------------trabajo con las tecnicas---------------------------------------------------------------    
    stats_duelo_final = calcular_stat_duelo(diccionario_jugador, multiplicador_equipo, tecnicas_final)


    diccionario_mostrar = {'statsVisuales': stats_visual_final, 'statsDuelo': stats_duelo_final}
    return diccionario_mostrar