document.addEventListener('DOMContentLoaded', () => {
    // Edit Post
    
    // set a variable for all edit buttons
    let editButtons = document.querySelectorAll(".edit");
    //loop through edit buttons
    editButtons.forEach((editButton) => {
        // set a variable for the post id
        let postId = editButton.dataset.id;
        // set a variable for the content element
        let content = editButton.nextElementSibling;
        // set a variable for the date element
        let date = content.nextElementSibling;
        // create a new element for editing the content
        let editContent = document.createElement('textarea');
        // set style attributes for content editing element
        editContent.style.width = "100%";
        editContent.rows = "4";
        // create a submit button
        let save = document.createElement('button');
        save.innerHTML = "Save"
        save.style.marginBottom = "7px"
        save.className = "btn btn-primary"
        save.type = "submit"
        // create a form for editing the content
        let editForm = document.createElement('form');
        // add the content editing element and submit button to the edit form
        editForm.appendChild(editContent)
        editForm.appendChild(save)
        // insert the edit form before the date element to keep consisting layout
        editButton.parentNode.insertBefore(editForm, date)
        // add the original content text to the edit content element
        editContent.innerHTML += content.innerHTML
        // keep the edit form hidden until the edit link is clicked
        editForm.style.display = "none"

        //set an event listener on click for the edit button
        editButton.addEventListener("click", (e) => {
            // prevent default behavious to not refresh the page
            e.preventDefault()
            // hide the content element and show the edit form
            content.style.display = 'none';
            editForm.style.display = "block"
            console.log(editForm)
            // add event listner for the form submission
            editForm.addEventListener('submit', (e) => {
                e.preventDefault()
                //fetch view from server
                fetch(`edit_post/${postId}`, {
                    method: "post",
                    body:JSON.stringify({content:editContent.value})
                })
                .then(res => res.json())
                .then(result => {
                    console.log(result)
                    content.style.display = "block"
                    content.innerHTML = result.content
                    editForm.style.display = "none"
                })
            })
        })        
    })
    

    //Like Post

    // set a variable for all like buttons
    let likeButtons = document.querySelectorAll('.like');
    //loop through the list of like buttons
    likeButtons.forEach(function(likeButton) {
        // Set a variable for the post id
        let post_id = likeButton.dataset.id;
        // Set an event listner for like button onclick
        likeButton.addEventListener('click', (e) => { 
            //prevent default
            e.preventDefault()       
            //Fetch view from server
            fetch(`like_post/${post_id}`, {
                method: 'put',
            })
                //Transform response to json
                .then(res => res.json())
                .then(data => {
                    console.log(data)
                    // set a variable for like count 
                    let likeCounter = document.querySelectorAll('#likeCounter');
                    // loop through the list of like counts 
                    likeCounter.forEach(function(likeCounter) {
                        //Confirm the like counter is the one for this post by checking ids
                        if (likeCounter.dataset.id === post_id) {
                            //Update the new like count
                            likeCounter.innerHTML = ' ' + data.likeCount;
                        }
                    })
                    //check like status to change button to like or unlike
                    if (data.likeStatus === true) {
                        likeButton.innerHTML = "Unlike"
                    } else {
                        likeButton.innerHTML = "Like"
                    }
                })
        })
    })
});



