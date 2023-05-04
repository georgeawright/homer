var fs = require('fs');
var tools = require('./tools');

exports.run = function(query) {
    run_id = query.run_id;
    page = query.page == undefined ? 1 : Number(query.page);
    items_per_page = query.items_per_page == undefined ? 100 : Number(query.items_per_page);
    filter = query.filter;
    log_directory = 'logs/' + run_id + '/';
    doc =`
<html>
  <body>
    <p><a href="../">&lt;&lt;All runs</a></p>
    <h1><a href="run?run_id=${run_id}">Linguoplotter run ${run_id}</a></h1>
    <p><a href="codelets?run_id=${run_id}">Codelets</a></p>
    <p><a href="structures?run_id=${run_id}">Structures</a></p>
`
    codelets_directory = log_directory + 'codelets/times';
    codelet_files = fs.readdirSync(codelets_directory);
    codelet_files.sort(
	function(a, b) {return Number(a.split(".")[0]) - Number(b.split(".")[0])}
    );
    slice_start = (page - 1) * items_per_page;
    slice_end = slice_start + items_per_page;

    console.log(codelet_files);

    doc += '<p>';
    if (page > 1) {
	doc += '<a href="codelets?run_id=' + run_id
	    + '&page=1&items_per_page=' + items_per_page
	    + '">First Page</a> ';
	doc += '<a href="codelets?run_id=' + run_id
	    + '&page=' + (page - 1)
	    +'&items_per_page=' + items_per_page
	    + '">Previous Page</a> ';
    }
    doc += page + ' ';
    last_page = Math.ceil(codelet_files.length / items_per_page);
    if (page < last_page) {
	doc += '<a href="codelets?run_id=' + run_id
	    + '&page=' + (page + 1)
	    +'&items_per_page=' + items_per_page
	    + '">Next Page</a> ';
	doc += '<a href="codelets?run_id=' + run_id
	    + '&page=' + last_page
	    + '&items_per_page=' + items_per_page
	    + '">Last Page</a> ';
    }
    doc += '</p>';

    doc += '<ul>';
    codelet_files.slice(slice_start, slice_end).forEach(file => {
	codelet_number = file.split(".")[0];
	codelet_file = 'logs/' + run_id + '/' + 'codelets/times/' + codelet_number + '.json';
	codelet_json = JSON.parse(fs.readFileSync(codelet_file));
	query.time = Number(codelet_number);
	
	url = 'codelet?run_id=' + run_id + '&codelet_number=' + codelet_number;
	doc += '<ul><h2>' + codelet_number + ': '
	    + '<a href="' + url + '">' + codelet_json.id + '</a></h2>'
	    + '<p>Parent: ' + tools.json_to_html(codelet_json.parent_id, query)
	    + ' | Urgency: ' + codelet_json.urgency + '</p>'
	    + 'Targets: ' + tools.json_to_html(codelet_json.targets, query)
	    + 'Activity: ' + tools.json_to_html(codelet_json.activity, query)
	    + '<p>Result: ' + codelet_json.result + '</p>'
	    + 'Child structures: ' + tools.json_to_html(codelet_json.child_structures, query)
	    + 'Child codelets: ' + tools.json_to_html(codelet_json.child_codelets, query)
	    + '<p>Satisfaction: ' + codelet_json.satisfaction
	    + ' | Coderack population: ' + codelet_json.coderack_population
	    + ' | View count: ' + codelet_json.view_count + '</p>'
	    + '<p>Focus: ' + tools.json_to_html(codelet_json.focus, query) + '</p>'
	    + '<p>Worldview: ' + tools.json_to_html(codelet_json.worldview, query) + '</p>'
	    + '</ul>';

    });
    doc += '</ul>';
    doc += '</body></html>';

    return doc;
}
