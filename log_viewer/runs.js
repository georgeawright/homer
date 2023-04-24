var fs = require('fs');

exports.run = function(query) {
    doc = '<html><body>';
    doc += '<h1>Linguoplotter Runs</h1>';
    doc += '<ul>';
    fs.readdirSync('logs/').forEach(directory => {
        console.log(directory);
	doc += '<li><a href="log_viewer/run?run_id='+directory+'">';
        doc += directory;
	doc += '</a></li>';
    });
    doc += '</ul>';
    doc += '</body></html>';
    return doc;
}
