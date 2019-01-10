import pcap, dpkt, socket, datetime, sys, os
from pathlib import Path
# Se o cliente for executado no windows ou Visual Code, descomentar a linha abaixo
# sys.path.insert(0, str(Path().resolve()))
# Se o cliente for executado no linux, descomentar a linha abaixo
sys.path.insert(0, str(Path().resolve().parent))
import util


class Package():
    def __init__(self, timestamp, pkt):
        try:
            eth = dpkt.ethernet.Ethernet(pkt)  #extraindo dados do pacote
            if isinstance(eth.data, dpkt.ip.IP):
                ip = eth.data
                if isinstance(ip.data, dpkt.tcp.TCP):
                    tcp = ip.data
                    self.timestamp = timestamp
                    self.readableTS = str(
                        datetime.datetime.utcfromtimestamp(timestamp))
                    self.destAddress = socket.inet_ntoa(ip.dst)
                    self.srcAddress = socket.inet_ntoa(ip.src)
                    self.id = ip.id
                    self.lenPkg = ip.len
                    self.destPort = tcp.dport
                    self.srcPort = tcp.sport
                    self.data = tcp.data
                    self.lenPayload = len(tcp.data)
        except (dpkt.dpkt.NeedData, dpkt.dpkt.UnpackError):
            pass

    def __str__(self):
        return '{}: {} | {} | {} | {}'.format(util.getFormattedDatetimeWithMillisec(self.timestamp), self.id, self.lenPkg, self.lenPayload, self.data)

class PackagePair():
    def __init__(self, sent, received = None):
        self.sent = sent
        self.received = received

    def findReceivedPair(self, packageReceivedList):
        tsLimit = util.addSecs(self.sent.timestamp, 60).timestamp()
        for pkg in packageReceivedList:
            if pkg.timestamp > tsLimit:
                break
            elif pkg.timestamp < self.sent.timestamp:
                continue
            elif (pkg.id == self.sent.id):
                self.received = pkg
                self.__calculateMetrics__()
                return True
        return False

    def __calculateMetrics__(self):
        self.delay = self.received.timestamp - self.sent.timestamp
        if (self.delay < 0):
            print('pacote enviado às {} e recebido às {}'.format(
                util.getFormattedDatetimeWithMillisec(self.sent.timestamp),
                util.getFormattedDatetimeWithMillisec(self.received.timestamp)))


class Repetition():
    averageDelay = -1
    averagePkgLen = -1
    averagePkgLenDelay = -1
    averagePayloadLen = -1
    averagePayloadLenDelay = -1
    ratePkgPerSec = -1
    pkgLost = -1

    def __init__(self, startTimestamp, endTtimestamp, listPackagesClient, listPackagesServer):
        self.startTimestamp = startTimestamp
        self.endTtimestamp = endTtimestamp
        self.listPackages = self.__extractPackages__(listPackagesClient, listPackagesServer)
        print('criando repetição de {} à {} com {} pacotes'.format(
            util.getFormattedDatetimeWithMillisec(startTimestamp),
            util.getFormattedDatetimeWithMillisec(endTtimestamp),
            len(self.listPackages)))
        self.calculateMetrics()


    def __extractPackages__(self, listPackagesClient, listPackagesServer):
        if len(listPackagesClient) > 0:
            self.pkgLost = 0

        list = []
        for pkg in listPackagesClient:
            if (pkg.timestamp >= self.endTtimestamp):
                break
            elif (pkg.timestamp < self.startTimestamp):
                continue
            pkgPair = PackagePair(pkg)
            if pkgPair.findReceivedPair(listPackagesServer):
                list.append(pkgPair)
            else:
                self.pkgLost += 1
        return list


    def calculateMetrics(self): #Calcula a média do atraso DA REPETIÇÃO
        if len(self.listPackages) == 0:
            return

        sumDelay = 0 #Incremento das diferenças
        sumPkgLen = 0
        sumPkgLenDelay = 0
        sumPayloadLen = 0
        sumPayloadLenDelay = 0
        for pkg in self.listPackages:
            sumDelay += pkg.delay
            sumPkgLen += pkg.received.lenPkg
            sumPkgLenDelay += (pkg.received.lenPkg/pkg.delay)
            sumPayloadLen += pkg.received.lenPayload
            sumPayloadLenDelay += (pkg.received.lenPayload/pkg.delay)
        self.averageDelay = sumDelay / len(self.listPackages)
        self.averagePkgLen = sumPkgLen / 60
        self.averagePkgLenDelay = sumPkgLenDelay / len(self.listPackages)
        self.averagePayloadLen = sumPayloadLen / 60
        self.averagePayloadLenDelay = sumPayloadLenDelay / len(self.listPackages)
        self.ratePkgPerSec = len(self.listPackages) / 60




