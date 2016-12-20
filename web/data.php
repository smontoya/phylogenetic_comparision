<?php

$arbol1 = trim(file_get_contents("uploads/tree1.tree"));
$arbol2 = trim(file_get_contents("uploads/tree2.tree"));

$data = explode(" ", trim(file_get_contents("uploads/distancias.txt")));
?>

<!DOCTYPE html>
<html>
<head>
  <meta charset="utf-8">
  <meta http-equiv="X-UA-Compatible" content="IE=edge">
  <title>Phylogenetic | Comparator</title>
  <!-- Tell the browser to be responsive to screen width -->
  <meta content="width=device-width, initial-scale=1, maximum-scale=1, user-scalable=no" name="viewport">
  <!-- Bootstrap 3.3.6 -->
  <link rel="stylesheet" href="css/bootstrap.min.css">
  <!-- Font Awesome -->
  <!-- <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.5.0/css/font-awesome.min.css">
  Ionicons
  <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/ionicons/2.0.1/css/ionicons.min.css"> -->
  <!-- Theme style -->
  <link rel="stylesheet" href="css/AdminLTE.min.css">
  <link rel="stylesheet" href="css/skins/_all-skins.min.css">
</head>
<body class="hold-transition skin-blue sidebar-mini">
<div class="wrapper">

  <header class="main-header">
    <a href="#" class="logo">
      <span class="logo-mini"><b>P</b>C</span>
      <span class="logo-lg"><b>Phylogenetic</b> Comparator</span>
    </a>
    <nav class="navbar navbar-static-top">
      <!-- Sidebar toggle button-->
      <a href="#" class="sidebar-toggle" data-toggle="offcanvas" role="button">
        <span class="sr-only">Toggle navigation</span>
        <span class="icon-bar"></span>
        <span class="icon-bar"></span>
        <span class="icon-bar"></span>
      </a>
    </nav>
  </header>
  <!-- Left side column. contains the sidebar -->
  <aside class="main-sidebar">
    <!-- sidebar: style can be found in sidebar.less -->
    <section class="sidebar">
      <ul class="sidebar-menu" role="tablist">
        <li class="active" role="presentation">
          <a href="#comparacion" role="tab" data-toggle="tab"  aria-controls="comparacion"><i class="fa fa-book"></i>
             <span>Comparación</span></a>
        </li> 
        <li role="presentation">
          <a href="#distancias" role="tab" data-toggle="tab"  aria-controls="distancias">
            <i class="fa fa-book"></i> <span>Distancias</span></a>
        </li> 
        <li role="presentation">
          <a href="#buscador" role="tab" data-toggle="tab"  aria-controls="distancias">
            <i class="fa fa-search"></i> <span>Buscador</span></a>
        </li> 
      </ul>
    </section>
  </aside>

  <!-- =============================================== -->

  <!-- Content Wrapper. Contains page content -->
  <div class="content-wrapper">
    <!-- Content Header (Page header) -->
    <section class="content-header">
      <h1>
        Resultado
        <small>Comparación de arboles</small>
      </h1>
    </section>

    <!-- Main content -->
    <section class="content">
      <div class="tab-content">
        <div role="tabpanel" class="tab-pane active" id="comparacion">
          <div class="box">
            <div class="box-body">
              <div id='phylograms'></div>
            </div>
          </div>  

        </div>
        <div role="tabpanel" class="tab-pane" id="distancias">
          <div class="box">

          <table class="table table-bordered">
            <thead>
              <td>symmetric.difference</td>
              <td>branch.score.difference</td>
              <td>path.difference</td>
              <td>quadratic.path.difference</td>
            </thead>
            <tr>
              <td> <?php echo $data[0]; ?> </td>
              <td> <?php echo $data[1]; ?> </td>
              <td> <?php echo $data[2]; ?> </td>
              <td> <?php echo $data[3]; ?> </td>              
            </tr>
          </table>
          </div>
        </div>
        <div role="tabpanel" class="tab-pane" id="buscador">
          <div class="box">
            
            <input type="text" id="especie_find">
            <br>
            <ul id="elements_list">
              
            </ul>
          </div>

        </div>
        <div role="tabpanel" class="tab-pane" id="settings">...</div>
      </div>

    </section>
  </div>

  <footer class="main-footer">
    <div class="pull-right hidden-xs"></div>
    <strong>Usach 2016 </strong>
  </footer>
  <div class="control-sidebar-bg"></div>
</div>
<!-- ./wrapper -->

<!-- jQuery 2.2.3 -->
<script src="js/jquery.min.js"></script>
<!-- Bootstrap 3.3.6 -->
<script src="js/bootstrap.min.js"></script>
<!-- AdminLTE App -->
<script src="js/app.min.js"></script>
<!-- AdminLTE for demo purposes -->
<script src="js/demo.js"></script>
<script src="http://d3js.org/d3.v3.min.js" type="text/javascript"></script>
<script src="js/newick.js" type="text/javascript"></script>
<script src="js/d3.phylogram.js" type="text/javascript"></script>
<script type="text/javascript">
$(function() {
    var arbol1 = Newick.parse("<?php echo $arbol1;?>");
    var arbol2 = Newick.parse("<?php echo $arbol2;?>");
    var newickNodes = []
    function buildNewickNodes(node, callback) {
      newickNodes.push(node)
      if (node.branchset) {
        for (var i=0; i < node.branchset.length; i++) {
          buildNewickNodes(node.branchset[i])
        }
      }
    }
    buildNewickNodes(arbol1)
    buildNewickNodes(arbol2)
    
   /* d3.phylogram.buildRadial('#radialtree', newick, {
      width: 400,
      skipLabels: true
    })*/
    
    d3.phylogram.build('#phylograms', arbol1, {
      width: 300,
      height: 650
    });
    d3.phylogram.build('#phylograms', arbol1, {
      width: 300,
      height: 650
    }, true);
    function get_elements (elements){
      var array_elem = []
      if ('branchset' in elements){
        for (index in elements['branchset']){
          if (elements['branchset'][index]['name'].length > 0)
            array_elem.push(elements['branchset'][index]['name']);
          if ('children' in elements['branchset'][index]){
            for (index_ch in elements['branchset'][index]['children']){
              array_elem = array_elem.concat(get_elements(elements['branchset'][index]['children'][index_ch]));
            }
          }
        }
      }
      if ('children' in elements){
        for (index in elements['children']){
          array_elem = array_elem.concat(get_elements(elements['children'][index]));
        }
      }
      return array_elem
    }
    function dibujar_elementos(elementos){
      $("#elements_list").empty();
      for (elem in elementos){
        $("#elements_list").append('<li>'+elementos[elem]+'</li>');
      }
    }
    var elementos = get_elements(arbol1);
    dibujar_elementos(elementos);
    $("#buscador").on("change", function(){
      substring  = '';
      sublist = [];
      for (index in elementos){
        if (elementos[index].indexOf(substring) !== -1){
          hola = 1;
        }
      }
    })
});
</script>

</body>
</html>
