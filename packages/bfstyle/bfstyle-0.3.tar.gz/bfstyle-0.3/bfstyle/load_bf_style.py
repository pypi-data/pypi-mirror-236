import seaborn as sns
import matplotlib.pyplot as plt
from matplotlib.font_manager import fontManager, FontProperties

# Colores Brain Food
colors = ["#1AC0D1", "#62F3D6", "#CCE622", "#F3F3F2", "#151D5B", "#F54B2F", "#000000", "#E88333"]
import matplotlib.colors as mcolors


def set_bf_style(colors=colors, path_fonts="fonts/"):
    path = path_fonts+"Roboto-Regular.ttf"
    path_title = path_fonts+"Roboto-Bold.ttf"
    fontManager.addfont(path)
    prop = FontProperties(fname=path)
    fontManager.addfont(path_title)
    # prop_title = FontProperties(fname=path_title)
    bf_style = {
        'axes.facecolor': 'white', # set the background color to white
        'axes.edgecolor': 'white', # set the edge color to black
        'axes.grid': True, # turn on the grid
        'axes.axisbelow': True,  # Set the grid behind the bars by default
        'grid.color': colors[3], # set the grid color to grey
        'grid.linewidth': 1,
        'xtick.bottom': True, # turn on the x-axis ticks on the bottom
        'ytick.left': True, # turn on the y-axis ticks on the left
        'xtick.color':"#3B3B3B",
        'font.family': prop.get_name(),
        'axes.titleweight': 'bold', # set the title weight to bold
    }
    plt.style.use(bf_style)
    return None


def set_bf_palette(colors=colors):
    sns.set_palette(sns.color_palette(colors))
    sns.palplot(sns.color_palette(colors))
    return None


def select_color(colors,x):
    sns.palplot(sns.color_palette(colors[x-1:x]))
    return colors[x-1]


def generate_gradient_colors(base_color, num_colors):
    """
    Genera una lista de colores degradados a partir de un color base en formato hexadecimal.

    Args:
        base_color (str): Color base en formato hexadecimal.
        num_colors (int): Número de colores en el degradado.

    Returns:
        list: Lista de colores degradados.
    """
    # Convierte el color base a un formato RGB
    base_color_rgb = mcolors.hex2color(base_color)

    # Genera una lista de colores degradados
    color_list = [base_color]

    for i in range(1, num_colors):
        # Calcula un nuevo color degradado
        new_color_rgb = [c + (1 - c) * i / num_colors for c in base_color_rgb]
        # Convierte el nuevo color a formato hexadecimal y lo agrega a la lista
        new_color_hex = mcolors.rgb2hex(new_color_rgb)
        color_list.append(new_color_hex)

    return color_list

