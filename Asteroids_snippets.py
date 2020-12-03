# classes / gameplay loop / some functions redacted

def keydown(key):
    for i in d_press:
        if key == simplegui.KEY_MAP[i]:
            d_press[i]()

def keyup(key):
    for i in d_release:
        if key == simplegui.KEY_MAP[i]:
            d_release[i]()

# key handlers

d_press = {'left': my_ship.dec_ang_vel,\
           'right': my_ship.inc_ang_vel,\
           'up': my_ship.thrust_on, \
           'space': my_ship.shoot}

d_release = {'left': my_ship.inc_ang_vel,\
             'right': my_ship.dec_ang_vel,\
             'up': my_ship.thrust_off}


# helper for sets
def process_sprite_group(given_set, canvas):
    for i in list(given_set):
            i.draw(canvas)
            i.update()
            if given_set == missile_group and i.update():
                given_set.remove(i)

tf_list = []
def group_collide(sg_object, other_object):
    global collide, tf_list, score
    for i in list(sg_object):
        if i.collision(other_object):
            radii_sum = i.get_radius() + other_object.get_radius()
            ob_dist = dist(i.get_position(), other_object.get_position())
            if radii_sum > ob_dist:
                sg_object.remove(i)
                if other_object == my_ship:
                    collide = True
                if type(sg_object) == type(set([])) and not other_object == my_ship:
                    tf_list.append(other_object)
                    score += 1


def group_group_collide(group_1, group_2):
    global tf_list
    for j in list(group_1):
        tf_list = []
        group_collide(group_2, j)
    group_1.difference_update(set(tf_list))

# timer handler that spawns a rock
def rock_spawner():
    global rock_group, score
    rock_pos = [random.randrange(0, WIDTH), random.randrange(0, HEIGHT)]
    if dist(rock_pos, my_ship.get_position()) < my_ship.get_radius()*2:
        return
    rock_vel = [random.random() * .6 - .3, random.random() * .6 - .3]
    rock_vel[0] *= score*0.2
    rock_vel[1] *= score*0.2
    rock_avel = random.random() * .2 - .1
    a_rock = Sprite(rock_pos, rock_vel, 0, rock_avel, asteroid_image, asteroid_info)
    if len(rock_group) < 12:
        rock_group.add(a_rock)
