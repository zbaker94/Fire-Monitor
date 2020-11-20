from sty import Style, RgbFg, fg
import math

def spread_colors(colors, size):
    sections_per_color = math.ceil(size/len(colors))
    print("size: ", str(size))
    print("colors: ", str(colors))
    print("colors len: ", len(colors))
    print("sections per color: ", str(sections_per_color))
    count = 0
    result = []
    for color in colors:
        while count < sections_per_color:
            result.append(color)
            count += 1
        count = 0
    return result

def create_gradient(colors, steps):
    result = []
    steps_per_color = math.floor(steps/(len(colors)))

    print("colors length: ", len(colors))
    print("steps per color: " + str(steps_per_color))
    for color in colors:
        next_color_index = [x for x, y in enumerate(colors) if y[0] == color[0] and y[1] == color[1] and y[2] == color[2]]
        next_color_index = next_color_index[0] + 1

        if next_color_index < len(colors):
            next_color = colors[next_color_index]
            
            r1,g1,b1 = color
            r2,g2,b2 = next_color

            delta_r, delta_g, delta_b = (r2-r1)/steps_per_color, (g2-g1)/steps_per_color, (b2-b1)/steps_per_color
        
            for step in range(0, steps_per_color):
                result.append((math.ceil(r1 + (delta_r * step)), math.ceil(g1 + (delta_g * step)), math.ceil(b1 + (delta_b * step))))
        
    return result    

list_of_colors = [(255,0,0), (0,0,255), (0,255,0), (255,0,0)]
# colors = spread_colors(list_of_colors, 25)
gradient = create_gradient(list_of_colors, 13)

print("colors: ", gradient)
print("result length: ", len(gradient))

for color in gradient:
    fg.color = Style(RgbFg(color[0], color[1], color[2]))
    buf = fg.color + '■' + fg.rs
    print(buf)