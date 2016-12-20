<?php 

exec("Rscript  main.R >> r.log 2>&1 ", $result);
system("Rscript  main.R >> r.log 2>&1 ");