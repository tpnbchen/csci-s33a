Hanabi Web App

Summary:

Play Hanabi the table top game online!

Project Scope and Goals:

Adapt a terminal based version of the game Hanabi (my final project from csci e-7) and turn it into a web app.
support 2-5 "concurrent" players 
game interface rendered in a dynamic webpage
players see text based game state presented by the webapp

Gameplay and Rule Summary:

Each player is delt a hand of cards.
Each card is a combination of a color, e.g. "red" and a number e.g. "1".
Each player cannot view their own hard but can see all other player's hand.
Each player takes turns either playing a card, discarding a card or giving another player a hint.
Giving a hint costs a hint token, if no hint tokens remain, a hint cannot be given.
A hint is strictly defined as:
    identifying for one other player, all of their cards of EITHER a particular number OR a particular color.
    e.g. all  "2" cards of any color OR all "blue" cards of any number
    There are 8 hint tokens to start, hints cannot be given with an available token.
Discarding a card recovers a spent hint token and a new card is drawn into the hand.
Playing a card adds to the score board if valid, or triggers a "fuse" if invalid. A new card is drawn into the hand.
If 3 fuses are triggered, the game ends.
If there are no more cards to draw, each player takes one more turn and the game ends.
A valid card play builds on any of the five sequences of colors on the board.
    The board starts with each color sequence at "0".
        In this state, a "1" card of any color is valid.
    E.g. if a "red" "1" card is played, now "red" "2" is the only valid play for the red sequence.
        Other red numbers are invalid.

Scoring:
Each card on the board is worth 1 point. 5 is the highest number so a perfect score is 25.

For full rules see : https://cdn.1j1ju.com/medias/b3/a9/0e-hanabi-rulebook.pdf


App Design
    Pages:
        Rules
            Static page of game rules
        Player profile
            Game history and scores
        Games list
            List of open games
            Create a new game
        Game interface
            Game state
            Actions
            Game hints

Challenges
...



