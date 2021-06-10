turn_left = 0
locked_treasures = []
locked_pirates_with_treasure = []
locked_pirates = []
is_boosted = False
locked_locations = []
go_def_pirates = []
sent_home = False
we_are_better = False
pirate_not_ordered = []
all_treasures_number = 0
last_treasure = 0
go_attackers_ids = []
go_treasures_ids = []
following = False
carry_treasure_speed = 0
attacker_p_up = 0
base_keeper = False
attacker_id = ""
problem_in_our_base = False

def do_turn(game):
    global turn_left
    turn_left = game.get_actions_per_turn()
    global pirate_not_moved
    pirate_not_moved = len(game.my_sober_pirates())
    global locked_treasures
    locked_treasures = []
    global locked_pirates
    locked_pirates = []
    global locked_pirates_with_treasure
    locked_pirates_with_treasure = []
    global locked_locations
    global sent_home
    global we_are_better
    global pirate_not_ordered
    global last_treasure
    global all_treasures_number
    global is_boosted
    global go_attackers_ids
    global go_treasures_ids
    global following
    global sent_home
    global base_keeper
    global attacker_id
    global problem_in_our_base
    locked_locations = []
    sent_home = False
    pirate_not_ordered = game.my_pirates()
    following = False
    attacker_p_up = False
    attacker_id = None
    if get_pirate_with_attack_powerup(game) != False:
        attacker_id = get_pirate_with_attack_powerup(game).id
        attacker_p_up = True
    game.debug("Turn: " + str(game.get_turn()))
    game.debug("Ort Holon B is the best")
    if (game.get_turn() == 1):
        all_treasures_number = len(game.treasures())
    #if game.get_turn() < (game.distance(game.all_my_pirates()[0].initial_loc, game.all_enemy_pirates()[0].initial_loc) / (turn_left / 2)) and len(game.all_my_pirates()) == 4:
    #    pirate_not_ordered = []
    #    for i in game.my_pirates():
    #        if i.id < 2:
    #            pirate_not_ordered.append(i)
    for i in game.my_pirates():
        if (len(game.treasures()) == 1):
            one_treasure_left(game, i)
        if len(game.treasures()) == 0:
            no_treasures(game, i)
        if len(game.all_my_pirates()) < len(game.all_enemy_pirates()):
            they_are_more_than_us(game, i)
        if len(game.all_my_pirates()) > 2:
            above_two(game, i)
        two_or_below(game, i)
    for i in pirate_not_ordered:
        if turn_left > 0:
            go_treasure(game, i.id)


#Tactics ===============================================


def two_or_below(game, i):
    global pirate_not_moved
    global sent_home
    global pirate_not_ordered
    global last_treasure
    global is_boosted
    global following
    global sent_home
    if i.id < int(len(game.my_pirates()) / 2):
        if attacker_p_up:
            if i.id == attacker_id:
                if (len(game.enemy_pirates_with_treasures()) >= 1) and i.turns_to_sober == 0 and i.reload_turns == 0:
                    #Sending the go_treasures with treasure to initial loc
                    if sent_home == False:
                        for j in game.my_pirates_with_treasures():
                            go_treasure(game, j.id)
                            sent_home = True
                    is_boosted = True
                    if (go_attack(game, i.id) == 0):
                        game.debug("in place")
                        is_boosted = False
                    else:
                        is_boosted = False
                        return
                else:
                    go_attack(game, i.id)
        elif (len(game.enemy_pirates_with_treasures()) >= 1) and i.turns_to_sober == 0 and i.reload_turns == 0:
            #Sending the go_treasures with treasure to initial loc
            if sent_home == False:
                for j in game.my_pirates_with_treasures():
                    go_treasure(game, j.id)
                    sent_home = True
            is_boosted = True
            if (go_attack(game, i.id) == 0):
                game.debug("in place")
                is_boosted = False
            else:
                is_boosted = False
                return
        else:
            go_treasure(game, i.id)
    else:
        if sent_home == False:
            go_treasure(game, i.id)


