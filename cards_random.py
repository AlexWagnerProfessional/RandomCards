# Idea: The computer generates random cards by assembling
# words into certain spots. These words determine the
# power, cost, and effects of the card.

# For example:
# [Adjective(s)] [Noun] of [Noun(s)]

# We should start by defining a class called Card.
# It will probably be the superclass of something or other.
# In any case, it should be endowed with all the necessary
# properties of a card: color, power, cost, effects, and so on.

import csv
import random
import tkinter
import tkinter.font
#from tkinter import *

class Card:
    def __init__(self, prefix1, prefix2, name, suffix1, suffix2, color, effects, powers, cost):
        self.prefix1 = prefix1 #STRING
        self.prefix2 = prefix2 #STRING
        self.name = name #STRING
        self.suffix1 = suffix1 #STRING
        self.suffix2 = suffix2 #STRING

        # Card name will take the form of:
        # prefix1 prefix2 name suffix1 suffix2

        # Ex:
        # "Extreme ""Blazing ""Cannonball""" of Icy ""Doom"

        # Or:
        # "The Honorable ""Mystical ""Judge"", the Bringer of ""Flowers"

        # STYLE GUIDE
        # Prefix 1:
            # (adjective ) or (The adjective )
            # End with a space
        # Prefix 2: 
            # (adjective )
            # End with a space
        # Name:
            # (noun)
            # No spaces on either side
        # Suffix 1:
            # ( of adjective ) or (, the verber of )
            # Space or comma on either side
        # Suffix 2:
            # (noun)
            # No spaces on either side
        
        # Cards with fewer bells and whistles may cut out
        # Prefix 2.
        # They may also have a placeholder " of " for 
        # Suffix 1, then a Suffix 2.

        # A string convenient for displaying to the user:
        self.fullname = prefix1 + prefix2 + name + suffix1 + suffix2

        # ...versus a list convenient for iterating through:
        self.fullnamelist = [prefix1, prefix2, name, suffix1, suffix2]

        self.color = color #STRING (color code)

        # Effects: Some strings representing what the
        # card does. There is a dictionary of
        # effects; each string can refer to a key
        # for more information on what to do.
        # 0: Generic/None
        # 1: Damage
        # 2: Defend
        # 3: Heal
        # 4: Boost own energy
        # 5: Boost own deck
        # 6: Reduce opponent energy
        # 7: Reduce opponent deck
        # 8: Debuff opponent damage
        # 9: Debuff opponent defense
        # 10: Debuff opponent heal
        # 11: (May not be used) Debuff opponent energy effects
        # 12: (May not be used) Debuff opponent deck effects
        # 13: Buff own damage
        # 14: Buff own defense
        # 15: Buff own healing
        # 16: (May not be used) Buff own energy effects
        # 17: (May not be used) Buff own deck effects
        self.effects = effects #LIST OF STRINGS

        # Powers: The card does its effects with this much
        # numerical magnitude, matching the index.
        self.powers = powers #LIST OF INTS

        # Cost: The character expends this much of their
        # main resource in order to use the card.
        self.cost = cost #INT


    
    def __str__(self):
        # For printing the object itself
        return self.fullname
    
    def __repr__(self):
        # For printing a list of such objects
        return self.fullname + " (" + str(self.cost) + ")"

    def play(self, user, target):
        # self is the card being played.
        # user is the Player object using the card.
        # target is the Player object they are fighting against.

        # There are a lot of possible effects to cover.
        # Let's get this if-else train rolling!

        # For each i'th effect out of 15 effects,
        # check what that effect is called and do the appropriate
        # adjustment to the numbers.
        for i in range(len(self.effects)):
            # 1: Damage
            if self.effects[i] == "Damage":
                # Attempt to reduce target's health by:
                # this card's damage power + user's damage buff
                # (cannot be less than 0)

                # There are a few different cases.
                # Case 1: No defense - just reduce health by the amount.
                # Case 2: Some defense but not enough - destroy all defense
                # and reduce health by what's left.
                # Case 3: Enough defense - just reduce defense by the amount.

                damage_amount = max( 0, self.powers[i] + user.buff_damage )
                #print("Target initially has %i health and %i defense." % (target.health, target.defense))

                if target.defense <= 0:
                    target.health -= damage_amount
                    #print("Damaged health by %i." % damage_amount)

                elif target.defense > 0 and target.defense < damage_amount:
                    #print("Damaged defense by %i." % target.defense)
                    damage_amount -= target.defense
                    target.defense = 0
                    target.health -= damage_amount
                    #print("Damaged health by %i." % damage_amount)
                    

                elif target.defense >= damage_amount:
                    target.defense -= damage_amount
                    #print("Damaged defense by %i." % damage_amount)

                #print("Target now has %i health and %i defense." % (target.health, target.defense))
            
            # 2: Defense
            elif self.effects[i] == "Defense":
                # Increase user's defense by:
                # this card's defense power + user's defense buff
                # (cannot be less than 0)
                #print("User initially has %i defense." % user.defense)
                user.defense += max( 0, self.powers[i] + user.buff_defense )
                #print("User now has %i defense." % user.defense)


            # 3: Healing
            elif self.effects[i] == "Healing":
                # Increase user's health by:
                # this card's healing power + user's healing buff
                # (cannot be less than 0)
                user.health += max( 0, self.powers[i] + user.buff_healing )


            # 4: Boost Energy
            elif self.effects[i] == "Boost Energy":
                # Increase user's energy by:
                # this card's boost energy power + user's energy buff
                # (cannot be less than 0)
                user.energy += max( 0, self.powers[i] + user.buff_energy )


            # 5: Boost Deck
            elif self.effects[i] == "Boost Deck":
                # Increase user's deck size by:
                # this card's boost deck power + user's deck buff
                # (cannot be less than 0)
                user.deck += max( 0, self.powers[i] + user.buff_deck )


            # 6: Reduce Energy
            elif self.effects[i] == "Reduce Energy":
                # Lower opponent's energy by:
                # this card's reduce energy power + user's energy buff
                # (cannot be less than 0)
                target.energy -= max ( 0, self.powers[i] + user.buff_energy )


            # 7: Reduce Deck
            elif self.effects[i] == "Reduce Deck":
                # Lower opponent's deck size by:
                # this card's reduce deck power + user's deck buff
                # (cannot be less than 0)
                target.deck -= max ( 0, self.powers[i] + user.buff_deck )


            # 8: Debuff Damage
            elif self.effects[i] == "Debuff Damage":
                # Lower opponent's damage buff by:
                # this card's debuff damage power
                target.buff_damage -= self.powers[i]


            # 9: Debuff Defense
            elif self.effects[i] == "Debuff Defense":
                # Lower opponent's defense buff by:
                # this card's debuff defense power
                target.buff_defense -= self.powers[i]


            # 10: Debuff Healing
            elif self.effects[i] == "Debuff Healing":
                # Lower opponent's healing buff by:
                # this card's debuff healing power
                target.buff_healing -= self.powers[i]


            # 11: (May not be used) Debuff opponent energy effects
            elif self.effects[i] == "Debuff Energy":
                # Lower opponent's energy buff by:
                # this card's debuff energy power
                target.buff_energy -= self.powers[i]


            # 12: (May not be used) Debuff opponent deck effects
            elif self.effects[i] == "Debuff Deck":
                # Lower opponent's deck buff by:
                # this card's debuff deck power
                target.buff_deck -= self.powers[i]


            # 13: Buff Damage
            elif self.effects[i] == "Buff Damage":
                # Increase user's damage buff by:
                # this card's buff damage power
                user.buff_damage += self.powers[i]


            # 14: Buff Defense
            elif self.effects[i] == "Buff Defense":
                # Increase user's defense buff by:
                # this card's buff defense power
                user.buff_defense += self.powers[i]


            # 15: Buff Healing
            elif self.effects[i] == "Buff Healing":
                # Increase user's healing buff by:
                # this card's buff healing power
                user.buff_healing += self.powers[i]


            # 16: (May not be used) Buff own energy effects
            elif self.effects[i] == "Buff Energy":
                # Increase user's energy buff by:
                # this card's buff energy power
                user.buff_energy += self.powers[i]


            # 17: (May not be used) Buff own deck effects
            elif self.effects[i] == "Buff Deck":
                # Increase user's deck buff by:
                # this card's buff deck power
                user.buff_deck += self.powers[i]




