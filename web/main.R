
setwd("/home/sam/Escritorio/usach/proyecto_bio/Proyecto 1/web") #Cambiar por tu directorio
# source("/usr/lib/R/library/")         #Carga un conjunto de paquetes
# cat("\014")                                 #Limpiar consola
# library(Biobase)
# library(GEOquery)
# library(plyr)
# library(siggenes)
library(ape)
library(phangorn)


#===================================
#1 Lectura de ?rboles
#===================================
tree1=read.tree('uploads/tree1.tree')
tree2=read.tree('uploads/tree2.tree')


#===================================
#2 Plotear arboles
#===================================
par(mfrow=c(1,4))
plot(tree1,main="tree1")
edgelabels(round(tree1$edge.length,1),cex=0.6,bg = "white")
plot(tree2,main="tree2")
edgelabels(round(tree2$edge.length,1),cex=0.6,bg = "white")

#===================================
#3 Distancia entre ?rboles
#===================================
distancias=NULL
distancias=round(treedist(tree1,tree2),1)
#cat("=======================================\n")
#cat("- \t Distancias entre tree1 and tree2\n")
#cat("=======================================\n")
print(distancias)
write(distancias, 'uploads/distancias.txt')


#===================================
#4 Estimaci?n de longitud de las ramas (cuando no existen)
#===================================
tree3=tree2
tree3$edge.length=NULL                        #Eliminaci?n de ramas
plot(tree3,main="tree3")
data=as.phyDat(read.dna("uploads/sequence.seq")) #Eliminaci?n de ramas #read.aa
tree3=optim.parsimony(tree3, data,trace = F)  #Optimizaci?n de parsimonia
tree3=acctran(tree3,data)                     #Estimaci?n de ramas
plot(tree3,main="tree3 con ramas")
edgelabels(round(tree3$edge.length,1),cex=0.6,bg = "white")

#===================================
#5 N?mero de sub?rboles
#===================================
stree1=subtrees(tree1)                  #sub?rboles tree1
stree2=subtrees(tree2)                  #sub?rboles tree2
matriz=matrix(0,length(stree1),length(stree2))
for (a in 1:length(stree1))
{ {for (b in 1:length(stree2))
    matriz[a,b]=as.numeric(all.equal(stree1[[a]],stree2[[b]]))
  }
}
# print(matriz)
 
#===================================
#6 Guardar ?rboles
#===================================
write.tree(tree1,"tree1_saved.tree")

