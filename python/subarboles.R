#Obtiene subarboles
# setwd("C:/Users/elper/Downloads/Proyecto 1") #Cambiar por tu directorio
# source("C:/Users/elper/Downloads/Proyecto 1/sources/system/packages.R") 
# install.packages("Rserve")
library(phangorn)
tree1=read.tree("uploads/tree1.tree")
stree1=subtrees(tree1)                  #subárboles tree1
print(length(stree1))
for (a in 1:length(stree1))
  print(stree1[a])