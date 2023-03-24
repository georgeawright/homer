fs = require('fs');

exports.json_to_html = function(input,query) {
    if (typeof(input) === 'number') {
	return input;
    }
    if (typeof(input) === 'string') {
	if (is_structure_id(input)) {
	    return structure_to_html(input, query);
	}
	if (is_codelet_id(input)) {
	    return '<a href="codelet?run_id=' + query.run_id
		+ '&codelet_id=' + input + '">'
		+ input + '</a>';
	}
	return input.replace("<", "&lt").replace(">", "&gt");
    }
    if (input === null) {
	return "undefined";
    }
    if (Array.isArray(input)) {
	html_string = '<ul>';
	input.forEach(item => {
	    html_string += '<li>' + exports.json_to_html(item, query) + '</li>';
	});
	html_string += '</ul>';
	return html_string;
    }
    if (typeof(input) === 'object') {
	console.log(input);
	html_string = '<table>';
	Object.entries(input).forEach(([k,v]) => {
	    html_string += '<tr>'
		+ '<td>' + exports.json_to_html(k, query) + '</td>'
		+ '<td>' + exports.json_to_html(v, query) + '</td>'
		+ '</tr>';
	});
	html_string += '</table>';
	return html_string;
    }
}

structure_to_html = function(id, query) {
    if (id === null) {
	return "undefined";
    }
    var structure_directory = 'logs/' + query.run_id + '/structures/structures/' + id;
    var structure_files = fs.readdirSync(structure_directory);
    var structure_file = '';
    console.log(id);
    var latest_time = 0;
    structure_files.forEach(file => {
	time = file.split(".")[0];
	if (time <= query.time && time > latest_time) {
	    structure_file = file;
	    latest_time = time;
	}
    });
    structure_file = structure_directory + '/' + structure_file;
    console.log(structure_file);
    var structure_json = JSON.parse(fs.readFileSync(structure_file));
    console.log(structure_json);

    if (is_chunk_id(id)
	|| is_contextual_space_id(id)
	|| is_view_id(id)
       ) {
	return '&lt'
	    + '<a href="structure_snapshot?run_id=' + query.run_id
	    + '&structure_id=' + id
	    + '&time=' + query.time + '">'
	    + id + '</a>&gt';
    }
    if (is_concept_id(id)
	|| is_conceptual_space_id(id)
	|| is_frame_id(id)
	|| is_letter_chunk_id(id)
       ) {
	return '&lt'
	    + '<a href="structure_snapshot?run_id=' + query.run_id
	    + '&structure_id=' + id
	    + '&time=' + query.time + '">'
	    + id + '</a> ' + structure_json.name + '&gt';
    }
    if (is_correspondence_id(id)) {
	return '&lt'
	    + '<a href="structure_snapshot?run_id=' + query.run_id
	    + '&structure_id=' + id
	    + '&time=' + query.time + '">'
	    + id + '</a> '
	    + structure_to_html(structure_json.parent_concept, query)
	    + '-' + structure_to_html(structure_json.conceptual_space, query)
	    + '(' + '<br>'
	    + '&emsp;' + structure_to_html(structure_json.start, query)
	    + ', ' + '<br>'
	    + '&emsp;' + structure_to_html(structure_json.end, query) + '<br>'
	    + ') ' + structure_to_html(structure_json.parent_view, query) + '&gt';
    }
    if (is_label_id(id)) {
	return '&lt'
	    + '<a href="structure_snapshot?run_id=' + query.run_id
	    + '&structure_id=' + id
	    + '&time=' + query.time + '">'
	    + id + '</a> '
	    + structure_to_html(structure_json.parent_concept, query)
	    + '(' + structure_to_html(structure_json.start, query) + ')'
	    + '&gt';
    }
    if (is_relation_id(id)) {
	return '&lt'
	    + '<a href="structure_snapshot?run_id=' + query.run_id
	    + '&structure_id=' + id
	    + '&time=' + query.time + '">'
	    + id + '</a> '
	    + structure_to_html(structure_json.parent_concept, query)
	    + '-' + structure_to_html(structure_json.conceptual_space, query)
	    + '(' + structure_to_html(structure_json.start, query)
	    + ', ' + structure_to_html(structure_json.end, query) + ')'
	    + '&gt';
    }
} 

is_codelet_id = function(str) {
    return /Builder[0-9]+$/.exec(str)
	|| /Evaluator[0-9]+$/.exec(str)
	|| /Selector[0-9]+$/.exec(str)
	|| /Suggester[0-9]+$/.exec(str)
	|| /Setter[0-9]+$/.exec(str)
	|| /Factory[0-9]+$/.exec(str)
	|| /Collector[0-9]+$/.exec(str)
	|| /Porter[0-9]+$/.exec(str)
	|| /Recycler[0-9]+$/.exec(str);
}

is_structure_id = function(str) {
    return is_chunk_id(str)
	|| is_concept_id(str)
	|| is_conceptual_space_id(str)
	|| is_contextual_space_id(str)
	|| is_correspondence_id(str)
	|| is_frame_id(str)
	|| is_label_id(str)
	|| is_letter_chunk_id(str)
	|| is_relation_id(str)
	|| is_view_id(str);
}

is_chunk_id = (str) => /^Chunk[0-9]+$/.exec(str);
is_concept_id = (str) => /^Concept[0-9]+$/.exec(str);
is_conceptual_space_id = (str) => /^ConceptualSpace[0-9]+$/.exec(str);
is_contextual_space_id = (str) => /^ContextualSpace[0-9]+$/.exec(str);
is_correspondence_id = (str) => /^Correspondence[0-9]+$/.exec(str);
is_frame_id = (str) => /^Frame[0-9]+$/.exec(str);
is_label_id = (str) => /^Label[0-9]+$/.exec(str);
is_letter_chunk_id = (str) => /^LetterChunk[0-9]+$/.exec(str);
is_relation_id = (str) => /^Relation[0-9]+$/.exec(str);
is_view_id = (str) => /^View[0-9]+$/.exec(str);
