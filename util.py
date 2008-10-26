def generate_circle(radius=100, steps=50):
  verts = []
  for step in xrange(steps):
    verts.append(radius * math.cos(step*1./(steps)*2*math.pi))
    verts.append(radius * math.sin(step*1./(steps)*2*math.pi))
  return verts

