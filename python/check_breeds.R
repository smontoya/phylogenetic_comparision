#check_newick
# setwd("C:/Users/elper/Downloads/Proyecto 1") #Cambiar por tu directorio
# source("C:/Users/elper/Downloads/Proyecto 1/sources/system/packages.R")
# source("C:/Users/elper/Desktop/Proyecto 2.0/R/newick_format.R")
# install.packages("Rserve")
library(phangorn)

tree1=read.tree("uploads/tree1.tree")
tree2=read.tree("uploads/tree2.tree")
validador = 1

if (is.null(tree1$edge.length)){
  cat(4)
  validador = 0
}  else{
 if (is.null(tree2$edge.length)){
    cat(5)
    validador = 0
  } 
}
if(validador == 1){
  largo_cantidad_especies_arbol1 = length(tree1[3]$tip.label)
  largo_cantidad_especies_arbol2 = length(tree1[3]$tip.label)
  mismas_especies = NULL;
  contador = 0

  if(largo_cantidad_especies_arbol1 == largo_cantidad_especies_arbol2){
    for(a in 1:largo_cantidad_especies_arbol1){
      for(b in 1:largo_cantidad_especies_arbol2){
        
        if(tree1[3]$tip.label[a] == tree2[3]$tip.label[b] ){
          contador = contador + 1
        }
      }
    }
    
    if(contador == largo_cantidad_especies_arbol2){
      cat(1)
    }else{
      cat(3)
    }
  }else{
    cat(2)
  }
}



#Opciones de print
# 1 Tienen mismas especies
# 2 distinta cantidad de especies
# 3 misma cantidad pero no mismas especies
