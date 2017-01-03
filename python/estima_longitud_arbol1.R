#estimación de longuitud de ramas
# setwd("C:/Users/elper/Downloads/Proyecto 1") #Cambiar por tu directorio
# source("C:/Users/elper/Downloads/Proyecto 1/sources/system/packages.R") 
# install.packages("Rserve")
library(phangorn)
tree1=read.tree("uploads/tree1.tree")
tree3=tree1
tree3$edge.length=NULL
result <- tryCatch({
    data=as.phyDat(read.dna("uploads/sequence1.seq")) #Eliminación de ramas #read.aa
    tree3=optim.parsimony(tree3, data,trace = F)  #Optimización de parsimonia
    tree3=acctran(tree3,data)                     #Estimación de ramas
    write.tree(tree3,"uploads/tree1.tree")
    cat(0)
}, warning = function(w) {
    cat(1)
}, error = function(e) {
    cat(1)
}   );
