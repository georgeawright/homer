const fs = require('fs');
const {spawn} = require('child_process');

exports.get_graph = function(run_id, structure_id, time) {
    const structure_directory = `logs/${run_id}/structures/structures/${structure_id}`;
    const file_name = `${time}.svg`;
    const structure_files = fs.readdirSync(structure_directory);
    if (file_name in structure_files) {
	return `${structure_directory}/${file_name}`;
    }
    const python = spawn(
	'python',
	['log_viewer/generate_graph.py', run_id, structure_id, time]
    );
    python.stdout.on('data', (data) => {
	console.log(`stdout: ${data}`);
    });
    python.stderr.on('data', (data) => {
	console.log(`stdout: ${data}`);
    });
    python.on('close', (code) => {
	console.log(`child process exited with code ${code}`);
    });
    return `${structure_directory}/${file_name}`;
}

exports.json_to_html = function(input,query) {
    console.log(input, is_codelet_id(input));
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

exports.generate_graph_script = function (div_id, data, x_title, y_title) {
    return `
<script>
  var margin = {top: 10, right: 30, bottom: 30, left: 60},
	width = 640 - margin.left - margin.right,
	height = 480 - margin.top - margin.bottom;
  var svg = d3.select('#${div_id}')
	.append('svg')
	.attr('width', width + margin.left + margin.right)
	.attr('height', height + margin.top + margin.bottom)
	.append('g')
	.attr('transform', \`translate(\${margin.left},\${margin.top})\`);
  var data = ${data};
  var x = d3.scaleLinear()
	.domain(d3.extent(data, function(d) { return d.time; }))
	.range([ 0, width ]);
  svg.append('g')
    .attr('transform', \`translate(0, \${height})\`)
    .call(d3.axisBottom(x))
    .append("text")
    .attr("class", "axis-title")
    .attr("x", width/2)
    .attr("y", 30)
    .style("text-anchor", "middle")
    .attr("fill", "#000000")
    .text("${x_title}");
  var y = d3.scaleLinear()
	.domain([0, d3.max(data, function(d) { return d.value; })])
	.range([ height, 0 ]);
  svg.append('g')
    .call(d3.axisLeft(y))
    .append("text")
    .attr("class", "axis-title")
    .attr("transform", "rotate(-90)")
    .attr("x", -height/2)
    .attr("y", -30)
    .style("text-anchor", "end")
    .attr("fill", "#000000")
    .text("${y_title}");
  svg.append('path')
    .datum(data)
    .attr('fill', 'none')
    .attr('stroke', 'steelblue')
    .attr('stroke-width', 1.5)
    .attr('d', d3.line()
          .x(function(d) { return x(d.time) })
          .y(function(d) { return y(d.value) })
         )
</script>
`;
}

structure_to_html = function(id, query) {
    console.log(query);
    if (id === null) {
	return "undefined";
    }
    var structure_directory = 'logs/' + query.run_id + '/structures/structures/' + id;
    var structure_files = fs.readdirSync(structure_directory).filter(
	(f) => {return f.endsWith("json")}
    );
    var structure_file = '';
    var latest_time = -1;
    structure_files.forEach(file => {
	time = Number(file.split(".")[0]);
	if (time <= query.time && time > latest_time) {
	    structure_file = file;
	    latest_time = time;
	}
    });
    structure_file = structure_directory + '/' + structure_file;
    var structure_json = JSON.parse(fs.readFileSync(structure_file));
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
	|| /Publisher[0-9]+$/.exec(str)
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
