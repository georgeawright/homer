var fs = require('fs');

exports.run = function(query) {
    run_id = query.run_id;
    page = query.page == undefined ? 1 : query.page;
    items_per_page = query.items_per_page;
    log_directory = 'logs/' + run_id + '/';
    doc = '<html><body>';
    doc += '<h1>Linguoplotter run '+run_id+'</h1>';
    doc += '<p><a href="codelets?run_id=' + run_id + '">Codelets</a></p>';
    doc += '<p><a href="structures?run_id=' + run_id + '">Structures</a></p>';
    file = log_directory + 'activity' + page + '.log';
    details = String(fs.readFileSync(file));
    lines = details.split("\n");
    lines.forEach(line => {
	doc += '<p>'+line+'</p>';
    });
    doc += '</body></html>';
    return doc;
}
