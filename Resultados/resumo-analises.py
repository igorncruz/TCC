import os


def main():
    protocolos = {'http': "HTTP", 'coap': "COAP", 'mqtt': "MQTT"}
    latencias = {'l1': 400, 'l2': 100, 'l3': 10}
    perdas = {'p1': 25, 'p2': 15, 'p3': 0}
    resumo = []
    repeticoesConsiderar = 30

    for protocolo in protocolos.keys():
        for latencia in latencias.keys():
            for perda in perdas.keys():
                nomeArquivo = '{}_factor_{}_{}_v3_result.csv'.format(
                    protocolo, latencia, perda)
                caminhoArquivo = "Resultados/{}/analise/{}".format(
                    protocolo, nomeArquivo)
                file = open(caminhoArquivo, 'r')
                linhas = file.readlines()
                for index in range(2, repeticoesConsiderar):
                    taxa = linhas[index].split(',')[3]
                    resumoValue = "{},{},{},{}".format(
                        taxa, latencias.get(latencia), perdas.get(perda),
                        protocolos.get(protocolo))
                    print(resumoValue)
                    resumo.append(resumoValue)
    resumoFileName = "./Resultados/resumo-analises.csv"
    try:
        os.remove(resumoFileName)
    except OSError:
        pass
    resumoFile = open(resumoFileName, 'w')
    resumoFile.write("Taxa,Lat,Perd,Proto")
    for resumoLine in resumo:
        resumoFile.write('\n' + resumoLine)
    resumoFile.close()


if __name__ == "__main__":
    main()
