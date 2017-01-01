#Distancias entre árboles
# setwd("C:/Users/elper/Downloads/Proyecto 1") #Cambiar por tu directorio
# source("C:/Users/elper/Downloads/Proyecto 1/sources/system/packages.R") 
# install.packages("Rserve")
library(phangorn)

tree1=read.tree("uploads/tree1.tree")
tree2=read.tree("uploads/tree2.tree")
distancias=NULL
distancias=round(treedist(tree1,tree2),1)
#diferencia simetrica
cat(paste(attr(distancias[1], 'names', exact = FALSE) ,distancias[1]), ';')
cat(paste(attr(distancias[2], 'names', exact = FALSE) ,distancias[2]), ';')
cat(paste(attr(distancias[3], 'names', exact = FALSE) ,distancias[3]), ';')
cat(paste(attr(distancias[4], 'names', exact = FALSE) ,distancias[4]), ';')


# #diferencia de puntaje de ramas
# print(distancias[2])
# #diferencia de caminos
# print(distancias[3])
# #diferencia cuadrática de caminos
# print(distancias[4])