locked_treasures = []
pirate_not_ordered = []
turns_left = 0
go_attackers_ids = []
go_treasures_ids = []
go_kamikaze_ids = []
go_base_cleaners_ids = []
locked_locations = []
locked_enemies = []
locked_attacking = []
last_roles = {}
is_boosted = False
sent_home = False
previous_locs={}
rushed_to_treasure = False
treasure_boosted = False
#try_attacked = {}
tried_attack={}
last_attacked={}
def do_turn(game):
    global pirate_not_ordered
    global turns_left
    global go_treasures_ids
    global go_attackers_ids
    global go_base_cleaners_ids
    global locked_locations
    global locked_enemies
    global is_boosted
    global sent_home
    global locked_attacking
    global rushed_to_treasure
    global treasure_boosted
    treasure_boosted = False
    rushed_to_treasure = False
    locked_attacking = []
    is_boosted = False
    sent_home = False
    locked_enemies = []
    locked_locations = []
    flag = False
    turns_left = game.get_actions_per_turn()
    pirate_not_ordered = game.my_sober_pirates()
    assign_roles(game)
    attack_p_up_on_map = False
    speed_p_up_on_map = False
    a_p_up = None
    s_p_up = None
    best_treasure = None
    enemy_with_crown = False
    for i in game.enemy_pirates_with_treasures():
        if i.treasure_value > 5:
            enemy_with_crown = True
    if not enemy_with_crown:
        for i in game.treasures():
            if i.value > 3:
                if best_treasure == None:
                    best_treasure = i
                elif best_treasure.value < i.value:
                    best_treasure = i
    if best_treasure != None:
        pirate_to_send = closest_free_pirate_to_powerup(game, best_treasure)
        if pirate_to_send != False:
            do_powerup(game, pirate_to_send, best_treasure, give_boost=True, is_rushing=True)
    for i in game.powerups():
        if i.type == "Attack":
            a_p_up = i
            attack_p_up_on_map = True
        if i.type == "Speed":
            s_p_up = i
            speed_p_up_on_map = True
    if attack_p_up_on_map and a_p_up != None:
        pirate_to_send = closest_free_pirate_to_powerup(game, a_p_up)
        if pirate_to_send != False:
            do_powerup(game, pirate_to_send, a_p_up, give_boost=True)
    elif speed_p_up_on_map and s_p_up != None:
        pirate_to_send = closest_free_pirate_to_powerup(game, s_p_up)
        if pirate_to_send != False:
            do_powerup(game, pirate_to_send, s_p_up, give_boost=True)
    if game.get_actions_per_turn() < len(game.my_pirates()):
        count = 0
        for i in game.my_sober_pirates():
            pirate_not_ordered = [i]
            do_treasure(game, i)
            if not i.has_treasure:
                count += 1
            if count == int(game.get_actions_per_turn() / 4):
                break
    else:
        kamikazes_kamikaze(game)

        attackers_attack(game)
        treasures_treasure(game)

    global previous_locs
    global tried_attack
    global last_attacked
    if game.get_turn()==1:
        for p in game.all_my_pirates():
            tried_attack[p]=False
            last_attacked[p]=None

    if game.get_turn()>=1:
        for p in game.all_my_pirates():
            previous_locs[p]=p.location

    #for i in game.my_sober_pirates():
    #    pirate, treasure = get_board_status(game, i)
    #    if treasure != False:
    #        locations, moves = assign_targets(game, pirate, treasure)
    #        take_action(game, pirate, locations, moves)


def attackers_attack(game):
    game.debug(str(go_attackers_ids) + "attackers_attack function")
    for i in game.my_sober_pirates():
        if i.id in go_attackers_ids:
            do_attack(game, i)


def treasures_treasure(game):
    for i in game.my_sober_pirates():
        if i.id in go_treasures_ids:
            do_treasure(game, i)


def kamikazes_kamikaze(game):
    for i in game.my_sober_pirates():
        if i.id in go_kamikaze_ids:
            do_kamikaze(game, i)


def do_defense(game, pirate):
    for enemy in game.enemy_pirates_without_treasures():
        for treasurerer in game.my_pirates_with_treasures():
            #if game.in_range(enemy.location, treasurerer.initial_loc):
            if enemy.location == treasurerer.initial_loc and enemy not in locked_enemies:
                game.debug("going kamikaze - " + str(pirate.id))
                do_kamikaze(game, pirate, enemy=enemy, give_boost=True)
                return
            #elif enemy not in locked_enemies:
            #    ##do_attack in order to kill the enemy
            #    do_attack(game, pirate, enemy=enemy, give_boost=True)
            #    return
            elif game.in_range(enemy, treasurerer) and enemy not in locked_enemies and enemy.turns_to_sober == 0 and enemy.reload_turns == 0:
                ##do attack in order to kill the enemy
                game.debug("going attack to defense - " + str(pirate.id))
                do_attack(game, pirate, enemy, give_boost=True)
                return
    do_attack(game, pirate)


def do_powerup(game, pirate, power_up, give_boost = False, is_rushing = False):
    global is_boosted
    global sent_home
    pirate = get_attack_board_status(game, pirate)
    if give_boost and not is_boosted:
        is_boosted = True
        for i in game.my_pirates_with_treasures():
            do_treasure(game, i)
        sent_home = True
    if power_up != False:
        locations, moves = assign_kamikaze_targets(game, pirate, power_up)
        game.debug(locations)
        if is_rushing:
            take_rushing_action(game, pirate, locations, moves)
        else:
            take_kamikaze_action(game, pirate, locations, moves)
    else:
        if len(game.treasures()) != 0:
            do_treasure(game, pirate)
            return


