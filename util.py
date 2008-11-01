from __future__ import division
# GRAPHICS
import math
import pymunk
def generate_circle(radius=100, steps=50):
  verts = []
  for step in xrange(steps):
    verts.append(radius * math.cos(step*1./(steps)*2*math.pi))
    verts.append(radius * math.sin(step*1./(steps)*2*math.pi))
  return verts

# PHYSICS
def mutual_gravitation(bodies,G):
  for body in bodies:
    for body2 in bodies:
      if body2 != body:
        body.apply_force(get_gravity(body, body2,G), pymunk.Vec2d(0,0))

def get_gravity(body1, body2, G):
  distance_squared = body1.position.get_distance(body2.position)
  gravity = -G * body1.mass * body2.mass / distance_squared
  return (body1.position - body2.position).normalized() * gravity

# FILES
def format_loader(file):
  from os.path import splitext
  type = splitext(file)[1]
  if type == '.js':
    try: import json 
    except ImportError: import simplejson as json
    data = json.load(open(file))
  else:
    print "%s: Unsupported Filetype" % file
    return None
  return data



# BASICS
def flatten(x):
    """flatten(sequence) -> list

    Returns a single, flat list which contains all elements retrieved
    from the sequence and all recursively contained sub-sequences
    (iterables).

    Examples:
    >>> [1, 2, [3,4], (5,6)]
    [1, 2, [3, 4], (5, 6)]
    >>> flatten([[[1,2,3], (42,None)], [4,5], [6], 7, MyVector(8,9,10)])
    [1, 2, 3, 42, None, 4, 5, 6, 7, 8, 9, 10]"""

    result = []
    for el in x:
        #if isinstance(el, (list, tuple)):
        if hasattr(el, "__iter__") and not isinstance(el, basestring):
            result.extend(flatten(el))
        else:
            result.append(el)
    return result

