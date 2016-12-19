<?php 

exec("Rscript  main.R >> /var/log/r.log 2>&1 ", $result);
var_dump($result);