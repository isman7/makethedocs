(function(){
"use strict";
function ՐՏ_Iterable(iterable) {
    var tmp;
    if (iterable.constructor === [].constructor || iterable.constructor === "".constructor || (tmp = Array.prototype.slice.call(iterable)).length) {
        return tmp || iterable;
    }
    return Object.keys(iterable);
}
var ՐՏ_modules = {};
ՐՏ_modules["variables"] = {};

(function(){
    var __name__ = "variables";
    var prueba;
    prueba = 0;
    ՐՏ_modules["variables"]["prueba"] = prueba;
})();

(function(){

    var __name__ = "__main__";

    var pieChartCanvas, pieChart, PieData, pieOptions;
    var variables = ՐՏ_modules["variables"];
    
    pieChartCanvas = $("#pieChart").get(0).getContext("2d");
    pieChart = new Chart(pieChartCanvas);
    PieData = [ {
        "value": 1e3,
        "color": "#f56954",
        "highlight": "#f56954",
        "label": "Chrome"
    }, {
        "value": 500,
        "color": "#00a65a",
        "highlight": "#00a65a",
        "label": "IE"
    }, {
        "value": 400,
        "color": "#f39c12",
        "highlight": "#f39c12",
        "label": "FireFox"
    }, {
        "value": 600,
        "color": "#00c0ef",
        "highlight": "#00c0ef",
        "label": "Safari"
    }, {
        "value": 300,
        "color": "#3c8dbc",
        "highlight": "#3c8dbc",
        "label": "Opera"
    }, {
        "value": 100,
        "color": "#d2d6de",
        "highlight": "#d2d6de",
        "label": "Navigator"
    } ];
    pieOptions = {
        "segmentShowStroke": true,
        "segmentStrokeColor": "#fff",
        "segmentStrokeWidth": 2,
        "percentageInnerCutout": 50,
        "animationSteps": 100,
        "animationEasing": "easeOutBounce",
        "animateRotate": true,
        "animateScale": false,
        "responsive": true,
        "maintainAspectRatio": true,
        "legendTemplate": '\n<ul class="<%=name.toLowerCase()%>-legend">\n    <% for (var i=0; i<segments.length; i++){%>\n    <li>\n    <span style="background-color:<%=segments[i].fillColor%>"></span>\n    <%if(segments[i].label){%><%=segments[i].label%><%}%>\n    </li><%}%>\n</ul>\n'
    };
    pieChart.Doughnut(PieData, pieOptions);
})();
})();
