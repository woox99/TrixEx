// Get all public projects
const getProjects = () => {
    fetch('/TrixEx/getAll') //change this to encoded. I think the @ in the email address is messing up java
        .then(res => res.json())
        .then(projects => {
            for (const project of projects) {
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

// Bookmark project
const toggleBookmark = (projectId) => {
    const bookmarkIcon = document.querySelector(`[data-bookmark-projectId='${projectId}']`)
    let isBookmarked = bookmarkIcon.getAttribute('data-is-bookmarked');
    if(isBookmarked == 1){
        bookmarkIcon.classList.remove('fa-solid');
        bookmarkIcon.classList.remove('selected');
        bookmarkIcon.classList.add('fa-regular')
        fetch(`/TrixEx/bookmark/${projectId}`)
        bookmarkIcon.setAttribute('data-is-bookmarked', 0);
    }
    else{
        bookmarkIcon.classList.remove('fa-regular')
        bookmarkIcon.classList.add('fa-solid');
        bookmarkIcon.classList.add('selected');
        fetch(`/TrixEx/bookmark/${projectId}`)
        bookmarkIcon.setAttribute('data-is-bookmarked', 1);
    }
    
}

// like project
const toggleLike = (projectId) => {
    const likeIcon = document.querySelector(`[data-like-projectId='${projectId}']`)
    let isLiked = likeIcon.getAttribute('data-is-liked');
    if(isLiked == 1){
        likeIcon.classList.remove('fa-solid');
        // likeIcon.classList.remove('selected');
        likeIcon.classList.add('fa-regular')
        fetch(`/TrixEx/like/${projectId}`)
        likeIcon.setAttribute('data-is-liked', 0);
    }
    else{
        likeIcon.classList.remove('fa-regular')
        likeIcon.classList.add('fa-solid');
        // likeIcon.classList.add('selected');
        fetch(`/TrixEx/like/${projectId}`)
        likeIcon.setAttribute('data-is-liked', 1);
    }
    
}

// Carousel Movement
const moveCarouselLeftButton = document.querySelector('.carousel-left-button')
const moveCarouselRightButton = document.querySelector('.carousel-right-button')
const pages = Math.ceil(document.querySelectorAll('.item').length / 6);
let page = 1;
let carouselMarginLeft = 0;
const moveCarouselRight = () => {
    const carousel = document.querySelector('.carousel');
    carouselMarginLeft -= 93;
    carousel.style.marginLeft = `calc(${carouselMarginLeft}vw)`;
    
    // Disable right button if on last page
    page += 1;
    if(page >= pages){
        moveCarouselRightButton.disabled = true;
        moveCarouselRightButton.style.opacity = '0.3';
    }
    moveCarouselLeftButton.disabled = false;
    moveCarouselLeftButton.style.opacity = '1.0';
}
const moveCarouselLeft = () => {
    const carousel = document.querySelector('.carousel');
    carouselMarginLeft += 93;
    carousel.style.marginLeft = `calc(${carouselMarginLeft}vw)`;
    
    // Disable left button if on first page
    page -= 1;
    if(page <= 1){
        moveCarouselLeftButton.disabled = true;
        moveCarouselLeftButton.style.opacity = '0.3';
    }
    moveCarouselRightButton.disabled = false;
    moveCarouselRightButton.style.opacity = '1.0';
}