def do_kamikaze(game, pirate, enemy = None, give_boost = False):
    if pirate not in pirate_not_ordered:
        return
    global is_boosted
    global sent_home
    pirate = get_attack_board_status(game, pirate)
    if enemy == None:
        enemy = closest_enemy_to_kamikaze(game, pirate)
        if enemy == False:
            enemy = closest_enemy(game, pirate)
        else:
            is_boosted = True
            for i in game.my_pirates_with_treasures():
                do_treasure(game, i)
            sent_home = True
    else:
        locked_enemies.append(enemy)
    if give_boost and not is_boosted:
        is_boosted = True
        for i in game.my_pirates_with_treasures():
            do_treasure(game, i)
        sent_home = True
    if enemy != False:
        locations, moves = assign_kamikaze_targets(game, pirate, enemy)
        game.debug(locations)
        take_kamikaze_action(game, pirate, locations, moves)
    else:
        if len(game.treasures()) != 0:
            do_treasure(game, pirate)
            return


def do_camper(game, pirate, enemy = None, give_boost = False):
    if pirate not in pirate_not_ordered:
        return
    global is_boosted
    global sent_home
    global locked_enemies
    if is_boosted:
        return
    if len(game.treasures()) == 1 and len(game.my_pirates_with_treasures()) == 0 and len(game.enemy_pirates_with_treasures()) == 0:
        return
    pirate = get_attack_board_status(game, pirate)
    if enemy == None:
        enemy = closest_enemy_with_treasure(game, pirate)
        if enemy == False:
            enemy = closest_enemy(game, pirate)
        else:
            is_boosted = True
            for i in game.my_pirates_with_treasures():
                do_treasure(game, i)
            sent_home = True
        if enemy == False:
            do_treasure(game, pirate)
    else:
        locked_enemies.append(enemy)
    if give_boost and not is_boosted:
        is_boosted = True
        for i in game.my_pirates_with_treasures():
            do_treasure(game, i)
        sent_home = True
    game.debug(str(enemy))
    if enemy != False:
        locations, moves = assign_camp_targets(game, pirate, enemy)
        game.debug(locations)
        take_attack_action(game, pirate, locations, moves)
    else:
        if len(game.treasures()) != 0:
            do_treasure(game, pirate)
            return


def do_attack(game, pirate, enemy = None, give_boost = False):
    if pirate not in pirate_not_ordered:
        return
    global is_boosted
    global sent_home
    global locked_enemies
    if is_boosted:
        return
    if len(game.treasures()) == 1 and len(game.my_pirates_with_treasures()) == 0 and len(game.enemy_pirates_with_treasures()) == 0:
        return
    pirate = get_attack_board_status(game, pirate)
    if enemy == None:
        enemy = closest_valuest_enemy(game, pirate)
        if enemy == False:
            enemy = closest_enemy(game, pirate)
        else:
            is_boosted = True
            for i in game.my_pirates_with_treasures():
                do_treasure(game, i)
            sent_home = True
        if enemy == False:
            do_treasure(game, pirate)
    else:
        locked_enemies.append(enemy)
    if give_boost and not is_boosted:
        is_boosted = True
        for i in game.my_pirates_with_treasures():
            do_treasure(game, i)
        sent_home = True
    game.debug(str(enemy))
    if enemy != False:
        locations, moves = assign_attack_targets(game, pirate, enemy)##1
        game.debug(locations)
        take_attack_action(game, pirate, locations, moves)
    else:
        if len(game.treasures()) != 0:
            do_treasure(game, pirate)
            return


def do_treasure(game, pirate):##
    if pirate not in pirate_not_ordered:
        return
    if rushed_to_treasure:
        return
    if sent_home == False:
        pirate = get_treasure_board_status(game, pirate)
        if not pirate.has_treasure:
            treasure = closest_valuest_treasure(game, pirate)
            if len(game.treasures()) == 1 and len(game.enemy_pirates_without_treasures()) != 0 and len(game.enemy_sober_pirates()) != 0 and len(game.all_enemy_pirates()) == 1:
                return
            if len(game.treasures()) == 0 and len(game.my_pirates_with_treasures()) != 0:
                do_defense(game, pirate)
                return
            if (len(game.treasures()) == 1 or len(game.treasures()) == 0) and len(game.enemy_sober_pirates()) != 0 and len(game.my_sober_pirates()) < 2:
                do_attack(game, pirate)
                return
            if treasure != False:
                locations, moves = assign_treasure_targets(game, pirate, treasure)
                game.debug(locations)
                if locations != False:
                    take_treasure_action(game, pirate, locations, moves)
            else:
                do_attack(game, pirate)
                return
        else:
            locations, moves = assign_treasure_targets(game, pirate, pirate.initial_loc)
            game.debug(locations)
            if locations != False:
                take_treasure_action(game, pirate, locations, moves)


def get_treasure_board_status(game, pirate):
    game.debug("pirate: " + str(pirate.id))
    #treasure = closest_treasure(game, pirate)
    #if treasure != False:
    #    game.debug("treasure: " + str(treasure.id))
    return pirate


def get_attack_board_status(game, pirate):
    game.debug("pirate: " + str(pirate.id))
    #enemy = closest_enemy(game, pirate)
    #if enemy != False:
    #    game.debug("enemy: " + str(enemy.id))
    return pirate


def assign_powerup_targets(game, pirate, p_up):
    if turns_left <= 0:
        return False, 0
    if p_up == False:
        return False, 0
    if not pirate.has_treasure:
        if is_boosted:
            moves = int(turns_left)
        else:
            moves = int(turns_left / len(pirate_not_ordered))
        locations = possible_location3(game, pirate, p_up.location, moves)
    else:
        moves = 1
        locations = possible_location(game, pirate, pirate.initial_loc, moves)
    return locations, moves


