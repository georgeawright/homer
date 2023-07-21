var fs = require('fs');
var tools = require('./tools');

exports.run = function(query) {
    try {
	stats = JSON.parse(fs.readFileSync("logs/stats.txt"));
    } catch (err) {
	stats = {};
    }
    programs_results = {};
    directories = [];
    fs.readdirSync('logs/').forEach(directory => {
	if (directory == "stats.txt") {
	    return;
	}
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
	graph_file_name = `maps/${program_name}.svg`;
	graph_svg = fs.readFileSync(graph_file_name);
	program_stats = stats[program];
	try {
	    mean_satisfaction = program_stats["mean_satisfaction"];
	    mean_rouge = program_stats["mean_pairwise_rouge"];
	    mean_zss = program_stats["mean_pairwise_zss"];
	    median_satisfaction = program_stats["median_satisfaction"];
	    median_rouge = program_stats["median_pairwise_rouge"];
	    median_zss = program_stats["median_pairwise_zss"];
	} catch(err) {
	    mean_satisfaction = undefined;
	    mean_rouge = undefined;
	    mean_zss = undefined;
	    median_satisfaction = undefined;
	    median_rouge = undefined;
	    median_zss = undefined;
	}
	doc += `
      <h3>${program_name}</h3>
      <object type="image/svg+xml" with="50%">${graph_svg}</object>
      <p>Mean satisfaction: ${mean_satisfaction};
         Mean pairwise rouge: ${mean_rouge};
         Mean pairwise ZSS: ${mean_zss}</p>
      <p>Median satisfaction: ${median_satisfaction};
         Median pairwise rouge: ${median_rouge};
         Median pairwise ZSS: ${median_zss}</p>
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
