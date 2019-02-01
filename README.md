# card-game

To start the game, simply type python3 Game.py in a console window in the main folder.
I have downloaded a few modules to get things running so that may be an issue, please contact me if any issues are encountered.

Hello!

This card game was designed with heavy inspiration from both Magic: the Gathering and Hearthstone, which are paper/digital strategy card 
games where the goal is to cast spells, summon units, and defeat your opponent. You and your opponent both start out with 25 life, and 
you can only attack your opponent if there are no units your opponent controls to block them.

In general, a turn you take in the game will proceed as follows:

First you would increase the amount of "Mana" or resource you have of one of the 4 colors located on the right. This action is performed
by left clicking one of the animated colored squares which will then add 1 resource of that color to be available. This is a permanent 
addition, so if you use it up on one turn, when you begin your next turn that mana will be restored in addition to whichever color you pick
then. So for example if I began my first turn by adding "Red", I would be able to spend 1 "Red" mana that turn. Then next turn, I would 
start out with 1 "Red" and could either add another "Red" allowing me to spend up to 2 "Red" mana, or I could add "Blue", allowing me to
spend up to 1 "Red and 1 "Blue" that turn.

The next step would be to play a unit or spell using your mana. units are cards in your hand that lie in the center of the screen 
and are denoted by the amount of mana they cost in colored circles on the bottom left of the card indicating the type of mana they cost. 
A colorless circle indicates that mana of any color can be used to play it. In addition, units also have "Attack/Defense" values in 
a box in the right corner. This value is used when doing battle with other units, or when attacking the enemy's life directly.

After playing your cards for the turn, the next step would be to attack with them if possible. units cannot attack the turn you play 
them. To attack with a unit, left click on it and all enemy units that can be attacked by it will be highlighted in red. When two
units battle, the attacking unit compares its attack with the defending units defense. Whichever is higher survives and the 
other is destroyed. Attacking the enemy hero directly on the left side of the board will reduce their life by the attacking unit's
attack.

After you have used up your mana and attacked with your units, you may then click the "end turn" button in the bottom left corner,
which passes the turn to your opponent.

This is a general overview of how each turn would play out in this game, but there are still many specifics to be learned.
Many descriptions of units and spells include "keywords" such as "Alacrity", "Arrival", or "Afterdeath". These words are used as 
shorthand to describe their effects.

#consume: can destroy an allied unit to pay for part of its mana cost mana
#stake: pick a unit zone to apply a lasting effect
#undermine: if your enemy only has units with defense higher than your attack, you can attack directly with this unit
#arrival: this effect will trigger when you play this unit
#afterdeath: this effect will trigger when this unit dies
#alacrity: this unit may attack immidiately after being played
#procure: draw a specific card from your deck
#prep: applies to spells that can be casted at the end of your turn to trigger on your opponents turn during the specified trigger

In addition, some units have abilities that can paid for and used once the unit is already on the field. This will be denoted by mana
circles appearing in their description. Spells and activated abilities such as these are cast by using right click instead of left click.

The goal of the game is to reduce your oppoenents life to 0, but its very hard to do that when they have unit's in the way. Prioritize
destroying enemy units efficiently and quickly to gain a lead and chip away at their life total.

Have fun!
