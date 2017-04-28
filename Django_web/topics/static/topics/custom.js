function drawWordCloud(data){
        var word_count = {};
        var arrayLength = data.length;
        for (var i = 0; i < arrayLength; i++) {
            word_count[data[i][0]] = data[i][1];
        }


        var svg_location = "#chart";
        var width = 400;
        var height = 600;
        var fill = d3.scale.category20();
        var word_entries = d3.entries(word_count);
        var xScale = d3.scale.linear()
           .domain([0, d3.max(word_entries, function(d) {
              return d.value;
            })
           ])
           .range([10,100]);
        d3.layout.cloud().size([width, height])
          .timeInterval(20)
          .words(word_entries)
          .fontSize(function(d) { return xScale(+d.value); })
          .text(function(d) { return d.key; })
          .rotate(function() { return ~~(Math.random() * 2) * 90; })
          .font("Impact")
          .on("end", draw)
          .start();

        function draw(words) {

         var tooltip = d3.select("body")
            .append("div")
            .style("position", "absolute")
            .style("font-size","30px")
            .style("z-index", "10")
            .style("visibility", "hidden")
            .style("background", "#C2DFFF")
            .style('fill','red')
            /*.style("font-weight","bold")*/
            .text("a simple tooltip");

      var svg =  d3.select(svg_location).append("svg")
              .attr("width", width)
              .attr("height", height)
              .attr("style", "outline:  dotted red;" , "fill: light grey")
            .append("g")
              .attr("transform", "translate(" + [width >> 1, height >> 1] + ")")
              /*.transition()
              .attr("transform", "translate(" + [width >> 1, height >> 1] + ")")*/
            .selectAll("text")
              .data(words)
            .enter().append("text")
              .style("font-size", function(d) { return xScale(d.value) + "px"; })
              .style("font-family", "Impact")
              .style("fill", function(d, i) { return fill(i); })
              .attr("text-anchor", "middle")
              .attr("transform", function(d) {
                return "translate(" + [d.x, d.y] + ")rotate(" + d.rotate + ")";
              })
               .text(function(d) { return d.text; })
               .on("mouseover", function(d){tooltip.text("Topic Weight = " +d.value.toFixed(3)); return tooltip.style("visibility", "visible");})
               .on("mousemove", function(){return tooltip.style("top", (d3.event.pageY-10)+"px").style("left",(d3.event.pageX+10)+"px");})
               .on("mouseout", function(){return tooltip.style("visibility", "hidden");});
        }
        d3.layout.cloud().stop();
      }


function dummyPagenation(data){
        var arrayLength = data.name.length;
        var timeout = 1000;
        setTimeout(function() { drawWordCloud(data.name.slice(0,10))}, timeout)
        setTimeout(function() { drawWordCloud(data.name.slice(10,20))}, 2*timeout)
        setTimeout(function() { drawWordCloud(data.name.slice(20,30))}, 4*timeout)
        setTimeout(function() { drawWordCloud(data.name.slice(30,40))}, 6*timeout)
        }


function changeColor(data){
     $(this).css('background-image', '#E66C2C');
}

function request_access(monthSelected){
   // alert("hello");
      $.ajax({
        type:"POST",
        url: "/fetchMonthTopics/",
        dataType: 'json',
        contentType: 'json',
        data: {
         'monthSelected': monthSelected
        },
        dataType: 'json',
        success: function (data) {
            d3.selectAll("svg").remove();
            dummyPagenation(data);
            //drawWordCloud(data);
           // alert(data);
        }
      });
    }