def assign_treasure_targets(game, pirate, treasure):
    global rushed_to_treasure
    global treasure_boosted
    if turns_left <= 0:
        return False, 0
    if not pirate.has_treasure:

        #else:
        #if treasure_boosted:
        #    return False, 0
        #else:
        #    treasure_boosted = True
        #    moves = int(turns_left)
        moves = int(turns_left / len(pirate_not_ordered))
        #if treasure.value > 1:
        #    moves = turns_left
        if moves == 0 and turns_left > 0:
            moves = 1
        if len(game.treasures()) == 1 and len(game.my_pirates_with_treasures()) == 0 and len(game.enemy_pirates_with_treasures()) == 0:
            rushed_to_treasure = True
            moves = int(turns_left)
        #locations = game.get_sail_options(pirate, treasure.location, moves)
        locations = possible_location(game, pirate, treasure.location, moves)
    else:
        moves = 1
        for i in pirate.powerups:
            if i == "speed" or i == "Speed":
                moves = int(turns_left / len(pirate_not_ordered))
        locations = possible_location(game, pirate, pirate.initial_loc, moves)
    return locations, moves


def assign_camp_targets(game, pirate, enemy):
    if turns_left <= 0:
        return False, 0
    if enemy == False or enemy == None:
        return False, 0
    if pirate.location == enemy.initial_loc:
        return enemy.initial_loc, 0
    if len(pirate.powerups) == 0 and (pirate.reload_turns != 0 or enemy.has_treasure and enemy.defense_expiration_turns > 0):
        if is_boosted:
            moves = int(turns_left)
        else:
            moves = int(turns_left / len(pirate_not_ordered))
        locations = possible_location3(game, pirate, game.get_sail_options(enemy, enemy.initial_loc, 1)[0], moves)
    elif not pirate.has_treasure:
        if is_boosted:
            moves = int(turns_left)
        else:
            moves = int(turns_left / len(pirate_not_ordered))
        if len(pirate.powerups) == 0:
            locations = possible_location_for_attackers(game, pirate, enemy.initial_loc, moves)#possible_location
        else:
            locations = possible_location(game, pirate, enemy.initial_loc, moves)
    else:
        moves = 1
        locations = possible_location(game, pirate, pirate.initial_loc, moves)
    return locations, moves


def assign_attack_targets(game, pirate, enemy):
    global tried_attack
    global last_attacked
    if turns_left <= 0:
        return False, 0
    if enemy == False or enemy == None:
        return False, 0
    if len(pirate.powerups) == 0 and enemy.has_treasure and (pirate.reload_turns != 0 or enemy.defense_expiration_turns > 0):##1
        if tried_attack[pirate]==True and last_attacked[pirate] in game.enemy_sober_pirates():
            if is_boosted:
                moves = int(turns_left)
            else:
                moves = int(turns_left / len(pirate_not_ordered))
            locations = possible_location3(game, pirate, game.get_sail_options(enemy, enemy.initial_loc, 1)[0], moves)
            if game.distance(game.get_sail_options(enemy, enemy.initial_loc, 1)[0],pirate)<=moves:
                tried_attack[pirate]=False
            #last_attacked[pirate]=None
            game.debug(str(tried_attack))
            game.debug(str(last_attacked))
    elif not pirate.has_treasure:
        if is_boosted:
            moves = int(turns_left)
        else:
            moves = int(turns_left / len(pirate_not_ordered))
        if len(pirate.powerups) == 0:
            locations = possible_location_for_attackers(game, pirate, enemy.location, moves)#possible_location
        else:
            locations = possible_location(game, pirate, enemy.location, moves)
    else:
        moves = 1
        locations = possible_location(game, pirate, pirate.initial_loc, moves)
    return locations, moves


def assign_kamikaze_targets(game, pirate, enemy):
    if turns_left <= 0:
        return False, 0
    if enemy == False:
        return False, 0
    if not pirate.has_treasure:
        if is_boosted:
            moves = int(turns_left)
        else:
            moves = int(turns_left / len(pirate_not_ordered))
        locations = possible_location3(game, pirate, enemy.location, moves)
    else:
        moves = 1
        locations = possible_location(game, pirate, pirate.initial_loc, moves)
    return locations, moves


#def assign_powerup_targets(game, pirate, enemy):
#    if turns_left <= 0:
#        return False, 0
#    if enemy == False:
#        return False, 0
#    if not pirate.has_treasure:
#        if is_boosted:
#            moves = int(turns_left)
#        else:
#            moves = int(turns_left / len(pirate_not_ordered))
#        locations = possible_location_for_powerup(game, pirate, enemy.location, moves, enemy)
#    else:
#        moves = 1
#        locations = possible_location(game, pirate, pirate.initial_loc, moves)
#    return locations, moves


def take_action(game, pirate, locations, moves):
    global turns_left
    if try_defend(game, pirate):
        pirate_not_ordered.remove(pirate)
        turns_left -= 1
        return
    if try_attack(game, pirate):
        pirate_not_ordered.remove(pirate)
        turns_left -= 1
        return
    game.set_sail(pirate, locations[0])
    turns_left -= moves
    pirate_not_ordered.remove(pirate)


def take_attack_action(game, pirate, location, moves):
    global turns_left
    global last_roles
    if not pirate.has_treasure:
        if try_attack(game, pirate, attacker=True):
            pirate_not_ordered.remove(pirate)
            turns_left -= 1
            last_roles[pirate.id] = None
            return
    if try_defend(game, pirate):
        pirate_not_ordered.remove(pirate)
        turns_left -= 1
        return
    if location == False:
        return
    game.set_sail(pirate, location)
    turns_left -= moves
    pirate_not_ordered.remove(pirate)
    last_roles[pirate.id] = "attacking"


