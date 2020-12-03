# classes / gameplay loop redacted

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
