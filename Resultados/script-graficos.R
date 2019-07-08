dados_http_l2_p2_v3 = read.csv("Projetos/TCC/Resultados/http/http_factor_l2_p2_v3_result.csv")
dados_http_l3_p3_v3 = read.csv("Projetos/TCC/Resultados/http/http_factor_l3_p3_v3_result.csv")
dados_http_l3_p3_v2 = read.csv("Projetos/TCC/Resultados/http/http_factor_l3_p3_v2_result.csv")
dados_http_l3_p3_v3 = dados_http_l3_p3_v3$TAX_MED_LEN_PKG_POR_SEG[2:32]

# dados_http_l3_v3_p3 = read.csv("Projetos/TCC/Resultados/http/http_factor_l3_v3_p3_result__2019-01-11.txt.csv")
# dados_http_l2_v2_p2 = read.csv("Projetos/TCC/Resultados/http/http_factor_l2_v2_p2_result__2019-01-11.txt.csv")
# 
# dados_mqtt_l3_v3_p3 = read.csv("Projetos/TCC/Resultados/mqtt/mqtt_factor_l3_v3_p3_result__2019-01-15.txt.csv")
# dados_mqtt_l2_v2_p2 = read.csv("Projetos/TCC/Resultados/mqtt/mqtt_factor_l2_v2_p2_result__2019-01-15.txt.csv")
# dados_mqtt_l1_v1_p1 = read.csv("Projetos/TCC/Resultados/mqtt/mqtt_factor_l1_v1_p1_result__2019-01-16.txt.csv")
# dados_coap_l3_v3_p3 = read.csv("Projetos/TCC/Resultados/coap/coap_factor_l3_v3_p3_result__2019-01-14.txt.csv")
# dados_coap_l2_v2_p2 = read.csv("Projetos/TCC/Resultados/coap/coap_factor_l2_v2_p2_result__2019-01-14.txt.csv")
# dados_coap_l1_v1_p1 = read.csv("Projetos/TCC/Resultados/coap/coap_factor_l1_v1_p1_result__2019-01-14.txt.csv")

plot(dados_http_l3_v3_p3$TAX_MED_LEN_PKG_POR_SEG)
boxplot(dados_http_l3_v3_p3$TAX_MED_LEN_PKG_POR_SEG[1:30],dados_mqtt_l3_v3_p3$TAX_MED_LEN_PKG_POR_SEG[1:30],dados_mqtt_l3_v3_p3$TAX_MED_LEN_PKG_POR_SEG[1:31])