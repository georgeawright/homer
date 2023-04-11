var fs = require('fs');
var tools = require('./tools');

exports.run = function(query) {
    run_id = query.run_id;
    details_file = 'logs/'+run_id+'/details.txt';
    doc = `
<html>
  <head>
    <script src="https://d3js.org/d3.v6.js"></script>
    <style>
div.plot {
  float: left;
}
    </style>
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
    <div id="satisfaction_graph" class="plot"></div>`;
    doc += satisfaction_graph_script(query);
    doc +=  `
    <div id="coderack_population_graph" class="plot"></div>`;
    doc += coderack_pop_graph_script(query);
    doc +=  `
    <div id="view_count_graph" class="plot"></div>`;
    doc += view_count_graph_script(query);
    doc += `
  </body>
</html>`;
    return doc;
}

const satisfaction_graph_script = function(query) {
    const satisfaction_data = data_string_from_csv(query, 'satisfaction.csv');
    return tools.generate_graph_script(
	'satisfaction_graph',
	satisfaction_data,
	x_title='Codelets Run',
	y_title='Satisfaction',
    );
}

const coderack_pop_graph_script = function(query) {
    const coderack_population_data = data_string_from_csv(query, 'coderack_population.csv');
    return tools.generate_graph_script(
	'coderack_population_graph',
	coderack_population_data,
	x_title='Codelets Run',
	y_title='Coderack Population',
    );
}

const view_count_graph_script = function(query) {
    const view_count_data = data_string_from_csv(query, 'view_count.csv');
    return tools.generate_graph_script(
	'view_count_graph',
	view_count_data,
	x_title='Codelets Run',
	y_title='View Count',
    );
}

const data_string_from_csv = function(query, csv_file_name) {
    const csv = `logs/${query.run_id}/${csv_file_name}`;
    data = '[';
    String(fs.readFileSync(csv))
	.split("\n")
	.forEach(line => {
	    const row = line.split(',');
	    if (row == '') {
		return;
	    }
	    if (data.length > 1) {
		data += ', ';
	    }
	    data += `\{time: ${row[0]}, value: ${row[1]}\}`;
	});
    data +=  ']';
    return data;
}