def above_two(game, i):
    global pirate_not_moved
    global sent_home
    global pirate_not_ordered
    global last_treasure
    global is_boosted
    global following
    global sent_home
    if len(check_base(game)) > 0: #and len(game.enemy_pirates_with_treasures()) < 2:
        if i.id <= int(len(game.my_pirates()) / 2):
            #Sending the go_treasures with treasure to initial loc
            if sent_home == False:
                for j in game.my_pirates_with_treasures():
                    go_treasure(game, j.id)
                    sent_home = True
            is_boosted = True
            if (go_base_keeping(game, i.id) == 0):
                game.debug("in place")
                is_boosted = False
            else:
                is_boosted = False
                return
        else:
            if sent_home == False:
                go_treasure(game, i.id)
    if attacker_p_up:
        if i.id == attacker_id:
            if (len(game.enemy_pirates_with_treasures()) >= 1) and i.turns_to_sober == 0 and i.reload_turns == 0:
                #Sending the go_treasures with treasure to initial loc
                if sent_home == False:
                    for j in game.my_pirates_with_treasures():
                        go_treasure(game, j.id)
                        sent_home = True
                is_boosted = True
                if (go_attack(game, i.id) == 0):
                    game.debug("in place")
                    is_boosted = False
                else:
                    is_boosted = False
                    return
            else:
                go_attack(game, i.id)
    elif i.id == 1:
        if (len(game.enemy_pirates_with_treasures()) >= 1) and i.turns_to_sober == 0 and i.reload_turns == 0:
            #Sending the go_treasures with treasure to initial loc
            if sent_home == False:
                for j in game.my_pirates_with_treasures():
                    go_treasure(game, j.id)
                    sent_home = True
            is_boosted = True
            if (go_camp(game, i.id) == 0):
                game.debug("in place")
                is_boosted = False
            else:
                is_boosted = False
                return
        else:
            go_camp(game, i.id)
    elif i.id <= int(len(game.my_pirates()) / 2):
    #elif i in go_attackers_ids:
        if (len(game.enemy_pirates_with_treasures()) >= 1) and i.turns_to_sober == 0 and i.reload_turns == 0:
            #Sending the go_treasures with treasure to initial loc
            if sent_home == False:
                for j in game.my_pirates_with_treasures():
                    go_treasure(game, j.id)
                    sent_home = True
            is_boosted = True
            if (go_camp(game, i.id) == 0):
                game.debug("in place")
                is_boosted = False
            else:
                is_boosted = False
                return
        else:
            go_attack(game, i.id)
    else:
        if sent_home == False:
            go_treasure(game, i.id)


def they_are_more_than_us(game, i):
    global pirate_not_moved
    global sent_home
    global pirate_not_ordered
    global last_treasure
    global is_boosted
    global following
    global sent_home
    if i.id < int(len(game.my_pirates()) / 2):
        if attacker_p_up:
            if i.id == attacker_id:
                if (len(game.enemy_pirates_with_treasures()) >= 1) and i.turns_to_sober == 0 and i.reload_turns == 0:
                    #Sending the go_treasures with treasure to initial loc
                    if sent_home == False:
                        for j in game.my_pirates_with_treasures():
                            go_treasure(game, j.id)
                            sent_home = True
                    is_boosted = True
                    if (go_attack(game, i.id) == 0):
                        game.debug("in place")
                        is_boosted = False
                    else:
                        is_boosted = False
                        return
                else:
                    go_attack(game, i.id)
        elif (len(game.enemy_pirates_with_treasures()) >= 1) and i.turns_to_sober == 0 and i.reload_turns == 0:
            #Sending the go_treasures with treasure to initial loc
            if sent_home == False:
                for j in game.my_pirates_with_treasures():
                    go_treasure(game, j.id)
                    sent_home = True
            is_boosted = True
            if (go_camp(game, i.id) == 0):
                game.debug("in place")
                is_boosted = False
            else:
                is_boosted = False
                return
        else:
            go_camp(game, i.id)
    else:
        if sent_home == False:
            go_treasure(game, i.id)


def no_treasures(game, i):
    global pirate_not_moved
    global sent_home
    global pirate_not_ordered
    global last_treasure
    global is_boosted
    global following
    global sent_home
    global base_keeper
    if len(game.my_pirates_with_treasures()) == 0: #and len(game.enemy_pirates_with_treasures()) == 0:
        if i.id == 0:
            go_treasure(game, i.id)
        else:
            if (len(game.enemy_pirates_with_treasures()) >= 1) and i.turns_to_sober == 0 and i.reload_turns == 0:
                #Sending the go_treasures with treasure to initial loc
                if sent_home == False:
                    for j in game.my_pirates_with_treasures():
                        go_treasure(game, j.id)
                        sent_home = True
                is_boosted = True
                if (go_attack(game, i.id) == 0):
                    game.debug("in place")
                    is_boosted = False
                else:
                    is_boosted = False
                    return
            else:
                go_camp(game, i.id)
    else:
        if following == False and not i.has_treasure and not i.turns_to_sober > 0:
            following = True
            if sent_home == False:
                for j in game.my_pirates_with_treasures():
                    go_treasure(game, j.id)
                    sent_home = True
            if not go_follow(game, i.id) == 0:
                following = True
            else:
                following = False
        else:
            if sent_home == False:
                for j in game.my_pirates_with_treasures():
                    go_treasure(game, j.id)
                    sent_home = True
            go_attack(game, i.id)


