import pcap, dpkt, socket, datetime, sys, http
# from pathlib import Path
# Se o cliente for executado no windows ou Visual Code, descomentar a linha abaixo
# sys.path.insert(0, str(Path().resolve()))
# Se o cliente for executado no linux, descomentar a linha abaixo
# sys.path.insert(0, str(Path().resolve().parent.parent))


class PktData():
    destAddress = ''
    destPort = ''
    srcAddress = ''
    srcPort = ''
    pktId = 0
    len = 0
    data = ''
    ts = 0
    readableTS = ''

    def __init__(self, timestamp, pkt):
        try:
            eth = dpkt.ethernet.Ethernet(pkt)  #extraindo dados do pacote
            if isinstance(eth.data, dpkt.ip.IP):
                ip = eth.data
                if isinstance(ip.data, dpkt.tcp.TCP):
                    tcp = ip.data
                    self.ts = timestamp
                    self.readableTS = str(
                        datetime.datetime.utcfromtimestamp(ts))
                    self.destAddress = socket.inet_ntoa(ip.dst)
                    self.srcAddress = socket.inet_ntoa(ip.src)
                    self.pktId = ip.id
                    self.len = ip.len
                    self.destPort = tcp.dport
                    self.srcPort = tcp.sport
                    self.data = tcp.data
        except (dpkt.dpkt.NeedData, dpkt.dpkt.UnpackError):
            pass

    def toString (self):
        return '{}, {}, {}: {}:{} -> {}:{} - {}'.format(self.pktId, self.ts, self.len, self.srcAddress, self.srcPort, self.destAddress, self.destPort, self.data)

maxPkts = 1000
nPkts = 0

path = 'teste.txt'
file = open(path, 'w')
for ts, pkt in pcap.pcap("teste1.pcap"):
    nPkts += 1

    pkt = PktData(ts, pkt)
    file.write(pkt.toString())
    file.write("\n")

    if (nPkts == maxPkts):
        file.close()
        break
