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
    var previous_time = -1;
    var next_time = -1;
    structure_files.forEach(file => {
	file_time = Number(file.split(".")[0]);
	if (file_time <= query.time && time > latest_time && file.endsWith("json")) {
	    structure_file = file;
	    previous_time = latest_time;
	    latest_time = file_time;
	} else {
	    if (next_time == -1 && file.endsWith("json")) {
		next_time = file_time;
	    }
	}
    });

    const previous_link = previous_time > -1 ?
	  `<a href="structure_snapshot?run_id=${run_id}&structure_id=${structure_id}`
	+`&time=${previous_time}">&lt- ${structure_id}@${previous_time}</a>`
	  : "";
    const next_link = next_time > -1 ?
	  `<a href="structure_snapshot?run_id=${run_id}&structure_id=${structure_id}`
	+`&time=${next_time}">${structure_id}@${next_time} -&gt</a>`
	  : "";
    const codelet_no = Number(time) + 1;
    const codelet_link = `<a href="codelet?run_id=${run_id}&codelet_number=${codelet_no}">`
	+`Codelet@${codelet_no}</a>`;

    const graph_file = tools.get_graph(run_id, structure_id, time);
    const graph_svg = fs.readFileSync(graph_file);

    const log_file = structure_directory + '/' + structure_file;
    const structure_json = JSON.parse(fs.readFileSync(log_file));
    const structure_html = tools.json_to_html(structure_json, query);

    snapshot_files = fs.readdirSync(structure_directory).filter(
	function(a) {return a.split(".")[1] == "json"}
    );
    snapshot_files.sort(
	function(a, b) {return Number(a.split(".")[0]) - Number(b.split(".")[0])}
    );


    const doc = `
<html>
  <body>
    <p><a href="../">&lt;&lt;All runs</a></p>
    <h1><a href="run?run_id=${run_id}">Linguoplotter run ${run_id}</a></h1>
    <p><a href="codelets?run_id=${run_id}">Codelets</a></p>
    <p><a href="structures?run_id=${run_id}">Structures</a></p>
    <h2><a href="structure_lifetime?run_id=${run_id}&structure_id=${structure_id}">${structure_id}</a></h2>
    <p>${previous_link} ${codelet_link} ${next_link}</p>
    <object type="image/svg+xml">${graph_svg}</object>
    ${structure_html}
  </body>
</html>
`;
    return doc;
}
