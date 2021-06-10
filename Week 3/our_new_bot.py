locked_treasures = []
pirate_not_ordered = []
turns_left = 0
go_attackers_ids = []
go_treasures_ids = []
go_campers_ids = []
locked_locations = []
locked_enemies = []
last_roles = {}
is_boosted = False
sent_home = False

def do_turn(game):
    global pirate_not_ordered
    global turns_left
    global go_treasures_ids
    global go_attackers_ids
    global locked_locations
    global locked_enemies
    global is_boosted
    global sent_home
    is_boosted = False
    sent_home = False
    locked_enemies = []
    locked_locations = []
    turns_left = game.get_actions_per_turn()
    pirate_not_ordered = game.my_sober_pirates()
    assign_roles(game)
    attackers_attack(game)
    treasures_treasure(game)
    #for i in game.my_sober_pirates():
    #    pirate, treasure = get_board_status(game, i)
    #    if treasure != False:
    #        locations, moves = assign_targets(game, pirate, treasure)
    #        take_action(game, pirate, locations, moves)


def attackers_attack(game):
    game.debug(str(go_attackers_ids))
    for i in game.my_sober_pirates():
        if i.id in go_attackers_ids:
            do_attack(game, i)


def treasures_treasure(game):
    for i in game.my_sober_pirates():
        if i.id in go_treasures_ids:
            do_treasure(game, i)


def do_attack(game, pirate):
    global is_boosted
    global sent_home
    pirate = get_attack_board_status(game, pirate)
    enemy = closest_enemy_with_treasure(game, pirate)
    if enemy == False:
        enemy = closest_enemy(game, pirate)
    #else:
    #    for i in game.enemy_pirates_with_treasures():
    #        do_treasure(game, i)
    #    sent_home = True
    #    is_boosted = True
    #    locations, moves = assign_attack_targets(game, pirate, enemy)
    #    game.debug(locations)
    #    if locations != False:
    #        take_attack_action(game, pirate, locations, moves)
    #        return
    #    else:
    #        is_boosted = False
    #        return
    if enemy != False:
        locations, moves = assign_attack_targets(game, pirate, enemy)#1
        game.debug(locations)
        if locations != False:
            take_attack_action(game, pirate, locations, moves)
    else:
        if len(game.treasures()) != 0:
            do_treasure(game, pirate)
            return


def do_treasure(game, pirate):
    pirate = get_treasure_board_status(game, pirate)
    if not pirate.has_treasure:
        treasure = closest_safe_treasure(game, pirate)
        if len(game.treasures()) == 1 and len(game.enemy_pirates_without_treasures) != 0:
            return
        if len(game.treasures()) == 1 or len(game.treasures()) == 0:
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


def assign_treasure_targets(game, pirate, treasure):
    if not pirate.has_treasure:
        moves = int(turns_left / len(pirate_not_ordered))
        #locations = game.get_sail_options(pirate, treasure.location, moves)
        locations = possible_location(game, pirate, treasure.location, moves)
    else:
        moves = 1
        locations = possible_location(game, pirate, pirate.initial_loc, moves)
    return locations, moves


def assign_attack_targets(game, pirate, enemy):
    if not pirate.has_treasure:
        if is_boosted:
            moves = int(turns_left)
        else:
            moves = int(turns_left / len(pirate_not_ordered))
        locations = possible_location_for_attackers(game, pirate, enemy.location, moves)
    else:
        moves = 1
        locations = possible_location(game, pirate, pirate.initial_loc, moves)
    return locations, moves


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
        if try_attack(game, pirate):
            pirate_not_ordered.remove(pirate)
            turns_left -= 1
            last_roles[pirate.id] = None
            return
    if try_defend(game, pirate):
        pirate_not_ordered.remove(pirate)
        turns_left -= 1
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


def try_defend(game, pirate):
    for enemy in game.enemy_sober_pirates():
        if game.in_range(pirate, enemy) and pirate.defense_reload_turns == 0 and enemy.reload_turns == 0:
            game.defend(pirate)
            return True
    return False


def try_attack(game, pirate):
    for enemy in game.enemy_sober_pirates():
        if game.in_range(pirate, enemy) and pirate.reload_turns == 0:
            game.attack(pirate, enemy)
            return True
    return False


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


def assign_roles(game):
    global go_attackers_ids
    global go_treasures_ids
    global go_campers_ids
    global last_roles
    for i in game.all_my_pirates():
        if i.is_lost:
            last_roles[i.id] = None
    go_treasures_ids = []
    go_attackers_ids = []
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
        while len(go_attackers_ids) < int(len(game.all_my_pirates()) / 2):
            if (pirate1.id not in last_roles.keys() or last_roles[pirate1.id] == "attacking" or last_roles[pirate1.id] == None) and pirate1.id not in go_attackers_ids and pirate1.reload_turns == 0 and not pirate1.has_treasure:
                go_attackers_ids.append(pirate1.id)
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
        if i.id not in go_attackers_ids and i.id not in go_campers_ids:
            go_treasures_ids.append(i.id)
    return


