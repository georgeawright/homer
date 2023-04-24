var fs = require('fs');

exports.run = function(query) {
    run_id = query.run_id;
    page = query.page == undefined ? 1 : Number(query.page);
    items_per_page = query.items_per_page == undefined ? 100 : Number(query.items_per_page);
    log_directory = 'logs/' + run_id + '/';

    doc = '<html><body>';
    doc += '<p><a href="../">&lt;&lt;All runs</a></p>';
    doc += '<h1><a href="run?run_id=' + run_id + '">Linguoplotter run '+run_id+'</a></h1>';
    doc += '<p><a href="codelets?run_id=' + run_id + '">Codelets</a></p>';
    doc += '<p><a href="structures?run_id=' + run_id + '">Structures</a></p>';

    structures_directory = log_directory + 'structures/structures';
    structure_directories = fs.readdirSync(structures_directory);
    slice_start = (page - 1) * items_per_page;
    slice_end = slice_start + items_per_page;

    doc += '<p>';
    if (page > 1) {
	doc += '<a href="structures?run_id=' + run_id
	    + '&page=1&items_per_page=' + items_per_page
	    + '">First Page</a> ';
	doc += '<a href="structures?run_id=' + run_id
	    + '&page=' + (page - 1)
	    +'&items_per_page=' + items_per_page
	    + '">Previous Page</a> ';
    }
    doc += page + ' ';
    last_page = Math.ceil(structure_directories.length / items_per_page);
    if (page < last_page) {
	doc += '<a href="structures?run_id=' + run_id
	    + '&page=' + (page + 1)
	    +'&items_per_page=' + items_per_page
	    + '">Next Page</a> ';
	doc += '<a href="structures?run_id=' + run_id
	    + '&page=' + last_page
	    + '&items_per_page=' + items_per_page
	    + '">Last Page</a> ';
    }
    doc += '</p>';

    doc += '<ul>';
    structure_directories.slice(slice_start, slice_end).forEach(directory => {
	url = 'structure_lifetime?run_id=' + run_id + '&structure_id=' + directory;
	doc += '<ul><a href="' + url + '">' + directory + '</a></ul>';
    });
    doc += '</ul>';
    doc += '</body></html>';
    return doc;
}
