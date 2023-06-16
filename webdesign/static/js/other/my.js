var spec1 = {"config": {"view": {"continuousWidth": 1100, "continuousHeight": 1100}}, "data": {"name": "data-c2a3e89ba9d5d1687d5e8c28d630a033"}, "mark": {"type": "bar"}, "encoding": {"x": {"field": "a", "type": "nominal"}, "y": {"field": "b", "type": "quantitative"}}, "params": [{"name": "param_4", "select": {"type": "interval", "encodings": ["x", "y"]}, "bind": "scales"}], "$schema": "https://vega.github.io/schema/vega-lite/v5.8.0.json", "datasets": {"data-c2a3e89ba9d5d1687d5e8c28d630a033": [{"a": "A", "b": 28}, {"a": "B", "b": 55}, {"a": "C", "b": 43}, {"a": "D", "b": 91}, {"a": "E", "b": 81}, {"a": "F", "b": 53}, {"a": "G", "b": 19}, {"a": "H", "b": 87}, {"a": "I", "b": 52}]}};
var embed_opt2 = {"mode": "vega-lite", "actions": false};


function displaySelect(){
    if (document.getElementById("categorizetypelevel").checked) {
        document.getElementById("levelbasedtype").style.display = '';
        document.getElementById("trendbasedtype").style.display = 'none';
        document.getElementById("trendbasedtypetextdiv").style.display = 'none';
      }
    if (document.getElementById('categorizetypetrend').checked) {
        document.getElementById("trendbasedtype").style.display = '';
        document.getElementById("trendbasedtypetextdiv").style.display = '';
        document.getElementById("levelbasedtype").style.display = 'none';
      }
      if (document.getElementById("custombin").checked) {
        document.getElementById("customsizediv").style.display = '';
      }
      else {
          document.getElementById("customsizediv").style.display = 'none';
      }
}

// var spec=chartspec
// var embed_opt=chartembed_opt

// var spec = "{{ chartspec | safe}}";
// var embed_opt = "{{ chartembed_opt | safe}}";

// console.log(spec);
// console.log(embed_opt);


// function showError(chartId, error){{
//     chartId.innerHTML = ('<div class="error">'
//                     + '<p>JavaScript Error: ' + error.message + '</p>'
//                     + "<p>This usually means there's a typo in your chart specification. "
//                     + "See the javascript console for the full traceback.</p>"
//                     + '</div>');
//     throw error;
// }}
// const chartId = document.getElementById('chartId');
// vegaEmbed("#chartId", spec, embed_opt)
//   .catch(error => showError(chartId, error));


