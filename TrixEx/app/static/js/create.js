
// Initialize CodeMirror with different variable names
var htmleditor = CodeMirror.fromTextArea(document.getElementById("htmleditor"), {
    lineNumbers: true,
    mode: "htmlmixed", // Set the programming language mode
    htmlMode: true,
    theme: 'moxer',
});

var csseditor = CodeMirror.fromTextArea(document.getElementById("csseditor"), {
    lineNumbers: true,
    mode: "css", // Set the programming language mode
    theme: 'moxer',
});

var jseditor = CodeMirror.fromTextArea(document.getElementById("jseditor"), {
    lineNumbers: true,
    mode: "javascript", // Set the programming language mode
    theme: 'moxer',
});

// Set the height for each editor
var newHeight = "calc(100vh / 3)"; // Adjust the height as needed
htmleditor.setSize(null, newHeight);
csseditor.setSize(null, newHeight);
jseditor.setSize(null, newHeight);