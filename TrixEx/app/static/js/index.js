// ########## SCROLL TO SECTION #########
document.addEventListener("DOMContentLoaded", function () {
    // Add smooth scrolling behavior to links with the "smooth-scroll" class
    const smoothScrollLinks = document.querySelectorAll(".smooth-scroll");

    smoothScrollLinks.forEach(function (link) {
        link.addEventListener("click", function (e) {
            e.preventDefault(); // Prevent the default link behavior

            const targetId = this.getAttribute("href").substring(1); // Get the target element's ID
            const targetElement = document.getElementById(targetId);

            if (targetElement) {
                // Scroll smoothly to the target element
                targetElement.scrollIntoView({
                    behavior: "smooth",
                });
            }
        });
    });
});

// Carousel
var carousel = $(".carousel"),
    currdeg = 0;

$(".next").on("click", { d: "n" }, rotate);
$(".prev").on("click", { d: "p" }, rotate);

function rotate(e) {
    if (e.data.d == "n") {
        currdeg = currdeg - 60;
    }
    if (e.data.d == "p") {
        currdeg = currdeg + 60;
    }
    carousel.css({
        "-webkit-transform": "rotateY(" + currdeg + "deg)",
        "-moz-transform": "rotateY(" + currdeg + "deg)",
        "-o-transform": "rotateY(" + currdeg + "deg)",
        "transform": "rotateY(" + currdeg + "deg)"
    });
}

// Get all landing projects
const getProjects = () => {
    fetch('/TrixEx/getAllLanding') 
        .then(res => res.json())
        .then(projects => {
            for (const project of projects) {
                console.log(project.title)
                const iframe = document.querySelector(`[data-project-id="${project.id}"]`)
                const htmlCode = project.html;
                const cssCode = project.css;
                const jsCode = project.js;
                const scale = project.scale;
                const marginTop = project.margin_top;
                const marginLeft = project.margin_left;
                
                // Clear existing content
                iframe.innerHTML = "";

                // Write HTML and CSS to the iframe document
                var doc = iframe.contentDocument || iframe.contentWindow.document;
                doc.open();
                doc.write("<body>" + htmlCode + "</body>");
                doc.write(`<style> body{background-color:black; transform: scale(${scale}) !important; margin-top: ${marginTop}vw !important; margin-Left: ${marginLeft}vw !important; overflow: hidden !important;} ${cssCode} </style>`)
                doc.write("<script>" + jsCode + "</" + "script>");
                doc.close();
                console.log()
                console.log(doc)
            }
            return null;

        })
}