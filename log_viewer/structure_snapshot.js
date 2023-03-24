var fs = require('fs');
var tools = require('./tools');

exports.run = function(query) {
    run_id = query.run_id;
    structure_id = query.structure_id;
    time = query.time
    log_file = 'logs/' + run_id + '/' + 'structures/structures/'
	+ structure_id + '/' + time + '.json';

    doc = '<html><body>';
    doc += '<h1>Linguoplotter run '+run_id+'</h1>';
    doc += '<p><a href="codelets?run_id=' + run_id + '">Codelets</a></p>';
    doc += '<p><a href="structures?run_id=' + run_id + '">Structures</a></p>';

    doc += '<h2>' + structure_id + '</h2>';
    structure_json = JSON.parse(fs.readFileSync(log_file));
    console.log(structure_json);
    structure_html = tools.json_to_html(structure_json, query);

    doc += structure_html;

    doc += '</body></html>';
    return doc;
}