def take_treasure_action(game, pirate, location, moves):
    global turns_left
    global last_roles
    if try_defend(game, pirate):
        pirate_not_ordered.remove(pirate)
        turns_left -= 1
        return
    if not pirate.has_treasure:
        if try_attack(game, pirate):
            pirate_not_ordered.remove(pirate)
            turns_left -= 1
            return
    game.set_sail(pirate, location)
    turns_left -= moves
    pirate_not_ordered.remove(pirate)
    if location == pirate.initial_loc:
        last_roles[pirate.id] = None
    else:
        last_roles[pirate.id] = "treasuring"


def take_rushing_action(game, pirate, location, moves):
    global turns_left
    global last_roles
    if try_defend(game, pirate):
        pirate_not_ordered.remove(pirate)
        turns_left -= 1
        return
    if location == False:
        return
    game.set_sail(pirate, location)
    turns_left -= moves
    pirate_not_ordered.remove(pirate)
    last_roles[pirate.id] = "attacking"


def take_kamikaze_action(game, pirate, location, moves):
    global turns_left
    global last_roles
    if not pirate.has_treasure:
        if try_attack(game, pirate):
            pirate_not_ordered.remove(pirate)
            turns_left -= 1
            last_roles[pirate.id] = None
            return
    if try_defend(game, pirate):
        pirate_not_ordered.remove(pirate)
        turns_left -= 1
        return
    if location == False:
        return
    game.set_sail(pirate, location)
    turns_left -= moves
    pirate_not_ordered.remove(pirate)
    last_roles[pirate.id] = "attacking"


def try_defend(game, pirate):
    for enemy in game.enemy_sober_pirates():
        if game.in_range(pirate, enemy) and pirate.defense_reload_turns == 0 and enemy.reload_turns == 0 and not enemy.has_treasure:
            game.defend(pirate)
            return True
    return False


def try_attack(game, pirate, treasurer = False, attacker = False):
    global locked_attacking
    global tried_attack
    global last_attacked
    if not treasurer:
        for enemy in game.enemy_sober_pirates():
            if game.in_range(pirate, enemy) and pirate.reload_turns == 0 and enemy not in locked_attacking: #and enemy.defense_reload_turns > 0 and not enemy.defense_expiration_turns > 0:
                game.attack(pirate, enemy)
                locked_attacking.append(enemy)
                tried_attack[pirate]=True
                last_attacked[pirate]=enemy
                #try_attacked[pirate] = True
                return True
    else:
        for enemy in game.enemy_sober_pirates():
            if game.in_range(pirate, enemy) and pirate.reload_turns == 0 and enemy not in locked_attacking and (enemy.reload_turns == 0 or enemy.has_treasure): #and enemy.defense_reload_turns > 0 and not enemy.defense_expiration_turns > 0:
                game.attack(pirate, enemy)
                locked_attacking.append(enemy)
                tried_attack[pirate]=True
                last_attacked[pirate]=enemy
                return True

    return False


def closest_free_pirate_to_powerup(game, powerup):
    closest = None
    if len(game.my_sober_pirates()) == 0:
        return False
    else:
        for i in game.my_sober_pirates():
            if closest == None:
                if not i.has_treasure:
                    closest = i
                    continue
            elif game.distance(i, powerup.location) < game.distance(i, powerup.location) and not i.has_treasure:
                closest = i
    if closest == None:
        return False
    return closest


def closest_safe_treasure(game, pirate):
    closest = None
    if len(game.treasures()) == 0:
        return False
    else:
        for i in game.treasures():
            if closest == None:
                if i not in locked_treasures:
                    closest = i
                    continue
            elif game.distance(pirate, i) < game.distance(pirate, closest) and i not in locked_treasures and len(dangerous_enemies_in_range(game, i)) == 0:
                closest = i
    if closest == None:
        return farest_treasure(game, 1)
    locked_treasures.append(closest)
    return closest


def closest_valuest_treasure(game, pirate):
    closest = None
    if len(game.treasures()) == 0:
        return False
    else:
        for i in game.treasures():
            if closest == None:
                if i not in locked_treasures:
                    closest = i
                    continue
            elif i.value > closest.value:
                closest = i
            elif game.distance(pirate, i) < game.distance(pirate, closest) and i not in locked_treasures and len(dangerous_enemies_in_range(game, i)) == 0:
                closest = i
    if closest == None:
        return farest_treasure(game, 1)
    locked_treasures.append(closest)
    return closest


def closest_enemy_to_kamikaze(game, pirate):
    init_locs = get_my_initial_locs(game)
    global locked_enemies
    closest = None
    if len(game.enemy_pirates()) == 0:
        return False
    else:
        for i in game.enemy_pirates():
            if closest == None:
                if i.location in init_locs:
                    closest = i
                    continue
            elif game.distance(pirate, i) < game.distance(pirate, closest) and i not in locked_enemies:
                if i.location in init_locs:
                    closest = i
    if closest == None:
        return False
    locked_enemies.append(closest)
    return closest


def farest_treasure(game, pirate):
    farest = None
    if len(game.treasures()) == 0:
        return False
    else:
        for i in game.treasures():
            if farest == None:
                if i not in locked_treasures:
                    closest = i
                    continue
            elif game.distance(pirate, i) > game.distance(pirate, farest) and i not in locked_treasures:
                closest = i
    if farest == None:
        return False
    locked_treasures.append(farest)
    return farest


def get_my_initial_locs(game):
    init_locs = []
    for i in game.all_my_pirates():
        init_locs.append(i.initial_loc)
    return init_locs


def closest_treasure(game, pirate):
    closest = None
    if len(game.treasures()) == 0:
        return False
    else:
        for i in game.treasures():
            if closest == None:
                if i not in locked_treasures:
                    closest = i
                    continue
            elif game.distance(pirate, i) < game.distance(pirate, closest) and i not in locked_treasures:
                closest = i
    if closest == None:
        return False
    locked_treasures.append(closest)
    return closest


