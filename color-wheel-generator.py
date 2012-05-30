from PIL import Image
import random
import math

def make_color(base, adj, ratio, shade):
  output = 0x0
  bit = 0
  """
  Go through each bit of the colors adjusting blue with blue, red with red,
  green with green, etc.
  """
  for pos in xrange(3):
    base_chan = color_wheel[base][pos]
    adj_chan = color_wheel[adj][pos]
    new_chan =  int(round(base_chan * (1 - ratio) + adj_chan * ratio))
    
    # now alter the channel by the shade
    if shade < 1:
      new_chan = new_chan * shade
    elif shade > 1:
      shade_ratio = shade - 1
      new_chan = (0xff * shade_ratio) + (new_chan * (1 - shade_ratio))

    output = output + (int(new_chan) << bit)
    bit = bit + 8
  return output

bg_color = 0x888888
img_size = 500
img_half = img_size / 2;
inner_radius = 100
outer_radius = 240

color_wheel = [
  [0xff, 0x00, 0xff], 
  [0xff, 0x00, 0x00], 
  [0xff, 0xff, 0x00], 
  [0x00, 0xff, 0x00], 
  [0x00, 0xff, 0xff], 
  [0x00, 0x00, 0xff], 
  [0xff, 0x00, 0xff]] # one extra so less wrap-around logic is required

im = Image.new('RGB', (img_size, img_size), bg_color)
for x in xrange(img_size):
  for y in xrange(img_size):
    dist = abs(math.sqrt((x - img_half) ** 2 + (y - img_half) ** 2));
    if dist < inner_radius or dist > outer_radius:
      continue;
    shade = 2 * (dist - inner_radius) / (outer_radius - inner_radius)

    # probably an error in my logic, but the center line is getting
    # inverted. so, manually set it if it's not right
    if x - img_half == 0:
      angle = angle = -90
      if y > img_half:
        angle = 90
    else: 
      angle = math.atan2((y - img_half), (x - img_half)) * 180 / math.pi
  
    angle = (angle + 30) % 360
      
    idx = angle / 60
    if idx < 0: 
      idx = 6 + idx
    base = int(round(idx))

    adj = (6 + base + (-1 if base > idx else 1)) % 6

    ratio = max(idx, base) - min(idx, base)
    
    color = make_color(base, adj, ratio, shade)
     
    im.putpixel((x, y), color)
    
im.save('gamut.png', 'PNG')
