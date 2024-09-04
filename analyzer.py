import math

def aplicar_modificaciones(diccionario_jugador, aumento_base, stats_a_modificar):
    for stat in stats_a_modificar:
        diccionario_jugador['stats'][stat] += aumento_base

def aplicar_modificaciones_porcentaje(diccionario_jugador, porcentaje, stats_a_modificar):
    for stat in stats_a_modificar:
        diccionario_jugador['stats'][stat] = diccionario_jugador['stats'][stat] * porcentaje


def modificar_por_lb(diccionario_jugador):
    stats_base = ['potencia', 'tecnica', 'rapidez']
    aplicar_modificaciones(diccionario_jugador, 1000, stats_base)
    
    lb_config = diccionario_jugador['otros']['lb']
    if lb_config == 'Todo (Atacante)':
        stats_extra = ['regate', 'remate', 'pase', 'entrada', 'intercepcion']
    elif lb_config == 'Todo (Defensor)':
        stats_extra = ['regate', 'remate', 'pase', 'entrada', 'bloqueo']
    elif lb_config == 'Ataque':
        stats_extra = ['regate', 'remate', 'pase']
    elif lb_config == 'Defensa':
        stats_extra = ['entrada', 'bloqueo', 'intercepcion']
    else:
        stats_extra = []

    aplicar_modificaciones(diccionario_jugador, 1000, stats_extra)

def modificar_por_formacion(diccionario_jugador):
    formacion = diccionario_jugador['otros']['formacion']
    multiplicador = 1.10
    if formacion == '+10% Ataque':
        stats_base = ['regate', 'remate', 'pase']
    elif formacion == '+10% Defensa':
        stats_base = ['entrada', 'bloqueo', 'intercepcion']
    elif formacion == '+10% Fisico':
        stats_base = ['potencia', 'tecnica', 'rapidez']
    elif formacion == '+12% Fisico':
        stats_base = ['potencia', 'tecnica', 'rapidez']
        multiplicador = 1.12
    
    aplicar_modificaciones_porcentaje(diccionario_jugador, multiplicador, stats_base)
    


def modificar_por_bb4(diccionario_jugador):
    stats_base = ['potencia', 'tecnica', 'rapidez']
    stats_extra = ['regate', 'remate', 'pase', 'entrada', 'bloqueo', 'intercepcion']
    
    aplicar_modificaciones(diccionario_jugador, 2400, stats_base)
    aplicar_modificaciones(diccionario_jugador, 1200, stats_extra)

def calcular_fuerza_tecnicas(diccionario_jugador):
    tecnicas_final = {}
    otros = diccionario_jugador['otros']
    potencia_base = otros['potencia']
    
    for tecnica, valor in diccionario_jugador['tecnicas'].items():
        if tecnica == 'pared':
            continue
        multiplicador_balones_aire = 0
        if tecnica == 'alto':
            if otros['cabeceo'] in ['Muy Bueno']:
                multiplicador_balones_aire = 25 
            elif otros['cabeceo'] == 'Bueno':
                multiplicador_balones_aire = 12.5
        if tecnica == 'bajo':
            if otros['volea'] in ['Muy Bueno']:
                multiplicador_balones_aire = 25 
            elif otros['volea'] == 'Bueno':
                multiplicador_balones_aire = 12.5

        tecnicas_final[tecnica] = ((valor + multiplicador_balones_aire) *
                                   (potencia_base + diccionario_jugador['extras'][tecnica] - 1))
    tecnicas_final['pared'] = diccionario_jugador['tecnicas']['pared'] * (potencia_base + diccionario_jugador['extras']['pase'] - 1)
    tecnicas_final['bloqueoBajo'] = tecnicas_final['bloqueo']
    tecnicas_final['bloqueoAlto'] = tecnicas_final['bloqueo']
    if otros['volea'] == 'Muy Bueno':
        tecnicas_final['bloqueoBajo'] = (diccionario_jugador['tecnicas']['bloqueo'] + 25) * (potencia_base + diccionario_jugador['extras']['bloqueo'] - 1)
    elif otros['volea'] == 'Bueno':
        tecnicas_final['bloqueoBajo'] = (diccionario_jugador['tecnicas']['bloqueo'] + 12.5) * (potencia_base + diccionario_jugador['extras']['bloqueo'] - 1)

    if otros['cabeceo'] == 'Muy Bueno':
        tecnicas_final['bloqueoAlto'] = (diccionario_jugador['tecnicas']['bloqueo'] + 25) * (potencia_base + diccionario_jugador['extras']['bloqueo'] - 1)
    elif otros['cabeceo'] == 'Bueno':
        tecnicas_final['bloqueoAlto'] = (diccionario_jugador['tecnicas']['bloqueo'] + 12.5) * (potencia_base + diccionario_jugador['extras']['bloqueo'] - 1)

    return tecnicas_final