class Analyze():
    secondsForEachRep = 60 #Cada repetição dura 1 min
    def __init__(self, pcapFileFromServer, pcapFileFromClient, outputFileName):
        self.outputFileName = outputFileName
        self.pcapFileFromClient = pcapFileFromClient
        self.pcapFileFromServer = pcapFileFromServer
        self.listPackageServer = self.__extractPackages__(self.pcapFileFromServer)
        self.listPackageClient = self.__extractPackages__(self.pcapFileFromClient)
        self.generateReps()

    def __extractPackages__(self, pcapFile):
        list = []
        for ts, pkt in pcap.pcap(pcapFile):
            pkg = Package(ts, pkt)
            if (pkg.id > 0):
                list.append(pkg)
        list.sort(key=lambda x: x.timestamp, reverse=False)
        return list

    def generateReps(self):
        self.reps = []
        startTS = self.listPackageClient[0].timestamp
        endTS = self.listPackageServer[-1].timestamp
        while (startTS <= endTS):
            print('processando repetição : {}'.format(len(self.reps)))
            endTSAux = util.addSecs(startTS, self.secondsForEachRep).timestamp()
            self.reps.append(Repetition(startTS, endTSAux, self.listPackageClient, self.listPackageServer))
            startTS = endTSAux

    def generateFile(self):
        self.generateFileTXT()
        self.generateFileCSV()

    def generateFileCSV(self):
        try:
            os.remove(self.outputFileName+'.csv')
        except OSError:
            pass
        path = self.outputFileName+'.csv'
        file = open(path, 'w')
        file.write(
            'QTD_PACOTES,MED_ATRASO,TAX_MED_LEN_PKG,TAX_MED_LEN_PKG_POR_SEG,TAX_MED_LEN_PAYLOAD,TAX_MED_LEN_PAYLOAD_POR_SEG,TAX_PKG_POR_SEG,QTD_PKG_PERDIDOS'
        )
        for rep in self.reps:
            file.write('\n{},{},{},{},{},{},{},{}'.format(len(rep.listPackages), rep.averageDelay,
                rep.averagePkgLenDelay, rep.averagePkgLen, rep.averagePayloadLenDelay,
                rep.averagePayloadLen, rep.ratePkgPerSec, rep.pkgLost))
        file.close()

    def generateFileTXT(self):
        try:
            os.remove(self.outputFileName+'.txt')
        except OSError:
            pass
        path = self.outputFileName+'.txt'
        file = open(path, 'w')
        file.write('Início no servidor às: {}\n'.format(self.listPackageServer[0]))
        file.write('Fim no servidor às: {}\n'.format(self.listPackageServer[-1]))
        file.write('Quantidade total de pacotes no servidor: {}\n'.format(
            len(self.listPackageServer)))
        file.write('Início no cliente às: {}\n'.format(self.listPackageClient[0]))
        file.write('Fim no cliente às: {}\n'.format(
            self.listPackageClient[-1]))
        file.write('Quantidade total de pacotes no cliente: {}\n'.format(
            len(self.listPackageClient)))
        file.write('Quantidade total de repetições: {}'.format(len(self.reps)))
        file.write('\n\n')
        for i in range(0, len(self.reps)):
            rep = self.reps[i]
            file.write('\nRepetição {}\n'.format(i+1))
            file.write('Início às: {}\n'.format(
                util.getFormattedDatetimeWithMillisec(rep.startTimestamp)))
            file.write('Fim às: {}\n'.format(
                util.getFormattedDatetimeWithMillisec(rep.endTtimestamp)))
            file.write('Quantidade total de pacotes: {}\n'.format(
                len(rep.listPackages)))
            file.write('Atraso médio dos pacotes: {}\n'.format(
                rep.averageDelay))
            file.write('Taxa média de pacotes (média(tamanho pkt/atraso pkt)): {}\n'.format(
                rep.averagePkgLenDelay))
            file.write('Taxa média de pacotes por seg (sum(tamanho pkt)/300): {}\n'.format(
                rep.averagePkgLen))
            file.write('Taxa média de payload dos pacotes por seg (sum(tamanho payload)/300): {}\n'.format(
                rep.averagePayloadLen))
            file.write('Taxa média de payload dos pacotes (média(tamanho payload/atraso pkt)): {}\n'.format(
                rep.averagePayloadLenDelay))
            file.write('Taxa de pacotes por segund (total pkt/300)): {}\n'.format(rep.ratePkgPerSec))
            file.write('Quantidade de pacotes perdidos: {}\n'.format(rep.pkgLost))

        file.close()



def main():
    analise = Analyze('http/notebook/http_no_factor_server__2019-01-09-v2.pcap',
                      'http/rPi/http_no_factor_client__2019-01-09-v2.pcap',
                      'http/http_no_factor_result__2019-01-09-v2.txt')
    analise.generateFile()

if __name__ == '__main__':
    main()
