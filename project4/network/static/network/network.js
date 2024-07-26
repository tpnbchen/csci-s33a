document.addEventListener('DOMContentLoaded', function() {

    // document.querySelector('#following').addEventListener('click', () => load_posts('following'));
    document.querySelector('#post-form').addEventListener('submit', (event) => {
        submit_post();
        event.preventDefault();
    });
    load_posts('all');
});

function load_posts(filter) {

    document.querySelector('#posts-view-title').innerHTML = 
        `<h3>${filter.charAt(0).toUpperCase() + filter.slice(1)}</h3>`;
    // document.querySelector('posts-view-table').innerHTML = null;

    const token = document.querySelector('[name="csrfmiddlewaretoken"]').value;

    // get posts
    fetch(`/posts/${filter}`, {
        headers: {
            "X-CSRFToken": token,
        }
    })
    .then(response => response.json())
    .then(posts => {
        posts.forEach(post => {
            let post_id = `post-${post.id}`;
            let post_item = document.querySelector(`#${post_id}`);

            post_item = document.createElement('div');
            post_item.id = post_id;
            post_item.classList.add('row', 'border');
            document.querySelector('#posts-view-table').appendChild(post_item);

            post_contents = document.createElement('div');
            post_contents.id = `post-${post_id}-content`;
            post_contents.classList.add("col");
            post_item.appendChild(post_contents); 
        });
    });
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