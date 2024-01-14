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
let scaleElement = document.getElementById('scale');
let marginTopElement = document.getElementById('margin-top');
let marginLeftElement = document.getElementById('margin-left');
let scale = parseFloat(scaleElement.value);
let marginTop = parseFloat(marginTopElement.value);
let marginLeft = parseFloat(marginLeftElement.value);
const iframe = document.createElement('iframe');
function updatePreview() {
    const htmlCode = htmlEditor.getValue();
    const cssCode = cssEditor.getValue();
    const jsCode = jsEditor.getValue();
    var viewport = document.getElementById('screen');
    
    // Clear existing content
    iframe.innerHTML = "";
    
    iframe.style.width = "100%";
    iframe.style.height = "100%";
    iframe.style.border = "0";
    viewport.appendChild(iframe);
    
    // Write HTML and CSS to the iframe document
    var doc = iframe.contentDocument || iframe.contentWindow.document;
    doc.open();
    doc.write("<body>" + htmlCode + "</body>");
    doc.write(`<style> body{background-color:black; transform: scale(${scale}) !important; margin-top: ${marginTop}vw !important; margin-Left: ${marginLeft}vw !important; overflow: hidden !important;} ${cssCode} </style>`)
    doc.write("<script>" + jsCode + "</script>");
    doc.close();
    console.log(doc)

    return null;
}

// Scale
const decreaseScale = () => {
    scale = parseFloat(scaleElement.value);
    scale = scale - (0.1 * scale);
    scaleElement.value = scale;
    return updatePreview();
}
const increaseScale = () => {
    scale = scale + (0.1 * scale);
    scaleElement.value = scale;
    return updatePreview();
}

// Direction Pad
const moveUp = () => {
    marginTop = marginTop - 2;
    marginTopElement.value = marginTop;
    return updatePreview();
}
const moveDown = () => {
    marginTop = marginTop + 2;
    marginTopElement.value = marginTop;
    return updatePreview();
}
const moveRight = () => {
    marginLeft = marginLeft + (3);
    marginLeftElement.value = marginLeft;
    return updatePreview();
}
const moveLeft = () => {
    marginLeft = marginLeft - (3);
    marginLeftElement.value = marginLeft;
    return updatePreview();
}

// Visibility Button
const publicIcon = document.querySelector('.public-icon')
const privateIcon = document.querySelector('.private-icon')
const publicButton = document.querySelector('.public-button')
const privateButton = document.querySelector('.private-button')
const isPublic = document.getElementById('is-public')
const togglePublic = (element) => {
    privateButton.style.opacity = 0.4;
    element.style.opacity = 0.85;
    privateIcon.style.display = 'none';
    publicIcon.style.display = 'contents';
    isPublic.value = 1;
}
const togglePrivate = (element) => {
    publicButton.style.opacity = 0.4;
    element.style.opacity = 0.85;
    publicIcon.style.display = 'none';
    privateIcon.style.display = 'contents';
    isPublic.value = 0;
}
