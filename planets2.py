from __future__ import division
import math
from util import *

import pyglet
from pyglet.gl import *

import pymunk
from pymunk.vec2d import Vec2d

def space_controls(player,keys):
  from pyglet.window import key
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
  player.body.torque = 60000.0 * min( (player.body.angular_velocity - spinning*max_w)/max_w, 1.0)


class Thing:
  def __init__(self, level):
    self.level = level


class RoundThing:
  def __init__(self, radius=100, position=(200,200), verticies=None, level=None):
    # physics
    mass = 4/3 * math.pi * radius**3 / 200
    inertia = pymunk.moment_for_circle(mass, 0, radius, (0,0))
    body = pymunk.Body(mass, inertia)
    body.position = Vec2d(position)
    body.radius = radius
    shape = pymunk.Circle(body, radius, (0,0))
    shape.friction = 2
    level.space.add(body,shape)

    # visuals
    if not verticies:
      verticies = int(radius / 5.) + 10
    vert_list = generate_circle(radius=radius, steps=verticies)
    display = level.batch.add(verticies, GL_LINE_LOOP, PositionedList(self), ('v2f', vert_list))

    self.body = body
    self.shape = shape
    self.display = display
    self.level = level


class PositionedList(pyglet.graphics.Group):
  def __init__(self,thing,**args):
    super(PositionedList, self).__init__(**args)
    self.thing = thing

  def set_state(self):
    glPushMatrix()
    glTranslatef((self.thing.level.game.window.width - self.thing.level.camera_focus().x)/2, (self.thing.level.game.window.height - self.thing.level.camera_focus().y)/2, 0)
    glScalef(0.5,0.5,0)
    glTranslatef(self.thing.body.position.x, self.thing.body.position.y, 0)
    glRotatef(self.thing.body.angle * 180 / math.pi,0,0,1)

  def unset_state(self):
    glPopMatrix()



class SpaceLevel:
  def camera_focus(self):
    return self.game.controlling.body.position
  
  def __init__(self,game):
    self.game  = game
    self.space = pymunk.Space()
    self.batch = pyglet.graphics.Batch()

    player = RoundThing(level=self)
    self.things = {'player':player}
    self.game.controlling = player
    RoundThing(level=self,position=(0,1))
    
  def step(self, dt):
    #apply_mutual_gravitation(self.space.bodies)
    print "FOO"
    self.space.step(dt)

class GameWindow(pyglet.window.Window):
  def __init__(self,game,**args):
    super(GameWindow, self).__init__(**args)
    self.game = game
    self.keys = pyglet.window.key.KeyStateHandler()
    self.push_handlers(self.keys)

  def on_key_press(self, symbol, modifier):
    super(GameWindow, self).on_key_press(symbol, modifier)    

  def on_draw(self):
    glClear(GL_COLOR_BUFFER_BIT)
    glLoadIdentity()
    self.game.current_level.batch.draw()

  def passive(self):
    if self.game.controlling:
      space_controls(self.game.controlling, self.keys)

class Game:
  def __init__(self):
    self.window = GameWindow(game=self)
    self.controlling = None
    self.current_level = SpaceLevel(game=self)
    pyglet.clock.schedule_interval(self.update, 1/60.)

  def update(self,dt):
    self.window.passive()
    self.current_level.step(dt)
    
  def play(self):
    pyglet.app.run()


if __name__ == '__main__':
  Game().play()
  
  

