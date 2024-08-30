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




def analizar_jugador(progress, diccionario_jugador):

    stat_final_remate = 0
    stat_final_pase = 0
    stat_final_regate = 0
    stat_final_entrada = 0
    stat_final_bloqueo = 0
    stat_final_intercepcion = 0
    stat_ig_regate = 0
    stat_ig_remate = 0
    stat_ig_volea = 0
    stat_ig_cabezazo = 0
    stat_ig_pase = 0
    stat_ig_entrada = 0
    stat_ig_bloqueo = 0
    stat_ig_balto = 0
    stat_ig_bbajo = 0
    stat_ig_intercepcion = 0
    

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
    # ts = 1 + diccionario_jugador['ts']/100
    # bond = 1 + diccionario_jugador['bond']/100
    # parametros = 1 + diccionario_jugador['parametros']/100

    multiplicador_equipo = diccionario_jugador['otros']['ts']*(diccionario_jugador['otros']['bond']+diccionario_jugador['otros']['parametros']-1)

    stat_final_regate = math.ceil(math.ceil(diccionario_jugador['stats']['regate'] * multiplicador_equipo) + math.ceil(diccionario_jugador['stats']['rapidez'] * multiplicador_equipo)/2)
    stat_final_remate = (diccionario_jugador['stats']['remate'] * multiplicador_equipo) + (diccionario_jugador['stats']['potencia'] * multiplicador_equipo)/2
    stat_final_pase = math.ceil(math.ceil(diccionario_jugador['stats']['pase'] * multiplicador_equipo) + math.ceil(diccionario_jugador['stats']['tecnica'] * multiplicador_equipo)/2)
    stat_final_entrada = math.ceil(math.ceil(diccionario_jugador['stats']['entrada'] * multiplicador_equipo) + math.ceil(diccionario_jugador['stats']['rapidez'] * multiplicador_equipo)/2)
    stat_final_bloqueo = math.ceil(math.ceil(diccionario_jugador['stats']['bloqueo'] * multiplicador_equipo) + math.ceil(diccionario_jugador['stats']['potencia'] * multiplicador_equipo)/2)
    stat_final_intercepcion = math.ceil(math.ceil(diccionario_jugador['stats']['intercepcion'] * multiplicador_equipo) + math.ceil(diccionario_jugador['stats']['tecnica'] * multiplicador_equipo)/2)

    print(stat_final_regate, stat_final_remate, stat_final_pase, stat_final_entrada, stat_final_bloqueo, stat_final_intercepcion)
    #---------------------------------trabajo con las tecnicas---------------------------------------------------------------    
    diccionario_mostrar = {'regate': stat_final_regate, 'remate': stat_final_remate, 'pase': stat_final_pase, 'entrada': stat_final_entrada, 'bloqueo': stat_final_bloqueo, 'intercepcion': stat_final_intercepcion}


    return diccionario_mostrar