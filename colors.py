from sty import Style, RgbFg, fg
import math

def point_to_point_gradient(start_color, end_color, steps):
    r1, g1, b1 = start_color
    r2, g2, b2 = end_color
    delta_r = r2-r1 
    delta_g = g2-g1
    delta_b = b2-b1

    result = []

    for step in range(0, steps):
        color_step = (math.ceil(r1 + ((delta_r/steps) * step)), math.ceil(g1 + ((delta_g/steps) * step)), math.ceil(b1 + ((delta_b/steps) * step)))
        result.append(color_step)
    return result

### need to limit colors to steps/color_len = 6 or just 4 colors?
def gradient_steps(colors, steps):
    colors = colors[0:6]
    result_floor = []
    result_ceil = []
    # determine how many steps each color transition should take
    steps_per_color_floor = math.floor(steps/(len(colors) - 1))
    steps_per_color_ceil = math.ceil(steps/(len(colors) - 1))
    print("Steps per color floor: " + str(steps_per_color_floor))
    print("Steps per color ceil: " + str(steps_per_color_ceil))

    # step through the colors
    for idx, color in enumerate(colors):
        print("color: ", str(color))
        #find the next color
        next_color_idx = int(str(idx)) + 1
        print("next color idx: " + str(next_color_idx))
        if(next_color_idx < len(colors)):
            next_color = colors[next_color_idx]
            print("next color: ", next_color)

            #get gradient between color and next color
            gradient_floor = point_to_point_gradient(color, next_color, steps_per_color_floor)
            gradient_ceil = point_to_point_gradient(color, next_color, steps_per_color_ceil)
            result_floor += gradient_floor
            result_ceil += gradient_ceil
    
    len_floor = len(result_floor)
    len_ceil = len(result_ceil)
    if len_floor - steps >= 0 and len_floor -steps < len_ceil - steps:
        return result_floor
    else:
        return result_ceil

def print_colors(colors):
    for color in colors:
        fg.color = Style(RgbFg(color[0], color[1], color[2]))
        buf = fg.color + '■' + fg.rs
        print(buf)


list_of_colors = [(0,255,0), (0,0,255), (255,0,0), (0,255,0)]
gradient = gradient_steps(list_of_colors, 25)

print("colors: ", gradient)
print("result length: ", len(gradient))

print_colors(gradient)