# We should also define what a player is.
# There is one player vs another, playing cards
# to buff and heal themselves, or damage and debuff
# the opponent player. They can also affect number
# of cards drawn and max energy per turn.

# Whoever reduces the other player's health, energy, or deck
# to 0 first wins.

# Cards all cost energy. The more energy a player has, the more
# cards, or the costlier cards, they can use every turn.

class Player:
    def __init__(self, health=30, energy=8, energy_current = 8,  deck=4, defense=0, buff_damage=0, buff_defense=0, buff_healing=0, buff_energy=0, buff_deck=0, perks=[]):
        # debuff_damage=0, debuff_defense=0, debuff_healing=0,  debuff_energy=0, debuff_deck=0, 
        self.health = health # Default: 30
        self.energy = energy # Default: 8
        self.energy_current = energy_current # Default: same as energy
        self.defense = defense # Default: 0
        self.deck = deck # Default: 5
        self.buff_damage = buff_damage # Default: 0
        self.buff_defense = buff_defense # Default: 0
        self.buff_healing = buff_healing # Default: 0
        self.buff_energy = buff_energy # Default: 0
        self.buff_deck = buff_deck # Default: 0
        self.perks = perks # Default: []

    def __str__(self):
        return_me = "Health: " + str(self.health) + "\nEnergy: " + str(self.energy) + \
            "\nDefense: " + str(self.defense) + "\nDeck: " + str(self.deck) + \
            "\nDamage Buff: " + str(self.buff_damage) + \
            "\nDefense Buff: " + str(self.buff_defense) + \
            "\nHealing Buff: " + str(self.buff_healing)
        return return_me


# There should be a function that generates a random card.
# It returns that card as an object.
# It will probably have a database of many possible name pieces
# to put together. Those name pieces determine certain effects
# which are simply known to the program.
# There should likely be a dictionary (or five) with name pieces 
# as keys and effects as values.



