var fs = require('fs');

exports.run = function(query) {
    run_id = query.run_id;
    details_file = 'logs/'+run_id+'/details.txt';
    doc = `
<html>
  <head>
    <script src="https://d3js.org/d3.v6.js"></script>
  </head>
  </body>
    <p><a href="../">&lt;&lt;All runs</a></p>
    <h1><a href="run?run_id=${run_id}">Linguoplotter run ${run_id}</a></h1>
    <p><a href="codelets?run_id=${run_id}">Codelets</a></p>
    <p><a href="structures?run_id=${run_id}">Structures</a></p>
`
    details = String(fs.readFileSync(details_file));
    lines = details.split("\n");
    lines.forEach(line => {
	doc += `
    <p>${line}</p>`;
    });
    doc +=  `
    <div id="satisfaction_graph"></div>`;
    doc += satisfaction_graph_script(query);
    doc += `
  </body>
</html>`;
    return doc;
}

satisfaction_graph_script = function(query) {
    const satisfaction_csv = `logs/${query.run_id}/satisfaction.csv`;
    satisfaction_data = '[';
    String(fs.readFileSync(satisfaction_csv))
	.split("\n")
	.forEach(line => {
	    const row = line.split(',');
	    if (row == '') {
		return;
	    }
	    if (satisfaction_data.length > 1) {
		satisfaction_data += ', ';
	    }
	    satisfaction_data += `\{time: ${row[0]}, satisfaction: ${row[1]}\}`;
	});
    satisfaction_data +=  ']';
    const script = `
<script>
  const margin = {top: 10, right: 30, bottom: 30, left: 60},
	width = 640 - margin.left - margin.right,
	height = 480 - margin.top - margin.bottom;
  const svg = d3.select("#satisfaction_graph")
	.append("svg")
	.attr("width", width + margin.left + margin.right)
	.attr("height", height + margin.top + margin.bottom)
	.append("g")
	.attr("transform", \`translate(\${margin.left},\${margin.top})\`);
  const data = ${satisfaction_data};
  const x = d3.scaleLinear()
	.domain(d3.extent(data, function(d) { return d.time; }))
	.range([ 0, width ]);
  svg.append("g")
    .attr("transform", \`translate(0, \${height})\`)
    .call(d3.axisBottom(x));
  const y = d3.scaleLinear()
	.domain([0, d3.max(data, function(d) { return d.satisfaction; })])
	.range([ height, 0 ]);
  svg.append("g")
    .call(d3.axisLeft(y));
  svg.append("path")
    .datum(data)
    .attr("fill", "none")
    .attr("stroke", "steelblue")
    .attr("stroke-width", 1.5)
    .attr("d", d3.line()
          .x(function(d) { return x(d.time) })
          .y(function(d) { return y(d.satisfaction) })
         )
</script>
`
    return script;
}