def one_treasure_left(game, i):
    global pirate_not_moved
    global sent_home
    global pirate_not_ordered
    global last_treasure
    global is_boosted
    global following
    global sent_home
    if (len(game.treasures()) == 1) and len(game.all_my_pirates()) != 1:
        if sent_home == False:
            for j in game.my_pirates_with_treasures():
                go_treasure(game, j.id)
                sent_home = True
        is_boosted = True
        go_treasure(game, i.id)
        is_boosted = False
    elif (len(game.treasures()) == 1) and len(game.all_my_pirates()) == 1:
        if sent_home == False:
            for j in game.my_pirates_with_treasures():
                go_treasure(game, j.id)
                sent_home = True
        if len(game.enemy_sober_pirates()) == 0:
            go_treasure(game, i.id)
        else:
            go_camp(game, i.id)


#Positions =============================================


def go_base_keeping(game, i):
    try:
        global pirate_not_moved
        global turn_left
        global go_def_pirates
        global is_boosted
        pirate = 0
        for p in game.my_pirates():
            if p.id == i:
                pirate = p
        if pirate == 0:
            pirate_not_moved = pirate_not_moved - 1
            pirate_not_ordered.remove(pirate)
            return
        if pirate not in pirate_not_ordered:
            return 0
        if pirate.turns_to_sober > 0:
            pirate_not_moved = pirate_not_moved - 1
            pirate_not_ordered.remove(pirate)
            return
        #if he isn't sober or is lost - give up on this ship for this turn.
        if pirate.is_lost or pirate.turns_to_sober > 0:
            pirate_not_ordered.remove(pirate)
            return
        #if he has a treasure - go_treasure
        if pirate.has_treasure:
            game.debug("go treasure")
            go_treasure(game, i)
            return
        #if there is no sober enemy pirates - go_treasure.
        elif len(game.enemy_sober_pirates()) == 0 and len(game.treasures()) != 0:
            go_treasure(game, i)
            return
        #if pirate.reload_turns > 0:
        #    return False
        game.debug("attacking")
        if not is_boosted:
            pirate_not_moved = len(pirate_not_ordered)
        else:
            pirate_not_moved = 1
        moves = int(turn_left / pirate_not_moved)
        if moves == 0:
            pirate_not_ordered.remove(pirate)
            return
        game.debug("pirate: " + str(pirate.id))
        is_with_treasure = False
        attack_power_up = False
        for i in pirate.powerups:
            if i == "Attack" or i == "attack":
                attack_power_up = True
        pirate_to_attack = assign_base_targets(game)
        if pirate_to_attack == 0:
            is_boosted = False
            if go_camp(game, i) == 0:
                go_attack(game, i)
            return
            #pirate_not_ordered.remove(pirate)
        else:
            in_range_enemies = if_dangerous_enemies_in_range(game, pirate)
            if len(in_range_enemies) != 0 and pirate.reload_turns != 0:
                if pirate.defense_reload_turns == 0 or game.get_defense_expiration_turns() > 0:
                    game.defend(pirate)
                    turn_left = turn_left - 1
                    pirate_not_ordered.remove(pirate)
                    return
            destination = pirate_to_attack.location
            if not len(game.treasures()) == 0 and not len(game.my_pirates_with_treasures()):
                p_ups = get_power_ups(game)
                for i in p_ups:
                    if i.type == "Attack":
                        pirate_to_attack = i
                        destination = i.location
            #location = #possible_location(game, pirate, destination, moves)
            location = possible_dangerous_location(game, pirate, destination, moves)
            if (location != 0 and location != pirate.location):
                game.set_sail(pirate, location)
                turn_left = turn_left - moves
                pirate_not_ordered.remove(pirate)
                return
            else:
                pirate_not_ordered.remove(pirate)
                return 0
    except Exception, e:
        print_errors(game, i, "go_attack", e)


def go_follow(game, i):
    try:
        global pirate_not_moved
        global turn_left
        global go_def_pirates
        pirate = 0
        for p in game.my_pirates():
            if p.id == i:
                pirate = p
        if pirate == 0:
            pirate_not_moved = pirate_not_moved - 1
            pirate_not_ordered.remove(pirate)
            return
        if pirate not in pirate_not_ordered:
            return 0
        #if he isn't sober or is lost - give up on this ship for this turn.
        if pirate.is_lost or pirate.turns_to_sober > 0:
            pirate_not_ordered.remove(pirate)
            return
        #if he has a treasure - go_treasure
        if pirate.has_treasure:
            game.debug("go treasure")
            go_treasure(game, i)
            return
        #if there is no sober enemy pirates - go_treasure.
        #if pirate.reload_turns > 0:
        #    return False
        game.debug("following")
        if not is_boosted:
            pirate_not_moved = len(pirate_not_ordered)
        else:
            pirate_not_moved = 1
        moves = int(turn_left / pirate_not_moved)
        if moves == 0:
            pirate_not_ordered.remove(pirate)
            return
        game.debug("pirate: " + str(pirate.id))
        is_with_treasure = False
        if (len(game.enemy_sober_pirates()) > 0):
            #p1 = closest_enemy_with_treasure(game, pirate)
            pirate_to_follow = game.my_pirates_with_treasures()[0]
            in_range_enemies = if_dangerous_enemies_in_range(game, pirate)
            if len(in_range_enemies) != 0 and pirate.reload_turns != 0:
                if pirate.defense_reload_turns == 0 or game.get_defense_expiration_turns() > 0:
                    game.defend(pirate)
                    turn_left = turn_left - 1
                    pirate_not_ordered.remove(pirate)
                    return
            if pirate.reload_turns == 0:
                in_range_enemies = if_enemies_in_range(game, pirate)
                if len(in_range_enemies) != 0 and pirate.reload_turns == 0:
                    game.attack(pirate, in_range_enemies[0])
                    turn_left = turn_left - 1
                    pirate_not_ordered.remove(pirate)
                    return
            destination = pirate_to_follow.location
            location = possible_location(game, pirate, destination, moves)
            #if game.is_occupied(pirate_to_follow.initial_loc) and pirate_to_follow.location != pirate_to_follow.initial_loc:
            #    moves = turn_left
            #    location = pirate_to_follow.initial_loc
            if (location != 0 and location != pirate.location):
                game.set_sail(pirate, location)
                turn_left = turn_left - moves
                pirate_not_ordered.remove(pirate)
                return
            else:
                pirate_not_ordered.remove(pirate)
                return 0
    except Exception, e:
        print_errors(game, i, "go_attack", e)


