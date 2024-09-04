from bs4 import BeautifulSoup

# Abre el archivo HTML
def extractor(archivo):
    with open(archivo, "r", encoding="utf-8") as file:
        contenido = file.read()

    diccionario = {}
    stats = {"regate": "1" , "remate": "2", "pase": "3" , "entrada": "5", "bloqueo": "6", "intercepcion": "7", "rapidez": "9", "potencia": "10", "tecnica": "11"}
    tecnicas = {"regate": "3", "remate": "4", "pase": "5", "pared":"6", "entrada": "7", "bloqueo": "8", "intercepcion": "9", "bajo": "10", "alto": "11" }
    soup = BeautifulSoup(contenido, 'html.parser')

    for stat in stats:
        row = soup.find('td', {'way-data': 'total.parameter.' + stats[stat]})
        if row:
            value = int(row.get('title'))
            if stats[stat] in ["9","10","11"]:
                stats[stat] = value - 2400
            else:
                stats[stat] = value - 1200


    for tecnica in tecnicas:
        rows = soup.findAll('td',{'class': 'skill-table-col-power', 'data-action': tecnicas[tecnica]})
        max_value = max(int(row.get_text(strip=True)) for row in rows)
        tecnicas[tecnica] = max_value
        

    diccionario = {"stats": stats, "tecnicas": tecnicas}
    return diccionario

    