def dangerous_enemies_in_range(game, pirate):
    l = []
    for i in game.enemy_sober_pirates():
        if game.in_range(i, pirate) and i.reload_turns == 0 and not i.has_treasure:
            l.append(i)
    return l


def enemies_in_range(game, pirate):
    l = []
    for i in game.enemy_sober_pirates():
        if game.in_range(i, pirate):
            l.append(i)
    return l


def closest_enemy(game, pirate):
    global locked_enemies
    closest = None
    if len(game.enemy_pirates()) == 0:
        return False
    else:
        for i in game.enemy_sober_pirates():
            if closest == None:
                closest = i
                continue
            if game.distance(pirate, i) < game.distance(pirate, closest) and i not in locked_enemies:
                closest = i
    locked_enemies.append(closest)
    return closest


def closest_enemy_with_treasure(game, pirate):
    global locked_enemies
    closest = None
    if len(game.enemy_pirates_with_treasures()) == 0:
        return False
    else:
        for i in game.enemy_pirates_with_treasures():
            if closest == None:
                closest = i
                continue
            if game.distance(pirate, i) < game.distance(pirate, closest) and i not in locked_enemies:
                closest = i
    locked_enemies.append(closest)
    return closest


def closest_valuest_enemy(game, pirate):
    global locked_enemies
    closest = None
    if len(game.enemy_pirates_with_treasures()) == 0:
        return False
    else:
        for i in game.enemy_pirates_with_treasures():
            if closest == None:
                closest = i
                continue
            if (game.distance(pirate, i) < game.distance(pirate, closest) or i.treasure_value > closest.treasure_value) and i not in locked_enemies:
                closest = i
    locked_enemies.append(closest)
    return closest


def assign_roles(game, sum=None):
    global go_attackers_ids
    global go_treasures_ids
    global go_base_cleaners_ids
    global last_roles
    global go_kamikaze_ids
    go_kamikaze_ids = []
    for i in game.all_my_pirates():
        if i.is_lost:
            last_roles[i.id] = None
    if sum == None:
        sum = len(game.all_my_pirates())
    else:
        sum = sum * 2
    distances = []
    pirates = []
    init_locs = get_my_initial_locs(game)
    for i in game.my_pirates_without_treasures():
        for j in game.enemy_pirates():
            if j.location in init_locs:
                distances.append(game.distance(i.location, j.location))
                pirates.append(i)
    if len(distances) != 0:
        min_dis1 = min(distances)
        index = distances.index(min_dis1)
        pirate1 = pirates[index]
        while len(go_kamikaze_ids) < 1:
            #if (pirate1.id not in last_roles.keys() or last_roles[pirate1.id] == "attacking" or last_roles[pirate1.id] == None) and pirate1.id not in go_attackers_ids and pirate1.reload_turns == 0 and not pirate1.has_treasure:
            if pirate1.id not in go_kamikaze_ids and not pirate1.has_treasure:
                go_kamikaze_ids.append(pirate1.id)
            #if pirate1.id not in go_attackers_ids and not pirate1.has_treasure and len(enemies_in_range(game, pirate1)) > 0:
            #    go_attackers_ids.append(pirate1.id)
            if not len(distances) == 0:
                distances.remove(min_dis1)
                pirates.remove(pirate1)
                if not len(distances) == 0:
                    min_dis1 = min(distances)
                    index = distances.index(min_dis1)
                    pirate1 = pirates[index]
            else:
                break
    last_go_attackers = go_attackers_ids
    go_treasures_ids = []
    go_attackers_ids = []
    #for i in last_go_attackers:
    #    for j in game.my_sober_pirates():
    #        if j.id == i:
    #            for k in game.enemy_pirates_with_treasures():
    #                if j.reload_turns > 0 and game.in_range(j, k) and j.id not in go_attackers_ids:
    #                    go_attackers_ids.append(j.id)
#
    distances = []
    pirates = []
    for i in game.my_pirates_without_treasures():
        for j in game.enemy_pirates():
            distances.append(game.distance(i.location, j.location))
            pirates.append(i)
    if len(distances) != 0:
        min_dis1 = min(distances)
        index = distances.index(min_dis1)
        pirate1 = pirates[index]
        while len(go_attackers_ids) + len(go_kamikaze_ids) < int(sum / 2):
            #if (pirate1.id not in last_roles.keys() or last_roles[pirate1.id] == "attacking" or last_roles[pirate1.id] == None) and pirate1.id not in go_attackers_ids and pirate1.reload_turns == 0 and not pirate1.has_treasure:
            if pirate1.id not in go_attackers_ids and not pirate1.has_treasure and (pirate1.reload_turns == 0 or tried_attack[pirate1]==True and last_attacked[pirate1] in game.enemy_sober_pirates()):
                go_attackers_ids.append(pirate1.id)
            #for k in game.all_enemy_pirates():
            #    if game.in_range(pirate1.initial_loc, k.initial_loc):
            #        if pirate1.id not in go_attackers_ids:
            #            go_attackers_ids.append(pirate1.id)
            #if pirate1.id not in go_attackers_ids and not pirate1.has_treasure and len(enemies_in_range(game, pirate1)) > 0:
            #    go_attackers_ids.append(pirate1.id)
            if not len(distances) == 0:
                distances.remove(min_dis1)
                pirates.remove(pirate1)
                if not len(distances) == 0:
                    min_dis1 = min(distances)
                    index = distances.index(min_dis1)
                    pirate1 = pirates[index]
            else:
                break
    for i in game.my_pirates():
        if i.id not in go_attackers_ids:
            go_treasures_ids.append(i.id)
    return


def possible_location3(game, pirate, destination, moves):
    global locked_locations
    possible_locations = game.get_sail_options(pirate, destination, moves)
    game.debug(possible_locations)
    for i in possible_locations:
        if i not in locked_locations:
            locked_locations.append(i)
            return i
    return False


