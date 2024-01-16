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
var carousel = document.querySelector('.carousel');
let currdeg = 0;

function rotateCarousel() {
    currdeg -= 0.2;
    carousel.style.transform = "rotateY(" + currdeg + "deg)";
}
setInterval(rotateCarousel, 1);

// function turnCarousel() {
//     currdeg -= 60;
//     carousel.style.transform = "rotateY(" + currdeg + "deg)";
// }
// setInterval(turnCarousel, 3000);


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
                doc.write(`<style> body{background-color:#00000050 !important; transform: scale(${scale}) !important; margin-top: ${marginTop}vw !important; margin-Left: ${marginLeft}vw !important; overflow: hidden !important;} ${cssCode} </style>`)
                doc.write("<script>" + jsCode + "</" + "script>");
                doc.close();
                console.log()
                console.log(doc)
            }
            return null;

        })
}