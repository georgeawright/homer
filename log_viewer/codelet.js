var fs = require('fs');
var tools = require('./tools');

exports.run = function(query) {
    run_id = query.run_id;
    codelet_number = query.codelet_number;
    codelet_id = query.codelet_id;
    if (codelet_number !== undefined) {
	log_file = 'logs/' + run_id + '/' + 'codelets/times/' + codelet_number + '.json';
    } else {
	log_file = 'logs/' + run_id + '/' + 'codelets/ids/' + codelet_id + '.json';
    }

    doc = '<html><body>';
    doc += '<p><a href="../">&lt;&lt;All runs</a></p>';
    doc += '<h1><a href="run?run_id=' + run_id + '">Linguoplotter run '+run_id+'</a></h1>';
    doc += '<p><a href="codelets?run_id=' + run_id + '">Codelets</a></p>';
    doc += '<p><a href="structures?run_id=' + run_id + '">Structures</a></p>';

    codelet_json = JSON.parse(fs.readFileSync(log_file));
    query.time = codelet_json.time;

    doc += '<h2>' + codelet_json.id + '</h2>';
    codelet_html = tools.json_to_html(codelet_json, query);
    doc += codelet_html;

    doc += '</body></html>';
    return doc;
}