def go_camp(game, i):
    try:
        global pirate_not_moved
        global turn_left
        global go_def_pirates
        pirate = 0
        for p in game.my_pirates():
            if p.id == i:
                pirate = p
        if pirate == 0:
            pirate_not_moved = pirate_not_moved - 1
            pirate_not_ordered.remove(pirate)
            return
        if pirate not in pirate_not_ordered:
            return 0
        if pirate.turns_to_sober > 0:
            pirate_not_moved = pirate_not_moved - 1
            pirate_not_ordered.remove(pirate)
            return
        #if he isn't sober or is lost - give up on this ship for this turn.
        if pirate.is_lost or pirate.turns_to_sober > 0:
            pirate_not_ordered.remove(pirate)
            return
        #if he has a treasure - go_treasure
        if pirate.has_treasure:
            game.debug("go treasure")
            go_treasure(game, i)
            return
        #if there is no sober enemy pirates - go_treasure.
        elif len(game.enemy_sober_pirates()) == 0 and len(game.treasures()) != 0:
            go_treasure(game, i)
            return
        game.debug("camping")
        if not is_boosted:
            pirate_not_moved = len(pirate_not_ordered)
        else:
            pirate_not_moved = 1
        moves = int(turn_left / pirate_not_moved)
        if moves == 0:
            pirate_not_ordered.remove(pirate)
            return
        game.debug("pirate: " + str(pirate.id))
        is_with_treasure = False
        if (len(game.enemy_sober_pirates()) > 0):
            p1 = closest_enemy_with_treasure(game, pirate)
            if p1 != False:
                pirate_to_attack = p1
                is_with_treasure = True
            else:
                p2 = closest_enemy(game, pirate)
                pirate_to_attack = p2
            if game.in_range(pirate, pirate_to_attack) and pirate.reload_turns == 0:
                game.attack(pirate, pirate_to_attack)
                turn_left = turn_left - 1
                pirate_not_ordered.remove(pirate)
                return
            else:
                in_range_enemies = if_dangerous_enemies_in_range(game, pirate)
                if len(in_range_enemies) != 0 and pirate.reload_turns != 0:
                    if pirate.defense_reload_turns == 0 or game.get_defense_expiration_turns() > 0:
                        game.defend(pirate)
                        turn_left = turn_left - 1
                        pirate_not_ordered.remove(pirate)
                        return
                if not is_with_treasure and pirate.reload_turns == 0:
                    in_range_enemies = if_enemies_in_range(game, pirate)
                    if len(in_range_enemies) != 0 and pirate.reload_turns == 0:
                        game.attack(pirate, in_range_enemies[0])
                        turn_left = turn_left - 1
                        pirate_not_ordered.remove(pirate)
                        return
                    elif pirate.reload_turns == 0:
                        destination = pirate_to_attack.initial_loc
                    else:
                        destination = pirate_to_attack.initial_loc
                elif pirate.reload_turns == 0:
                    destination = pirate_to_attack.initial_loc
                else:
                    destination = pirate_to_attack.initial_loc
                location = possible_location(game, pirate, destination, moves)
                if (location != 0 and location != pirate.location):
                    game.set_sail(pirate, location)
                    turn_left = turn_left - moves
                    pirate_not_ordered.remove(pirate)
                    return
                else:
                    pirate_not_ordered.remove(pirate)
                    return 0
    except Exception, e:
        print_errors(game, i, "go_attack", e)