def CollectFromFiles():
    # Collect possible names from file
    with open('names.csv') as names_file:
        names_reader = csv.reader(names_file, delimiter=',')
        # An object has been created. We can do several things with it.
        # It is iterable. Each element can be considered a row.
        # Each row is a list of strings.

        # For skipping the first line
        line_number = 0

        # Start some lists that we will fill:
        names = []
        names_effects_1 = []
        names_effects_2 = []
        names_effects_3 = []
        names_powers_1 = []
        names_powers_2 = []
        names_powers_3 = []
        names_costs = []

        for row in names_reader:
            if line_number == 0:
                line_number += 1 # Skip first row (it just has titles)
            else:
                # Distribute everything. Indices go from 0-7.
                names.append(row[0])
                names_effects_1.append(row[1])
                names_effects_2.append(row[2])
                names_effects_3.append(row[3])
                # Account for some being empty strings

                if row[4] != "":
                    names_powers_1.append(int(row[4]))
                else:
                    names_powers_1.append(0)
                
                if row[5] != "":
                    names_powers_2.append(int(row[5]))
                else:
                    names_powers_2.append(0)

                if row[6] != "":
                    names_powers_3.append(int(row[6]))
                else:
                    names_powers_3.append(0)
                
                names_costs.append(int(row[7]))
                line_number += 1
            #print(row)
        # Now the index of a card name should match
        # the index of all the stuff it does, for
        # clean assigning later.

        # Package them up for returning:
        names_all = [names, names_effects_1, names_effects_2, names_effects_3, names_powers_1, names_powers_2, names_powers_3, names_costs]

    # Collect possible prefix 1's from file
    with open('prefix1.csv') as prefix1_file:
        prefix1_reader = csv.reader(prefix1_file, delimiter=',')
        # An object has been created. We can do several things with it.
        # It is iterable. Each element can be considered a row.
        # Each row is a list of strings.

        # For skipping the first line
        line_number = 0

        # Start some lists that we will fill:
        prefix1 = []
        prefix1_effects_1 = []
        prefix1_effects_2 = []
        prefix1_effects_3 = []
        prefix1_powers_1 = []
        prefix1_powers_2 = []
        prefix1_powers_3 = []
        prefix1_costs = []

        for row in prefix1_reader:
            if line_number == 0:
                line_number += 1 # Skip first row (it just has titles)
            else:
                # Distribute everything. Indices go from 0-7.
                prefix1.append(row[0])
                prefix1_effects_1.append(row[1])
                prefix1_effects_2.append(row[2])
                prefix1_effects_3.append(row[3])
                # Account for some being empty strings

                if row[4] != "":
                    prefix1_powers_1.append(int(row[4]))
                else:
                    prefix1_powers_1.append(0)
                
                if row[5] != "":
                    prefix1_powers_2.append(int(row[5]))
                else:
                    prefix1_powers_2.append(0)

                if row[6] != "":
                    prefix1_powers_3.append(int(row[6]))
                else:
                    prefix1_powers_3.append(0)
                
                prefix1_costs.append(int(row[7]))
                line_number += 1
            #print(row)
        # Now the index of a card name should match
        # the index of all the stuff it does, for
        # clean assigning later.

        # Package them up for returning:
        prefix1_all = [prefix1, prefix1_effects_1, prefix1_effects_2, prefix1_effects_3, prefix1_powers_1, prefix1_powers_2, prefix1_powers_3, prefix1_costs]

    # Collect possible prefix 2's from file
    with open('prefix2.csv') as prefix2_file:
        prefix2_reader = csv.reader(prefix2_file, delimiter=',')
        # An object has been created. We can do several things with it.
        # It is iterable. Each element can be considered a row.
        # Each row is a list of strings.

        # For skipping the first line
        line_number = 0

        # Start some lists that we will fill:
        prefix2 = []
        prefix2_effects_1 = []
        prefix2_effects_2 = []
        prefix2_effects_3 = []
        prefix2_powers_1 = []
        prefix2_powers_2 = []
        prefix2_powers_3 = []
        prefix2_costs = []

        for row in prefix2_reader:
            if line_number == 0:
                line_number += 1 # Skip first row (it just has titles)
            else:
                # Distribute everything. Indices go from 0-7.
                prefix2.append(row[0])
                prefix2_effects_1.append(row[1])
                prefix2_effects_2.append(row[2])
                prefix2_effects_3.append(row[3])
                # Account for some being empty strings

                if row[4] != "":
                    prefix2_powers_1.append(int(row[4]))
                else:
                    prefix2_powers_1.append(0)
                
                if row[5] != "":
                    prefix2_powers_2.append(int(row[5]))
                else:
                    prefix2_powers_2.append(0)

                if row[6] != "":
                    prefix2_powers_3.append(int(row[6]))
                else:
                    prefix2_powers_3.append(0)
                
                prefix2_costs.append(int(row[7]))
                line_number += 1
            #print(row)
        # Now the index of a card name should match
        # the index of all the stuff it does, for
        # clean assigning later.

        # Package them up for returning:
        prefix2_all = [prefix2, prefix2_effects_1, prefix2_effects_2, prefix2_effects_3, prefix2_powers_1, prefix2_powers_2, prefix2_powers_3, prefix2_costs]
    

    # Collect possible suffix 1's from file
    with open('suffix1.csv') as suffix1_file:
        suffix1_reader = csv.reader(suffix1_file, delimiter=',')
        # An object has been created. We can do several things with it.
        # It is iterable. Each element can be considered a row.
        # Each row is a list of strings.

        # For skipping the first line
        line_number = 0

        # Start some lists that we will fill:
        suffix1 = []
        suffix1_effects_1 = []
        suffix1_effects_2 = []
        suffix1_effects_3 = []
        suffix1_powers_1 = []
        suffix1_powers_2 = []
        suffix1_powers_3 = []
        suffix1_costs = []

        for row in suffix1_reader:
            if line_number == 0:
                line_number += 1 # Skip first row (it just has titles)
            else:
                # Distribute everything. Indices go from 0-7.
                suffix1.append(row[0])
                suffix1_effects_1.append(row[1])
                suffix1_effects_2.append(row[2])
                suffix1_effects_3.append(row[3])
                # Account for some being empty strings

                if row[4] != "":
                    suffix1_powers_1.append(int(row[4]))
                else:
                    suffix1_powers_1.append(0)
                
                if row[5] != "":
                    suffix1_powers_2.append(int(row[5]))
                else:
                    suffix1_powers_2.append(0)

                if row[6] != "":
                    suffix1_powers_3.append(int(row[6]))
                else:
                    suffix1_powers_3.append(0)
                
                suffix1_costs.append(int(row[7]))
                line_number += 1
            #print(row)
        # Now the index of a card name should match
        # the index of all the stuff it does, for
        # clean assigning later.

        # Package them up for returning:
        suffix1_all = [suffix1, suffix1_effects_1, suffix1_effects_2, suffix1_effects_3, suffix1_powers_1, suffix1_powers_2, suffix1_powers_3, suffix1_costs]

    # Collect possible suffix 2's from file
    with open('suffix2.csv') as suffix2_file:
        suffix2_reader = csv.reader(suffix2_file, delimiter=',')
        # An object has been created. We can do several things with it.
        # It is iterable. Each element can be considered a row.
        # Each row is a list of strings.

        # For skipping the first line
        line_number = 0

        # Start some lists that we will fill:
        suffix2 = []
        suffix2_effects_1 = []
        suffix2_effects_2 = []
        suffix2_effects_3 = []
        suffix2_powers_1 = []
        suffix2_powers_2 = []
        suffix2_powers_3 = []
        suffix2_costs = []

        for row in suffix2_reader:
            if line_number == 0:
                line_number += 1 # Skip first row (it just has titles)
            else:
                # Distribute everything. Indices go from 0-7.
                suffix2.append(row[0])
                suffix2_effects_1.append(row[1])
                suffix2_effects_2.append(row[2])
                suffix2_effects_3.append(row[3])
                # Account for some being empty strings

                if row[4] != "":
                    suffix2_powers_1.append(int(row[4]))
                else:
                    suffix2_powers_1.append(0)
                
                if row[5] != "":
                    suffix2_powers_2.append(int(row[5]))
                else:
                    suffix2_powers_2.append(0)

                if row[6] != "":
                    suffix2_powers_3.append(int(row[6]))
                else:
                    suffix2_powers_3.append(0)
                
                suffix2_costs.append(int(row[7]))
                line_number += 1
            #print(row)
        # Now the index of a card name should match
        # the index of all the stuff it does, for
        # clean assigning later.

        # Package them up for returning:
        suffix2_all = [suffix2, suffix2_effects_1, suffix2_effects_2, suffix2_effects_3, suffix2_powers_1, suffix2_powers_2, suffix2_powers_3, suffix2_costs]
        

    return (names_all, prefix1_all, prefix2_all, suffix1_all, suffix2_all)

