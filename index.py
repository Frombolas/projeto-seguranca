from pypdf import PdfReader, PdfWriter
from pypdf.generic import DictionaryObject, NameObject, TextStringObject
import os
import socket

try:
    user = os.getlogin()
except:
    user = "Desconhecido"

try:
    hostname = socket.gethostname()
    local_ip = socket.gethostbyname(hostname)
except:
    local_ip = "Não identificado"

# Simulação de dados extraídos
data_extracted = f"""
Dados extraídos (simulacao):
Usuario do sistema: {user}
IP local: {local_ip}
"""

with open("dados_extraidos.txt", "w") as f:
    f.write(data_extracted)

#JavaScript
js_code = f"""
app.alert({{
  cTitle: "Simulacao de Seguranca",
  cMsg: "⚠️ SIMULACAO EDUCACIONAL\\n\\n"
       + "Este PDF esta simulando a coleta de dados.\\n\\n"
       + "Usuario do sistema: {user}\\n"
       + "IP local: {local_ip}\\n\\n",
  nIcon: 2
}});
"""

reader = PdfReader("conteudo_social.pdf")
writer = PdfWriter()

for page in reader.pages:
    writer.add_page(page)

# Adiciona JavaScript como OpenAction
writer._root_object.update({
    NameObject("/OpenAction"): DictionaryObject({
        NameObject("/S"): NameObject("/JavaScript"),
        NameObject("/JS"): TextStringObject(js_code)
    })
})

with open("conteudo_social.pdf", "wb") as f:
    writer.write(f)

