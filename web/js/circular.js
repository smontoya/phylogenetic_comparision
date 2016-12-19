var r = 960 / 2;

var cluster = d3.layout.cluster()
    .size([360, 1])
    .sort(null)
    .value(function(d) { return d.length; })
    .children(function(d) { return d.branchset; })
    .separation(function(a, b) { return 1; });

function project(d) {
  var r = d.y, a = (d.x - 90) / 180 * Math.PI;
  return [r * Math.cos(a), r * Math.sin(a)];
}

function cross(a, b) { return a[0] * b[1] - a[1] * b[0]; }
function dot(a, b) { return a[0] * b[0] + a[1] * b[1]; }

function step(d) {
  var s = project(d.source),
      m = project({x: d.target.x, y: d.source.y}),
      t = project(d.target),
      r = d.source.y,
      sweep = d.target.x > d.source.x ? 1 : 0;
  return (
    "M" + s[0] + "," + s[1] +
    "A" + r + "," + r + " 0 0," + sweep + " " + m[0] + "," + m[1] +
    "L" + t[0] + "," + t[1]);
}

var wrap = d3.select("#vis").append("svg")
    .attr("width", r * 2)
    .attr("height", r * 2)
    .style("-webkit-backface-visibility", "hidden");

// Catch mouse events in Safari.
wrap.append("rect")
    .attr("width", r * 2)
    .attr("height", r * 2)
    .attr("fill", "none")

var vis = wrap.append("g")
    .attr("transform", "translate(" + r + "," + r + ")");

var start = null,
    rotate = 0,
    div = document.getElementById("vis");

function mouse(e) {
  return [
    e.pageX - div.offsetLeft - r,
    e.pageY - div.offsetTop - r
  ];
}

wrap.on("mousedown", function() {
  wrap.style("cursor", "move");
  start = mouse(d3.event);
  d3.event.preventDefault();
});
d3.select(window)
  .on("mouseup", function() {
    if (start) {
      wrap.style("cursor", "auto");
      var m = mouse(d3.event);
      var delta = Math.atan2(cross(start, m), dot(start, m)) * 180 / Math.PI;
      rotate += delta;
      if (rotate > 360) rotate %= 360;
      else if (rotate < 0) rotate = (360 + rotate) % 360;
      start = null;
      wrap.style("-webkit-transform", null);
      vis
          .attr("transform", "translate(" + r + "," + r + ")rotate(" + rotate + ")")
        .selectAll("text")
          .attr("text-anchor", function(d) { return (d.x + rotate) % 360 < 180 ? "start" : "end"; })
          .attr("transform", function(d) {
            return "rotate(" + (d.x - 90) + ")translate(" + (r - 170 + 8) + ")rotate(" + ((d.x + rotate) % 360 < 180 ? 0 : 180) + ")";
          });
    }
  })
  .on("mousemove", function() {
    if (start) {
      var m = mouse(d3.event);
      var delta = Math.atan2(cross(start, m), dot(start, m)) * 180 / Math.PI;
      wrap.style("-webkit-transform", "rotateZ(" + delta + "deg)");
    }
  });

function phylo(n, offset) {
  if (n.length != null) offset += n.length * 115;
  n.y = offset;
  if (n.children)
    n.children.forEach(function(n) {
      phylo(n, offset);
    });
}

/*d3.text("life.txt", function(text) {*/
  var text = "(1_2dn3-Hum:0.07530769665,((4_1hds-Dee:0.0528073453,6_1qpw-Pig:0.06665859446):0.02152352081,((3_2d5x-Hor:1e-08,5_2qss-Cow:1e-08):1e-08,20_1s0h-Do:1e-08):0.06472462393):0.02032419956,(((((((12_1out-Tr:0.2387258463,16_1spg-Fi:0.3731048609):0.05254102815,(((13_2h8f-Em:1e-08,15_3d1k-An:1e-08):0.1749055632,18_1V4W-Bl:0.09770713149):0.1479325642,19_1xq5-Ye:0.1992590704):0.07668473559):0.1801915413,((11_1wmu-Al:1e-08,17_1gcv-Ho:1e-08):0.4395960015,14_1cg5-Ca:0.3474616143):0.8944824012):1e-08,8_1hbr-Chi:0.2820483041):0.0189194681,2_1jeb-Hum:0.3128283876):0.08144709769,(9_1a4f-Bar:1e-08,10_1faw-Gr:1e-08):0.1655575179):0.1382264995,7_1fhj-Man:0.07975001425):0.01337333371);"
  var x = Newick.parse(text);
  var nodes = cluster.nodes(x);
  phylo(nodes[0], 0);

  var link = vis.selectAll("path.link")
      .data(cluster.links(nodes))
    .enter().append("path")
      .attr("class", "link")
      .attr("d", step);

  var node = vis.selectAll("g.node")
      .data(nodes.filter(function(n) { return n.x !== undefined; }))
    .enter().append("g")
      .attr("class", "node")
      .attr("transform", function(d) { return "rotate(" + (d.x - 90) + ")translate(" + d.y + ")"; })

  node.append("circle")
      .attr("r", 2.5);

  var label = vis.selectAll("text")
      .data(nodes.filter(function(d) { return d.x !== undefined && !d.children; }))
    .enter().append("text")
      .attr("dy", ".31em")
      .attr("text-anchor", function(d) { return d.x < 180 ? "start" : "end"; })
      .attr("transform", function(d) { return "rotate(" + (d.x - 90) + ")translate(" + (r - 170 + 8) + ")rotate(" + (d.x < 180 ? 0 : 180) + ")"; })
      .text(function(d) { return d.name.replace(/_/g, ' '); });
/*});*/
