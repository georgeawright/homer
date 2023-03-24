var fs = require('fs');

exports.run = function(query) {
    run_id = query.run_id;
    details_file = 'logs/'+run_id+'/details.txt';
    doc = '<html><body>';
    doc += '<h1>Linguoplotter run '+run_id+'</h1>';
    doc += '<p><a href="codelets?run_id=' + run_id + '">Codelets</a></p>';
    doc += '<p><a href="structures?run_id=' + run_id + '">Structures</a></p>';
    details = String(fs.readFileSync(details_file));
    lines = details.split("\n");
    lines.forEach(line => {
	doc += '<p>'+line+'</p>';
    });
    doc += '</body></html>';
    return doc;
}
