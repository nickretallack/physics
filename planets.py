import pyglet
from pyglet.window import key
from pyglet.gl import *
import random
import math

import pymunk
from pymunk import Vec2d
pymunk.init_pymunk()
space = pymunk.Space()

window = pyglet.window.Window()
keys = key.KeyStateHandler()
batch = pyglet.graphics.Batch()

gravitational_constant = 20000.
jump_impulse = 300.

def generate_circle(radius=100, steps=50):
  verts = []
  for step in xrange(steps):
    verts.append(radius * math.cos(step/(steps*1.)*2*math.pi))
    verts.append(radius * math.sin(step/(steps*1.)*2*math.pi))
  return verts

def generate_circular_object(radius=100, location=(200,200), verticies=None):
  # physics
  mass = 4/3 * math.pi * radius**3 / 200.
  inertia = pymunk.moment_for_circle(mass, 0, radius, (0,0))
  body = pymunk.Body(mass, inertia)
  body.position = location
  body.radius = radius
  shape = pymunk.Circle(body, radius, (0,0))
  shape.friction = 2
  space.add(body, shape)

  # visuals
  if verticies:
    vert_count = verticies
  else:
    vert_count = int(radius / 5.) + 10
  vert_list = generate_circle(radius=radius, steps=vert_count)
  print len(vert_list), vert_count
  display = batch.add(vert_count, GL_LINE_LOOP, PositionedList(shape), ('v2f', vert_list))

  return shape

class PositionedList(pyglet.graphics.Group):
  def __init__(self,shape,**args):
    super(PositionedList, self).__init__(**args)
    self.body = shape.body

  def set_state(self):
    glPushMatrix()
    glTranslatef((window.width - player.body.position.x)/2, (window.height - player.body.position.y)/2, 0)
    glScalef(0.5,0.5,0)
    glTranslatef(self.body.position.x, self.body.position.y, 0)
    glRotatef(self.body.angle * 180 / math.pi,0,0,1)

  def unset_state(self):
    glPopMatrix()

planet = generate_circular_object(radius=100, location=(200,200))
moon = generate_circular_object(radius=50, location=(700,200))
moon.body.velocity = Vec2d(0,10)
player = generate_circular_object(radius=10,  location=(400,400), verticies=5)

bodies = [player.body, planet.body]

def get_gravity(body1, body2):
  distance_squared = body1.position.get_dist_sqrd(body2.position)
  gravity = -gravitational_constant * body1.mass * body2.mass / distance_squared
  return (body1.position - body2.position).normalized() * gravity
  

def find_nearest_body(our_body):
  nearest_body = None
  nearest_distance = 999999999999.
  for body in bodies:
    if body != our_body:
      distance = body.position.get_dist_sqrd(our_body.position)
      if distance < nearest_distance:
        nearest_body = body
        nearest_distance = distance
  return nearest_body

def maybe_jump(player):
  body = player.body
  nearest_body = find_nearest_body(body)
  distance = body.position.get_distance(nearest_body.position) 
  if distance < body.radius + nearest_body.radius + 5:
    impulse = (body.position - nearest_body.position).normalized() * jump_impulse
    body.apply_impulse(impulse,(0,0))
    
@window.event
def update(dt):
  for body in bodies:
    body.reset_forces()
    for body2 in bodies:
      if body2 != body:
        body.apply_force(get_gravity(body, body2), pymunk.Vec2d(0,0))

  max_w = -10.0
  sv = pymunk.vec2d.Vec2d(5,5)
  spinning = 0
  if keys[key.LEFT]:
    spinning = -1
  elif keys[key.RIGHT]:
    spinning = 1
  
  player.body.torque = 60000.0 * min( (player.body.angular_velocity - spinning*max_w)/max_w, 1.0)

  space.step(dt)
pyglet.clock.schedule_interval(update, 1/60.)

@window.event
def on_key_press(symbol, modifier):
  if symbol == key.UP:
    # jump -- should probably check that we're close enough to the planet
    maybe_jump(player)

@window.event
def on_draw():
  glClear(GL_COLOR_BUFFER_BIT)
  glLoadIdentity()
  batch.draw()

window.push_handlers(keys)
pyglet.app.run()