def possible_location_for_attackers(game, pirate, destination, moves):
    global locked_locations
    possible_locations = game.get_sail_options(pirate, destination, moves)
    game.debug(possible_locations)
    for i in possible_locations:
        is_occupied_by_us = False
        for j in game.my_pirates():
            if j.location == i:
                is_occupied_by_us = True
        if not is_occupied_by_us and i not in locked_locations:
            locked_locations.append(i)
            return i
    return False


def another_treasure_in_location(game, location, treasure):
    for i in game.treasures():
        if i.location == location and i != treasure:
            return True
    return False


def possible_location2(game, pirate, destination, moves):## We get in here in case if no good destination was chosen for some reason ... ?
    global locked_locations
    global turn_left
    possible_locations = game.get_sail_options(pirate, destination, moves)## Get all of the possible locations , again..
    for i in possible_locations:
        if i not in locked_locations:
            if not game.is_occupied(i) and len(dangerous_enemies_in_range(game, i)) <= 2:
                locked_locations.append(i)
                return i
    i = pirate.location
    if pirate.initial_loc[0] < int(game.get_rows() / 2):
        if moves > 1:
            new_loc = (i[0] - int(moves / 2), i[1])
            if not game.is_occupied(new_loc) and new_loc[0] != 0 and new_loc[0] != 0 and new_loc[0] != game.get_rows() and new_loc[0] != game.get_cols() and not new_loc in locked_locations:
                locked_locations.append(new_loc)
                return new_loc
            new_loc = (i[0] + int(moves / 2), i[1])
            if not game.is_occupied(new_loc) and new_loc[0] != 0 and new_loc[0] != 0 and new_loc[0] != game.get_rows() and new_loc[0] != game.get_cols() and not new_loc in locked_locations:
                locked_locations.append(new_loc)
                return new_loc
        else:
            new_loc = (i[0] - moves, i[1])
            if not game.is_occupied(new_loc) and new_loc[0] != 0 and new_loc[0] != 0 and new_loc[0] != game.get_rows() and new_loc[0] != game.get_cols() and not new_loc in locked_locations:
                locked_locations.append(new_loc)
                return new_loc
            new_loc = (i[0] + moves, i[1])
            if not game.is_occupied(new_loc) and new_loc[0] != 0 and new_loc[0] != 0 and new_loc[0] != game.get_rows() and new_loc[0] != game.get_cols() and not new_loc in locked_locations:
                locked_locations.append(new_loc)
                return new_loc
    else:
        if moves > 1:
            new_loc = (i[0] + int(moves / 2), i[1])
            if not game.is_occupied(new_loc) and new_loc[0] != 0 and new_loc[0] != 0 and new_loc[0] != game.get_rows() and new_loc[0] != game.get_cols() and not new_loc in locked_locations:
                locked_locations.append(new_loc)
                return new_loc
            new_loc = (i[0] - int(moves / 2), i[1])
            if not game.is_occupied(new_loc) and new_loc[0] != 0 and new_loc[0] != 0 and new_loc[0] != game.get_rows() and new_loc[0] != game.get_cols() and not new_loc in locked_locations:
                locked_locations.append(new_loc)
                return new_loc
        else:
            new_loc = (i[0] + moves, i[1])
            if not game.is_occupied(new_loc) and new_loc[0] != 0 and new_loc[0] != 0 and new_loc[0] != game.get_rows() and new_loc[0] != game.get_cols() and not new_loc in locked_locations:
                locked_locations.append(new_loc)
                return new_loc
            new_loc = (i[0] - moves, i[1])
            if not game.is_occupied(new_loc) and new_loc[0] != 0 and new_loc[0] != 0 and new_loc[0] != game.get_rows() and new_loc[0] != game.get_cols() and not new_loc in locked_locations:
                locked_locations.append(new_loc)
                return new_loc
    if pirate.initial_loc[1] < int(game.get_cols() / 2):
        if moves > 1:
            new_loc = (i[0], i[1] - int(moves / 2))
            if not game.is_occupied(new_loc) and new_loc[0] != 0 and new_loc[0] != 0 and new_loc[0] != game.get_rows() and new_loc[0] != game.get_cols() and not new_loc in locked_locations:
                locked_locations.append(new_loc)
                return new_loc
            new_loc = (i[0], i[1] + int(moves / 2))
            if not game.is_occupied(new_loc) and new_loc[0] != 0 and new_loc[0] != 0 and new_loc[0] != game.get_rows() and new_loc[0] != game.get_cols() and not new_loc in locked_locations:
                locked_locations.append(new_loc)
                return new_loc
        else:
            new_loc = (i[0], i[1] - moves)
            if not game.is_occupied(new_loc) and new_loc[0] != 0 and new_loc[0] != 0 and new_loc[0] != game.get_rows() and new_loc[0] != game.get_cols() and not new_loc in locked_locations:
                locked_locations.append(new_loc)
                return new_loc
            new_loc = (i[0], i[1] + moves)
            if not game.is_occupied(new_loc) and new_loc[0] != 0 and new_loc[0] != 0 and new_loc[0] != game.get_rows() and new_loc[0] != game.get_cols() and not new_loc in locked_locations:
                locked_locations.append(new_loc)
                return new_loc
    else:
        if moves > 1:
            new_loc = (i[0], i[1] + int(moves / 2))
            if not game.is_occupied(new_loc) and new_loc[0] != 0 and new_loc[0] != 0 and new_loc[0] != game.get_rows() and new_loc[0] != game.get_cols() and not new_loc in locked_locations:
                locked_locations.append(new_loc)
                return new_loc
            new_loc = (i[0], i[1] - int(moves / 2))
            if not game.is_occupied(new_loc) and new_loc[0] != 0 and new_loc[0] != 0 and new_loc[0] != game.get_rows() and new_loc[0] != game.get_cols() and not new_loc in locked_locations:
                locked_locations.append(new_loc)
                return new_loc
        else:
            new_loc = (i[0], i[1] + moves)
            if not game.is_occupied(new_loc) and new_loc[0] != 0 and new_loc[0] != 0 and new_loc[0] != game.get_rows() and new_loc[0] != game.get_cols() and not new_loc in locked_locations:
                locked_locations.append(new_loc)
                return new_loc
            new_loc = (i[0], i[1] - moves)
            if not game.is_occupied(new_loc) and new_loc[0] != 0 and new_loc[0] != 0 and new_loc[0] != game.get_rows() and new_loc[0] != game.get_cols() and not new_loc in locked_locations:
                locked_locations.append(new_loc)
                return new_loc
    return False


