# classes / gameplay loop / some functions redacted

def simulate_clicker(build_info, duration, strategy):
    """
    Function to run a Cookie Clicker game for the given
    duration with the given strategy.  Returns a ClickerState
    object corresponding to the final state of the game.
    """
    bi_clone = build_info.clone()
    game_state = ClickerState()
    #once max duration reached, check strategy again to see possible purchases & perform
    item = strategy(game_state.get_cookies(), game_state.get_cps(), game_state.get_history(),
                    duration-game_state.get_time(), bi_clone)
    if item == None:
        return game_state

    while game_state.get_time() <= duration:
        #check buildinfo item, using get_cost
        time = game_state.time_until(bi_clone.get_cost(item))
        if game_state.get_time() + time > duration:
            max_wait = duration - game_state.get_time()
            game_state.wait(max_wait)
            break

        game_state.wait(time)
        game_state.buy_item(item, bi_clone.get_cost(item), bi_clone.get_cps(item))
        bi_clone.update_item(item)
        item = strategy(game_state.get_cookies(), game_state.get_cps(), game_state.get_history(),
                        duration-game_state.get_time(), bi_clone)
        if item == None:
            break
    while not item == None:
        num_pur = game_state.get_cookies() // bi_clone.get_cost(item)
        for dummy_i in range(int(num_pur)):
            game_state.buy_item(item, bi_clone.get_cost(item), bi_clone.get_cps(item))
            bi_clone.update_item(item)
        item = strategy(game_state.get_cookies(), game_state.get_cps(), game_state.get_history(),
                        duration-game_state.get_time(), bi_clone)

    # Replace with your code
    return game_state

def strategy_cheap(cookies, cps, history, time_left, build_info):
    """
    Always buy the cheapest item you can afford in the time left.
    """
    #take whole item list
    #find lowest cost of list
    #buy it
    b_items = build_info.build_items()
    cheapest_cost = 0.0
    chosen_item = None
    for item in b_items:
        if chosen_item == None:
            chosen_item = item
            cheapest_cost = build_info.get_cost(item)
            continue
        if cheapest_cost > build_info.get_cost(item):
            cheapest_cost = build_info.get_cost(item)
            chosen_item = item
    if (time_left*cps+cookies) < cheapest_cost or (time_left == 0.0 and cheapest_cost > cookies):
        return None
    return chosen_item

def strategy_expensive(cookies, cps, history, time_left, build_info):
    """
    Always buy the most expensive item you can afford in the time left.
    """
    #take whole item list
    #find most expensive item
    #buy it
    b_items = build_info.build_items()
    highest_cost = 0.0
    chosen_item = None
    for item in b_items:
        if chosen_item == None:
            chosen_item = item
            highest_cost = build_info.get_cost(item)
            continue
        if highest_cost < build_info.get_cost(item) and time_left*cps+cookies >= build_info.get_cost(item):
            highest_cost = build_info.get_cost(item)
            chosen_item = item
    if (time_left*cps+cookies) < highest_cost:
        return None
    if time_left == 0.0 and highest_cost > cookies:
        return None
    return chosen_item

def strategy_best(cookies, cps, history, time_left, build_info):
    """
    The best strategy that you are able to implement.
    """
    possible_items = affordable(cookies, cps, time_left, build_info)
    if possible_items == []:
        return None
    #once filtered,
    #append via ratio of cps & cost

    r_lst = []
    for idx in range(len(possible_items)):
        ratio = build_info.get_cps(possible_items[idx]) / build_info.get_cost(possible_items[idx])
        r_lst.append(ratio)

    idx_num = r_lst.index(max(r_lst))
    #pick & return best_choice
    chosen_item = possible_items[idx_num]

    return chosen_item

def strategy_earned_value(cookies, cps, history, time_left, build_info):
    """
    The best strategy that you are able to implement.
    """
    afford_items = affordable(cookies, cps, time_left, build_info)
    if afford_items == []:
        return None

    expected_outcome = []
    for dummy_i in range(len(afford_items)):
        item_cps = build_info.get_cps(afford_items[dummy_i])
        item_cost = build_info.get_cost(afford_items[dummy_i])

        # the strategy is: in each step, calculate the possible earned value for each affordable items
        time_to_earn = (item_cost - cookies)/ cps
        earned_value = item_cps * (time_left - time_to_earn)
        expected_outcome.append(earned_value)

    #print "affordable items: ", afford_items, "expected: ", expected_outcome, "when time left ", time_left
    best_idx = expected_outcome.index(max(expected_outcome))
    best_item = afford_items[best_idx]

    #print "return affordable best item ", best_item, " with cost of ", build_info.get_cost(best_item)
    return best_item
