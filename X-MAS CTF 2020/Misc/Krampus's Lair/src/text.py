hlp = """
You can specify places, actions and things. To move, try words like
NORTH, EAST, SOUTH, WEST. You can LOOK in a room, TAKE, READ or USE things.
"""

unknownCommand = ["What do you want to do?", "You should ask for help.", "Huh?", "What's that?", "What do you mean?"]
badCharacter = ["Hey, where did you get that weird character from?", "That character is not allowed.", "You can't use that!", "Where do you even want to obtain that character from?"]
execFail = ["Your contraption did not work.", "You tried to escape the jail, but you failed.", "That failed.", "Your invention broke.", "Gah! Your payload just broke in your hands!"]

roomConnections = {
    # N E S W
    0: [3, 1, -1, 2],
    1: [-1, -1, -1, 0],
    2: [-1, 0, -1, -1],
    3: [-1, 5, 0, 4],
    4: [-1, 3, -1, -1],
    5: [-1, 6, -1, 3],
    6: [-1, 7, -1, 5],
    7: [-1, -1, -1, 6],
}

roomState = {
    0: 0,
    1: 0,
    2: 0,
    3: 0,
    4: 0,
    5: 0,
    6: 0,
    7: 0,
}

jailText = """
YOU ARE NOW STUCK IN THE JAIL, AND YOU MUST ESCAPE IF YOU WANT TO SEE THE
LIGHT OF DAY EVER AGAIN. YOU HAVE ACQUIRED THE FOLLOWING ITEMS:

