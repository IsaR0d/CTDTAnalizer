import email
from io import StringIO

def converter(mhtml_file):

    # Leer el archivo MHTML
    with open(mhtml_file, 'rb') as file:
        mhtml_content = file.read()

    # Parsear el contenido MHTML
    msg = email.message_from_bytes(mhtml_content)
    
    # Buscar la parte HTML
    html_content = None
    for part in msg.walk():
        if part.get_content_type() == 'text/html':
            html_content = part.get_payload(decode=True).decode('utf-8')
            break

    if html_content is None:
        raise ValueError("No se encontró contenido HTML en el archivo MHTML.")

    # Guardar el contenido HTML en un objeto StringIO
    html_in_memory = StringIO(html_content)

    return html_in_memory

