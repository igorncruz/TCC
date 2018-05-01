import time, datetime
import socket
from general import *
from networking.ethernet import Ethernet
from networking.ipv4 import IPv4
from networking.icmp import ICMP
from networking.tcp import TCP
from networking.udp import UDP
from networking.pcap import Pcap
from networking.http import HTTP
import sys
from pathlib import Path
# Se o cliente for executado no windows, descomentar a linha abaixo
# sys.path.insert(0, str(Path().resolve()))
# Se o cliente for executado no linux, descomentar a linha abaixo
sys.path.insert(0, str(Path().resolve().parent.parent))
import util

TAB_1 = '\t - '
TAB_2 = '\t\t - '
TAB_3 = '\t\t\t - '
TAB_4 = '\t\t\t\t - '

DATA_TAB_1 = '\t   '
DATA_TAB_2 = '\t\t   '
DATA_TAB_3 = '\t\t\t   '
DATA_TAB_4 = '\t\t\t\t   '

class PackageInfo():
    __sentDatetimePackage = ''
    __receivedDatetimePackage = ''

    def __init__(self, eth, receivedDatetimePackage):
        self.__receivedDatetimePackage = receivedDatetimePackage

    def getReceivedDTPackg(self):
        return self.__receivedDatetimePackage

class PackageManager():
    __packageList = list()
    __maxTimeInSecBetweenPackages = 3

    def receivePackage(self, eth, receivedDatetimePackage):
        print('Recebendo pacote ' + str(len(self.__packageList)))
        self.__addPackage(eth, receivedDatetimePackage)
        if len(self.__packageList) <= 0:
            self.__addPackage(eth, receivedDatetimePackage)
        else:
            dtLastPackgReceived = self.__packageList[-1].getReceivedDTPackg()
            dtLimit = util.addSecs(dtLastPackgReceived, self.__maxTimeInSecBetweenPackages)
            if (dtLimit > datetime.datetime.fromtimestamp(receivedDatetimePackage) ):
                self.__packageList = list()
            self.__addPackage(eth, receivedDatetimePackage)


    def __addPackage(self, eth, receivedDatetimePackage):
        self.__packageList.append(PackageInfo(eth, receivedDatetimePackage))
        path = "HTTPPackageInfo.txt"
        openType = ('w' if len(self.__packageList) <= 0 else 'a')
        infoFile = open(path, openType)
        infoFile.write(
            "Interceptado pacote {}, enviado às {}, e recebido às {} (diferença de {})\n"
            .format(
                len(self.__packageList), '00:00:00',
                util.getFormattedDatetimeWithMillisec(
                    receivedDatetimePackage), '00:00:00 000'))
        infoFile.close()


def printInfo(eth):
    print('\nEthernet Frame:')
    print(TAB_1 + 'Destination: {}, Source: {}, Protocol: {}'.format(eth.dest_mac, eth.src_mac, eth.proto))

    ipv4 = IPv4(eth.data)
    print(TAB_1 + 'IPv4 Packet:')
    print(TAB_2 + 'Version: {}, Header Length: {}, TTL: {},'.format(ipv4.version, ipv4.header_length, ipv4.ttl))
    print(TAB_2 + 'Protocol: {}, Source: {}, Target: {}'.format(ipv4.proto, ipv4.src, ipv4.target))

    tcp = TCP(ipv4.data)
    print(TAB_1 + 'TCP Segment:')
    print(TAB_2 + 'Source Port: {}, Destination Port: {}'.format(tcp.src_port, tcp.dest_port))
    print(TAB_2 + 'Sequence: {}, Acknowledgment: {}'.format(tcp.sequence, tcp.acknowledgment))
    print(TAB_2 + 'Flags:')
    print(TAB_3 + 'URG: {}, ACK: {}, PSH: {}'.format(tcp.flag_urg, tcp.flag_ack, tcp.flag_psh))
    print(TAB_3 + 'RST: {}, SYN: {}, FIN:{}'.format(tcp.flag_rst, tcp.flag_syn, tcp.flag_fin))

    print(TAB_2 + 'HTTP Data:')
    try:
        http = HTTP(tcp.data)
        http_info = str(http.data).split('\n')
        for line in http_info:
            print(DATA_TAB_3 + str(line))
    except:
        print(format_multi_line(DATA_TAB_3, tcp.data))


def main():
    pcap = Pcap('capture.pcap')
    conn = socket.socket(socket.AF_PACKET, socket.SOCK_RAW, socket.ntohs(3))
    packageManager = PackageManager()
    print("\nSniffer iniciado...\n")

    while True:
        raw_data, addr = conn.recvfrom(65535)
        pcap.write(raw_data)
        receivedDatetimePacket = time.time()
        eth = Ethernet(raw_data)

        # IPv4
        if eth.proto == 8:
            ipv4 = IPv4(eth.data)

            # ICMP
            if ipv4.proto == 1:
                icmp = ICMP(ipv4.data)
                # print(format_multi_line(DATA_TAB_3, icmp.data))

            # TCP
            elif ipv4.proto == 6:
                tcp = TCP(ipv4.data)

                if len(tcp.data) > 0:

                    # HTTP
                    # if tcp.src_port == 8080 or tcp.dest_port == 8080:
                    if tcp.dest_port == 8080:
                        packageManager.receivePackage(eth, receivedDatetimePacket)

            # UDP
            elif ipv4.proto == 17:
                # print('\n\n\n\n\nERRO UDP: + ' + str(ipv4.data))
                udp = UDP(ipv4.data)

    pcap.close()


main()
