// Text Editor
var htmlEditor = CodeMirror.fromTextArea(document.getElementById("htmlEditor"), {
    lineNumbers: true,
    mode: "htmlmixed", // Set the programming language mode
    htmlMode: true,
    theme: 'moxer',
    onChange: updatePreview, // Use CodeMirror's onChange event
});

var cssEditor = CodeMirror.fromTextArea(document.getElementById("cssEditor"), {
    lineNumbers: true,
    mode: "css", // Set the programming language mode
    theme: 'moxer',
});

var jsEditor = CodeMirror.fromTextArea(document.getElementById("jsEditor"), {
    lineNumbers: true,
    mode: "javascript", // Set the programming language mode
    theme: 'moxer',
});

// Set the height for each editor
var newHeight = "calc(100vh / 3)"; // Adjust the height as needed
htmlEditor.setSize(null, newHeight);
cssEditor.setSize(null, newHeight);
jsEditor.setSize(null, newHeight);

// Attach onChange event after the editors are created
htmlEditor.on("change", updatePreview);
cssEditor.on("change", updatePreview);
jsEditor.on("change", updatePreview);

// Update screen preview
function updatePreview() {
    const htmlCode = htmlEditor.getValue();
    const cssCode = cssEditor.getValue();
    const jsCode = jsEditor.getValue();
    var iframe = document.getElementById('screen');

    // Clear existing content
    iframe.innerHTML = "";


    // Write HTML and CSS to the iframe document
    var doc = iframe.contentDocument || iframe.contentWindow.document;
    doc.open();
    doc.write("<body>" + htmlCode + "</body>");
    doc.write("<style>" + cssCode + "</style>");
    doc.write("<script>" + jsCode + "</" + "script>");
    doc.close();
}