def possible_location_for_powerup(game, pirate, destination, moves, powerup):
    global locked_locations
    possible_locations = game.get_sail_options(pirate, destination, moves)
    game.debug("possible locations:  "+str(pirate.id)+ " DESTINATION " + str(destination))
    game.debug(possible_locations)
    couldbe,danger=Danger_protocolv2(game,pirate,moves)
    temp=list(possible_locations)
    safe_paths=[]## doesnt appear in couldbe or danger
    maybe_safe=[]## appears only in couldbe
    death=[] ## appears only on danger
    for t in temp:
        if t not in danger:
            if t not in couldbe:
                safe_paths.append(t)
            else:
                maybe_safe.append(t)
        else:
            death.append(t)
    #if len(safe_paths)>0:
    #    possible_locations=list(safe_paths)
    #elif len(maybe_safe)>0:
    #    possible_locations=list(maybe_safe)
    #elif len(death)>0:
    #    possible_locations=list(death)
        ## if we have to die then why not just stand in place and let someone else take a turn
    ## possible_locations must have the most short safe paths right now available to the pirate
    #if pirate.initial_loc in death:
    #    return False
    global previous_locs
    for i in list(safe_paths):
        if not game.is_occupied(i) and i not in locked_locations and i !=previous_locs.get(pirate):
            if not another_treasure_in_location(game, i, powerup):
                locked_locations.append(i)
                return i
    for i in list(maybe_safe):
        if not game.is_occupied(i) and i not in locked_locations and i !=previous_locs.get(pirate):
            if not another_treasure_in_location(game, i, powerup):
                locked_locations.append(i)
                return i
    for i in list(death):
        if not game.is_occupied(i) and i not in locked_locations and i !=previous_locs.get(pirate):
            if not another_treasure_in_location(game, i, powerup):
                locked_locations.append(i)
                return i
    game.debug("I am fucked a up pirate ship  "+ str(pirate.id))
    game.debug("locked_locations=")
    game.debug(str(locked_locations))
    game.debug("possible_locations=")
    game.debug(str(possible_locations))
    if len(possible_locations)==0:
        return False#return possible_location2(game,pirate,destination,moves)# False
    return possible_location35(game,possible_locations,pirate,moves,destination)


def possible_location(game, pirate, destination, moves):
    global locked_locations
    possible_locations = game.get_sail_options(pirate, destination, moves)
    game.debug("possible locations:  "+str(pirate.id)+ " DESTINATION " + str(destination))
    game.debug(possible_locations)
    couldbe,danger=Danger_protocolv2(game,pirate,moves)
    temp=list(possible_locations)
    safe_paths=[]## doesnt appear in couldbe or danger
    maybe_safe=[]## appears only in couldbe
    death=[] ## appears only on danger
    for t in temp:
        if t not in danger:
            if t not in couldbe:
                safe_paths.append(t)
            else:
                maybe_safe.append(t)
        else:
            death.append(t)
    #if len(safe_paths)>0:
    #    possible_locations=list(safe_paths)
    #elif len(maybe_safe)>0:
    #    possible_locations=list(maybe_safe)
    #elif len(death)>0:
    #    possible_locations=list(death)
        ## if we have to die then why not just stand in place and let someone else take a turn
    ## possible_locations must have the most short safe paths right now available to the pirate
    #if pirate.initial_loc in death:
    #    return False
    global previous_locs
    for i in list(safe_paths):
        if not game.is_occupied(i) and i not in locked_locations and i !=previous_locs.get(pirate):

            locked_locations.append(i)
            return i
    for i in list(maybe_safe):
        if not game.is_occupied(i) and i not in locked_locations and i !=previous_locs.get(pirate):
            locked_locations.append(i)
            return i
    for i in list(death):
        if not game.is_occupied(i) and i not in locked_locations and i !=previous_locs.get(pirate):
            locked_locations.append(i)
            return i
    game.debug("I am fucked a up pirate ship  "+ str(pirate.id))
    game.debug("locked_locations=")
    game.debug(str(locked_locations))
    game.debug("possible_locations=")
    game.debug(str(possible_locations))
    if len(possible_locations)==0:
        return False#return possible_location2(game,pirate,destination,moves)# False
    return possible_location35(game,possible_locations,pirate,moves,destination)
def possible_location35(game,possible_locations,pirate,moves,destination):
    global locked_locations
    max_dist=0
    farest_p=()
    spooky_pirates=dangerous_enemies_in_range(game,pirate)
    poss=[]
    for p in possible_locations:
        if p not in locked_locations and not game.is_occupied(p):
            poss.append(p)

    if len(poss)==0:
        new_poss=Get_all_possible_tiles(game,pirate,moves)
        game.debug("This function causes a bug !!!!")
        game.debug("NEW POSS ="+str(new_poss))
        global previous_locs
        game.debug(previous_locs)
        for po in new_poss:
            if po not in locked_locations and not game.is_occupied(po):
                    if po !=previous_locs.get(pirate):
                        game.debug(po)
                        poss.append(po)
        game.debug ("POSS ="+str(poss))
    possible_locations=list(poss)
    dist=[]
    for p in possible_locations:
        dist.append(game.distance(p,destination))
    for i in xrange(len(dist)):
        min_dist=min(dist)
        ind=dist.index(min_dist)
        if not possible_locations[ind] in locked_locations:
            locked_locations.append(possible_locations[ind])
            return possible_locations[ind]
        dist.remove(min_dist)
    return False
    #for p in possible_locations:
    #    for spook in spooky_pirates:
    #        dist=game.distance(p,spook)
    #        if dist>max_dist:
    #            max_dist=dist
    #            farest_p=p
    #global previous_locs
    #for p in game.all_my_pirates():
    #    previous_locs.append[p.location]
    #game.debug(previous_locs)

    #return farest_p