def go_attack(game, i):
    try:
        global pirate_not_moved
        global turn_left
        global go_def_pirates
        pirate = 0
        for p in game.my_pirates():
            if p.id == i:
                pirate = p
        if pirate == 0:
            pirate_not_moved = pirate_not_moved - 1
            pirate_not_ordered.remove(pirate)
            return
        if pirate not in pirate_not_ordered:
            return 0
        if pirate.turns_to_sober > 0:
            pirate_not_moved = pirate_not_moved - 1
            pirate_not_ordered.remove(pirate)
            return
        #if he isn't sober or is lost - give up on this ship for this turn.
        if pirate.is_lost or pirate.turns_to_sober > 0:
            pirate_not_ordered.remove(pirate)
            return
        #if he has a treasure - go_treasure
        if pirate.has_treasure:
            game.debug("go treasure")
            go_treasure(game, i)
            return
        #if there is no sober enemy pirates - go_treasure.
        elif len(game.enemy_sober_pirates()) == 0 and len(game.treasures()) != 0:
            go_treasure(game, i)
            return
        if pirate.reload_turns > 0:
            return False
        game.debug("attacking")
        if not is_boosted:
            pirate_not_moved = len(pirate_not_ordered)
        else:
            pirate_not_moved = 1
        moves = int(turn_left / pirate_not_moved)
        if moves == 0:
            pirate_not_ordered.remove(pirate)
            return
        game.debug("pirate: " + str(pirate.id))
        is_with_treasure = False
        attack_power_up = False
        for i in pirate.powerups:
            if i == "Attack" or i == "attack":
                attack_power_up = True
        if (len(game.enemy_sober_pirates()) > 0):
            p1 = closest_enemy_with_treasure(game, pirate)
            if p1 != False:
                pirate_to_attack = p1
                is_with_treasure = True
            else:
                p2 = closest_enemy(game, pirate)
                pirate_to_attack = p2
            if game.in_range(pirate, pirate_to_attack) and pirate.reload_turns == 0:
                game.attack(pirate, pirate_to_attack)
                turn_left = turn_left - 1
                pirate_not_ordered.remove(pirate)
                return
            else:
                in_range_enemies = if_dangerous_enemies_in_range(game, pirate)
                if len(in_range_enemies) != 0 and pirate.reload_turns != 0:
                    if pirate.defense_reload_turns == 0 or game.get_defense_expiration_turns() > 0:
                        game.defend(pirate)
                        turn_left = turn_left - 1
                        pirate_not_ordered.remove(pirate)
                        return
                if not is_with_treasure and (pirate.reload_turns == 0 or attack_power_up):
                    in_range_enemies = if_enemies_in_range(game, pirate)
                    if len(in_range_enemies) != 0 and pirate.reload_turns == 0:
                        game.attack(pirate, in_range_enemies[0])
                        turn_left = turn_left - 1
                        pirate_not_ordered.remove(pirate)
                        return
                    elif pirate.reload_turns == 0 or attack_power_up:
                        destination = pirate_to_attack.location
                    else:
                        destination = pirate_to_attack.initial_loc
                elif pirate.reload_turns == 0 or attack_power_up:
                    destination = pirate_to_attack.location
                else:
                    destination = pirate_to_attack.initial_loc
                if not len(game.treasures()) == 0 and not len(game.my_pirates_with_treasures()):
                    p_ups = get_power_ups(game)
                    for i in p_ups:
                        if i.type == "Attack":
                            pirate_to_attack = i
                            destination = i.location
                location = possible_location(game, pirate, destination, moves)
                if (location != 0 and location != pirate.location):
                    game.set_sail(pirate, location)
                    turn_left = turn_left - moves
                    pirate_not_ordered.remove(pirate)
                    return
                else:
                    pirate_not_ordered.remove(pirate)
                    return 0
    except Exception, e:
        print_errors(game, i, "go_attack", e)


