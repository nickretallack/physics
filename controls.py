from pymunk.vec2d import Vec2d

def passive_space_controls(player,symbol):
  from pyglet.window import key
  if symbol == key.UP:
    maybe_jump(player,player.level.space)


def active_space_controls(player,keys):
  from pyglet.window import key
  spinning = 0
  if keys[key.LEFT]:
    spinning += -1
  if keys[key.RIGHT]:
    spinning += 1

  max_w = -10.0
  player.body.torque = 60000.0 * min( (player.body.angular_velocity - spinning*max_w)/max_w, 1.0)


  jetpack = Vec2d(0,0)
  if keys[key.NUM_6] or keys[key.D]:
    jetpack.x += 1
  if keys[key.NUM_4] or keys[key.A]:
    jetpack.x -= 1
  if keys[key.NUM_8] or keys[key.W]:
    jetpack.y += 1
  if keys[key.NUM_2] or keys[key.S]:
    jetpack.y -= 1

  if keys[key.NUM_1]:
    jetpack += (-0.5,-0.5)
  if keys[key.NUM_3]:
    jetpack += (+0.5,-0.5)
  if keys[key.NUM_7]:
    jetpack += (-0.5,+0.5)
  if keys[key.NUM_9]:
    jetpack += (+0.5,+0.5)

  player.body.apply_force(jetpack.normalized()*3000,(0,0))

def find_nearest_body(our_body,space):
  nearest_body = None
  nearest_distance = 999999999999.
  for body in space.bodies:
    if body != our_body:
      distance = body.position.get_dist_sqrd(our_body.position)
      if distance < nearest_distance:
        nearest_body = body
        nearest_distance = distance
  return nearest_body

def maybe_jump(player,space):
  body = player.body
  nearest_body = find_nearest_body(body,space)
  distance = body.position.get_distance(nearest_body.position) 
  if distance < body.radius + nearest_body.radius + 5:
    impulse = (body.position - nearest_body.position).normalized() * 3000.
    body.apply_impulse(impulse,(0,0))
