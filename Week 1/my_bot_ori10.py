#Bot 3
turn_left = 6
locked_treasures = []
locked_pirates_with_treasure = []
locked_pirates = []
pirate_not_moved = 4
locked_locations = []
go_def_pirates = []
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
    locked_locations = []
    global go_def_pirates
    go_def_pirates = []
    if game.get_turn() < (game.distance(game.my_pirates()[0].initial_loc, game.enemy_pirates()[0].initial_loc) / (turn_left / 2)):
        pirate_not_moved = 2
    for i in xrange(len(game.my_pirates())):
        #if 4 pirates or more - 2 go_attack and all the others go_treasure
        if len(game.all_my_pirates()) >= 4:
            if len(game.enemy_pirates_with_treasures()) > 1:
                count = 2
                count2 = 0
                if i < 2:
                    if (game.my_pirates()[i].turns_to_sober == 0) and game.my_pirates()[i].reload_turns == 0:
                        for j in xrange(len(game.my_pirates_with_treasures())):
                            go_treasure(game, count)
                            count = count + 1
                            count2 = count2 + 1
                        pirate_not_moved = 1
                        if (go_attack(game, i) != 0):
                            #go_attack(game, i)
                            return
                pirate_not_moved = len(game.my_pirates()) - count2
                if (i < 2):
                    if (game.my_pirates()[i].turns_to_sober == 0):
                        go_attack(game, i)
                elif count == 2:
                    if (game.my_pirates()[i].turns_to_sober == 0):
                        go_treasure(game, i)
                elif count == 3:
                    if (game.my_pirates()[i].turns_to_sober == 0) and i == 3:
                        go_treasure(game, i)
            else:
                if (i < 2):
                    if (game.my_pirates()[i].turns_to_sober == 0):
                        go_attack(game, i)
                else:
                    if (game.my_pirates()[i].turns_to_sober == 0):
                        go_treasure(game, i)
        #if less than 4 pirates - 1 go_attack and all the others go_treasure
        else:
            count = 1
            if len(game.enemy_pirates_with_treasures()) >= 1:
                if i < 1:
                    for j in xrange(len(game.my_pirates_with_treasures())):
                        go_treasure(game, count)
                    pirate_not_moved = 1
                    if (go_attack(game, i) != 0):
                        #go_attack(game, i)
                        return
            if (i < 1):
                go_attack(game, i)
            elif count == 1:
                if (game.my_pirates()[i].turns_to_sober == 0):
                    go_treasure(game, i)

def go_treasure(game, i):
    try:
        global pirate_not_moved
        global turn_left
        # choose your first pirate ship
        game.debug("i = " + str(i))
        pirate = game.my_pirates()[i]
        #if he isn't sober or is lost - give up on this ship for this turn.
        if pirate.is_lost or pirate.turns_to_sober > 0:
            pirate_not_moved = pirate_not_moved - 1
            return
        if not pirate.has_treasure and len(game.treasures()) == 0:
            go_attack(game, i)
        if pirate_not_moved == 0:
            pirate_not_moved = 1
        game.debug("turn_left: " + str(turn_left))
        game.debug("pirate_not_moved: " + str(pirate_not_moved))
        moves = int(turn_left / pirate_not_moved)
        game.debug("moves: " + str(moves))
        treasure = closest_treasure(game, pirate)
        if treasure != 0:
            game.debug("t1: " + str(treasure.id))
        if not pirate.has_treasure and treasure != 0:
            destination = treasure.location
            in_range_enemies = if_enemies_in_range(game, pirate)
            if len(in_range_enemies) != 0 and pirate.reload_turns == 0:
                game.attack(pirate, in_range_enemies[0])
                pirate_not_moved = pirate_not_moved - 1
                turn_left = turn_left - 1
                return
        else:
            moves = 1
            destination = pirate.initial_loc
            in_range_enemies = if_enemies_in_range(game, pirate)
            if len(in_range_enemies) != 0:
                if game.get_defense_reload_turns() == 0:# or game.get_defense_expiration_turns() > 0:
                    game.defend(pirate)
                    return

            #moves = 1
        possible_locations = game.get_sail_options(pirate, destination, moves)
        location = possible_location(game, pirate, destination, moves)
        if location != 0 and location != pirate.location:
            game.set_sail(pirate, location)
            turn_left = turn_left - moves
            pirate_not_moved = pirate_not_moved - 1
            return
        else:
            pirate_not_moved = pirate_not_moved - 1
            return
    except Exception, e:
        print_errors(game, i, "go_treasure", e)

