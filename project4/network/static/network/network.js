document.addEventListener('DOMContentLoaded', function() {

    // document.querySelector('#following').addEventListener('click', () => load_posts('following'));
    document.querySelector('#post-form').addEventListener('submit', (event) => {
        submit_post();
        event.preventDefault();
    });
    load_posts('all');

    for (child of document.querySelector('#post-view-table-html').children) {
        child.addEventListener('click', (event) => {
            if (event.target.id.includes("user")) {
                console.log(`data = ${event.target.innerHTML}`);
            };
        });
    };

});

function load_posts(filter) {
    const token = document.querySelector('[name="csrfmiddlewaretoken"]').value;
    const posts_view_table = document.querySelector('#posts-view-table');



    document.querySelector('#posts-view-title').innerHTML = 
        `<h3>${filter.charAt(0).toUpperCase() + filter.slice(1)}</h3>`;

    // get posts
    fetch(`/posts?filter=${filter}`, {
        headers: {
            "X-CSRFToken": token,
        }
    })
    .then(response => {
        let post_item = document.createElement('div');
        posts_view_table.appendChild(post_item);
        console.log(response)
    });
    // .then(response => response.json())
    // .then(posts => {
    //     posts.forEach(post => {

    //         let post_item = document.createElement('div');
    //         post_item.id = `post-${post.id}`;
    //         post_item.classList.add('row', 'border');

    //         posts_view_table.appendChild(post_item);

    //         post_contents = document.createElement('div');
    //         post_item.appendChild(post_contents); 
    //         post_contents.id = `${post_item.id}-content`;
    //         post_contents.classList.add("col");
    //         for (const field in post) {
    //             const field_id = `${post_item.id}-${field}`;
    //             field_element = document.createElement('div');
    //             field_element.id = field_id;
    //             field_element.innerHTML = `${field}: ${post[field]}`;
    //             post_contents.appendChild(field_element);
    //         }
    //     });
    // });

    // Each post should include the username, the content, the date and time the post was made, and number of “likes”
};

function submit_post() {
    
    content = document.querySelector('#post-text').value;
    const token = document.querySelector('[name="csrfmiddlewaretoken"]').value;

    fetch('/post', {
        method: 'POST',
        body: JSON.stringify({ 
            content: content 
        }),
        headers: {
            "X-CSRFToken": token,
            "Content-Type": "application/json"
        }
    }).then(load_posts('all'));
};

function edit_post() {
    // When a user clicks “Edit” for one of their own posts, the content of their post should be replaced with a textarea where the user can edit the content of their post.
    // The user should then be able to “Save” the edited post. Using JavaScript, you should be able to achieve this without requiring a reload of the entire page.
    // For security, ensure that your application is designed such that it is not possible for a user, via any route, to edit another user’s posts.
};


function like_post() {
    // Using JavaScript, you should asynchronously let the server know to update the like count 
    // (as via a call to fetch) and then update the post’s like count displayed on the page, without requiring a reload of the entire page.
};

function follow_user() {

};

function load_profile(username) {

    // Display the number of followers the user has, as well as the number of people that the user follows.
    // Display all of the posts for that user, in reverse chronological order.
    // For any other user who is signed in, this page should also display a “Follow” or “Unfollow” button that will let the current user toggle whether or not they are following this user’s posts. Note that this only applies to any “other” user: a user should not be able to follow themselves.
};
