from pypdf import PdfReader, PdfWriter
from pypdf.generic import DictionaryObject, NameObject, TextStringObject
import os
import socket
import platform
from datetime import datetime
import psutil
import getpass

try:
    user = os.getlogin()
except:
    user = "Desconhecido"

try:
    hostname = socket.gethostname()
    local_ip = socket.gethostbyname(hostname)
except:
    local_ip = "Não identificado"


system = platform.system()
system_release = platform.release()
architecture = platform.architecture()[0]
processor = platform.processor()
device_name = platform.node()
home_dir = os.path.expanduser("~")
timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

# =============================
# Interfaces de Rede
# =============================

network_interfaces_info = []

interfaces = psutil.net_if_addrs()
for interface_name, addresses in interfaces.items():
    for addr in addresses:
        if addr.family == socket.AF_INET:
            network_interfaces_info.append(
                f"{interface_name} → IPv4: {addr.address}"
            )

if not network_interfaces_info:
    network_interfaces_info.append("Nenhuma interface IPv4 identificada")
    
user_info = f"""
Usuário logado: {user}
Diretório HOME: {home_dir}
"""


# Simulação de dados extraídos
data_extracted = f"""
DADOS EXTRAÍDOS (SIMULAÇÃO EDUCACIONAL)

=== USUÁRIO ===
{user_info}

=== DISPOSITIVO ===
Nome do dispositivo: {device_name}
Hostname: {hostname}
IP local principal: {local_ip}

=== SISTEMA ===
Sistema operacional: {system} {system_release}
Arquitetura: {architecture}
Processador: {processor}

=== INTERFACES DE REDE ===
""" + "\n".join(network_interfaces_info) + f"""

=== DATA / HORA ===
{timestamp}
"""

with open("dados_extraidos.txt", "w", encoding="utf-8") as f:
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

