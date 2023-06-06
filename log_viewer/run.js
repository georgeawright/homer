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
br {
  clear: both;
}
    </style>
  </head>
  </body>
    <p><a href="../">&lt;&lt;All runs</a></p>
    <h1><a href="run?run_id=${run_id}">Linguoplotter run ${run_id}</a></h1>
    <p><a href="codelets?run_id=${run_id}">Codelets</a></p>
    <p><a href="structures?run_id=${run_id}">Structures</a></p>
`
    details = JSON.parse(fs.readFileSync(details_file));

    structures_directory = `logs/${run_id}/structures/structures`;
    structure_directories = fs.readdirSync(structures_directory);
    structure_directories.forEach(directory => {
	if (!directory.includes("ContextualSpace")) {
	    return;
	}
	structure_directory = `${structures_directory}/${directory}`;
	snapshot_files = fs.readdirSync(structure_directory);
	try {
	    file_path = `${structure_directory}/0.json`;
	    structure = JSON.parse(fs.readFileSync(file_path));
	    if (structure["is_main_input"]) {
		details["main_input"] = structure["structure_id"];
		return;
	    }
	} catch (err) {
	}
    });

    doc += tools.json_to_html(details, query);
    doc +=  `
    <div id="satisfaction_graph" class="plot"></div>`;
    doc += satisfaction_graph_script(query);
    doc +=  `
    <div id="determinism_graph" class="plot"></div>`;
    doc += determinism_graph_script(query);
    doc +=  `
    <div id="coderack_population_graph" class="plot"></div>`;
    doc += coderack_pop_graph_script(query);
    doc +=  `
    <div id="view_count_graph" class="plot"></div>`;
    doc += view_count_graph_script(query);

    worldviews = [];
    codelets_directory = `logs/${run_id}/codelets/ids`;
    codelet_files = fs.readdirSync(codelets_directory);
    codelet_files.forEach(file => {
	if (!file.includes("WorldviewSetter")) {
	    return;
	}
	file_path = `${codelets_directory}/${file}`;
	codelet = JSON.parse(fs.readFileSync(file_path));
	worldviews.push({"worldview": codelet["worldview"], "time": codelet["time"]});
    });
    worldviews.sort(function(a,b) {return a["time"] - b["time"]});
    doc += `
    <br>
    <h2>Worldview History</h2>
    <ul>`;
    previous_worldview = null;
    worldviews.forEach(worldview => {
	time = worldview["time"];
	view = worldview["worldview"];

	if (view === previous_worldview) {
	    return;
	}

	structure_directory = `logs/${run_id}/structures/structures/${view}`;
	structure_files = fs.readdirSync(structure_directory).filter(
	    (f) => {return f.endsWith("json")}
	);
	structure_file = '';
	latest_file_time = -1;
	structure_files.forEach(file => {
	    file_time = Number(file.split(".")[0]);
	    if (file_time <= time && file_time > latest_file_time) {
	    structure_file = file;
	    latest_file_time = file_time;
	    }
	});
	structure_file_path = `${structure_directory}/${structure_file}`;
        structure_json = JSON.parse(fs.readFileSync(structure_file_path));

	text = structure_json["output"];

	doc += `
      <li>${time}: <a href="structure_snapshot?run_id=${run_id}&structure_id=${view}&time=${time}">${view}</a>: ${text}</li>`;
	previous_worldview = view;
    });
    doc += `
    </ul>`;
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

const determinism_graph_script = function(query) {
    const determinism_data = data_string_from_csv(query, 'determinism.csv');
    return tools.generate_graph_script(
	'determinism_graph',
	determinism_data,
	x_title='Codelets Run',
	y_title='Determinism',
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
