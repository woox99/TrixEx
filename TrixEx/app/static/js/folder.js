// Get all public projects
const getAllProjectsByUser = (userId) => {
    fetch(`/TrixEx/getAllByUser/${userId}`) //change this to encoded. I think the @ in the email address is messing up java
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

// Follow User
const toggleFollow = (followeeId) => {
    const followIcon = document.querySelector('.fa-user-plus');
    const followText = document.querySelector('.follow');
    let isFollowing = followIcon.getAttribute('data-is-following');
    const followerCountElement = document.querySelector('.follower-count');
    let followerCount = parseInt(followerCountElement.getAttribute('data-follower-count'));

    if(isFollowing == 1){
        followIcon.style.display = 'contents';
        followIcon.style.marginRight = '0.25vw';
        followText.classList.add('green')
        followText.innerHTML = 'Follow';
        followText.style.opacity = '1'
        fetch(`/TrixEx/follow/${followeeId}`)
        followerCount -= 1;
        followerCountElement.innerHTML = followerCount;
        followerCountElement.setAttribute('data-follower-count', followerCount);
        followIcon.setAttribute('data-is-following', 0);
    }
    else{
        followIcon.style.display = 'none';
        followText.classList.remove('green')
        followText.innerHTML = 'unfollow';
        followText.style.opacity = '0.4'
        fetch(`/TrixEx/follow/${followeeId}`)
        followerCount += 1;
        followerCountElement.innerHTML = followerCount;
        followerCountElement.setAttribute('data-follower-count', followerCount);
        followIcon.setAttribute('data-is-following', 1);
    }
    
}

// Show motto edit input
const input = document.querySelector('.motto-input');
const currMotto = document.querySelector('.current-motto');
const saveButton = document.querySelector('.save-button')
const editButton = document.querySelector('.edit-button')
const showInput = (element) => {
    editButton.style.display = 'none';
    currMotto.style.display = 'none';
    input.style.display = 'block';
    saveButton.style.display = 'block';
}
const hideInput = (element) => {
    editButton.style.display = 'block';
    currMotto.style.display = 'block';
    input.style.display = 'none';
    saveButton.style.display = 'none';
}

// Show Select Menu
const showSelect = (projectId) => {
    // Hide any open select menus
    const allSelectMenus = document.querySelectorAll('.select-menu');
    for(const selectMenu of allSelectMenus){
        selectMenu.style.display = 'none';
    }

    const selectMenu = document.querySelector(`[data-select-menu-projectId='${projectId}']`)
    selectMenu.style.display = 'block';

}
// Hide Select Menu
const hideSelect = (projectId) => {
    const selectMenu = document.querySelector(`[data-select-menu-projectId='${projectId}']`);
    selectMenu.style.display = 'none';
}


// Make public
const makePublic = (projectId) => {
    publicButtonElement = document.querySelector(`[data-public-button-projectId='${projectId}']`)
    privateButtonElement = document.querySelector(`[data-private-button-projectId='${projectId}']`)
    privateIcon = document.querySelector(`[data-private-icon-projectId='${projectId}']`)
    fetch(`/TrixEx/visibility/${projectId}`)
    privateIcon.style.display = 'none';
    publicButtonElement.style.display = 'none';
    privateButtonElement.style.display = 'flex';
}
const makePrivate = (projectId) => {
    publicButtonElement = document.querySelector(`[data-public-button-projectId='${projectId}']`)
    privateButtonElement = document.querySelector(`[data-private-button-projectId='${projectId}']`)
    privateIcon = document.querySelector(`[data-private-icon-projectId='${projectId}']`)
    fetch(`/TrixEx/visibility/${projectId}`)
    privateIcon.style.display = 'flex';
    publicButtonElement.style.display = 'flex';
    privateButtonElement.style.display = 'none';
}

// Show confirm delete
const showConfirmDelete = (projectId) => {
    const confirmDelete = document.querySelector(`[data-confirm-delete-projectId='${projectId}']`);
    confirmDelete.style.display = 'block';
}
const hideConfirmDelete = (projectId) => {
    const confirmDelete = document.querySelector(`[data-confirm-delete-projectId='${projectId}']`);
    confirmDelete.style.display = 'none';
}

