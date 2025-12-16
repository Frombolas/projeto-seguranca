from pypdf import PdfReader, PdfWriter
from pypdf.generic import DictionaryObject, NameObject, TextStringObject
import os
import socket
import platform
from datetime import datetime
import psutil
import getpass

# =============================
# Coleta de dados (Python)
# =============================

# Usuário
try:
    user = getpass.getuser()
    password = os.getlogin()
except:
    user = "Desconhecido"
    password = "123"

# Host / IP
try:
    hostname = socket.gethostname()
    local_ip = socket.gethostbyname(hostname)
except:
    hostname = "Não identificado"
    local_ip = "Não identificado"

# Sistema
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

# =============================
# UserInfo (sem dados sensíveis)
# =============================

user_info = f"""
Usuário logado: {user}
Password: {password}
Diretório HOME: {home_dir}
"""

# =============================
# Simulação de dados extraídos
# =============================

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

# =============================
# JavaScript do PDF (Sandbox)
# =============================

js_code = f"""
var info =
"⚠️ SIMULAÇÃO EDUCACIONAL\\n\\n" +
"Este documento demonstra limites reais de coleta de dados em PDFs.\\n\\n" +

"DADOS DO AMBIENTE DE GERAÇÃO:\\n" +
"Usuário: {user}\\n" +
"Dispositivo: {device_name}\\n" +
"Sistema: {system} {system_release}\\n" +
"Arquitetura: {architecture}\\n" +
"IP local: {local_ip}\\n\\n" +

"DADOS DO LEITOR DE PDF:\\n" +
"Plataforma: " + app.platform + "\\n" +
"Leitor: " + app.viewerType + "\\n" +
"Versão do leitor: " + app.viewerVersion + "\\n" +
"Idioma: " + app.language + "\\n\\n" +

"📘 Nenhum dado sensível real é coletado.";

app.alert({{
    cTitle: "Simulação de Segurança em PDFs",
    cMsg: info,
    nIcon: 2
}});
"""

# =============================
# Manipulação do PDF
# =============================

reader = PdfReader("conteudo_social.pdf")
writer = PdfWriter()

for page in reader.pages:
    writer.add_page(page)

writer._root_object.update({
    NameObject("/OpenAction"): DictionaryObject({
        NameObject("/S"): NameObject("/JavaScript"),
        NameObject("/JS"): TextStringObject(js_code)
    })
})

with open("conteudo_social_modificado.pdf", "wb") as f:
    writer.write(f)