def go_treasure(game, i):
    try:
        global pirate_not_moved
        global turn_left
        global is_boosted
        global following
        # choose your first pirate ship
        game.debug("i = " + str(i))
        pirate = 0
        for p in game.my_pirates():
            if p.id == i:
                pirate = p
        if pirate == 0:
            pirate_not_ordered.remove(pirate)
            return
        if pirate not in pirate_not_ordered:
            return 0
        #if he isn't sober or is lost - give up on this ship for this turn.
        if pirate.is_lost or pirate.turns_to_sober > 0:
            pirate_not_ordered.remove(pirate)
            return
        if not pirate.has_treasure and len(game.treasures()) == 0 and len(game.my_pirates_with_treasures()) != 0:
            go_attack(game, i)
            return
        if not pirate.has_treasure and len(game.treasures()) == 0:
            go_camp(game, i)
            return
        if not is_boosted:
            pirate_not_moved = len(pirate_not_ordered)
        else:
            pirate_not_moved = 1
        game.debug("turn_left: " + str(turn_left))
        game.debug("pirate_not_moved: " + str(pirate_not_moved))
        if len(pirate_not_ordered) == 0:
            return
        else:
            moves = int(turn_left / pirate_not_moved)
        if moves == 0:
            pirate_not_ordered.remove(pirate)
            return
        game.debug("moves: " + str(moves))
        treasure = closest_safe_treasure(game, pirate)
        if treasure != 0:
            game.debug("t1: " + str(treasure.id))
        else:
            treasure = last_treasure
            pirate_not_moved = 1
            moves = int(turn_left / pirate_not_moved)
        p_ups = get_power_ups(game)
        for i in p_ups:
            if i.type == "Speed":
                treasure = i
                break
        if not pirate.has_treasure and treasure != 0:
            destination = treasure.location
            in_range_enemies = if_enemies_in_range(game, pirate)
            if len(in_range_enemies) != 0 and pirate.reload_turns == 0:
                game.attack(pirate, in_range_enemies[0])
                turn_left = turn_left - 1
                pirate_not_ordered.remove(pirate)
                return
        else:
            has_speed = False
            moves = 1
            for i in pirate.powerups:
                if i == "Speed" or i == "speed":
                    moves = carry_treasure_speed
                    has_speed = True
            if moves >= turn_left:
                if has_speed:
                    moves = turn_left - len(pirate_not_ordered)
            destination = pirate.initial_loc
            in_range_enemies = if_dangerous_enemies_in_range(game, pirate)
            if len(in_range_enemies) != 0: #and not following:
                #game.debug("2:" + str(game.get_defense_reload_turns()))
                if pirate.defense_reload_turns == 0 or game.get_defense_expiration_turns() > 0:
                    game.defend(pirate)
                    turn_left = turn_left - 1
                    pirate_not_ordered.remove(pirate)
                    return 0
        if pirate.has_treasure:
            location = possible_location2(game, pirate, destination, moves)
        else:
            location = possible_location2(game, pirate, destination, moves)
        if location != 0 and location != pirate.location:
            game.set_sail(pirate, location)
            turn_left = turn_left - moves
            pirate_not_ordered.remove(pirate)
            return
        else:
            pirate_not_ordered.remove(pirate)
            return
    except Exception, e:
        print_errors(game, i, "go_treasure", e)


#Functions =================================================


def get_pirate_with_attack_powerup(game):
    for i in game.my_pirates():
        if "Attack" in i.powerups or "attack" in i.powerups:
            return i
    return False


def get_power_ups(game):
    global carry_treasure_speed
    powerups_list = []
    for i in game.powerups():
        powerups_list.append(i)
        if i.type == "Speed":
            carry_treasure_speed = i.carry_treasure_speed
    return powerups_list


def if_enemies_in_range(game, pirate):
    l = []
    for i in game.enemy_sober_pirates():
        if game.in_range(pirate, i):
            l.append(i)
    return l


def if_enemies_in_range2(game, location):
    l = []
    for i in game.enemy_sober_pirates():
        if game.in_range(i, location):
            l.append(i)
    return l


def if_enemies_in_range3(game, location):
    l = []
    for i in game.enemy_pirates():
        if game.in_range(i, location):
            l.append(i)
    return l


def if_dangerous_enemies_in_range(game, pirate):
    l = []
    for i in game.enemy_sober_pirates():
        if game.in_range(pirate, i) and i.reload_turns == 0 and not i.has_treasure:
            l.append(i)
    return l


def closest_enemy(game, pirate):
    global locked_pirates
    if len(game.enemy_sober_pirates()) == 0:
        return False
    enemies = game.enemy_sober_pirates()
    distances = []
    enemies_list = []
    for enemy in enemies:
        distances.append(game.distance(pirate, enemy))
        enemies_list.append(enemy)
    min_dis = min(distances)
    index = distances.index(min_dis)
    enemy = enemies_list[index]
    while enemy.id in locked_pirates:
        distances.remove(min_dis)
        enemies_list.remove(enemies_list[index])
        if (len(distances) == 0):
            return enemy
        min_dis = min(distances)
        index = distances.index(min_dis)
        enemy = enemies_list[index]
    locked_pirates.append(enemy.id)
    return enemy


def closest_enemy_with_treasure(game, pirate):
    global locked_pirates
    if len(game.enemy_pirates_with_treasures()) == 0:
        return False
    enemies = game.enemy_pirates_with_treasures()
    distances = []
    enemies_list = []
    for enemy in enemies:
        distances.append(game.distance(pirate, enemy))
        enemies_list.append(enemy)
    min_dis = min(distances)
    index = distances.index(min_dis)
    enemy = enemies_list[index]
    while enemy.id in locked_pirates:
        distances.remove(min_dis)
        enemies_list.remove(enemies_list[index])
        if (len(distances) == 0):
            locked_pirates.append(enemy.id)
            #specific_locked_pirates[pirate.id] = enemy
            return enemy
        min_dis = min(distances)
        index = distances.index(min_dis)
        enemy = enemies_list[index]
    locked_pirates.append(enemy.id)
    #specific_locked_pirates[pirate.id] = enemy
    return enemy