def CardMakerRandom():
    names_all, prefix1_all, prefix2_all, suffix1_all, suffix2_all = CollectFromFiles()

    # Now pick a random name...
    # NAME SELECTION

    # Recall that names_all[0] is the list of names themselves.
    # We want to pick just one name out of there.
    name_selection = random.randrange(0, len(names_all[0]))
    name = names_all[0][name_selection]

    # This same index will be used to pull out the other values
    # matching this name - its effects, powers, and cost.
    # All of these should later be collected into the attributes
    # of the card - the list of effects, list of powers, and such.
    # Perhaps some smaller function could be written that takes in
    # a list and collapses duplicates together....
    name_effect1 = names_all[1][name_selection]
    name_effect2 = names_all[2][name_selection]
    name_effect3 = names_all[3][name_selection]
    name_power1 = names_all[4][name_selection]
    name_power2 = names_all[5][name_selection]
    name_power3 = names_all[6][name_selection]
    name_cost = names_all[7][name_selection]

    # Similarly...
    # PREFIX 1 SELECTION
    prefix1_selection = random.randrange(0, len(prefix1_all[0]))
    prefix1 = prefix1_all[0][prefix1_selection]

    # This same index will be used to pull out the other values
    # matching this prefix1 - its effects, powers, and cost.
    # All of these should later be collected into the attributes
    # of the card - the list of effects, list of powers, and such.
    # Perhaps some smaller function could be written that takes in
    # a list and collapses duplicates together....
    prefix1_effect1 = prefix1_all[1][prefix1_selection]
    prefix1_effect2 = prefix1_all[2][prefix1_selection]
    prefix1_effect3 = prefix1_all[3][prefix1_selection]
    prefix1_power1 = prefix1_all[4][prefix1_selection]
    prefix1_power2 = prefix1_all[5][prefix1_selection]
    prefix1_power3 = prefix1_all[6][prefix1_selection]
    prefix1_cost = prefix1_all[7][prefix1_selection]

    # PREFIX 2 SELECTION
    prefix2_selection = random.randrange(0, len(prefix2_all[0]))
    prefix2 = prefix2_all[0][prefix2_selection]

    # This same index will be used to pull out the other values
    # matching this prefix2 - its effects, powers, and cost.
    # All of these should later be collected into the attributes
    # of the card - the list of effects, list of powers, and such.
    # Perhaps some smaller function could be written that takes in
    # a list and collapses duplicates together....
    prefix2_effect1 = prefix2_all[1][prefix2_selection]
    prefix2_effect2 = prefix2_all[2][prefix2_selection]
    prefix2_effect3 = prefix2_all[3][prefix2_selection]
    prefix2_power1 = prefix2_all[4][prefix2_selection]
    prefix2_power2 = prefix2_all[5][prefix2_selection]
    prefix2_power3 = prefix2_all[6][prefix2_selection]
    prefix2_cost = prefix2_all[7][prefix2_selection]

    # SUFFIX 1 SELECTION
    suffix1_selection = random.randrange(0, len(suffix1_all[0]))
    suffix1 = suffix1_all[0][suffix1_selection]

    # This same index will be used to pull out the other values
    # matching this suffix1 - its effects, powers, and cost.
    # All of these should later be collected into the attributes
    # of the card - the list of effects, list of powers, and such.
    # Perhaps some smaller function could be written that takes in
    # a list and collapses duplicates together....
    suffix1_effect1 = suffix1_all[1][suffix1_selection]
    suffix1_effect2 = suffix1_all[2][suffix1_selection]
    suffix1_effect3 = suffix1_all[3][suffix1_selection]
    suffix1_power1 = suffix1_all[4][suffix1_selection]
    suffix1_power2 = suffix1_all[5][suffix1_selection]
    suffix1_power3 = suffix1_all[6][suffix1_selection]
    suffix1_cost = suffix1_all[7][suffix1_selection]

    # SUFFIX 2 SELECTION
    suffix2_selection = random.randrange(0, len(suffix2_all[0]))
    suffix2 = suffix2_all[0][suffix2_selection]

    # This same index will be used to pull out the other values
    # matching this suffix2 - its effects, powers, and cost.
    # All of these should later be collected into the attributes
    # of the card - the list of effects, list of powers, and such.
    # Perhaps some smaller function could be written that takes in
    # a list and collapses duplicates together....
    suffix2_effect1 = suffix2_all[1][suffix2_selection]
    suffix2_effect2 = suffix2_all[2][suffix2_selection]
    suffix2_effect3 = suffix2_all[3][suffix2_selection]
    suffix2_power1 = suffix2_all[4][suffix2_selection]
    suffix2_power2 = suffix2_all[5][suffix2_selection]
    suffix2_power3 = suffix2_all[6][suffix2_selection]
    suffix2_cost = suffix2_all[7][suffix2_selection]


    # Lots of data has been extracted and randomly selected!
    # Now to pile it all into a card.

    # EFFECTS PILE
    effects = []

    effects.append(prefix1_effect1)
    effects.append(prefix1_effect2)
    effects.append(prefix1_effect3)

    effects.append(prefix2_effect1)
    effects.append(prefix2_effect2)
    effects.append(prefix2_effect3)

    effects.append(name_effect1)
    effects.append(name_effect2)
    effects.append(name_effect3)

    effects.append(suffix1_effect1)
    effects.append(suffix1_effect2)
    effects.append(suffix1_effect3)

    effects.append(suffix2_effect1)
    effects.append(suffix2_effect2)
    effects.append(suffix2_effect3)

    # POWERS PILE
    powers = []

    powers.append(prefix1_power1)
    powers.append(prefix1_power2)
    powers.append(prefix1_power3)

    powers.append(prefix2_power1)
    powers.append(prefix2_power2)
    powers.append(prefix2_power3)

    powers.append(name_power1)
    powers.append(name_power2)
    powers.append(name_power3)

    powers.append(suffix1_power1)
    powers.append(suffix1_power2)
    powers.append(suffix1_power3)

    powers.append(suffix2_power1)
    powers.append(suffix2_power2)
    powers.append(suffix2_power3)


    # COST PILE
    cost = prefix1_cost + prefix2_cost + name_cost + suffix1_cost + suffix2_cost


    color = "#FFEBCD"
    card = Card(prefix1, prefix2, name, suffix1, suffix2, color, effects, powers, cost)

    """ 
    # Debug printing:
    print(card)
    print(card.effects)
    print(card.powers)
    print(card.cost)
    """

    return card

