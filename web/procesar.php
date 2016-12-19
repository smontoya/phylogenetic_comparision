<?php 

exec("Rscript  main.R >> r.log 2>&1 ", $result);
var_dump($result);