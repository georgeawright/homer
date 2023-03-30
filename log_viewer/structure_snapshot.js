var fs = require('fs');
var tools = require('./tools');

exports.run = function(query) {
    var run_id = query.run_id;
    var structure_id = query.structure_id;
    var time = query.time
    var structure_directory = 'logs/' + query.run_id
	+ '/structures/structures/' + structure_id;
    var structure_files = fs.readdirSync(structure_directory);
    var structure_file = '';
    var latest_time = -1;
    structure_files.forEach(file => {
	file_time = Number(file.split(".")[0]);
	if (file_time <= query.time && time > latest_time) {
	    structure_file = file;
	    latest_time = file_time;
	}
    });
    var log_file = structure_directory + '/' + structure_file;

    var doc = '<html><body>';
    doc += '<p><a href="../">&lt;&lt;All runs</a></p>';
    doc += '<h1><a href="run?run_id=' + run_id + '">Linguoplotter run '+run_id+'</a></h1>';
    doc += '<p><a href="codelets?run_id=' + run_id + '">Codelets</a></p>';
    doc += '<p><a href="structures?run_id=' + run_id + '">Structures</a></p>';

    var structure_url = 'structure_lifetime?run_id=' + run_id + '&structure_id=' + structure_id;
    doc += '<h2><a href="' + structure_url + '">' + structure_id + '</a></h2>'

    structure_json = JSON.parse(fs.readFileSync(log_file));
    console.log(structure_json);
    structure_html = tools.json_to_html(structure_json, query);

    doc += structure_html;

    doc += '</body></html>';
    return doc;
}
