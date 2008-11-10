from __future__ import division
import levels
import controls
import things

import pyglet
from util import *
from pymunk import Vec2d


from pyglet.gl import *
class GameWindow(pyglet.window.Window):
  def __init__(self,game,**args):
    super(GameWindow, self).__init__(resizable=True,**args)
    self.game = game
    self.keys = pyglet.window.key.KeyStateHandler()
    self.push_handlers(self.keys)
    self.edit_polygon = []

  def on_key_press(self, symbol, modifier):
    super(GameWindow, self).on_key_press(symbol, modifier)    
    controls.passive_space_controls(self.game.controlling, symbol)

  def on_mouse_release(self, x, y, button, modifiers):
    object_center = Vec2d(pymunk.util.calc_center(self.edit_polygon)) 
    window_center = Vec2d(self.width, self.height)/2 
    camera_center = self.game.current_level.camera_focus()
    position = object_center - window_center + camera_center
    for index in xrange(len(self.edit_polygon)):
      self.edit_polygon[index] = (self.edit_polygon[index][0], -self.edit_polygon[index][1])
    things.Asteroid(level=self.game.current_level, verticies=self.edit_polygon, position=position)
    self.edit_polygon = []

  def on_mouse_drag(self, x, y, dx, dy, buttons, modifiers):
    self.edit_polygon.append((x,y))


  def on_draw(self):
    glClear(GL_COLOR_BUFFER_BIT)
    glLoadIdentity()
    pyglet.graphics.draw(len(self.edit_polygon), GL_LINE_STRIP, 
        ('v2f', flatten(self.edit_polygon)))
    self.game.current_level.batch.draw()

  def passive(self):
    if self.game.controlling:
      controls.active_space_controls(self.game.controlling, self.keys)

class Game:
  def __init__(self):
    import pymunk
    pymunk.init_pymunk()
    self.window = GameWindow(game=self)
    self.controlling = None
    self.current_level = levels.Fun(game=self)
    pyglet.clock.schedule_interval(self.update, 1/60.)

  def update(self,dt):
    self.current_level.pre_step()
    self.window.passive()
    self.current_level.step(dt)
    
  def play(self):
    pyglet.app.run()


if __name__ == '__main__':
  Game().play()
