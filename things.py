from __future__ import division
import math

from util import *

import pymunk
from pymunk.vec2d import Vec2d
from pyglet.gl import *
import pyglet



class Thing:
  def __init__(self, level):
    self.level = level


class Circle:
  def __init__(self, level, radius=100, position=(0,0), density=1.0, verticies=None, orbit=None, mass=None, static=False, **kwargs):
    # physics
    if not mass:
      mass = math.pi * radius**2 * density  #4/3 * math.pi * radius**3 * density * 0.1
    inertia = pymunk.moment_for_circle(mass, 0, radius, (0,0))
    body = pymunk.Body(mass, inertia)
    body.position = Vec2d(position)
    body.radius = radius
    shape = pymunk.Circle(body, radius, (0,0))
    shape.friction = 2

    if static:
      level.space.add_static(body,shape)
    else:
      level.space.add(body,shape)

    # visuals
    if not verticies:
      verticies = int(radius / 5.) + 10
    vert_list = generate_circle(radius=radius, steps=verticies)
    display = level.batch.add(verticies, GL_LINE_LOOP, PositionedList(self), ('v2f', vert_list))

    if orbit:
      gravitation = level.gravity * (body.mass + orbit.body.mass)
      distance = body.position.get_distance(orbit.body.position)
      speed = (gravitation/distance)**(0.5)
      body.velocity = (body.position - orbit.body.position).rotated(90).normalized() * speed


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
    #glScalef(0.5,0.5,0)
    glTranslatef(self.thing.body.position.x, self.thing.body.position.y, 0)
    glRotatef(self.thing.body.angle * 180 / math.pi,0,0,1)

  def unset_state(self):
    glPopMatrix()



class Asteroid:
  def __init__(self, level, position=(0,0), density=1.0, verticies=None, orbit=None, mass=None, static=False, **kwargs):
    # physics
    #if not mass:
      #mass = math.pi * radius**2 * density  #4/3 * math.pi * radius**3 * density * 0.1
    mass = 100

    verticies = pymunk.util.reduce_poly(pymunk.util.poly_vectors_around_center(pymunk.util.convex_hull(verticies), points_as_Vec2d=False),0.3)
    #center = pymunk.util.calc_center(verticies)
    #for index in xrange(len(verticies)):
    #  newpoint = Vec2d(verticies[index]) - center
    #  verticies[index] = (-newpoint.x, -newpoint.y)

    inertia = pymunk.moment_for_poly(mass, verticies, (0,0))
    body = pymunk.Body(mass, inertia)
    body.position = position
    body.radius = 100
    shape = pymunk.Poly(body, verticies, (0,0))
    shape.friction = 2

    if static:
      level.space.add_static(body,shape)
    else:
      level.space.add(body,shape)

    # visuals
    display = level.batch.add(len(verticies), GL_LINE_LOOP, PositionedList(self), ('v2f', flatten(verticies)))

    if orbit:
      gravitation = level.gravity * (body.mass + orbit.body.mass)
      distance = body.position.get_distance(orbit.body.position)
      speed = (gravitation/distance)**(0.5)
      body.velocity = (body.position - orbit.body.position).rotated(90).normalized() * speed


    self.body = body
    self.shape = shape
    self.display = display
    self.level = level