def calcular_stats_visuales(diccionario_jugador, multiplicador_equipo, multiplicador_color):
    stats = diccionario_jugador['stats']
    exStats = diccionario_jugador['exStats']
    
    def calcular_stat(stat, extra_stat):
        return math.ceil(stats[stat] * multiplicador_color * exStats[stat] * multiplicador_equipo + 
                         (stats[extra_stat] * multiplicador_color * multiplicador_equipo) / 2)

    return {
        'regate': calcular_stat('regate', 'rapidez'),
        'remate': calcular_stat('remate', 'potencia'),
        'pase': calcular_stat('pase', 'tecnica'),
        'entrada': calcular_stat('entrada', 'rapidez'),
        'bloqueo': calcular_stat('bloqueo', 'potencia'),
        'intercepcion': calcular_stat('intercepcion', 'tecnica')
    }

def calcular_stat_duelo(diccionario_jugador, multiplicador_equipo, tecnicas_final):
    multiplicador_color = 1.25 if diccionario_jugador['otros']['color'] else 1
    stats_sin_tecnica = calcular_stats_visuales(diccionario_jugador, multiplicador_equipo, multiplicador_color)
    
    def calcular_duelo(stat, tecnica):
        return math.ceil(stats_sin_tecnica[stat] * (tecnicas_final[tecnica] / 100))

    return {
        'regate': calcular_duelo('regate', 'regate'),
        'remate': calcular_duelo('remate', 'remate'),
        'pase': calcular_duelo('pase', 'pase'),
        'pared': calcular_duelo('pase', 'pared'),
        'entrada': calcular_duelo('entrada', 'entrada'),
        'bloqueo': calcular_duelo('bloqueo', 'bloqueo'),
        'intercepcion': calcular_duelo('intercepcion', 'intercepcion'),
        'cabeceo': calcular_duelo('remate', 'alto'),
        'volea': calcular_duelo('remate', 'bajo'),
        'bloqueoAlto': calcular_duelo('bloqueo', 'bloqueoAlto'),
        'bloqueoBajo': calcular_duelo('bloqueo', 'bloqueoBajo')
    }

def analizar_jugador(diccionario_jugador):
    # Modificación por BB4
    if diccionario_jugador['otros'].get('bb4', False):
        modificar_por_bb4(diccionario_jugador)
    
    if diccionario_jugador['otros']['formacion'] != 'Sin Efecto':
        modificar_por_formacion(diccionario_jugador)

    # Modificación por LB
    if diccionario_jugador['otros']['lb'] != 'Nada':
        modificar_por_lb(diccionario_jugador)
    
    # Cálculo de fuerza de técnicas
    tecnicas_final = calcular_fuerza_tecnicas(diccionario_jugador)
    
    # Cálculo de multiplicador del equipo
    otros = diccionario_jugador['otros']
    multiplicador_equipo = otros['ts'] * (otros['bond'] + otros['parametros'] - 1)
    
    # Cálculo de estadísticas visuales y de duelo
    stats_visual_final = calcular_stats_visuales(diccionario_jugador, multiplicador_equipo, 1)
    stats_duelo_final = calcular_stat_duelo(diccionario_jugador, multiplicador_equipo, tecnicas_final)
    
    return {'statsVisuales': stats_visual_final, 'statsDuelo': stats_duelo_final}
