from random import randint
from os import system

def colorize_text(text, start_color, end_color, steps):
    # calculate the color step for each component (rgb)
    r_step, g_step, b_step = [(end - start) // steps for start, end in zip(start_color, end_color)]
    
    colored_text = ""
    
    red, green, blue = start_color

    lines = text.splitlines()

    for line in lines:
        # construct the ANSI escape code for the current color
        color_code = f"\033[38;2;{red};{green};{blue}m"
        
        # append the current line with the color code and reset (0m) to the colored_text
        colored_text += f"{color_code}{line}\033[0m\n"
        
        # update the color components for the next line
        red += r_step
        green += g_step
        blue += b_step

    return colored_text

def text_color_transition(text, start_color, end_color, steps, direction="vertical"):
    colored_text = ""
    
    red, green, blue = start_color

    lines = text.splitlines()

    if direction == "vertical":
        # vertical gradient (top to bottom)
        r_step, g_step, b_step = [(end - start) // steps for start, end in zip(start_color, end_color)]
        
        for line in lines:
            # construct the ANSI escape code for the current color
            color_code = f"\033[38;2;{red};{green};{blue}m"
            
            # append the current line with the color code and reset (0m) to the colored_text
            colored_text += f"{color_code}{line}\033[0m\n"
            
            # update the color components for the next line
            red += r_step
            green += g_step
            blue += b_step
    elif direction == "horizontal":
        # horizontal gradient (left to right)
        for line in lines:
            if not line:
                continue  # skip empty lines
            r_step, g_step, b_step = [(end - start) // len(line) for start, end in zip(start_color, end_color)]
            r, g, b = start_color
            colored_line = ""
            for char in line:
                color_code = f"\033[38;2;{r};{g};{b}m"
                colored_line += f"{color_code}{char}\033[0m"
                r += r_step
                g += g_step
                b += b_step
            colored_text += colored_line + "\n"
    else:
        # default to vertical gradient
        r_step, g_step, b_step = [(end - start) // steps for start, end in zip(start_color, end_color)]
        
        for line in lines:
            # construct the ANSI escape code for the current color
            color_code = f"\033[38;2;{red};{green};{blue}m"
            
            # append the current line with the color code and reset (0m) to the colored_text
            colored_text += f"{color_code}{line}\033[0m\n"
            
            # update the color components for the next line
            red += r_step
            green += g_step
            blue += b_step

    return colored_text

def color_transition(text, start_color, end_color, steps, direction="vertical"):
    colored_text = ""
    lines = text.splitlines()
    
    if direction == "horizontal":
        for line in lines:
            if not line:
                continue  # skip empty lines

            char_count = len(line)
            r_step, g_step, b_step = [(end - start) // char_count for start, end in zip(start_color, end_color)]
            r, g, b = start_color
            colored_line = ""

            for char in line:
                color_code = f"\033[38;2;{r};{g};{b}m"
                colored_line += f"{color_code}{char}\033[0m"
                r += r_step
                g += g_step
                b += b_step

            colored_text += colored_line + "\n"
    else:
        r_step, g_step, b_step = [(end - start) // steps for start, end in zip(start_color, end_color)]
        red, green, blue = start_color

        for line in lines:
            color_code = f"\033[38;2;{red};{green};{blue}m"
            colored_text += f"{color_code}{line}\033[0m\n"
            red += r_step
            green += g_step
            blue += b_step

    return colored_text

def black_to_white(text, direction="vertical"):
    if direction == "horizontal":
        char_count = max(len(line) for line in text.splitlines())
        start_color = (0, 0, 0)
        end_color = (255, 255, 255)
        return color_transition(text, start_color, end_color, char_count, direction)
    else:
        start_color = (0, 0, 0)
        end_color = (255, 255, 255)
        return color_transition(text, start_color, end_color, 20, direction)

def purple_to_pink(text, direction="vertical"):
    if direction == "horizontal":
        char_count = max(len(line) for line in text.splitlines())
        start_color = (40, 0, 220)
        end_color = (255, 0, 220)
        return color_transition(text, start_color, end_color, char_count, direction)
    else:
        start_color = (40, 0, 220)
        end_color = (255, 0, 220)
        return color_transition(text, start_color, end_color, 10, direction)

def green_to_blue(text, direction="vertical"):
    if direction == "horizontal":
        char_count = max(len(line) for line in text.splitlines())
        start_color = (0, 255, 100)
        end_color = (0, 255, 255)
        return color_transition(text, start_color, end_color, char_count, direction)
    else:
        start_color = (0, 255, 100)
        end_color = (0, 255, 255)
        return color_transition(text, start_color, end_color, 9, direction)

def pink_to_red(text, direction="vertical"):
    if direction == "horizontal":
        char_count = max(len(line) for line in text.splitlines())
        start_color = (255, 0, 255)
        end_color = (255, 0, 0)
        return color_transition(text, start_color, end_color, char_count, direction)
    else:
        start_color = (255, 0, 255)
        end_color = (255, 0, 0)
        return color_transition(text, start_color, end_color, 12, direction)

def water(text, direction="vertical"):
    if direction == "horizontal":
        char_count = max(len(line) for line in text.splitlines())
        start_color = (0, 10, 255)
        end_color = (0, 255, 255)
        return color_transition(text, start_color, end_color, char_count, direction)
    else:
        start_color = (0, 10, 255)
        end_color = (0, 255, 255)
        return color_transition(text, start_color, end_color, 15, direction)

def fire(text, direction="vertical"):
    if direction == "horizontal":
        char_count = max(len(line) for line in text.splitlines())
        start_color = (255, 250, 0)
        end_color = (255, 0, 0)
        return color_transition(text, start_color, end_color, char_count, direction)
    else:
        start_color = (255, 250, 0)
        end_color = (255, 0, 0)
        return color_transition(text, start_color, end_color, 10, direction)

def brazil(text, direction="vertical"):
    if direction == "horizontal":
        char_count = max(len(line) for line in text.splitlines())
        start_color = (0, 255, 0)
        end_color = (255, 255, 0)
        return color_transition(text, start_color, end_color, char_count, direction)
    else:
        start_color = (0, 255, 0)
        end_color = (255, 255, 0)
        return color_transition(text, start_color, end_color, 6, direction)

def autumn_colors(text, direction="vertical"):
    if direction == "horizontal":
        char_count = max(len(line) for line in text.splitlines())
        start_color = (255, 140, 0)
        end_color = (139, 69, 19)
        return color_transition(text, start_color, end_color, char_count, direction)
    else:
        start_color = (255, 140, 0)
        end_color = (139, 69, 19)
        return color_transition(text, start_color, end_color, 10, direction)

def blue_to_green(text, direction="vertical"):
    if direction == "horizontal":
        char_count = max(len(line) for line in text.splitlines())
        start_color = (0, 0, 255)
        end_color = (0, 255, 0)
        return color_transition(text, start_color, end_color, char_count, direction)
    else:
        start_color = (0, 0, 255)
        end_color = (0, 255, 0)
        return color_transition(text, start_color, end_color, 10, direction)

def orange_to_yellow(text, direction="vertical"):
    if direction == "horizontal":
        char_count = max(len(line) for line in text.splitlines())
        start_color = (255, 140, 0)
        end_color = (255, 255, 0)
        return color_transition(text, start_color, end_color, char_count, direction)
    else:
        start_color = (255, 140, 0)
        end_color = (255, 255, 0)
        return color_transition(text, start_color, end_color, 10, direction)
    
def cyan_to_green(text, direction="vertical"):
    if direction == "horizontal":
        char_count = max(len(line) for line in text.splitlines())
        start_color = (0, 255, 255)
        end_color = (0, 128, 0)
        return color_transition(text, start_color, end_color, char_count, direction)
    else:
        start_color = (0, 255, 255)
        end_color = (0, 128, 0)
        return color_transition(text, start_color, end_color, 10, direction)

def random_color(text):
    system("")
    faded = ""
    
    for line in text.splitlines():
        for character in line:
            faded += f"\033[38;2;{randint(0, 255)};{randint(0, 255)};{randint(0, 255)}m{character}\033[0m"
        faded += "\n"

    return faded