# TESTING: Comment out at the end
# Card generation: Passed
#CardMakerRandom()

def updateLabels():
    # Some global TKinter labels will need to be updated too.
    global player_health
    global player_energy
    global player_defense
    global player_deck
    global player_buff_damage
    global player_buff_defense
    global player_buff_healing

    global opponent_health
    global opponent_energy
    global opponent_defense
    global opponent_deck
    global opponent_buff_damage
    global opponent_buff_defense
    global opponent_buff_healing

    player_health.configure(text = "Health: " + str(player.health))
    player_energy.configure(text = "Energy: " + str(player.energy_current) + "/" + str(player.energy))
    player_defense.configure(text = "Defense: " + str(player.defense))
    player_deck.configure(text = "Deck: " + str(player.deck))
    player_buff_damage.configure(text = "Damage Buff: " + str(player.buff_damage))
    player_buff_defense.configure(text = "Defense Buff: " + str(player.buff_defense))
    player_buff_healing.configure(text = "Healing Buff: " + str(player.buff_healing))

    opponent_health.configure(text = "Health: " + str(opponent.health))
    opponent_energy.configure(text = "Energy: " + str(opponent.energy_current) + "/" + str(opponent.energy))
    opponent_defense.configure(text = "Defense: " + str(opponent.defense))
    opponent_deck.configure(text = "Deck: " + str(opponent.deck))
    opponent_buff_damage.configure(text = "Damage Buff: " + str(opponent.buff_damage))
    opponent_buff_defense.configure(text = "Defense Buff: " + str(opponent.buff_defense))
    opponent_buff_healing.configure(text = "Healing Buff: " + str(opponent.buff_healing))

