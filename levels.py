from __future__ import division
import pymunk
from pymunk.vec2d import Vec2d
import pyglet

import things
from util import *

import random
random.seed()

class Level:
  def camera_focus(self):
    return Vec2d(0,0)#return self.game.controlling.body.position
  
  def __init__(self,game):
    self.gravity = 1
    self.game  = game
    self.space = pymunk.Space()
    self.batch = pyglet.graphics.Batch()
    self.things = {}
    self.create_player()
    self.create_things()
    
  def create_player(self):
    #player = things.Circle(level=self, radius=10, verticies=5)
    player = things.Asteroid(level=self, verticies=[(0,0),(5,0),(5,100),(0,100)])
    self.game.controlling = player
    
  def create_things(self):
    things.Circle(level=self,position=(0,-100))
  
  def pre_step(self):
    for body in self.space.bodies:
      body.reset_forces()
  
  def step(self, dt):
    mutual_gravitation(self.space.bodies, G=self.gravity)
    substeps = 2
    for substep in xrange(substeps):
      self.space.step(dt/substeps)

class Fun(Level):
  def create_things(self):
    planet = things.Circle(level=self, radius=200, position=(0,-210))
    for thing in xrange(20):
      position = (random.randint(400,500), thing*10)
      troid = things.Circle(level=self, radius=10, position=position, orbit=planet)
      #troid.body.velocity = (-0,200)


class File(Level):
  def __init__(self,game,file):
    self.file = file
    super(self, Level).__init__(game)

  def create_things(self):
    data = format_loader(self.file)

    for body_tag in data:
      things.Circle(level=self, *data[body_tag])
