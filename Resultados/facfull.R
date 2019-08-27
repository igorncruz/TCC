r = c()
lat=c("l1","l2","l3")
proto=c("http","mqtt","coap")
perd=c("p1","p2","p3")
#para cada protocolo
for (pr in proto) {
    #para cada perda
    for (pe in perd) {
      #para cada latencia
      for (l in lat) {
        read.csv()
        #pega dado do csv
        print(paste(pr,"qaaa",pe,sep="",l))
        #pega somente 30
        #anexa ao r
        r=c(r,a)
      }
  }
}

#r = c(20,30,14,13)
# 20 é L10,P25,HTTP
# 30 é L10,P25,HTTP
# 14 é L100,P25,HTTP
# 13 é L100,P25,HTTP
# 3 é L400,P25,HTTP
# 4 é L400,P25,HTTP
# x é L10,P15,HTTP
# x é L10,P15,HTTP
# x é L100,P15,HTTP
# x é L100,P15,HTTP
# x é L400,P15,HTTP
# x é L400,P15,HTTP
# x é L10,P0,HTTP
f1 = c("L10", "L100", "L400") # 1st factor levels 
f2 = c("P25", "P15", "P0")    # 2nd factor levels 
f3 = c("HTTP", "COAP", "MQTT")
k1 = length(f1)          # number of 1st factors 
k2 = length(f2)          # number of 2nd factors 
k3 = length(f3)
n = 30                    # repeticoes
tm1 = gl(k1, n, n*k1*k2*k3, factor(f1))
tm2 = gl(k2,n*k1,n*k1*k2*k3,factor(f2))
tm3 = gl(k3,n*k1*k2,n*k1*k2*k3,factor(f3))
av = aov(r ~ tm1 * tm2 * tm3)
summary(av)