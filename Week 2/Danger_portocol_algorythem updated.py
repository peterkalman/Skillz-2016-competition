## Attack radius is 4 tiles
#In order to dodge an enemy , we will have to look at the threatening ways and put them into an array.
Attack_radius=4

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
    xloc=loc.row
    yloc=loc.col
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
            
        
        
