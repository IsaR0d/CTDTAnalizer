from bs4 import BeautifulSoup
from io import StringIO
import io
import re
from email import policy
from email.parser import BytesParser
# Abre el archivo HTML
def extractor(archivo):
    if isinstance(archivo, StringIO):
        contenido = archivo.read()
    else:
        with open(archivo, "r", encoding="utf-8") as file:
            contenido = file.read()
    diccionario = {}
    stats = {"regate": "1" , "remate": "2", "pase": "3" , "entrada": "5", "bloqueo": "6", "intercepcion": "7", "rapidez": "9", "potencia": "10", "tecnica": "11"}
    tecnicas = {"regate": "3", "remate": "4", "pase": "5", "pared":"6", "entrada": "7", "bloqueo": "8", "intercepcion": "9", "bajo": "10", "alto": "11" }
    otros = {}
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
        if rows:
            max_value = max(int(row.get_text(strip=True)) for row in rows)
            tecnicas[tecnica] = max_value
        else:
            tecnicas[tecnica] = 0
    


    
    # Manejo de 'low_ball'
    if soup.find('a', href=re.compile(r'/global/(es|en)/players/\?low_ball=0')):
        otros["volea"] = "Normal"
    elif soup.find('a', href=re.compile(r'/global/(es|en)/players/\?low_ball=1250')):
        otros["volea"] = "Bueno"
    elif soup.find('a', href=re.compile(r'/global/(es|en)/players/\?low_ball=2500')):
        otros["volea"] = "Muy Bueno"

    # Manejo de 'high_ball'
    if soup.find('a', href=re.compile(r'/global/(es|en)/players/\?high_ball=0')):
        otros["cabeceo"] = "Normal"
    elif soup.find('a', href=re.compile(r'/global/(es|en)/players/\?high_ball=1250')):
        otros["cabeceo"] = "Bueno"
    elif soup.find('a', href=re.compile(r'/global/(es|en)/players/\?high_ball=2500')):
        otros["cabeceo"] = "Muy Bueno"

    diccionario = {"stats": stats, "tecnicas": tecnicas, "otros": otros}
    return diccionario


def extraer_imagen(mhtml_file_path):
    # Leer el archivo .mhtml
    with open(mhtml_file_path, 'rb') as file:
        mhtml_content = file.read()

    # Analizar el contenido como un mensaje de email
    msg = BytesParser(policy=policy.default).parsebytes(mhtml_content)

    # Buscar y devolver la imagen GIF en memoria
    for part in msg.iter_parts():
        if part.get_content_type() == 'image/gif':
            base64_data = part.get_payload(decode=True)
            gif_io = io.BytesIO(base64_data)
            return gif_io

    # Si no se encuentra un GIF, devolver None
    return None
    