# Have a player and opponent play
# single cards against each other: Passed
def singleCardTest():


    player = Player()
    opponent = Player()

    player_card = CardMakerRandom()
    print("Player will play: ", end="")
    print(player_card)
    opponent_card = CardMakerRandom()

    player_card.play(player, opponent)
    print("First card played. Player status:")
    print(player)
    print("Opponent status:")
    print(opponent)

    print("Opponent will play: ", end="")
    print(opponent_card)

    opponent_card.play(opponent, player)
    print("Second card played. Player status:")
    print(player)
    print("Opponent status:")
    print(opponent)


def singleCardTestPersistent(player, opponent):


    # player and opponent are Player objects

    player_card = CardMakerRandom()
    print("Player will play: ", end="")
    print(player_card)
    opponent_card = CardMakerRandom()

    player_card.play(player, opponent)
    print("First card played. Player status:")
    print(player)
    print("Opponent status:")
    print(opponent)

    print("Opponent will play: ", end="")
    print(opponent_card)

    opponent_card.play(opponent, player)
    print("Second card played. Player status:")
    print(player)
    print("Opponent status:")
    print(opponent)

    # Make sure to preserve these in a variable somewhere!
    return player, opponent

def singleCardTestGlobal():
    # Inform the function that it should use the external/global
    # variable when = is used.
    # Apparently it also preserves progress when play() is used.
    global player
    global opponent

    # Some global TKinter labels will need to be updated too.
    """ 
    global player_health
    global player_energy
    global player_defense
    global player_deck
    global player_buff_damage
    global player_buff_defense
    global player_buff_healing

    global opponent_health
    global opponent_energy
    global opponent_defense
    global opponent_deck
    global opponent_buff_damage
    global opponent_buff_defense
    global opponent_buff_healing
    """

    # player and opponent are Player objects

    player_card = CardMakerRandom()
    print("Player will play: ", end="")
    print(player_card)
    opponent_card = CardMakerRandom()

    player_card.play(player, opponent)
    print("First card played. Player status:")
    print(player)
    print("Opponent status:")
    print(opponent)

    print("Opponent will play: ", end="")
    print(opponent_card)

    opponent_card.play(opponent, player)
    print("Second card played. Player status:")
    print(player)
    print("Opponent status:")
    print(opponent)

    # UPDATE TKINTER LABELS
    """
    player_health.configure(text = "Health: " + str(player.health))
    player_energy.configure(text = "Energy: " + str(player.energy))
    player_defense.configure(text = "Defense: " + str(player.defense))
    player_deck.configure(text = "Deck: " + str(player.deck))
    player_buff_damage.configure(text = "Damage Buff: " + str(player.buff_damage))
    player_buff_defense.configure(text = "Defense Buff: " + str(player.buff_defense))
    player_buff_healing.configure(text = "Healing Buff: " + str(player.buff_healing))

    opponent_health.configure(text = "Health: " + str(opponent.health))
    opponent_energy.configure(text = "Energy: " + str(opponent.energy))
    opponent_defense.configure(text = "Defense: " + str(opponent.defense))
    opponent_deck.configure(text = "Deck: " + str(opponent.deck))
    opponent_buff_damage.configure(text = "Damage Buff: " + str(opponent.buff_damage))
    opponent_buff_defense.configure(text = "Defense Buff: " + str(opponent.buff_defense))
    opponent_buff_healing.configure(text = "Healing Buff: " + str(opponent.buff_healing))
    """
    updateLabels()

end_button_pressed = False # False until the player clicks a certain button

def pressEndButton():
    global end_button_pressed
    global card_pressed
    end_button_pressed.set(True) # Will ignore remaining energy and cards and let the opponent play their turn
    card_pressed.set(1) # Updating this to anything will cause the turn to progress



