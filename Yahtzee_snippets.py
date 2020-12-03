# classes / gameplay loop / some functions redacted

def gen_all_sequences(outcomes, length):
    """
    Iterative function that enumerates the set of all sequences of
    outcomes of given length.
    """

    answer_set = set([()])
    for dummy_idx in range(length):
        temp_set = set()
        for partial_sequence in answer_set:
            for item in outcomes:
                new_sequence = list(partial_sequence)
                new_sequence.append(item)
                temp_set.add(tuple(new_sequence))
        answer_set = temp_set
    return answer_set


def score(hand): #calculate score of given hand, assume any length; highest val of single num sum
    """
    Compute the maximal score for a Yahtzee hand according to the
    upper section of the Yahtzee score card.

    hand: full yahtzee hand

    Returns an integer score
    """
    #assume any # of sides for each die in hand
    #can double loop, for each match += cur_score & append
    #end result will be the highest sum of single num

    ##can just append to inner variable & compare to outer
    ## per loop
    hand_score = 0
    check_hand = set(sorted(hand))
    for cur_val in check_hand:
        cur_score = 0
        for other_val in hand:
            if cur_val == other_val and cur_score == 0:
                cur_score = other_val
            elif cur_val == other_val:
                cur_score += other_val
        if cur_score > hand_score:
            hand_score = cur_score

    return hand_score
    #return 0


def expected_value(held_dice, num_die_sides, num_free_dice): #given possible hold, use score to calc all variations w/ gen_all_sequences
    """
    Compute the expected value based on held_dice given that there
    are num_free_dice to be rolled, each with num_die_sides.

    held_dice: dice that you will hold
    num_die_sides: number of sides on each die
    num_free_dice: number of dice to be rolled

    Returns a floating point expected value
    """
    ev_total = 0.0
    #use num_die_sides & free_dice to create latter variations of given hand
    #loop each item created by gen_all_sequence & 'score it' after appending w/ held_dice
    #use all scores to calc expected value

    # after all scores calculated, multiply each by their possibility & add them
    # for each loop, EV_total+=(score * possibility fraction)

    #calculate the EV of the given hand
    #in strategy, will have a matching index for each or dict?
    #use some way of keeping track of highest EV and then returning the best one
    die_sides = range(num_die_sides)
    for dummy_i, dummy_j in enumerate(die_sides):
        die_sides[dummy_i] += 1
    hand_variations = gen_all_sequences(die_sides, num_free_dice)
    for cur_variation in hand_variations:
        test_hand = list(held_dice)
        test_hand.extend(cur_variation)
        ev_total += score(test_hand)
    ev_total /= len(hand_variations)
    return ev_total
    #return 0.0



def gen_all_holds(hand):
    """
    Generate all possible choices of dice from hand to hold.

    hand: full yahtzee hand

    Returns a set of tuples, where each tuple is dice to hold
    """
    #create binary subsets & then use it to create subsets of actual hand
    binary_sets = gen_all_sequences([0,1], len(hand)) # returns set w/ binary mapping

    #for every binary tuple, creates corresponding subset of hand
    #manipulate the final list of subsets
    hand_subsets = []
    for cur_binary in binary_sets: # applies to every binary mapping
        temp_subset = []
        for dummy_i, dummy_j in zip(cur_binary, hand):
            if dummy_i == 1:
                temp_subset.append(dummy_j)

        hand_subsets.append(tuple(temp_subset))

    return set(hand_subsets)



def strategy(hand, num_die_sides):
    """
    Compute the hold that maximizes the expected value when the
    discarded dice are rolled.

    hand: full yahtzee hand
    num_die_sides: number of sides on each die

    Returns a tuple where the first element is the expected score and
    the second element is a tuple of the dice to hold
    """
    possible_holds = gen_all_holds(hand)

    ##hold the EV somewhere to compare possible holds; can possibly make a dictionary?
    #each loop checks if the EV compared to highest EV, places hold & EV in return var.
    highest_ev = 0
    best_hold = None
    for held_dice in possible_holds:
        cur_ev = expected_value(held_dice, num_die_sides, len(hand)-len(held_dice))
        if cur_ev > highest_ev:
            highest_ev = cur_ev
            best_hold = held_dice


    return (highest_ev, best_hold)
