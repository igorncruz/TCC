#-----------------------------#
#--- Factorial Design in R ---#
#-----------------------------#

options(scipen=999)


dados <- read.csv2('./Projetos/TCC/Resultados/resumo-analises.csv', sep = ",") # Open file
#dados <- dados[-1] # remove the "Run" column

View(dados)

dadosMedida = dados[,c(1:4,10)]# media
#dadosMedida = dados[,c(1:4,6)]# mediana
#dadosMedida = dados[,c(1:4,8)] #erro padrão
#dadosMedida = dados[,c(1:4,9)] #Margem de erro
#dadosMedida = dados[,c(1:4,11)] #Primeiro Quartis
#dadosMedida = dados[,c(1:4,12)] #Segundo Quartis
#dadosMedida = dados[,c(1:4,13)] #Terceiro Quartis
#dadosMedida = dados[,c(1:4,14)] #IntervaloConfMediaMais
#dadosMedida = dados[,c(1:4,15)] #IntervaloConfMediaMenos
#dadosMedida = dados[,c(1:4,16)] #RegressaoLinearCoeficientsinteceptBeta0
#dadosMedida = dados[,c(1:4,17)] #RegressaoLinearCoeficientsinteceptBeta1
# dadosMedida = dados[,c(1:4,22)] #Correlação - R 
# dadosMedida = dados[,c(1:4,23)] #Coeficiente de Determinação - R²
# Convert into factors
dadosMedida$Mix = factor(dadosMedida$Mix,levels=c("0_100","25_75","50_50","75_25","100_0"))
dadosMedida$Algoritmos = factor(dadosMedida$Algoritmos)
dadosMedida$Pontos.Modelo = factor(dadosMedida$Pontos.Modelo)
dadosMedida$Usuarios.Virtuais = factor(dadosMedida$Usuarios.Virtuais)

#removendo os pontos 0
#dadosMedida = dadosMedida[dadosMedida$Pontos.Modelo!=0,]
#dadosMedida = dadosMedida[dadosMedida$Usuarios.Virtuais!=1,]

# A few plots can help us see the data
plot(dados)

# par(mfrow=c(2,2))


interaction.plot(dados$Taxa, dados$Lat, 
                 dadosMedida$Media, 
                 main = "Interação entre a quantidade\n de Pontos do Modelo e os\n Usuários Virtuais no Tempo", 
                 ylab = "Tempo Médio de Resposta (ms)", 
                 xlab = "Pontos do Modelo", 
                 trace.label = "Usuários Virtuais")

interaction.plot(dadosMedida$Pontos.Modelo, dadosMedida$Algoritmos, 
                 dadosMedida$Media, 
                 main = "Interação entre a quantidade\n de Pontos do Modelo e os\n Algoritmos no Tempo", 
                 ylab = "Tempo Médio de Resposta (ms)", 
                 xlab = "Pontos do Modelo", 
                 trace.label = "Algoritmo")

interaction.plot(dadosMedida$Mix, dadosMedida$Algoritmos, 
                 dadosMedida$Media, 
                 main = "Interação entre o Mix Modelo/Interpolação e os\n Algoritmos no Tempo", 
                 ylab = "Tempo Médio de Resposta (ms)", 
                 xlab = "Mix Modelo/Interpolação", 
                 trace.label = "Algoritmo")

interaction.plot(dadosMedida$Usuarios.Virtuais, dadosMedida$Algoritmos, 
                 dadosMedida$Media, 
                 main = "Interação entre a quantidade\n de Usuários Virtuais e os\n Algoritmos no Tempo", 
                 ylab = "Tempo Médio de Resposta (ms)", 
                 xlab = "Usuários Virtuais", 
                 trace.label = "Algoritmo")

interaction.plot(yield$Lat,yield$Proto,yield$Taxa)
interaction.plot(yield$Perd,yield$Proto,yield$Taxa) 

par(mfrow=c(1,1))

par(mfrow=c(2,2))



boxplot(Media~Mix, data=dadosMedida, main="Tempo de Resposta por Tipo de \nRequisição Mix modelo/Interpolação",
        xlab="Mix modelo/Interpolação",ylab="Tempo de Resposta (ms)")

boxplot(Media~Algoritmos, data=dadosMedida, main="Tempo de Resposta \npor Algoritmo",
        xlab="Algoritmo ",ylab="Tempo de Resposta (ms)")

boxplot(Media~Pontos.Modelo, data=dadosMedida, main="Tempo de Resposta \npor Pontos do Modelo",
        xlab="Pontos do Modelo",ylab="Tempo de Resposta (ms)")

boxplot(Media~Usuarios.Virtuais, data=dadosMedida, main="Tempo de Resposta \npor Usuários Virtuais",
        xlab="Usuários Virtuais",ylab="Tempo de Resposta (ms)")

par(mfrow=c(1,1))

# ANOVA
aov1.out = aov(Media ~ ., data=dadosMedida) #Model considering only the variables with no interactions
summary(aov1.out)

aov2.out = aov(Media ~ .^2, data=dadosMedida) #Model considering two variable interactions
summary(aov2.out)

aov3.out = aov(Media ~ .^3, data=dadosMedida) #Model considering three variable interactions
summary(aov3.out)

aov4.out = aov(Media ~ .^4, data=dadosMedida) #Model considering four variable interactions
summary(aov4.out)

# You can plot the ANOVA results in a couple of ways:

plot(aov1.out, 1)           # residuals versus fitted values
plot(aov1.out, 2)           # QQ plot 