def battle():
    # Inform the function that it should use the external/global
    # variable when = is used.
    # Apparently it also preserves progress when play() is used.
    global player
    global opponent
    global end_button_pressed
    global card_pressed # Helps the pressEndButton function integrate with this one
    global main # I think this affects the TKinter window successfully...
    global frame_cards

    # Upon starting the battle, we remove the Begin button and replace it with the End Turn button.
    end_button.pack() 
    battle_button.destroy()
    

    # Updating the labels will be done by the now-separate function, updateLabels().

    # Let's keep track of per-turn stats like energy and remaining cards:
    player.energy_current = 0
    player_card_count = player.deck

    opponent.energy_current = 0
    opponent_card_count = opponent.deck

    # We should have a player turn and an opponent turn.
    battle_continue = True # When false, battle is over; run some code at the end to finish up
    player_turn = True # When false, it's the opponent's turn
    
    this_turn_deck_buttons = [] # Initialize
    end_button_pressed = tkinter.BooleanVar() # Starts false
    card_pressed = tkinter.IntVar(value=-1) # Starts at -1; wait for it to become a positive number before proceeding

    # Tips from Stack Overflow for the Button Click Version:
    """Don't use sleep() in tkinter. use after() instead."""
    """
    The simplest way to get tkinter to wait for some event is to call one of the "wait" functions, such as wait_variable, wait_window, or wait_visibility.

    In your case you want to wait for a button click, so you can use wait_variable and then have the button set the variable. When you click the button the variable will be set, and when the variable is set the call to wait_variable will return. 

    Note: you don't have to use IntVar -- any of the special Tkinter variables will do. Also, it doesn't matter what you set it to; the method will wait until it changes.
    """

    # Job prospects/ways to use Python:
    """
    Have you ever heard about Python Backend? I'm working as a Python Backend dev, currently with Flask. It is really good. I just hope Python Web Development will become more popular.

    FastAPI

    What about Python Django? Is Django as great as Flask? -> They serve different purposes and are not directly comparable. Django is great for large apps where you're going to use most of the Django stuff; Flask is great for small ones where that would all be extra.

    Python web dev already hit its peak a while ago and has settled into a comfortable space. If you remember when nodejs got created, that was the next big thing after Python. -> So what do you recommend? Stick to it? -> It is a solid choice from a career perspective, yes. But as with any particular technology, keep an eye on what job postings for jobs you want are frequently asking for and if something starts to be big and you don't have experience with it, get it.
    """

    # BUTTON CLICK VERSION
    def click(button):
        #"""
        print("Player will play: ", end="")
        print(button.card)

        # Play the card, subtract the energy cost, remove that card
        # from the deck, and remove its button.
        button.card.play(player, opponent)
        player.energy_current -= button.card.cost
        this_turn_deck.remove(button.card)
        this_turn_deck_buttons.remove(button)
        button.destroy()

        updateLabels()

        # CHECK FOR END OF PLAYER TURN
        # Click the end turn button, energy is depleted, or cards are all gone
        if end_button_pressed.get() == True or player.energy_current <= 0 or len(this_turn_deck) <= 0:
            player_turn = False
        #"""

    
        card_pressed.set(1) # Just set it so it notices this function ran; don't rely on card index

    def endCleanup():
        # Just a few commands to remove some buttons once the game is over,
        # making it clearer that play has concluded.
        for b in this_turn_deck_buttons:
            b.destroy()
        end_button.destroy()

    while(battle_continue):
        # Set current values to what they should be at the start of each turn
        player.defense = 0 # Defense only lasts one turn and should be reset
        player.energy_current += player.energy # Suppose you keep "debt" from how much you overspent last turn...
        #player_card_count = player.deck # Not needed because the list length is enough

        # Provide player with cards: First, make a list that will
        # contain Card objects, or clear the existing list.
        this_turn_deck = []
        # Populate with one new card for each deck slot the player has.
        for i in range(player.deck):
            this_turn_deck.append(CardMakerRandom())
        
            
        # Now this_turn_deck contains all the cards the player has available
        # for now.
        #end_button_pressed = False

        # Reset these:
        end_button_pressed.set(False)
        card_pressed.set(-1)

        # Let's try to render in those cards as options on the screen....
        # Before resetting the list, clear out any previous buttons.
        for b in this_turn_deck_buttons:
            b.destroy()
        
        this_turn_deck_buttons = [] # A fresh list of buttons

        

        # Create a button for every card and stick it in the list of buttons.
        #card_index = 0 # Keep track of which index it is
        for card in this_turn_deck:
            # RADIO BUTTON VERSION
            #this_turn_deck_buttons.append(tkinter.Radiobutton(frame_cards, text = card.fullname + " (" + str(card.cost) + ")"))

            # REGULAR BUTTON VERSION
            button_to_add = (tkinter.Button(frame_cards, text = card.fullname + " (" + str(card.cost) + ")")) # Place it within the frame that holds cards, display the card's name and energy cost, set it to run a function when clicked
            button_to_add.card = card # Can you just add new attributes??
            #button_to_add.index = card_index
            button_to_add.configure(command = lambda b=button_to_add: click(b)) 
            # Does this b=button_to_add syntax from some Redditor make a difference? YES! It's absolutely what I needed! Why?! Oh, who cares.
            this_turn_deck_buttons.append(button_to_add)
            
        
        
        

        # Make all the buttons render.
        for b in this_turn_deck_buttons:
            #print("Button at index %d:" % this_turn_deck_buttons.index(b), end = " ")
            #print(b, end = " which has card ")
            #print(b.card)
            b.pack()

        # PLAYER'S TURN!
        while(player_turn):
            # Next step: Let the player select a card from the buttons available to them.

            print("Your cards: ", this_turn_deck)
            print("You have %i cards and %i energy available." % (len(this_turn_deck), player.energy_current), end = "\n")

            updateLabels()

            # BUTTON CLICK VERSION
            # We must have Tkinter wait for a button to be clicked.
            # Each button's command is the "click" function, so that must be written to change the necessary variable.
            dummybutton = tkinter.Button() # wait_variable needs an object, which I don't like. Let's generate an arbitrary one so we know it won't have been destroyed.
            dummybutton.wait_variable(card_pressed)

            

            # Now find the chosen card and play it!
            """
            player_choice = card_pressed.get() # An integer

            if player_choice < len(this_turn_deck) and player_choice >= 0:
                card_choice = this_turn_deck[player_choice]
                button_choice = this_turn_deck_buttons[player_choice]
            else:
                card_choice = this_turn_deck[0] # Default to first card if input is too large or small
                button_choice = this_turn_deck_buttons[0]
            
            print("Player will play: ", end="")
            print(card_choice)

            # Play the card, subtract the energy cost, remove that card
            # from the deck, and remove its button.
            card_choice.play(player, opponent)
            player.energy_current -= card_choice.cost
            this_turn_deck.remove(card_choice)
            button_choice.destroy()

            card_pressed.set(-1)

            updateLabels()
            #"""
            # CHECK FOR END OF PLAYER TURN
            # Click the end turn button, energy is depleted, or cards are all gone
            if end_button_pressed.get() == True or player.energy_current <= 0 or len(this_turn_deck) <= 0:
                player_turn = False
            #"""
            
            
        
        updateLabels()

        # Between turns: Check for end of battle
        if opponent.health <= 0 or opponent.energy <= 0 or opponent.deck <= 0:
            battle_continue = False
            print("You win!")
            endCleanup()
            break

        
        # Set opponent's current values to what they should be at the start of each turn
        opponent.defense = 0 # Defense only lasts one turn and should be reset
        opponent.energy_current += opponent.energy
        opponent_card_count = opponent.deck

        # OPPONENT'S TURN!
        while (player_turn == False):
            # Random fighting mechanism: Computer plays random cards
            # until it runs out of energy or cards.
            opponent_card = CardMakerRandom()
            print("Opponent will play: ", end="")
            print(opponent_card)

            opponent_card.play(opponent, player)
            opponent.energy_current -= opponent_card.cost
            opponent_card_count -= 1

            # CHECK FOR END OF OPPONENT TURN
            if opponent.energy_current <= 0 or opponent_card_count <= 0:
                player_turn = True
        
        updateLabels()
        # Both loops are done: Check for end of battle
        if player.health <= 0 or player.energy <= 0 or player.deck <= 0:
            battle_continue = False
            print("Your opponent wins!")
            endCleanup()
            break


