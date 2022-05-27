# number-guessing-game-gui
A GUI number guessing game

User can choose from three difficulty levels. Easy, Medium and Hard.

Easy:
User gets 7 chances to correctly guess a number between '0' and '9'

Medium:
User gets 8 chances to correctly guess a number between '0' and '15'

Hard:
User gets 9 chances to correctly guess a number between '0' and '30'

```mermaid
graph TD;

    Start -->Yes;
    Start -->No;

    Yes -->Tries;
    No -->Exit;

    Tries -->Win;
    Tries -->Retry;

    Win -->Start;
    Retry -->Tries;
    Retry -->Lost;
    Lost -->Start;
