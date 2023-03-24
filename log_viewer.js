var http = require('http');
var url = require('url');
var fs = require('fs');

http.createServer(function (req, res) {
    res.writeHead(200, {'Content-Type': 'text/html'});
    var request_url = url.parse(req.url, true);
    var path = request_url.pathname;
    var query = request_url.query;
    console.log(path)
    if (path == '/') {
	var module = require('./log_viewer/runs');
    }
    else {
	path = './' + path
	var module = require(path);
    }
    res.write(module.run(query));
    res.end()
}).listen(8080); 