def Danger_protocolv2(game,pirate_to_check,moves):
    obviously_dangereous=[]
    could_be_dangereous=[]
    enemy_pirates=game.enemy_sober_pirates()
    if len(enemy_pirates)==0:
        enemy_pirates=game.all_enemy_pirates()
    enemy_moves=game.get_actions_per_turn()
    ## Lets check the dangereous paths first now , shall we ?

    for enemy in enemy_pirates:
        if game.in_range(pirate_to_check,enemy): ## if no one moves at all and they have a clear shot at us.
            obviously_dangereous.append(pirate_to_check.location)
            break
    for enemy in enemy_pirates:
        possible_enemy_tiles=game.get_sail_options(enemy,pirate_to_check,enemy_moves)
        for x in possible_enemy_tiles:
            if game.in_range(pirate_to_check,x) or x==pirate_to_check.location: ## if they move and we dont,  will they reach us with the barrels or even crash at us.
                obviously_dangereous.append(pirate_to_check.location)
                break
    for enemy in enemy_pirates:
        possible_pirate_tiles=game.get_sail_options(pirate_to_check,enemy,moves)
        for x in possible_pirate_tiles:
            if game.in_range(enemy,x) or x==enemy.location:## If we move and they dont , will we reach them with barrels or even crush on them.
                obviously_dangereous.append(x)

    ## Finished Dangereous paths
    ## Lets do the Could be dangereous paths now.
    for enemy in enemy_pirates:
        possible_enemy_tiles=game.get_sail_options(enemy,pirate_to_check,enemy_moves)
        possible_pirate_tiles=game.get_sail_options(pirate_to_check,enemy,moves)
        for x in possible_enemy_tiles:
            if x in possible_pirate_tiles:
                could_be_dangereous.append(x)## Will be a crash,same location
            for k in possible_pirate_tiles:
                if game.in_range(k,x): ## will be in shooting range
                    could_be_dangereous.append(k)
    obviously_dangereous=MakeSetThenList(obviously_dangereous)
    could_be_dangereous=MakeSetThenList(could_be_dangereous)
    return could_be_dangereous,obviously_dangereous
#################################################################################################################################################################################
def MakeSetThenList(lis1):
    lis1_set=set(lis1)
    lis1=list(lis1_set)
    return lis1
def Get_all_possible_tiles(game,pirate,moves):
    possible_tiles=[]
    loc=pirate.location
    xloc=loc[0]
    yloc=loc[1]
    for action in xrange(moves):
        action+=1
        xlocnew=xloc+action
        possible_tiles.append((xlocnew,yloc))
        if action<moves:
            actions_left=moves-action
            tempx=xlocnew
            tempy=yloc
            for act in xrange(actions_left):
                xloctemp=xlocnew+act
                possible_tiles.append((xloctemp,tempy))
                xloctemp=xlocnew-act
                possible_tiles.append((xloctemp,tempy))
                yloctemp=yloc+act
                possible_tiles.append((tempx,yloctemp))
                yloctemp=yloc-act
                possible_tiles.append((tempx,yloctemp))

        xlocnew=xloc-action
        possible_tiles.append((xlocnew,yloc))
        if action<moves:
            actions_left=moves-action
            tempx=xlocnew
            tempy=yloc
            for act in xrange(actions_left):
                xloctemp=xlocnew+act
                possible_tiles.append((xloctemp,tempy))
                xloctemp=xlocnew-act
                possible_tiles.append((xloctemp,tempy))
                yloctemp=yloc+act
                possible_tiles.append((tempx,yloctemp))
                yloctemp=yloc-act
                possible_tiles.append((tempx,yloctemp))


        ylocnew=yloc+action
        possible_tiles.append((xloc,ylocnew))
        if action<moves:
            actions_left=moves-action
            tempx=xloc
            tempy=ylocnew
            for act in xrange(actions_left):
                xloctemp=xlocnew+act
                possible_tiles.append((xloctemp,tempy))
                xloctemp=xlocnew-act
                possible_tiles.append((xloctemp,tempy))
                yloctemp=yloc+act
                possible_tiles.append((tempx,yloctemp))
                yloctemp=yloc-act
                possible_tiles.append((tempx,yloctemp))


        ylocnew=yloc-action
        possible_tiles.append((xloc,ylocnew))
        if action<moves:
            actions_left=moves-action
            tempx=xloc
            tempy=ylocnew
            for act in xrange(actions_left):
                xloctemp=xlocnew+act
                possible_tiles.append((xloctemp,tempy))
                xloctemp=xlocnew-act
                possible_tiles.append((xloctemp,tempy))
                yloctemp=yloc+act
                possible_tiles.append((tempx,yloctemp))
                yloctemp=yloc-act
                possible_tiles.append((tempx,yloctemp))
    possible_tiles=MakeSetThenList(possible_tiles)
    fixed_possible_tiles=[]
    for tile in possible_tiles:
        x=tile[0]
        y=tile[1]
        if x>=0 and x<=game.get_rows() and y>=0 and y<=game.get_cols():
            fixed_possible_tiles.append(tile)
    return fixed_possible_tiles