# GUI: Use Tkinter to create a screen for the cards.
# Create persistent player and opponent...
player = Player()
opponent = Player()


# ...then start the tkinter boilerplate.
main = tkinter.Tk()
main.geometry("500x600")

# MAKE ALL NEEDED WIDGETS
# A frame to hold the card buttons
frame_cards = tkinter.Frame(main)

# A frame to hold the canvas, start button, and end turn button
frame_middle = tkinter.Frame(main)

# Canvas for weird art
canv = tkinter.Canvas(frame_middle, bd=20, width=170, height=145, bg="blue")
canv.create_oval(25, 35, 70, 75, fill="red")
#canv.create_text()



# Button creation
#play_button = tkinter.Button(main, command=singleCardTestGlobal, fg="#FFAABB", bg="gray", activebackground="white", activeforeground="orange", cursor="dot", text="FIGHT!!!!!")
battle_button = tkinter.Button(frame_middle, command=battle, fg="#FFAABB", bg="gray", activebackground="white", activeforeground="orange", cursor="dot", text="Begin!")
end_button = tkinter.Button(frame_middle, command=pressEndButton, fg="#FFAABB", bg="black", activebackground="gray", activeforeground="red", cursor="dot", text="End Turn")


# LABELS FOR STATS
frame_left = tkinter.Frame(main)
frame_right = tkinter.Frame(main)

# Fonts
bold = tkinter.font.Font(size=14, weight="bold")
bold_small = tkinter.font.Font(size=11, weight="bold")
font12 = tkinter.font.Font(size=12)

# Create player labels
player_header = tkinter.Label(frame_left, text = "YOUR STATS", font = bold)
player_health = tkinter.Label(frame_left, text = "Health: " + str(player.health), font = font12)
player_energy = tkinter.Label(frame_left, text = "Energy: " + str(player.energy_current) + "/" + str(player.energy), font = font12)
player_defense = tkinter.Label(frame_left, text = "Defense: " + str(player.defense), font = font12)
player_deck = tkinter.Label(frame_left, text = "Deck Size: " + str(player.deck), font = font12)
player_buff_damage = tkinter.Label(frame_left, text = "Damage Buff: " + str(player.buff_damage), font = font12)
player_buff_defense = tkinter.Label(frame_left, text = "Defense Buff: " + str(player.buff_defense), font = font12)
player_buff_healing = tkinter.Label(frame_left, text = "Healing Buff: " + str(player.buff_healing), font = font12)

# Create opponent labels
opponent_header = tkinter.Label(frame_right, text = "OPPONENT STATS", font = bold)
opponent_health = tkinter.Label(frame_right, text = "Health: " + str(opponent.health), font = font12)
opponent_energy = tkinter.Label(frame_right, text = "Energy: " + str(opponent.energy_current) + "/" + str(opponent.energy), font = font12)
opponent_defense = tkinter.Label(frame_right, text = "Defense: " + str(opponent.defense), font = font12)
opponent_deck = tkinter.Label(frame_right, text = "Deck Size: " + str(opponent.deck), font = font12)
opponent_buff_damage = tkinter.Label(frame_right, text = "Damage Buff: " + str(opponent.buff_damage), font = font12)
opponent_buff_defense = tkinter.Label(frame_right, text = "Defense Buff: " + str(opponent.buff_defense), font = font12)
opponent_buff_healing = tkinter.Label(frame_right, text = "Healing Buff: " + str(opponent.buff_healing), font = font12)

# FINISH UP RENDERING
# Won't show up unless you pack it.
# Or, grid() or place() may also work.
#play_button.pack(expand=True)
#play_button_text.pack()

frame_cards.pack(side = tkinter.TOP)
frame_middle.pack(side = tkinter.TOP)
canv.pack()
#play_button.pack()
battle_button.pack()
#end_button.pack()

#player_stats.pack()


frame_left.pack(side = tkinter.LEFT)
frame_right.pack(side = tkinter.RIGHT)


player_header.pack()
player_health.pack()
player_energy.pack()
player_defense.pack()
player_deck.pack()
player_buff_damage.pack()
player_buff_defense.pack()
player_buff_healing.pack()

opponent_header.pack()
opponent_health.pack()
opponent_energy.pack()
opponent_defense.pack()
opponent_deck.pack()
opponent_buff_damage.pack()
opponent_buff_defense.pack()
opponent_buff_healing.pack()


# TEST: Update a label
#player_buff_healing.configure(text = "Oh no")
# Success!

# Make tkinter do its thing
main.mainloop()