def closest_treasure(game, pirate):
    global locked_treasures
    global last_treasure
    if len(game.treasures()) == 0:
        return False
    treasures = game.treasures()
    distances = []
    treasures_list = []
    for treasure in treasures:
        distances.append(game.distance(pirate, treasure))
        treasures_list.append(treasure)
    min_dis = min(distances)
    index = distances.index(min_dis)
    treasure = treasures_list[index]
    while treasure.id in locked_treasures:
        distances.remove(min_dis)
        treasures_list.remove(treasures_list[index])
        if (len(distances) == 0):
            return treasure
        min_dis = min(distances)
        index = distances.index(min_dis)
        treasure = treasures_list[index]
    last_treasure = treasure
    locked_treasures.append(treasure.id)
    return treasure


def closest_safe_treasure(game, pirate):
    global locked_treasures
    global last_treasure
    if len(game.treasures()) == 0:
        return False
    treasures = game.treasures()
    distances = []
    treasures_list = []
    for treasure in treasures:
        distances.append(game.distance(pirate, treasure))
        treasures_list.append(treasure)
    min_dis = min(distances)
    index = distances.index(min_dis)
    treasure = treasures_list[index]
    while treasure.id in locked_treasures: #and len(if_enemies_in_range2(game, treasure.location)) >= 3:###
        distances.remove(min_dis)
        treasures_list.remove(treasures_list[index])
        if len(if_enemies_in_range3(game, treasure.location)) >= 2:
            return farest_treasure(game, pirate)
        if (len(distances) == 0):
            return treasure
        min_dis = min(distances)
        index = distances.index(min_dis)
        treasure = treasures_list[index]
    last_treasure = treasure
    locked_treasures.append(treasure.id)
    return treasure


def farest_treasure(game, pirate):
    global locked_treasures
    global last_treasure
    if len(game.treasures()) == 0:
        return False
    treasures = game.treasures()
    distances = []
    treasures_list = []
    for treasure in treasures:
        distances.append(game.distance(pirate, treasure))
        treasures_list.append(treasure)
    min_dis = max(distances)
    index = distances.index(min_dis)
    treasure = treasures_list[index]
    while treasure.id in locked_treasures:
        distances.remove(min_dis)
        treasures_list.remove(treasures_list[index])
        if (len(distances) == 0):
            return treasure
        min_dis = max(distances)
        index = distances.index(min_dis)
        treasure = treasures_list[index]
    last_treasure = treasure
    locked_treasures.append(treasure.id)
    return treasure


def possible_location(game, pirate, destination, moves):
    global locked_locations
    global turn_left
    possible_locations = game.get_sail_options(pirate, destination, moves)
    for i in possible_locations:
        if not game.is_occupied(i) and i not in locked_locations:
            locked_locations.append(i)
            return i
    return False


def possible_dangerous_location(game, pirate, destination, moves):
    global locked_locations
    global turn_left
    possible_locations = game.get_sail_options(pirate, destination, moves)
    for i in possible_locations:
        if i not in locked_locations:
            locked_locations.append(i)
            return i
    return False


