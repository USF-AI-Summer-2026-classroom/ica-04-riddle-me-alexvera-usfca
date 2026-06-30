from logic import *

# ------------------------------------------------------------------
# Propositions
#
# Mapping of statements to propositions:
#
# Suspects:
#   street_criminal  — a low-level street criminal committed the crime
#   joker            — the Joker committed the crime
#   penguin          — the Penguin committed the crime
#   riddler          — the Riddler committed the crime
#
# Clues / evidence:
#   acid_burn        — an acid burn is present at the crime scene
#   umbrella_mark    — an umbrella mark is present at the crime scene
#   playing_cards    — playing cards are present at the crime scene
#   joy_buzzer       — a deadly joy buzzer is present at the crime scene
#   riddle           — a riddle/puzzle/word game is present at the crime scene
#
# Observation:
#   hole_in_ground   — a hole in the ground was found at the crime scene
# ------------------------------------------------------------------


street_criminal, joker, penguin, riddler = vars(
    'street_criminal', 'joker', 'penguin', 'riddler'
)
 
acid_burn, umbrella_mark, playing_cards, joy_buzzer, riddle = vars(
    'acid_burn', 'umbrella_mark', 'playing_cards', 'joy_buzzer', 'riddle'
)
 
hole_in_ground = Variable('hole_in_ground')

#--------------------------------------------------------------------------------
# Formulas
#--------------------------------------------------------------------------------

# At least one criminal committed the crime
at_least_one_criminal = street_criminal | joker | penguin | riddler
 
# At most one criminal committed the crime (mutually exclusive suspects)
at_most_one_criminal = (
    (~street_criminal | ~joker)
    & (~street_criminal | ~penguin)
    & (~street_criminal | ~riddler)
    & (~joker | ~penguin)
    & (~joker | ~riddler)
    & (~penguin | ~riddler)
)
 
# The Joker leaves acid burns, playing cards, or deadly joy buzzers
joker_leaves_clues = joker >> (acid_burn | playing_cards | joy_buzzer)
 
# The Penguin leaves umbrella marks
penguin_leaves_clues = penguin >> umbrella_mark
 
# The Riddler only leaves riddles, puzzles, or word games
riddler_leaves_clues = riddler >> riddle
 
# An umbrella mark produces a hole in the ground
umbrella_causes_hole = umbrella_mark >> hole_in_ground
 
# An acid burn produces a hole in the ground
acid_causes_hole = acid_burn >> hole_in_ground
 
# ------------------------------------------------------------------
# Crime scene facts (Batman's observations)
# ------------------------------------------------------------------
 
found_hole = hole_in_ground    # A hole in the ground was found
no_playing_cards = ~playing_cards  # No playing cards were found
no_joy_buzzer = ~joy_buzzer        # No joy buzzer was found
no_riddle = ~riddle                # No riddle or puzzle was found
 
# ------------------------------------------------------------------
# Determine culpability
#
# A suspect definitely committed the crime if they are guilty in
# every truth assignment that satisfies all premises simultaneously.


# ------------------------------------------------------------------
# ArgumentForms
# ------------------------------------------------------------------


premises = [
    at_least_one_criminal,
    at_most_one_criminal,
    joker_leaves_clues,
    penguin_leaves_clues,
    riddler_leaves_clues,
    umbrella_causes_hole,
    acid_causes_hole,
    found_hole,
    no_playing_cards,
    no_joy_buzzer,
    no_riddle,
]
 
all_variables = frozenset.union(*[p.variables() for p in premises])
all_rows = truth_table_rows(all_variables)
consistent_rows = [r for r in all_rows if all(p.evaluate(**r) for p in premises)]
 
street_criminal_guilty = all(r['street_criminal'] for r in consistent_rows)
joker_guilty = all(r['joker'] for r in consistent_rows)
penguin_guilty = all(r['penguin'] for r in consistent_rows)
riddler_guilty = all(r['riddler'] for r in consistent_rows)
 
print('Who definitely committed this crime:')
print(f'A low-level criminal: {street_criminal_guilty}')
print(f'The Joker: {joker_guilty}')
print(f'The Penguin: {penguin_guilty}')
print(f'The Riddler: {riddler_guilty}')

