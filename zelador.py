from scapy.all import IP, ICMP, sr1, conf
import ipaddress, socket, sys, logging
from concurrent.futures import ThreadPoolExecutor
logging.getLogger("scapy.runtime").setLevel(logging.ERROR)
conf.verb = 0 

def ping(ip, timeout=1):
    pacote = IP(dst=ip) / ICMP()
    res = sr1(pacote, timeout=timeout, verbose=0)
    return res is not None

def ips(rede):
    ativos = []
    try:
        net = ipaddress.ip_network(rede, strict=False)
    except ValueError:
        print("Rede inválida. Use o formato ex: 10.0.0.0/24")
        return ativos

    hosts = list(net.hosts())
    print(f"Escaneando {len(hosts)} hosts em {net}...\n")

    for host in hosts:
        ip = str(host)
        if ping(ip):
            print(f"{ip} está ATIVO")
            ativos.append(ip)

    print(f"\nTotal de hosts ativos: {len(ativos)}")
    return ativos

def testar_porta(ip, porta, timeout=0.5):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(timeout)
    try:
        if s.connect_ex((ip, porta)) == 0:
            return porta
    except socket.error:
        pass
    finally:
        s.close()
    return None

def portas(ip, timeout=0.5, max_threads=200):
    abertas = []
    print(f"Escaneando portas em {ip}...\n")
    with ThreadPoolExecutor(max_workers=max_threads) as executor:
        resultados = executor.map(lambda p: testar_porta(ip, p, timeout), range(1, 65536))
        for porta in resultados:
            if porta:
                print(f"Porta {porta} está ABERTA")
                abertas.append(porta)
    print(f"\nTotal de portas abertas: {len(abertas)}")
    return abertas

def mostrar_ajuda():
    print("""
Uso: python zelador.py [opção] [valor]

Opções:
  -r, --rede <CIDR>     Escaneia hosts ativos numa rede (ex: -r 10.0.0.0/24)
  -p, --portas <IP>     Escaneia portas abertas num host (ex: -p 192.168.1.1)
  -h, --help            Mostra esta ajuda
""")

print("\n███████╗███████╗██╗      █████╗ ██████╗  ██████╗ ██████╗ \n"
      "╚══███╔╝██╔════╝██║     ██╔══██╗██╔══██╗██╔═══██╗██╔══██╗\n"
      "  ███╔╝ █████╗  ██║     ███████║██║  ██║██║   ██║██████╔╝\n"
      " ███╔╝  ██╔══╝  ██║     ██╔══██║██║  ██║██║   ██║██╔══██╗\n"
      "███████╗███████╗███████╗██║  ██║██████╔╝╚██████╔╝██║  ██║\n"
      "╚══════╝╚══════╝╚══════╝╚═╝  ╚═╝╚═════╝  ╚═════╝ ╚═╝  ╚═╝")

if __name__ == "__main__":
    args = sys.argv[1:]
    if len(args) == 0 or args[0] in ("-h", "--help"):
        mostrar_ajuda()

    elif args[0] in ("-r", "--rede"):
        if len(args) < 2:
            print("Erro: faltou informar a rede. Ex: -r 10.0.0.0/24")
        else:
            ips(args[1])

    elif args[0] in ("-p", "--portas"):
        if len(args) < 2:
            print("Erro: faltou informar o IP. Ex: -p 192.168.1.1")
        else:
            portas(args[1])

    else:
        print(f"Opção desconhecida: {args[0]}")
        mostrar_ajuda()
