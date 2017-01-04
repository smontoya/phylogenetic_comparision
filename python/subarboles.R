# setwd("/Users/maurorios/Downloads/Proyecto_filogenia/Proyecto 1") #Cambiar por tu directorio
# source("/Users/maurorios/Downloads/Proyecto_filogenia/Proyecto 1/sources/system/packages.R")         #Carga un conjunto de paquetes
library(ape)
library(phangorn)
cat("\014")                                 #Limpiar consola

tree1=read.tree("data/tree1.tree")
tree2=read.tree("data/tree1.tree")

stree1=subtrees(tree1)                  #sub?rboles tree1
stree2=subtrees(tree2)                  #sub?rboles tree2
matriz=matrix(0,length(stree1),length(stree2))
for (a in 1:length(stree1))
{ {for (b in 1:length(stree2))
  matriz[a,b]=as.numeric(all.equal(stree1[[a]],stree2[[b]]))
}
}
info = ''
texto =''
contador = 1
for( c in 1:dim(matriz)[1]){
  for( d in 1:dim(matriz)[2]){
    if(matriz[c,d] == 1){
        print(paste('arbol',contador))
        print('informacion del arbol :')
        print(paste('numero de nodos :',stree1[[c]]$Nnode))
        print(paste('numero de hojas :',stree1[[c]]$Ntip))
        contador = contador + 1
      for(e in 1:length(stree1[[c]]$tip)){
        info = stree1[[c]]$tip.label[e]
        print(info)
      }
      print('---')
    }
  }
}
