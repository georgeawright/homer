var fs = require('fs');
var tools = require('./tools');

exports.run = function(query) {
    const run_id = query.run_id;
    const structure_id = query.structure_id;
    const time = query.time
    const structure_directory = `logs/${run_id}/structures/structures/${structure_id}`;
    const structure_files = fs.readdirSync(structure_directory);

    var structure_file = '';
    var latest_time = -1;
    structure_files.forEach(file => {
	file_time = Number(file.split(".")[0]);
	if (file_time <= query.time && time > latest_time && file.endsWith("json")) {
	    structure_file = file;
	    latest_time = file_time;
	}
    });

    const graph_file = tools.get_graph(run_id, structure_id, time);
    const graph_svg = fs.readFileSync(graph_file);

    const log_file = structure_directory + '/' + structure_file;
    const structure_json = JSON.parse(fs.readFileSync(log_file));
    const structure_html = tools.json_to_html(structure_json, query);

    const doc = `
<html>
  <body>
    <p><a href="../">&lt;&lt;All runs</a></p>
    <h1><a href="run?run_id=${run_id}">Linguoplotter run ${run_id}</a></h1>
    <p><a href="codelets?run_id=${run_id}">Codelets</a></p>
    <p><a href="structures?run_id=${run_id}">Structures</a></p>
    <h2><a href="structure_lifetime?run_id=${run_id}&structure_id=${structure_id}">${structure_id}</a></h2>
    <object type="image/svg+xml">${graph_svg}</object>
    ${structure_html}
  </body>
</html>
`;
    return doc;
}
