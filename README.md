# Fantasy Football Schedule Generation

The goal of this project is to develop an algorithm to automatically generate our fantasy football schedule. A fantasy football schedule consists of a 14 week period.
## Constraints
- Each team must play each other team exactly twice - once in the first 7 weeks and once in the second 7 weeks.
- Each team will play exactly 7 games as the home team and 7 games as the road time.
- Certain games are marked as "primetime" games. These are games that occur in real life and must be part of the schedule. These will change every year and vary based on the teams in the league.
- Each team has a bye week in real life, giving their opponent one free win each year. This does count as one of the two meetings between teams. Each team will receieve exactly one free win in a set of 14 games.

## Format
Input is a text file. The first line tells us the number of teams n. Each of the next n lines contain the team name and their bye week. The rest of the lines in the input file are primetime games. We currently assume that it is possible to build a schedule, ie the primetime games do not dramatically contrain the search space.

Example Input
>
>8\
>Team1 9\
>Team2 6\
>Team3 1\
>Team4 5\
>Team5 6\
>Team6 13\
>Team7 10\
>Team8 11\
>Team1 Team3 7\
>Team5 Team2 3\
>Team6 Team2 7\
>Team7 Team2 5\
>Team1 Team3 10\
>Team8 Team3 2\
>Team8 Team4 1\
>Team7 Team5 4\
>Team3 Team6 8\
>Team8 Team6 5\
>Team7 Team2 11\
>Team7 Team6 12\
>Team4 Team8 13

Example Output
>Week 1\
>Team1 - Team3\
>Team2 - Team4\
>Team7 - Team8\
>Team6 - Team5
>
>Week 2\
>Team3 - Team4\
>.....
>
>.....\
>Week 14\
> Team 1 - Team 7\
>.....

