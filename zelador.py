from scapy.all import IP, ICMP, sr1
import ipaddress, time, socket

def portas(ip):
    abertas = []
    print(f"Escaneando portas em {ip}...\n")

    for porta in range(1, 65536):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            resultado = s.connect_ex((ip, porta))
            if resultado == 0:
                abertas.append(porta)
                print(f"Porta {porta} Aberta")
        except socket.error:
            pass
        finally:
            s.close()

    print(f"\nTotal de portas abertas: {len(abertas)}")
    return abertas

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
    total = len(hosts)

    print(f"Escaneando {total} hosts em {net}...\n")

    for i, host in enumerate(hosts, 1):
        ip = str(host)
        if ping(ip):
            ativos.append(ip)   



    print(f"\nTotal de hosts ativos: {len(ativos)}")
    for ip in ativos:
        print(f"  - {ip}")

    return ativos


print("\n███████╗███████╗██╗      █████╗ ██████╗  ██████╗ ██████╗ \n"
      "╚══███╔╝██╔════╝██║     ██╔══██╗██╔══██╗██╔═══██╗██╔══██╗\n"
      "  ███╔╝ █████╗  ██║     ███████║██║  ██║██║   ██║██████╔╝\n"
      " ███╔╝  ██╔══╝  ██║     ██╔══██║██║  ██║██║   ██║██╔══██╗\n"
      "███████╗███████╗███████╗██║  ██║██████╔╝╚██████╔╝██║  ██║\n"
      "╚══════╝╚══════╝╚══════╝╚═╝  ╚═╝╚═════╝  ╚═════╝ ╚═╝  ╚═╝\n")

while True:
    print("Varrer Portas [2]")
    print("Varrer Hosts [1]")
    print("Sair [0]")
    print()
    x = input("> ")
    if x == "0":
        print("Encerrando Programa...")
        time.sleep(1)
        break
    elif x == "1":
        rede = input("Digite a Rede (10.0.0.0/24): ")
        ips(rede)
    elif x == "2":
        ip = input("Digite o IP (10.0.0.10): ")
        portas(ip)
    else:
        print("Opção inválida.")