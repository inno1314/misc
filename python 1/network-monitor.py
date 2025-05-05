import socket
from datetime import datetime, timezone
from scapy.all import sniff, Packet
from scapy.layers.inet import IP, TCP, UDP
from colorama import init, Fore
from database import DBHandler

db = DBHandler()

init(autoreset=True)


def resolve_domain(ip):
    try:
        host, _, _ = socket.gethostbyaddr(ip)
        return host
    except socket.herror:
        return None


def packet_callback(pkt: Packet):
    if not pkt.haslayer(IP):
        return

    ip = pkt[IP]
    src_ip = ip.src
    dst_ip = ip.dst
    src_port = dst_port = protocol = None

    if pkt.haslayer(TCP):
        protocol = "TCP"
        src_port = pkt[TCP].sport
        dst_port = pkt[TCP].dport
    if pkt.haslayer(UDP):
        protocol = "UDP"
        src_port = pkt[UDP].sport
        dst_port = pkt[UDP].dport
    else:
        protocol = "OTHER"

    ts = datetime.now(timezone.utc).strftime("%d.%m.%Y %H:%M:%S")
    domain = resolve_domain(dst_ip)

    print(
        f"{Fore.GREEN}[{ts}] "
        f"{Fore.YELLOW}{src_ip}:{src_port} -> {dst_ip}:{dst_port} "
        f"{Fore.CYAN}{protocol} "
        f"{Fore.MAGENTA}{domain or ''}"
    )
    db.save(src_ip, src_port, dst_ip, dst_port, protocol, domain, ts)


def main():
    sniff(prn=packet_callback, filter="ip", store=0)


if __name__ == "__main__":
    main()
