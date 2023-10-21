# dotalib
#### Simple(st) representation of Dota 2 objects such as:
* `Hero`
* `Team`
* `Match`

Each of these representations is related to each other in a natural 

## Hero

`Hero` objects contains in `all_heroes` **dotalib.entities.hero**.
Every hero has:
* `id` - 27
* `sysname` - "npc_dota_hero_bane"
* `fullname` - "Bloodseeker"
* `name` - "pudge"

## Team

A few `Hero` combines in `Team`, and team also provids info:
* `heroes`
* `side` - "radiant" or "dire"
* `name` - team name
* `is_winner`

All of these fields can be `None` except `heroes`.
In fact `Team.__init__` method may request `five_players` and `no_repeat` flags (each of them default is True).
if `five_players` is True the init method will make sure number of heroes equals 5.
if `no_repeat` is True the init method will make sure there's no repeats in `heroes`.

## Match

`Match` representation contains inside 2 teams only - radiant and dire.
Every dota match has an id but `Match`'s `id` can be `None` (if you couldn't parse match id or smth).
It can show some match results:
* `winner` - winner team of the match
* `loser` - loser team of the match
* `heroes` - all heroes who participate in the match

Also `Match` can contains `map` and `championship` name.
=======
# dotalib
#### Simple(st) representation of Dota 2 objects such as:
* `Hero`
* `Team`
* `Match`

Each of these representations is related to each other in a natural 

## Hero

`Hero` objects contains in `all_heroes` **dotalib.entities.hero**.
Every hero has:
* `id` - 27
* `sysname` - "npc_dota_hero_bane"
* `fullname` - "Bloodseeker"
* `name` - "pudge"

## Team

A few `Hero` combines in `Team`, and team also provids info:
* `heroes`
* `side` - "radiant" or "dire"
* `name` - team name
* `is_winner`

All of these fields can be `None` except `heroes`.
In fact `Team.__init__` method may request `five_players` and `no_repeat` flags (each of them default is True).
if `five_players` is True the init method will make sure number of heroes equals 5.
if `no_repeat` is True the init method will make sure there's no repeats in `heroes`.

## Match

`Match` representation contains inside 2 teams only - radiant and dire.
Every dota match has an id but `Match`'s `id` can be `None` (if you couldn't parse match id or smth).
It can show some match results:
* `winner` - winner team of the match
* `loser` - loser team of the match
* `heroes` - all heroes who participate in the match

Also `Match` can contains `map` and `championship` name.