def go_attack(game, i):
    try:
        global pirate_not_moved
        global turn_left
        global go_def_pirates
        pirate = game.my_sober_pirates()[i]
        #if he isn't sober or is lost - give up on this ship for this turn.
        if pirate.is_lost or pirate.turns_to_sober > 0:
            pirate_not_moved = pirate_not_moved - 1
            return
        #if he has a treasure - go_treasure
        if pirate.has_treasure:
            game.debug("go treasure")
            go_treasure(game, i)
            return
        #if there is no sober enemy pirates - go_treasure.
        elif len(game.enemy_sober_pirates()) == 0:
            go_treasure(game, i)
            return
        if len(game.my_pirates_with_treasures()) > 1 and len(game.enemy_pirates_without_treasures()) > 1 and len(game.enemy_pirates_with_treasures()) < 2 and len(go_def_pirates) == 0:
            go_attack_directly(game, i)
            go_def_pirates.append(i)
            #return
        moves = int(turn_left / pirate_not_moved)
        if pirate_not_moved == 1:
            moves = int(turn_left / pirate_not_moved)
        game.debug("pirate: " + str(pirate.id))
        is_with_treasure = False
        game.defend(pirate)

                
        if (len(game.enemy_sober_pirates()) > 0):
            p1 = closest_enemy_with_treasure(game, pirate)
            if p1 != 0:
                pirate_to_attack = p1
                is_with_treasure = True
            else:
                p2 = closest_enemy(game, pirate)
                pirate_to_attack = p2
            if game.in_range(pirate, pirate_to_attack) and pirate.reload_turns == 0:
                game.attack(pirate, pirate_to_attack)
                pirate_not_moved = pirate_not_moved - 1
                turn_left = turn_left - 1
                return
            else:
                if not is_with_treasure:
                    destination = pirate_to_attack.location
                    in_range_enemies = if_enemies_in_range(game, pirate)
                    if len(in_range_enemies) != 0 and pirate.reload_turns == 0:
                        game.attack(pirate, in_range_enemies[0])
                        pirate_not_moved = pirate_not_moved - 1
                        turn_left = turn_left - 1
                        return
                    else:
                        destination = pirate_to_attack.initial_loc
                else:
                    destination = pirate_to_attack.initial_loc

                possible_locations = game.get_sail_options(pirate, destination, moves)
                location = possible_location(game, pirate, destination, moves)
                if (location != 0 and location != pirate.location):
                    game.set_sail(pirate, location)
                    turn_left = turn_left - moves
                    pirate_not_moved = pirate_not_moved - 1
                    return
                else:
                    pirate_not_moved = pirate_not_moved - 1
                    return 0
    except Exception, e:
        print_errors(game, i, "go_attack", e)

def go_attack_directly(game, i):
    try:
        global pirate_not_moved
        global turn_left
        pirate = game.my_sober_pirates()[i]
        #if he isn't sober or is lost - give up on this ship for this turn.
        if pirate.is_lost or pirate.turns_to_sober > 0:
            pirate_not_moved = pirate_not_moved - 1
            return
        #if he has a treasure - go_treasure
        if pirate.has_treasure:
            game.debug("go treasure")
            go_treasure(game, i)
            return
        #if there is no sober enemy pirates - go_treasure.
        elif len(game.enemy_sober_pirates()) == 0:
            go_treasure(game, i)
            return
        moves = int(turn_left / pirate_not_moved)
        if pirate_not_moved == 1:
            moves = int(turn_left / pirate_not_moved)
        game.debug("pirate: " + str(pirate.id))

        is_with_treasure = False
        if (len(game.enemy_sober_pirates()) > 0):
            p2 = closest_enemy(game, pirate)
            pirate_to_attack = p2
            in_range_enemies = if_enemies_in_range(game, pirate)
            if len(in_range_enemies) != 0 and pirate.reload_turns == 0:
                game.attack(pirate, in_range_enemies[0])
                pirate_not_moved = pirate_not_moved - 1
                turn_left = turn_left - 1
                return
            else:
                if not is_with_treasure:
                    destination = pirate_to_attack.location
                else:
                    destination = pirate_to_attack.location

                possible_locations = game.get_sail_options(pirate, destination, moves)
                location = possible_location(game, pirate, destination, moves)
                if (location != 0 and location != pirate.location):
                    game.set_sail(pirate, location)
                    turn_left = turn_left - moves
                    pirate_not_moved = pirate_not_moved - 1
                    return
                else:
                    pirate_not_moved = pirate_not_moved - 1
                    return 0
    except Exception, e:
        print_errors(game, i, "go_attack", e)

def if_enemies_in_range(game, pirate):
    l = []
    for i in game.enemy_sober_pirates():
        if game.in_range(pirate, i):
            l.append(i)
    return l

def closest_enemy(game, pirate):
    global locked_pirates
    if len(game.enemy_sober_pirates()) == 0:
        return 0
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
        return 0
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
            return enemy
        min_dis = min(distances)
        index = distances.index(min_dis)
        enemy = enemies_list[index]
    locked_pirates.append(enemy.id)
    return enemy

def closest_treasure(game, pirate):
    global locked_treasures
    if len(game.treasures()) == 0:
        return 0
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
    return 0

def print_errors(game, pirate, function, error):
    game.debug(function + " " + str(pirate) + " " + str(game.get_turn))
    game.debug(error)
