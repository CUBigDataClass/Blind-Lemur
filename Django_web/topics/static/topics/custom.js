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
          d3.select(svg_location).append("svg")
              .attr("width", width)
              .attr("height", height)
              .attr("style", "outline:  dotted red;" , "fill: light grey")
            .append("g")
              .attr("transform", "translate(" + [width >> 1, height >> 1] + ")")
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
              .text(function(d) { return d.key; });
        }
        d3.layout.cloud().stop();
      }


function dummyPagenation(data){
        var arrayLength = data.name.length;
            drawWordCloud(data.name.slice(0,10));
            drawWordCloud(data.name.slice(10,20));
            drawWordCloud(data.name.slice(20,30));
            drawWordCloud(data.name.slice(30,40));
        }


function request_access(data){
   // alert("hello");
     var monthSelected = $("#month").val();
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