def possible_location(game, pirate, destination, moves):
    global locked_locations
    possible_locations = game.get_sail_options(pirate, destination, moves)
    game.debug("possible locations:")
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
    if len(safe_paths)>0:
        possible_locations=list(safe_paths)
    elif len(maybe_safe)>0:
        possible_locations=list(maybe_safe)
    elif len(death)>0:
        possible_locations=list(death)
        ## if we have to die then why not just stand in place and let someone else take a turn
    ## possible_locations must have the most short safe paths right now available to the pirate
    for i in possible_locations:
        if not game.is_occupied(i) and i not in locked_locations:
            locked_locations.append(i)
            return i
    game.debug("I am fucked up pirate ship"+ str(pirate.id))
    game.debug("locked_locations=")
    game.debug(str(locked_locations))
    game.debug("possible_locations=")
    game.debug(str(possible_locations))
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
#################################################################################################################################################################################
def Danger_protocolv2(game,pirate_to_check,moves):
    obviously_dangereous=[]
    could_be_dangereous=[]
    enemy_pirates=game.enemy_sober_pirates()
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
def Danger_protocol(game,pirate_to_check,moves):
    safe_paths=[]
    obviously_dangereous=[]
    could_be_dangereous=[]
    enemy_pirates=game.enemy_sober_pirates()
    for enemy in enemy_pirates:## If we stand in the place and the enemy is incoming
        if game.in_range(pirate_to_check,enemy):
            obviously_dangereous.append(pirate_to_check.location)
            break


    possible_enemy_tiles=[]
    for enemy in enemy_pirates:
        possible_enemy_tiles+=Get_all_possible_tiles(game,enemy,game.get_actions_per_turn())

    possible_enemy_tiles=MakeSetThenList(possible_enemy_tiles)
    possible_pirate_tiles=Get_all_possible_tiles(game,pirate_to_check,moves)
    for z in possible_enemy_tiles:
        if game.in_range(z,pirate_to_check):
            obviously_dangereous.append(pirate_to_check.location)##if we stand in place and the enemy dashses to us.
            break
    for d in possible_pirate_tiles:
        for enemy in enemy_pirates:
            if game.in_range(d,enemy):
                obviously_dangereous.append(d)## If our pirate moves , and the enemies don't

    for x in possible_enemy_tiles :
        if x in possible_pirate_tiles:
            could_be_dangereous.append(x)## Will be a crash, same location
        for k in possible_pirate_tiles:
            if game.in_range(k,x):
                could_be_dangereous.append(k) ## Will be in shooting range

    could_be_dangereous=MakeSetThenList(could_be_dangereous)

    for y in possible_pirate_tiles:
        if y not in could_be_dangereous:
            safe_paths.append(y)
    ## JUST FOR CHECKING BEFORE RETURNING
    safe_paths=MakeSetThenList(safe_paths)
    obviously_dangereous=MakeSetThenList(obviously_dangereous)
    could_be_dangereous=MakeSetThenList(could_be_dangereous)
    return safe_paths,could_be_dangereous,obviously_dangereous
def MakeSetThenList(lis1):
    lis1_set=set(lis1)
    lis1=list(lis1_set)
    return lis1

#####################
#If 1 actions
#   O
#  OPO
#   O
#If 2 actions
#     O
#    OOO
#   OOPOO
#    OOO
#     O
#############
def Get_all_possible_tiles(game,pirate,moves):
    possible_tiles=[]
    turns_per_player=moves
    loc=pirate.location
    xloc=loc[0]
    yloc=loc[1]
    for action in xrange(turns_per_player):
        ######
        #   O
        #   O
        # OOPOO
        #   O
        #   O
        #######
        xlocnew=xloc+action
        possible_tiles.append((xlocnew,yloc))
        if action<turns_per_player:
            actions_left=turns_per_player-action
            tempx=xlocnew
            tempy=yloc
            for act in xrange(actions_left):
                ######(2actions)Say the x is the newtemp loc (after 1 move) we take all the possible locs from there.
                #
                #   O
                #  OXP
                #   O
                #
                ######
                ######(3actions)Say the x is the newtemp loc (after 1 move) we take all the possible locs from there.
                #   O
                #   O
                # OOXPO
                #   O
                #   O
                ######
                ######(3actions)Say the x is the newtemp loc (after 1 move) we take all the possible locs from there.
                #
                #  O
                # OXOP
                #  O
                #
                ######
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
        if action<turns_per_player:
            actions_left=turns_per_player-action
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
        if action<turns_per_player:
            actions_left=turns_per_player-action
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
        if action<turns_per_player:
            actions_left=turns_per_player-action
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