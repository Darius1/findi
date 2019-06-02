function print_text() {
    var pyshell = require("python-shell")
    var path = require("path")

    var text = document.getElementById("address").value

    var options = {
        scriptPath : path.join(__dirname, '/../'),
        args : [text]
    }

    pyshell.PythonShell.run('/findi/Findi/findi_scan_wrapper.py', options, function (err, results) {
        if (err) throw err;
        // results is an array consisting of messages collected during execution
        console.log('results: %j', results);
        alert(results[0])
      });
}
