// globals
const path = window.location.pathname
const page_size = 10
let post_counter = 0

document.addEventListener('DOMContentLoaded', function() {
    const token = document.querySelector('[name="csrfmiddlewaretoken"]').value;

    // if on the profile page, add event listener to Follow/Unfollow button
    if (path.startsWith('/profile')) {
        const profile = JSON.parse(document.getElementById('profile').textContent);
        const button_follow = document.querySelector('#button-follow');
        if (button_follow) {
            button_follow.addEventListener('click', (event) => {
                event.preventDefault();
                become_follower(profile);
            });
        }; 
        load_posts(`${path.split('/')[2]}`)
    // if on the home page, add event listener to post form and load all posts
    } else if (path === '/') {
        document.querySelector('#post-form').addEventListener('submit', (event) => {
            submit_post();
            event.preventDefault();
        });
        load_posts('all');
    };
    // load posts of followed users
    document.querySelector('#following').addEventListener('click', () => {
        load_posts('following');
    });
});

// retrieve posts 
function load_posts(filter) {
    const posts_view_table = document.querySelector('#posts-view-table');
    const start_post = post_counter;
    const end_post = start_post + page_size -1
    post_counter = end_post + 1;

    posts_view_table.innerHTML = null;

    document.querySelector('#posts-view-title').innerHTML = 
        `<h4>Posts: ${filter.charAt(0).toUpperCase() + filter.slice(1)}</h4>`;

    // get posts
    fetch(`/get_posts?filter=${filter}&start_post=${start_post}&end_post=${end_post}`)
    .then(response => response.json())
    .then(posts => {
        // generate parent div for each post
        posts.forEach(post => {
            let post_item = document.createElement('div');
            post_item.id = `post-${post['id']}`;
            post_item.classList.add('row', 'border');
            posts_view_table.appendChild(post_item);
            
            // generate parent div for post fields
            post_contents = document.createElement('div');
            post_item.appendChild(post_contents); 
            post_contents.id = `${post_item.id}-contents`;
            post_contents.classList.add('col');

            // generate div for post buttons
            post_buttons = document.createElement('div');
            post_item.appendChild(post_buttons); 
            post_buttons.id = `${post_item.id}-buttons`;
            post_buttons.classList.add('col-2');
        
            // generate div for each post field
            for (const field in post) {
                const field_id = `${post_item.id}-${field}`;
                field_element = document.createElement('div');
                field_element.id = field_id;
                post_contents.appendChild(field_element);
                if (field === 'user__username') {
                    field_element.innerHTML = `<a href="/profile/${post[field]}">${post[field]}</a>`;
                } else if (field === 'timestamp') {
                    const formatted_date = Date(post[field]).toLocaleString()
                    field_element.innerHTML = `${field}: ${formatted_date}`;
                } else if (field === 'id') {
                    field_element.remove()
                } else {
                    field_element.innerHTML = `${field}: ${post[field]}`;
                };
            };
            
            // like button
            post_button_like = document.createElement('button');
            post_buttons.appendChild(post_button_like); 
            post_button_like.classList.add('btn', 'btn-primary');
            post_button_like.id = `${post_item.id}-button-like`;
            post_button_like.addEventListener('click', () => {
                like_post(post);
            });
            update_frontend_like_status(post);

            // edit button
            const request_username = JSON.parse(document.getElementById('request_username').textContent);
            if (request_username === post.user__username) {
                post_button_edit = document.createElement('button');
                post_buttons.appendChild(post_button_edit); 
                post_button_edit.classList.add('btn', 'btn-primary');
                post_button_edit.id = `${post_item.id}-button-edit`;
                post_button_edit.innerHTML = 'Edit';
                post_button_edit.addEventListener('click', () => {
                    edit_post(post)
                });
                //save button
                post_button_save = document.createElement('button');
                post_buttons.appendChild(post_button_save);
                post_button_save.classList.add('btn', 'btn-primary');
                post_button_save.id = `post-${post['id']}-button-save`;
                post_button_save.innerHTML = 'Save';
                post_button_save.style.display = 'none';
            };
        });
    });
    next_button = document.querySelector('#posts-pagination-next');
    next_button.style.display = 'block';
    next_button.addEventListener('click', () => {
        load_posts(filter)
    })
};

// create a new post
function submit_post() {
    
    content = document.querySelector('#post-text').value;

    fetch('/post', {
        method: 'POST',
        body: JSON.stringify({ 
            content: content 
        }),
        headers: {
            'X-CSRFToken': token,
            'Content-Type': 'application/json'
        }
    })
    .then(load_posts('all'));
};

function edit_post(post) {
    post_content = document.querySelector(`#post-${post['id']}-content`);
    post_button_save = document.querySelector(`#post-${post['id']}-button-save`);
    
    // create input textarea
    post_content_new = document.createElement('textarea');
    post_content_new.classList.add('form-control');
    post_content_new.id = 'post-edit';
    post_content.innerHTML = null;
    post_content.appendChild(post_content_new);

    // show save button
    post_button_save.style.display = 'block';
    post_button_save.addEventListener('click', () => {
        edit = document.querySelector('#post-edit').value;
        fetch('/edit', {
            method: 'POST',
            headers: {
                'X-CSRFToken': token,
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                edit: edit,
                post: post
            })
        })
        .then(response => response.json())
        .then(content => {
            post_content = document.querySelector(`#post-${post['id']}-content`);
            post_content.innerHTML = `content: ${content['updated_content']}`;
            post_button_save.style.display = 'none';
        });
    });
};

// like or unlike post
function like_post(post) {
    fetch('/like', {
        method: 'POST',
        headers: {
            'X-CSRFToken': token,
            'Content-Type': 'application/json'

        },
        body: JSON.stringify({
            post: post
        })
    })
    .then(response => response.json())
    .then(message => {
        console.log(message);
        update_frontend_like_status(post);
    });
};

// add or remove logged in user as follower of profile user
function become_follower(profile) {
    fetch('/follow_status', {
        method: 'POST',
        headers: {
            'X-CSRFToken': token,
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            profile: profile
        })
    })
    .then(response => response.json())
    .then(message => {
        console.log(message);
        update_frontend_follow_status(profile);
    });
};

// get follower status of logged in user, update webpage to match
function update_frontend_follow_status(profile) {
    
    fetch(`/follow_status?profile=${profile}`)
    .then(response => response.json())
    .then(response => {
        console.log(response['is_following']);
        if (response['is_following'] === true) {
            document.querySelector('#button-follow').innerHTML = 'Unfollow'
        } else {
            document.querySelector('#button-follow').innerHTML = 'Follow'
        }
        console.log(response['follower_count'])
        document.querySelector('#follower-count').innerHTML = response['follower_count'];
    });
};

// get like status of post, update webpage to match
function update_frontend_like_status(post) {
    fetch(`/like?post_id=${post['id']}`)
    .then(response => response.json())
    .then(data => {
        post_button_like = document.querySelector(`#post-${post['id']}-button-like`);
        post_likes_count = document.querySelector(`#post-${post['id']}-likes`);
        if (data['liked'] == false) {
            post_button_like.innerHTML = 'Like';
        } else {
            post_button_like.innerHTML = 'Unlike';
        }
        post_likes_count.innerHTML = `Likes: ${data['like_count']}`
    });
}