def possible_location2(game, pirate, destination, moves):
    global locked_locations
    global turn_left
    possible_locations = game.get_sail_options(pirate, destination, moves)
    game.debug(str(possible_locations))
    for i in possible_locations:
        if i not in locked_locations:
            if not game.is_occupied(i) and len(if_enemies_in_range2(game, i)) <= 2:
                locked_locations.append(i)
                return i
    i = pirate.location
    if pirate.initial_loc[0] < int(game.get_rows() / 2):
        if moves > 1:
            new_loc = (i[0] - int(moves / 2), i[1])
            if not game.is_occupied(new_loc) and new_loc[0] != 0 and new_loc[0] != 0 and new_loc[0] != game.get_rows() and new_loc[0] != game.get_cols():
                return new_loc
            new_loc = (i[0] + int(moves / 2), i[1])
            if not game.is_occupied(new_loc) and new_loc[0] != 0 and new_loc[0] != 0 and new_loc[0] != game.get_rows() and new_loc[0] != game.get_cols():
                return new_loc
        else:
            new_loc = (i[0] - moves, i[1])
            if not game.is_occupied(new_loc) and new_loc[0] != 0 and new_loc[0] != 0 and new_loc[0] != game.get_rows() and new_loc[0] != game.get_cols():
                return new_loc
            new_loc = (i[0] + moves, i[1])
            if not game.is_occupied(new_loc) and new_loc[0] != 0 and new_loc[0] != 0 and new_loc[0] != game.get_rows() and new_loc[0] != game.get_cols():
                return new_loc
    else:
        if moves > 1:
            new_loc = (i[0] + int(moves / 2), i[1])
            if not game.is_occupied(new_loc) and new_loc[0] != 0 and new_loc[0] != 0 and new_loc[0] != game.get_rows() and new_loc[0] != game.get_cols():
                return new_loc
            new_loc = (i[0] - int(moves / 2), i[1])
            if not game.is_occupied(new_loc) and new_loc[0] != 0 and new_loc[0] != 0 and new_loc[0] != game.get_rows() and new_loc[0] != game.get_cols():
                return new_loc
        else:
            new_loc = (i[0] + moves, i[1])
            if not game.is_occupied(new_loc) and new_loc[0] != 0 and new_loc[0] != 0 and new_loc[0] != game.get_rows() and new_loc[0] != game.get_cols():
                return new_loc
            new_loc = (i[0] - moves, i[1])
            if not game.is_occupied(new_loc) and new_loc[0] != 0 and new_loc[0] != 0 and new_loc[0] != game.get_rows() and new_loc[0] != game.get_cols():
                return new_loc
    if pirate.initial_loc[1] < int(game.get_cols() / 2):
        if moves > 1:
            new_loc = (i[0], i[1] - int(moves / 2))
            if not game.is_occupied(new_loc) and new_loc[0] != 0 and new_loc[0] != 0 and new_loc[0] != game.get_rows() and new_loc[0] != game.get_cols():
                return new_loc
            new_loc = (i[0], i[1] + int(moves / 2))
            if not game.is_occupied(new_loc) and new_loc[0] != 0 and new_loc[0] != 0 and new_loc[0] != game.get_rows() and new_loc[0] != game.get_cols():
                return new_loc
        else:
            new_loc = (i[0], i[1] - moves)
            if not game.is_occupied(new_loc) and new_loc[0] != 0 and new_loc[0] != 0 and new_loc[0] != game.get_rows() and new_loc[0] != game.get_cols():
                return new_loc
            new_loc = (i[0], i[1] + moves)
            if not game.is_occupied(new_loc) and new_loc[0] != 0 and new_loc[0] != 0 and new_loc[0] != game.get_rows() and new_loc[0] != game.get_cols():
                return new_loc
    else:
        if moves > 1:
            new_loc = (i[0], i[1] + int(moves / 2))
            if not game.is_occupied(new_loc) and new_loc[0] != 0 and new_loc[0] != 0 and new_loc[0] != game.get_rows() and new_loc[0] != game.get_cols():
                return new_loc
            new_loc = (i[0], i[1] - int(moves / 2))
            if not game.is_occupied(new_loc) and new_loc[0] != 0 and new_loc[0] != 0 and new_loc[0] != game.get_rows() and new_loc[0] != game.get_cols():
                return new_loc
        else:
            new_loc = (i[0], i[1] + moves)
            if not game.is_occupied(new_loc) and new_loc[0] != 0 and new_loc[0] != 0 and new_loc[0] != game.get_rows() and new_loc[0] != game.get_cols():
                return new_loc
            new_loc = (i[0], i[1] - moves)
            if not game.is_occupied(new_loc) and new_loc[0] != 0 and new_loc[0] != 0 and new_loc[0] != game.get_rows() and new_loc[0] != game.get_cols():
                return new_loc
    return False


def check_base(game):##This function returns the 'problems' list which has all of the enemy pirates that are camping on the initial location.
    problems = []
    for i in game.enemy_pirates():
        for j in game.my_pirates_with_treasures():
            if i.location == j.initial_loc:
                problems.append(i)
    return problems


def assign_base_targets(game):
    global locked_pirates
    for i in check_base(game):
        if i not in locked_pirates:
            locked_pirates.append(i)
            return i
    return 0


def assign_orders(game):## This function gives the pirates orders and role
    global go_treasures_ids## There are the treasurers that hunt the coins
    global go_attackers_ids## There are the attackers that are aggressive ships and will hunt the enemy
    distances = []
    pirates = []
    for i in game.all_my_pirates():## The following Code is just to see which ship suits to be attacker or treasurer.
        for j in game.all_enemy_pirates():##Based on the distance between the ship and enemies
            distances.append(game.distance(i.initial_loc, j.initial_loc))
            pirates.append(i)
    min_dis1 = min(distances)
    index = distances.index(min_dis1)
    pirate1 = pirates[index]
    distances.remove(min_dis1)
    min_dis2 = min(distances)
    index = distances.index(min_dis2)
    pirate2 = pirates[index]
    while pirate1 == pirate2:
        min_dis2 = min(distances)
        index = distances.index(min_dis2)
        pirate2 = pirates[index]
    go_attackers_ids.append(pirate1)##The shortest distance between pirates and enemies will be assigned as an attacker
    go_attackers_ids.append(pirate2)
    for i in game.all_my_pirates():## The others will be assigned as treasurers
        if i != pirate1 and i != pirate2:
            go_treasures_ids.append(i)


def print_errors(game, pirate, function, error):## Function That Recieves current pirate being checked , the present function and the error it brought up 
    game.debug(function + " " + str(pirate))
    game.debug(str(error))
