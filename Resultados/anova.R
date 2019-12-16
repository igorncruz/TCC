dados <- read.csv('./Projetos/TCC/Resultados/resumo-analises.csv', sep = ",") # Open file
#dados <- dados[-1] # remove the "Run" column

#View(dados)


dados$Lat = factor(dados$Lat)
dados$Perd = factor(dados$Perd)
dados$Proto = factor(dados$Proto)

#plot(dados)
boxplot(dados$Taxa~dados$Proto, xlab="Protocolo", ylab="Taxa de dados recebidos (em B/s)", main="Diagrama de caixas da taxa de dados recebidos\n por protocolo")
boxplot(dados$Taxa~dados$Perd, xlab="Perda de pacotes (em %)", ylab="Taxa de dados recebidos (em B/s)", main="Diagrama de caixas da taxa de dados recebidos\n por nível de perda de pacotes")
boxplot(dados$Taxa~dados$Lat, xlab="Latência (em ms)", ylab="Taxa de dados recebidos (em B/s)", main="Diagrama de caixas da taxa de dados recebidos\n por nível de latência")

interaction.plot(dados$Perd,dados$Lat,dados$Taxa,xlab = "Perda de pacotes definida (em %)", ylab = "Taxa (B/s)", trace.label = "Latência \n(em ms)", main="Interação entre perda de pacotes e latência")
interaction.plot(dados$Perd,dados$Proto,dados$Taxa,xlab = "Perda de pacotes (em %)", ylab = "Taxa (B/s)", trace.label = "Protocolo", main="Interação entre protocolo e perda de pacotes")
interaction.plot(dados$Lat,dados$Proto,dados$Taxa,xlab = "Latência definida (em ms)", ylab = "Taxa (B/s)", trace.label = "Protocolo", main="Interação entre protocolo e latência")

# ANOVA
aov1.out = aov(Taxa ~ ., data=dados) #Model considering only the variables with no interactions
summary(aov1.out)
aov1.out


aov2.out = aov(Taxa ~ .^2, data=dados) #Model considering only the variables with no interactions
summary(aov2.out)

aov3.out = aov(Taxa ~ .^3, data=dados) #Model considering only the variables with no interactions
summary(aov3.out)

plot(aov1.out,1)
plot(aov2.out)

aggregate(Taxa ~ Proto+Perd+Lat, dados, summary)