GEM
HUNTER SNARE
CAN
TIMER
) ( (BOW SET)
  ,
 / (ARROW)
v

YOU ARE ONLY ALLOWED TO USE THE (LOWERCASE) CHARACTERS THAT MAKE UP THESE ITEMS
IN ORDER TO CRAFT A PAYLOAD AND ESCAPE THE PYTHON JAIL. GOOD LUCK!
"""

jailTextReminder = """
YOU ARE STUCK IN THE JAIL. YOU ONLY HAVE THE FOLLOWING ITEMS WITH YOU:

GEM
HUNTER SNARE
CAN
TIMER
) ( (BOW SET)
  ,
 / (ARROW)
v

YOU ARE ONLY ALLOWED TO USE THE (LOWERCASE) CHARACTERS THAT MAKE UP THESE ITEMS
IN ORDER TO CRAFT A PAYLOAD AND ESCAPE THE PYTHON JAIL.
"""

roomLook = {
    0: ["""
YOU ARE AT THE ENTRANCE OF KRAMPUS'S LAIR. THE WALLS ARE COVERED IN
A SLIM REFLECTIVE LAYER OF WHAT SEEMS TO BE MAGIC ASH. YOU STARE IN AWE
AT THE VIEW.
    """],

    1: ["""
THERE IS A WATERFALL OF SPARKLING WATER RUNNING ALONG THE ROCKY WALLS
OF THE ROOM. YOU SEE AN OLD RUSTY CAN THROWN ON THE GROUND.
    ""","""
THERE IS A WATERFALL OF SPARKLING WATER RUNNING ALONG THE ROCKY WALLS
OF THE ROOM. THE WATER IS A CRYSTALLINE SHADE, INVITING YOU TO DRINK FROM IT.
    ""","""
THERE IS A WATERFALL OF SPARKLING WATER RUNNING ALONG THE ROCKY WALLS
OF THE ROOM. YOU HAVE BEEN ENOUGH IN THIS ROOM TO KNOW IT WELL, AND YOU SEE A
SET OF OLD BOW AND ARROWS HIDING BEHIND A ROCK.
    ""","""
THERE IS A WATERFALL OF SPARKLING WATER RUNNING ALONG THE ROCKY WALLS
OF THE ROOM. YOU ADMIRE ITS BEAUTY FOR A WHILE.
"""],

    2: ["""
THE ROOM IS PITCH BLACK, YET YOU HEAR A FAINT TICKING IN THE BACKGROUND. YOU
CANNOT SEE ANYTHING, SO YOU DECIDE NOT TO INVESTIGATE FURTHER FOR NOW.
    ""","""
THE ROOM IS NOW LIT UP IN A BEAUTIFUL DIM NEON BLUE COLOR. YOU CAN FAINTLY SEE
THE ITEM THAT WAS TICKING. IT'S AN OLD KITCHEN TIMER.
""","""
THE ROOM IS NOW LIT UP IN A BEAUTIFUL DIM NEON BLUE COLOR. YOU SIT AROUND
QUIETLY, ENJOYING THE ATMOSPHERE.
"""],

    3: ["""
                            ,-.
       ___,---.__          /'|`\\          __,---,___
    ,-'    \\`    `-.____,-'  |  `-.____,-'    //    `-.             ZZZ
  ,'        |           ~'\\     /`~           |        `.         ZZ
 /      ___//              `. ,'          ,  , \\___      \\      ZZ
|    ,-'   `-.__   _         |        ,    __,-'   `-.    |    Z
|   /          /\\_  `   .    |    ,      _/\\          \\   |
\\  |           \\ \\`-.___ \\   |   / ___,-'/ /           |  /
 \\  \\           | `._   `\\\\  |  //'   _,' |           /  /
  `-.\\         /'  _ `---'' , . ``---' _  `\\         /,-'
     ``       /     \\    ,='/ \\`=.    /     \\       ''
             |__   /|\\_,--.,-.--,--._/|\\   __|
             /  `./  \\\\`\\ |  |  | /,//' \\,'  \\
            /   /     ||--+--|--+-/-|     \\   \\
           |   |     /'\\_\\_\\ | /_/_/`\\     |   |
            \\   \\__, \\_     `~'     _/ .__/   /
             `-._,-'   `-._______,-'   `-._,-'

YOU SEE KRAMPUS IN FRONT OF YOU, AND FEEL YOUR BODY SHIVER IN FEAR. THE BEAST
IS CURRENTLY ASLEEP. YOU DECIDE NOT TO WAKE IT UP, AND KEEP LOOKING FOR ITEMS
AROUND THE LAIR.
    ""","""
                            ,-.
       ___,---.__          /'|`\\          __,---,___
    ,-'    \\`    `-.____,-'  |  `-.____,-'    //    `-.
  ,'        |           ~'\\     /`~           |        `.
 /      ___//              `. ,'          ,  , \\___      \\
|    ,-'   `-.__   _         |        ,    __,-'   `-.    |
|   /          /\\_  `   .    |    ,      _/\\          \\   |
\\  |           \\ \\`-.___ \\   |   / ___,-'/ /           |  /
 \\  \\           | `._   `\\\\  |  //'   _,' |           /  /
  `-.\\         /'  _ `---'' , . ``---' _  `\\         /,-'
     ``       /     \\    ,='/ \\`=.    /     \\       ''
             |__   /|\\_,--.,-.--,--._/|\\   __|
             /  `./  \\\\`\\ |  |  | /,//' \\,'  \\
            /   /     ||--+--|--+-/-|     \\   \\
           |   |     /'\\_\\_\\ | /_/_/`\\     |   |
            \\   \\__, \\_     `~'     _/ .__/   /
             `-._,-'   `-._______,-'   `-._,-'

YOU STUMBLE ACROSS KRAMPUS'S ROOM AGAIN, BUT HE SEEMS TO HAVE BEEN AWAKENED BY
YOUR FUMBLING AROUND ITS LAIR. HE'S STARING AT YOU WITH COLD DEAD EYES, AND YOU
FEEL SHIVERS ALONG YOUR SPINE. IN ONE SWIFT MOTION, IT CASTS A SPELL AND YOU FIND
THE GROUND BELOW YOUR FEET CRUMBLE, AND YOU FALL DOWN IN A CAGE WITH 3 PYTHONS.
"""],

    4: ["""
THERE ARE A LOT OF BRIGHTLY-COLORED FIREFLIES DARTING ACROSS THE
ROOM, LIGHTING IT UP IN A BEAUTIFUL NEON BLUE LIGHT.
    ""","""
THERE ARE A LOT OF BRIGHTLY-COLORED FIREFLIES DARTING ACROSS THE
ROOM, LIGHTING IT UP IN A BEAUTIFUL NEON BLUE LIGHT. THE LIGHT IS A BIT DIMMER
NOW, SINCE YOU TOOK SOME FIREFLIES AWAY WITH YOU.

YOU SEE A HUNTER'S SNARE IN THE MIDDLE OF THE ROOM. IT MUST'VE BEEN LEFT BY AN
UNFORTUNATE HUNTER, THINKING THIS WAS SOME SORT OF A BEAR CAVE.
    ""","""
THERE ARE A LOT OF BRIGHTLY-COLORED FIREFLIES DARTING ACROSS THE
ROOM, LIGHTING IT UP IN A BEAUTIFUL NEON BLUE LIGHT. THE LIGHT IS A BIT DIMMER
NOW, SINCE YOU TOOK SOME FIREFLIES AWAY WITH YOU. YOU ADMIRE THE ROOM.
    """],

    5: ["""
THERE IS A WEIRD WOODEN SIGN IN FRONT OF YOU.
    """],

    6: ["""
THERE IS A WEIRD METALLIC SIGN IN FRONT OF YOU.
    """],

    7: ["""
YOU ARE IN A BEAUTIFUL YET ODD ROOM, FILLED WITH GEMS. YOU FEEL A SOFT VIBRATION
AT YOUR FEET, FEELING THE ETHEREAL ATMOSPHERE OF THE PLACE. THERE IS ONE GEM,
SHINIER THAN THE OTHERS, WHICH GRABS YOUR ATTENTION.
    ""","""
YOU ARE IN A BEAUTIFUL YET ODD ROOM, FILLED WITH GEMS. YOU FEEL A SOFT VIBRATION
AT YOUR FEET, FEELING THE ETHEREAL ATMOSPHERE OF THE PLACE. YOU FEEL A SOFT
BREEZE RUNNING ACROSS YOUR ARMS, GIVING YOU A SENSE OF WONDER AND DISCOVERY.
THERE IS NOTHING ELSE TO DO IN THIS ROOM.
"""]
}

useText = {
    1: {"can": """
YOU USE THE RUSTY CAN TO DRINK FROM THE CLEAR WATERFALL.
YOU TAKE YOUR TIME AND ADMIRE THE PLACE, AND SPOT A SET OF SOME OLD BOW AND
ARROWS HIDDEN BEHIND A ROCK.
    """},
    2: {"can": """
YOU OPEN THE RUSTY CAN AND FREE THE FIREFLIES FROM INSIDE. THE ROOM IS NOW
BEING LIT UP.
    """},
    4: {"can": """
YOU USE THE RUSTY CAN TO CATCH SOME FIREFLIES IN THE ROOM. YOU CAN USE THE CAN
AGAIN TO FREE THEM AND LIGHT UP ANOTHER ROOM.
    """}
}

takeText = {
    1: {"can": """
:----:
|====|
|    |
`===='

YOU TAKE THE RUSTY CAN.
 ""","bow": """
   (
    \\
     )
##-------->