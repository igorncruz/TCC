dados <- read.csv('./Projetos/TCC/Resultados/resumo-analises.csv', sep = ",") # Open file
#dados <- dados[-1] # remove the "Run" column

View(dados)


dados$Lat = factor(dados$Lat)
dados$Perd = factor(dados$Perd)
dados$Proto = factor(dados$Proto)

#plot(dados)

interaction.plot(dados$Perd,dados$Lat,dados$Taxa)
interaction.plot(dados$Perd,dados$Proto,dados$Taxa)
interaction.plot(dados$Lat,dados$Proto,dados$Taxa)
boxplot(dados$Taxa~dados$Lat)
boxplot(dados$Taxa~dados$Perd)
boxplot(dados$Taxa~dados$Proto)

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