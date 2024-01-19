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
var newHeight = "calc(100vh / 3 - 1vh)"; // Adjust the height as needed
htmlEditor.setSize(null, newHeight);
cssEditor.setSize(null, newHeight);
jsEditor.setSize(null, newHeight);

// Attach onChange event after the editors are created
htmlEditor.on("change", updatePreview);
cssEditor.on("change", updatePreview);
jsEditor.on("change", updatePreview);

// Update screen preview
const iframe = document.createElement('iframe');
function updatePreview() {
    const htmlCode = htmlEditor.getValue();
    const cssCode = cssEditor.getValue();
    const jsCode = jsEditor.getValue();
    const scale = document.getElementById('scale').value
    const marginTop = document.getElementById('margin-top').value
    const marginLeft = document.getElementById('margin-left').value
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

// Like project
const likeCountElement = document.querySelector('[data-like-count]')
let likeCount = parseInt(likeCountElement.getAttribute('data-like-count'))
const toggleLike = (projectId) => {
    const likeIcon = document.querySelector(`[data-like-projectId='${projectId}']`)
    let isLiked = likeIcon.getAttribute('data-is-liked');
    if(isLiked == 1){
        likeIcon.classList.remove('fa-solid');
        likeIcon.classList.add('fa-regular')
        fetch(`/TrixEx/like/project/${projectId}`)
        likeIcon.setAttribute('data-is-liked', 0);
        likeCount -= 1;
        likeCountElement.innerHTML = likeCount;
        likeCountElement.setAttribute('data-like-count', likeCount)
    }
    else{
        likeIcon.classList.remove('fa-regular')
        likeIcon.classList.add('fa-solid');
        fetch(`/TrixEx/like/project/${projectId}`)
        likeIcon.setAttribute('data-is-liked', 1);
        likeCount += 1;
        likeCountElement.innerHTML = likeCount;
        likeCountElement.setAttribute('data-like-count', likeCount)
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

// Like comment
const toggleCommentLike = (commentId) => {
    const commentLikeCountElement = document.querySelector(`[data-comment-like-count-commentId='${commentId}']`)
    let commentLikeCount = parseInt(commentLikeCountElement.getAttribute('data-comment-like-count'))
    const commentLikeIcon = document.querySelector(`[data-like-commentId='${commentId}']`)
    let isLiked = commentLikeIcon.getAttribute('data-is-liked');
    if(isLiked == 1){
        commentLikeIcon.classList.remove('fa-solid');
        commentLikeIcon.classList.add('fa-regular')
        fetch(`/TrixEx/like/comment/${commentId}`)
        commentLikeIcon.setAttribute('data-is-liked', 0);
        commentLikeCount -= 1;
        commentLikeCountElement.innerHTML = commentLikeCount;
        commentLikeCountElement.setAttribute('data-comment-like-count', commentLikeCount)
    }
    else{
        commentLikeIcon.classList.remove('fa-regular')
        commentLikeIcon.classList.add('fa-solid');
        fetch(`/TrixEx/like/comment/${commentId}`)
        commentLikeIcon.setAttribute('data-is-liked', 1);
        commentLikeCount += 1;
        commentLikeCountElement.innerHTML = commentLikeCount;
        commentLikeCountElement.setAttribute('data-comment-like-count', commentLikeCount)
    }
    console.log(commentLikeCountElement)
    
}

// Show Reply input
const showReply = commentId => {
    const replyInputElement = document.querySelector(`[data-reply-input-commentId='${commentId}']`)
    replyInputElement.style.display = 'flex';
}
const hideReply = commentId => {
    const replyInputElement = document.querySelector(`[data-reply-input-commentId='${commentId}']`)
    replyInputElement.style.display = 'none';
}