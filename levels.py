import pymunk
import pyglet

from things import *

class SpaceLevel:
  def camera_focus(self):
    return self.game.controlling.body.position
  
  def __init__(self,game):
    self.game  = game
    self.space = pymunk.Space()
    self.batch = pyglet.graphics.Batch()

    player = RoundThing(level=self, radius=10, verticies=5, )
    self.things = {'player':player}
    self.game.controlling = player
    RoundThing(level=self,position=(0,1))
  
  def pre_step(self):
    for body in self.space.bodies:
      body.reset_forces()
  
  def step(self, dt):
    mutual_gravitation(self.space.bodies)
    self.space.step(dt)
