document.addEventListener("DOMContentLoaded", () => {
    //follow or un follow user

    //set a variable to the follow button
    let followButton = document.querySelector('.followButton');
    //set a variable for the user id
    let userId = followButton.dataset.id
    //set an event listener for the follow button
    followButton.addEventListener('click', (e) => {
        // prevent refreshing the page
        e.preventDefault()
        // fetch view from server
        fetch(`follow/${userId}`, {
            method: "put",            
        })
        .then(res => res.json())
        .then(result => {
            console.log(result.followers)
            console.log(result.following)
            console.log(result.message)
            if(result.message === "added") {
                document.querySelector('.followButton').innerHTML = 'Unfollow';
            } else {
                document.querySelector('.followButton').innerHTML = "Follow";
            }
            document.querySelector('.following').innerHTML = result.following + " Following";
            document.querySelector('.followers').innerHTML = result.followers + " Followers";
        })
    })
})