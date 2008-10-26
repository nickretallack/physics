import pyglet
from pyglet.window import key
from pyglet.gl import *
import random
import math

import pymunk
pymunk.init_pymunk()
space = pymunk.Space()

window = pyglet.window.Window()
keys = key.KeyStateHandler()
window.push_handlers(keys)
batch = pyglet.graphics.Batch()

def generate_circle(radius=100, steps=50):
  verts = []
  for step in xrange(steps+1):
    verts.append(radius * math.cos(step/(steps*1.)*2*math.pi))
    verts.append(radius * math.sin(step/(steps*1.)*2*math.pi))
  return verts

def generate_circular_object(radius=100, location=(200,200), verticies=None):
  # physics
  mass = math.pi * radius * radius / 50.
  inertia = pymunk.moment_for_circle(mass, 0, radius, (0,0))
  body = pymunk.Body(mass, inertia)
  body.position = location
  shape = pymunk.Circle(body, radius, (0,0))
  shape.friction = 2
  space.add(body, shape)

  # visuals
  if verticies:
    vert_count = verticies + 1
  else:
    vert_count = int(radius / 5.) + 10
  vert_list = generate_circle(radius=radius, steps=vert_count)
  display = batch.add(vert_count+1, GL_LINE_STRIP, PositionedList(shape), ('v2f', vert_list))

  return shape

class PositionedList(pyglet.graphics.Group):
  def __init__(self,shape):
    super(PositionedList, self).__init__()
    self.body = shape.body

  def set_state(self):
    glPushMatrix()
    glTranslatef(self.body.position.x, self.body.position.y, 0)
    glRotatef(self.body.angle * 180 / math.pi,0,0,1)

  def unset_state(self):
    glPopMatrix()

planet = generate_circular_object(radius=100, location=(200,200))
player = generate_circular_object(radius=10,  location=(400,400), verticies=5)

bodies = [player.body, planet.body]

def get_gravity(body1, body2):
  distance_squared = body1.position.get_dist_sqrd(body2.position)
  gravity = -2000 * body1.mass * body2.mass / distance_squared
  return (body1.position - body2.position).normalized() * gravity
  

def nearest_body(our_body):
  nearest_body = None
  nearest_distance = 999999999999
  for body in bodies:
    if body != our_body:
      distance = unsquared_distance(body,our_body)
      if distance < nearest_distance:
        nearest_body = body
        nerest_distance = distance
  return nearest_body

def jump_impulse(body):
  nearest_body = None
  nearest_distance = 999999999999
  for body in bodies:
    if body != our_body:
      distance = unsquared_distance(body,our_body)
      if distance < nearest_distance:
        nearest_body = body
        nerest_distance = distance

  dx = our_body.position.x - nearest_body.position.x
  dy = our_body.position.y - nearest_body.position.y
  angle = math.atan2(dy,dx)
  components = (math.cos(angle)*impulse, math.sin(angle)*impulse)

  
    
@window.event
def update(dt):
  for body in bodies:
    body.reset_forces()
    for body2 in bodies:
      if body2 != body:
        body.apply_force(get_gravity(body, body2), pymunk.Vec2d(0,0))

  torque = 1000
  if keys[key.LEFT]:
    player.body.torque = +torque
  elif keys[key.RIGHT]:
    player.body.torque = -torque

  space.step(dt)
pyglet.clock.schedule_interval(update, 1/60.)

@window.event
def on_draw():
  glClear(GL_COLOR_BUFFER_BIT)
  glLoadIdentity()
  batch.draw()

pyglet.app.run()
