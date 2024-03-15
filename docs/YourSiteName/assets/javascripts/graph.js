$('.md-sidebar--secondary').each(function() {
  var link = $(this).html();
  $(this).contents().append('<div id="graph" style="height:300px; width: 100%;"></div>');
});

var dom = document.getElementById('graph');
var myChart = echarts.init(dom, null, {
  renderer: 'canvas',
  useDirtyRect: true
});
var option;

$.getJSON(document.currentScript.src + '/../graph.json', function (graph) {
  myChart.hideLoading();
  graph.nodes.forEach(function (node) {
    node.symbolSize += 5;
  });
  graph.nodes.forEach(function (node) {
    node.name = node.name.split(' •')[0];
  });
  graph.links.forEach(function (link) {
    link.source = link.source.split(' •')[0];
    link.target = link.target.split(' •')[0];
  });
  option = {
    tooltip: {
      show: false,
      formatter: '<b>{b0}</b>'
    },
    legend: [
      //{
      //  data: graph.categories.map(function (a) {
      //    return a.name;
      //  })
      //}
    ],
    darkMode: "auto",
    backgroundColor: $("body").css("background-color"),
    series: [
      {
        name: 'zRevival',
        type: 'graph',
        layout: 'force',
        data: graph.nodes,
        links: graph.links,
        categories: [],
        zoom: 2,
        roam: true,
        draggable: false,
        label: {
          show: true,
          position: 'right',
          formatter: '{b}'
        },
        emphasis: {
          focus: 'adjacency',
          label: {
            fontWeight: "bold"
	  }
	},
        labelLayout: {
          hideOverlap: false //true
        },
        scaleLimit: {
          min: 0.5,
          max: 5
        },
        lineStyle: {
          color: 'source',
          curveness: 0 //0.3
        }
      }
    ]
  };

  myChart.setOption(option);
  myChart.on('click', function (params) {
    //console.log('series', params, params.name);
    if(params.dataType == "node") {
      window.location = params.value;
    }
  });
});

if(option && typeof option === 'object') {
  myChart.setOption(option);
}

window.addEventListener('resize', myChart.resize);

$("#__palette_0").change(function(){
  option.backgroundColor = $("body").css("background-color");
  myChart.setOption(option);
});
$("#__palette_1").change(function(){
  option.backgroundColor = $("body").css("background-color");
  myChart.setOption(option);
});
