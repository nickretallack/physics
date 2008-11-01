from util import *

import pyglet
from pyglet.window import key
from pyglet.gl import *
import random
import math

import pymunk
from pymunk import Vec2d
pymunk.init_pymunk()


jump_impulse = 3000.


def generate_circular_object(radius=100, location=(200,200), verticies=None, level=None):
  # physics
  mass = 4/3 * math.pi * radius**3 / 200.
  inertia = pymunk.moment_for_circle(mass, 0, radius, (0,0))
  body = pymunk.Body(mass, inertia)
  body.position = Vec2d(location)
  body.radius = radius
  shape = pymunk.Circle(body, radius, (0,0))
  shape.friction = 2
  level.space.add(body,shape)

  # visuals
  if verticies:
    vert_count = verticies
  else:
    vert_count = int(radius / 5.) + 10
  vert_list = generate_circle(radius=radius, steps=vert_count)
  display = level.batch.add(vert_count, GL_LINE_LOOP, PositionedList(shape,level), ('v2f', vert_list))

  return shape

class PositionedList(pyglet.graphics.Group):
  def __init__(self,shape,level,**args):
    super(PositionedList, self).__init__(**args)
    self.body = shape.body
    self.level = level # refactor player centering as a parent group

  def set_state(self):
    glPushMatrix()
    glTranslatef((window.width - self.level.camera_focus().x)/2, (window.height - self.level.camera_focus().y)/2, 0)
    glScalef(0.5,0.5,0)
    glTranslatef(self.body.position.x, self.body.position.y, 0)
    glRotatef(self.body.angle * 180 / math.pi,0,0,1)

  def unset_state(self):
    glPopMatrix()


def find_nearest_body(our_body, bodies):
  nearest_body = None
  nearest_distance = 999999999999.
  for body in bodies:
    if body != our_body:
      distance = body.position.get_distance(our_body.position) - body.radius - our_body.radius
      if distance < nearest_distance:
        nearest_body = body
        nearest_distance = distance
  return nearest_body

def maybe_jump(player,bodies):
  body = player.body
  nearest_body = find_nearest_body(body,bodies)
  distance = body.position.get_distance(nearest_body.position) 
  if distance < body.radius + nearest_body.radius + 5:
    impulse = (body.position - nearest_body.position).normalized() * jump_impulse
    body.apply_impulse(impulse,(0,0))

class Thing:
  def __init__(self, level, args):
      radius = args['radius'] or 10
      
      #(radius=100, location=(200,200), verticies=None, level=None):
      # physics
      mass = 4/3 * math.pi * radius**3 / 200.
      inertia = pymunk.moment_for_circle(mass, 0, radius, (0,0))
      body = pymunk.Body(mass, inertia)
      body.position = Vec2d(location)
      body.radius = radius
      shape = pymunk.Circle(body, radius, (0,0))
      shape.friction = 2
      level.space.add(body,shape)

      # visuals
      if verticies:
        vert_count = verticies
      else:
        vert_count = int(radius / 5.) + 10
      vert_list = generate_circle(radius=radius, steps=vert_count)
      display = level.batch.add(vert_count, GL_LINE_LOOP, PositionedList(shape,level), ('v2f', vert_list))

      self.body = body
      self.shape = shape
      self.display = display
      self.level = level


class SpaceLevel:
  def __init__(self):
    self.space = pymunk.Space()
    self.batch = pyglet.graphics.Batch()
    
    # TODO: handle incoming player and objects?
    self.player = None

  def step(self,dt):
    mutual_gravitation(self.space.bodies)
    passive_space_controls(self.player)
    self.space.step(dt)
    

class FileLevel:
  def __init__(self,file):
    self.load(file)
    self.things = {}

  def camera_focus(self):
    return self.player.body.position

  def load(self, file):
    self.space = pymunk.Space()
    self.player = None
    self.batch = pyglet.graphics.Batch()

    data = format_loader(file)

    for body_tag in data:
      Thing(level=self, data[body_tag])
      #specs = data[body_tag]    # this process could be improved
      #body = generate_circular_object(radius=specs['radius'], location=specs['location'], level=self)
      #if body_tag == 'player':
      #  self.player = body

  def step(self,dt):
    mutual_gravitation(self.space.bodies)
    # todo: make jumping chargeable
    # todo in another game: simulate mario bros jump physics with chipmunk

    spinning = 0
    if keys[key.LEFT]:
      spinning = -1
    elif keys[key.RIGHT]:
      spinning = 1

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

    self.player.body.apply_force(jetpack.normalized()*1000,(0,0))
    max_w = -10.0
    self.player.body.torque = 60000.0 * min( (self.player.body.angular_velocity - spinning*max_w)/max_w, 1.0)

    self.space.step(dt)

  def keypress(self,symbol):
   if symbol == key.UP:
      maybe_jump(self.player, self.space.bodies)


class ControlSet:
  def __init__(self,player):
    self.player = player
    self.keys = key.KeyStateHandler()
    
  def handlers(self):
    return self.keys
    
    
  def passive(self):
    keys = self.keys
    player = self.player
    spinning = 0
    if keys[key.LEFT]:
      spinning += -1
    if keys[key.RIGHT]:
      spinning += 1

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

    player.body.apply_force(jetpack.normalized()*1000,(0,0))
    max_w = -10.0
    player.body.torque = 60000.0 * min( (self.player.body.angular_velocity - spinning*max_w)/max_w, 1.0)


class Game:
  def __init__(self):
    self.current_level = Level('mooney.js')
    pyglet.clock.schedule_interval(self.update, 1/60.)

  def update(self,dt):
    self.current_level.step(dt)


class GameWindow(pyglet.window.Window):
  def __init__(self,game,**args):
    super(GameWindow, self).__init__(**args)
    self.game = game
    self.push_handlers(keys)
  
  def on_key_press(self, symbol, modifier):
    super(GameWindow, self).on_key_press(symbol, modifier)    
    self.game.current_level.keypress(symbol)

  def on_draw(self):
    glClear(GL_COLOR_BUFFER_BIT)
    glLoadIdentity()
    self.game.current_level.batch.draw()

if __name__ == '__main__':
  game = Game()
  controls = ControlSet()
  window = GameWindow(game)
  pyglet.app.run()