
document.addEventListener('DOMContentLoaded', function() {
    const path = window.location.pathname;
    if (path.startsWith('/hanabi/games')) {
        load_games();
        document.querySelector('#new-game-form').addEventListener('submit', (event) => {
            new_game();
            event.preventDefault();
        });
    };
});

// start a new game
function new_game() {
    const token = document.querySelector('[name="csrfmiddlewaretoken"]').value;
    game_name = document.querySelector('#game-name').value;
    numplayers = document.querySelector('#game-numplayers').value;

    fetch('/hanabi/new_game', {
        method: 'POST',
        headers: {
            'X-CSRFToken': token,
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            game_name: game_name,
            numplayers: numplayers
        })
    })
    .then(response => response.json())
    .then(message => {
        console.log(message);
    });
}

// load available games to join
function load_games() {
    const list_games_table = document.querySelector('#list-games-table');
    list_games_table.innerHTML = null;

    // get games
    fetch(`/hanabi/list_games`)
    .then(response => response.json())
    .then(games_response => {
        games_response['games_list'].forEach(game => {
            let game_item = document.createElement('div');
            game_item.id = `game-${game['id']}`;
            game_item.classList.add('row', 'border');
            list_games_table.appendChild(game_item);

            game_info = document.createElement('div');
            game_item.appendChild(game_info);
            game_info.id = `${game.id}-info`;
            game_info.classList.add('col');

            game_buttons = document.createElement('div');
            game_item.appendChild(game_buttons);
            game_buttons.id = `${game.id}-buttons`;
            game_buttons.classList.add('col-2');

            for (const field in game) {
                const field_id = `${game.id}-${field}`;
                field_element = document.createElement('div');
                field_element.id = field_id;
                game_info.appendChild(field_element);
                if (field === 'creator__username') {
                    field_element.innerHTML = `Creator: ${game[field]}`;
                } else if (field === 'timestamp') {
                    const formatted_date = Date(game[field]).toLocaleString()
                    field_element.innerHTML = `${formatted_date}`;
                } else if (field === 'id') {
                    field_element.remove();
                } else {
                    field_element.innerHTML = `${field}: ${game[field]}`;
                }
            };

            // join button
            let game_button_join = document.createElement('button');
            game_buttons.appendChild(game_button_join);
            game_button_join.id = `${game.id}-button-join`;
            game_button_join.classList.add('btn', 'btn-primary');
            game_button_join.innerHTML = 'Join';
            game_button_join.addEventListener('click', () => {
                join_game(game);
            });
        });
    });
};

function join_game(game) {
    const token = document.querySelector('[name="csrfmiddlewaretoken"]').value;
    fetch('/hanabi/join_game', {
        method: 'POST',
        headers: {
            'X-CSRFToken': token,
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            game: game
        })
    })
    .then(response => response.json())
    .then(message => {
        console.log(message);
        render_game(game);
    });
};

// get current game state
function render_game(game){
    fetch(`hanabi/game_state/${game.id}`)
    .then(response => response.json())
    .then(game_state => {
        console.log(game_state);
    })
};
