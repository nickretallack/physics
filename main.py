import levels
import controls

import pyglet


from pyglet.gl import *
class GameWindow(pyglet.window.Window):
  def __init__(self,game,**args):
    super(GameWindow, self).__init__(**args)
    self.game = game
    self.keys = pyglet.window.key.KeyStateHandler()
    self.push_handlers(self.keys)

  def on_key_press(self, symbol, modifier):
    super(GameWindow, self).on_key_press(symbol, modifier)    
    controls.passive_space_controls(self.game.controlling, symbol)

  def on_draw(self):
    glClear(GL_COLOR_BUFFER_BIT)
    glLoadIdentity()
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
    self.current_level = levels.SpaceLevel(game=self)
    pyglet.clock.schedule_interval(self.update, 1/60.)

  def update(self,dt):
    self.current_level.pre_step()
    self.window.passive()
    self.current_level.step(dt)
    
  def play(self):
    pyglet.app.run()


if __name__ == '__main__':
  Game().play()
