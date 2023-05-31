var fs = require('fs');
var tools = require('./tools');

exports.run = function(query) {
    programs_results = {};
    directories = [];
    fs.readdirSync('logs/').forEach(directory => {
	directories.push(directory);
	details_file = `logs/${directory}/details.txt`;
	details = JSON.parse(fs.readFileSync(details_file));
	program_name = details["Program"];
	if (!(program_name in programs_results)) {
	    programs_results[program_name] = {};
	}
	program_results = programs_results[program_name];
	output = details["result"];
	if (!(output in program_results)) {
	    program_results[output] = {
		"satisfaction": [details["satisfaction"]],
		"codelets_run": [details["codelets_run"]],
		"directory": [directory],
		"seed": [details["random_seed"]],
	    };
	} else {
	    program_results[output]["satisfaction"].push(details["satisfaction"]);
	    program_results[output]["codelets_run"].push(details["codelets_run"]);
	    program_results[output]["directory"].push(directory);
	    program_results[output]["seed"].push(details["random_seed"]);
	}
    });
    Object.keys(programs_results).forEach(program => {
	program_results = programs_results[program];
	Object.keys(program_results).forEach(output => {
	    program_results[output]["satisfaction"] = tools.array_average(
		program_results[output]["satisfaction"]
	    );
	    program_results[output]["codelets_run"] = tools.array_average(
		program_results[output]["codelets_run"]
	    );
	});
    });
    programs_results_lists = {};
    Object.keys(programs_results).forEach(program => {
	program_results = programs_results[program];
	programs_results_lists[program] = [];
	Object.keys(program_results).forEach(output => {
	    programs_results_lists[program].push({
		"output": output,
		"satisfaction": program_results[output]["satisfaction"],
		"codelets_run": program_results[output]["codelets_run"],
		"seed": program_results[output]["seed"],
		"directory": program_results[output]["directory"],
	    });
	});
	programs_results_lists[program].sort((a,b) => {
	    return b["satisfaction"] - a["satisfaction"];
	});
    });
    doc = `
<html>
  <head>
    <style>
      table, th, td {
        border: 1px solid black;
        border-collapse: collapse;
        padding: 5px;
      }
    </style>
  </head>
  <body>
    <h1>Linguoplotter Saved Runs</h1>

    <h2>Summary of Results</h2>
`;
    Object.keys(programs_results_lists).forEach(program => {
	program_name = program.split(".")[0];
	doc += `
      <h3>${program_name}</h3>
      <table>
        <tr>
          <th style="width:30%">Output Text</th>
          <th style="width:10%">Mean Satisfaction</th>
          <th style="width:10%">Mean Run Length (Codelets)</th>
          <th style="width:10%">Random Seeds</th>
        <tr>
`;
	program_results = programs_results_lists[program];
	program_results.forEach(result => {
	    output = result["output"]
	    satisfaction = result["satisfaction"];
	    codelets_run = result["codelets_run"];
	    seeds = result["seed"];
	    program_directories = result["directory"];
	    doc += `
        <tr>
          <td>${output}</td>
          <td>${satisfaction}</td>
          <td>${codelets_run}</td>
          <td>
`;
	    seeds.forEach((seed, index) => {
		directory = program_directories[index];
		doc += `
            <a href="log_viewer/run?run_id=${directory}">${seed}</a>
`;
	    });
	    doc += `
          </td>
        <tr>
`;
	});
	doc += `
    </table>
`;
    });
    doc += `
    <h2>List of Runs</h2>
    <ul>
`;
    directories.forEach(directory => {
	doc += `
      <li><a href="log_viewer/run?run_id=${directory}">${directory}</a></li>
`;
    });
    doc += `
    </ul>

  </body>
</html>`;
    return doc;
}
