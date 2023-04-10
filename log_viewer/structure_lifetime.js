var fs = require('fs');
var tools = require('./tools');

exports.run = function(query) {
    const run_id = query.run_id;
    const structure_id = query.structure_id;
    const page = query.page == undefined ? 1 : Number(query.page);
    const items_per_page = query.items_per_page == undefined ? 100 : query.items_per_page;
    const log_directory = 'logs/' + run_id + '/';

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
    <h2>${structure_id}</h2>
    <p>
`;
    structure_directory = log_directory + 'structures/structures/' + structure_id;
    snapshot_files = fs.readdirSync(structure_directory);
    snapshot_files.sort(
	function(a, b) {return Number(a.split(".")[0]) - Number(b.split(".")[0])}
    );
    slice_start = (page - 1) * items_per_page;
    slice_end = slice_start + items_per_page;
    const prev_page = page - 1
    const next_page = page + 1
    const last_page = Math.ceil(snapshot_files.length / items_per_page);
    if (page > 1) {
	doc +=`
      <a href="structures?run_id=${run_id}&page=1&items_per_page=${items_per_page}">&lt;&lt;</a>
      <a href="structures?run_id=${run_id}&page=${prev_page}&items_per_page=${items_per_page}">&lt;</a>
`;
    }
    if (page < last_page) {
	doc +=`
      <a href="structures?run_id=${run_id}&page=${next_page}&items_per_page=${items_per_page}">&gt;</a>
      <a href="structures?run_id=${run_id}&page=${last_page}&items_per_page=${items_per_page}">&gt;&gt;</a>
`;
    }
    doc += `
    </p>
    <div id="activation_graph"></div>
    <div id="unhappiness_graph"></div>
    <div id="quality_graph"></div>
`;
    doc += activation_graph_script(query);
    doc += unhappiness_graph_script(query);
    doc += quality_graph_script(query);

    doc += `
    <ul>
`;
    snapshot_files.slice(slice_start, slice_end).forEach(file => {
	const time = file.split(".")[0]
	doc += `
      <li>
        <a href="structure_snapshot?run_id=${run_id}&structure_id=${structure_id}&time=${time}">${time}</a>
      </li>
`;
    });
    doc += `
    </ul>
  </body>
</html>
`;
    return doc;
}

const activation_graph_script = function(query) {
    const activation_data = data_string_for_field(query, 'activation');
    return tools.generate_graph_script(
	'activation_graph',
	activation_data,
	x_title="Codelets Run",
	y_title="Activation",
    );
}

const unhappiness_graph_script = function(query) {
    const unhappiness_data = data_string_for_field(query, 'unhappiness');
    return tools.generate_graph_script(
	'unhappiness_graph',
	unhappiness_data,
	x_title="Codelets Run",
	y_title="Unhappiness",
    );
}

const quality_graph_script = function(query) {
    const quality_data = data_string_for_field(query, 'quality');
    return tools.generate_graph_script(
	'quality_graph',
	quality_data,
	x_title="Codelets Run",
	y_title="Quality",
    );
}

const data_string_for_field = function(query, field_name) {
    const structure_directory = `logs/${query.run_id}/structures/structures/${query.structure_id}`;
    snapshot_files = fs.readdirSync(structure_directory);
    console.log(snapshot_files);
    snapshot_files = fs.readdirSync(structure_directory).filter(
	file_name => {return file_name.endsWith("json")}
    );
    console.log(snapshot_files);
    snapshot_files.sort(
	function(a, b) {return Number(a.split(".")[0]) - Number(b.split(".")[0])}
    );
    data = '[';
    snapshot_files.forEach(file => {
	const time = file.split(".")[0];
	const structure_json = JSON.parse(fs.readFileSync(`${structure_directory}/${file}`));
	const value = structure_json[field_name];
	if (data.length > 1) {
	    data += ', ';
	}
	data += `\{time: ${time}, value: ${value}\}`;
    });
    data +=  ']';
    return data;
}
