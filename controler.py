import math

def modificar_por_lb(diccionario_jugador):
    diccionario_jugador['stat']['potencia'] += 1000
    diccionario_jugador['stat']['tecnica'] += 1000
    diccionario_jugador['stat']['rapidez'] += 1000

    if diccionario_jugador['otros']['lb'] == 'Todo (Atacante)':
        diccionario_jugador['stat']['regate'] += 1000
        diccionario_jugador['stat']['remate'] += 1000
        diccionario_jugador['stat']['pase'] += 1000
        diccionario_jugador['stat']['entrada'] += 1000
        diccionario_jugador['stat']['intercepcion'] += 1000

    elif diccionario_jugador['otros']['lb'] == 'Todo (Defensor)':
        diccionario_jugador['stat']['regate'] += 1000
        diccionario_jugador['stat']['remate'] += 1000
        diccionario_jugador['stat']['pase'] += 1000
        diccionario_jugador['stat']['entrada'] += 1000
        diccionario_jugador['stat']['bloqueo'] += 1000

    elif diccionario_jugador['otros']['lb'] == 'Ataque':
        diccionario_jugador['stat']['regate'] += 1000
        diccionario_jugador['stat']['remate'] += 1000
        diccionario_jugador['stat']['pase'] += 1000

    elif diccionario_jugador['otros']['lb'] == 'Defensa':
        diccionario_jugador['stat']['entrada'] += 1000
        diccionario_jugador['stat']['bloqueo'] += 1000
        diccionario_jugador['stat']['intercepcion'] += 1000

def modificar_por_bb4(diccionario_jugador):
    diccionario_jugador['stat']['potencia'] += 2400
    diccionario_jugador['stat']['tecnica'] += 2400
    diccionario_jugador['stat']['rapidez'] += 2400
    diccionario_jugador['stat']['regate'] += 1200
    diccionario_jugador['stat']['remate'] += 1200
    diccionario_jugador['stat']['pase'] += 1200
    diccionario_jugador['stat']['entrada'] += 1200
    diccionario_jugador['stat']['bloqueo'] += 1200
    diccionario_jugador['stat']['interceptacion'] += 1200

def calcular_fuerza_tecnicas(diccionario_jugador):
    

    #A todas las tecnicas, la multiplico por el aumento de potencia y por el extra que puedan tener
    diccionario_jugador['tecnicas']['regate'] = math.ceil(math.ceil(diccionario_jugador['tecnicas']['regate']*diccionario_jugador['otros']['potencia'])*diccionario_jugador['extras']['regate'])
    



def analizar_jugador(progress, diccionario_jugador):

    stat_final_remate = 0
    stat_final_pase = 0
    stat_final_regate = 0
    stat_final_entrada = 0
    stat_final_bloqueo = 0
    stat_final_interceptacion = 0
    stat_ig_regate = 0
    stat_ig_remate = 0
    stat_ig_volea = 0
    stat_ig_cabezazo = 0
    stat_ig_pase = 0
    stat_ig_entrada = 0
    stat_ig_bloqueo = 0
    stat_ig_balto = 0
    stat_ig_bbajo = 0
    stat_ig_interceptacion = 0
    

    #verifico si el jugador tiene ventaja de color (aun no modifica nada)
    multiplicador_color = 1
    if diccionario_jugador['extras']['color'] == True:
        multiplicador_color = 1.25

    #sumo los parametros del bb4
    if diccionario_jugador['otros']['bb4'] == True:
        modificar_por_bb4(diccionario_jugador)
    
    #sumo los parametros del lb
    if diccionario_jugador['otros']['lb'] == 'Nada':
        pass
    else:
        modificar_por_lb(diccionario_jugador)

    
    #-----------------------------------------------------------------------
    ts = 1 + diccionario_jugador['ts']/100
    bond = 1 + diccionario_jugador['bond']/100
    parametros = 1 + diccionario_jugador['parametros']/100






    return diccionario_jugador