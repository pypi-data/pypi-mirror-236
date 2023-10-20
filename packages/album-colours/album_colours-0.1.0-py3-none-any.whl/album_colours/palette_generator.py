from colour import Color

palettes = {
    'devendra': ['#74b6e2', '#135793', '#2164b4', '#3f8dc9', '#143a67', '#0a1a2a', '#6694a6', '#a8b6b3',
                 '#5e462d', '#776248'],
    'tyler': ['#eed28c', '#e7d3a5', '#df8e3f', '#cd502f', '#a23425', '#c3a282', '#549462', '#53835c',
              '#726447', '#3f3a25'],
    'kanye': ['#F48B57', '#77412C', '#E6DABC', '#2C0B07', '#D9875F', '#965B35', '#465969', '#B6724F', '#51251B',
              '#C2B099'],
    'soda_stereo': ['#879C98', '#FAF9F8', '#173DF7', '#FA2FFA', '#5A6D6D', '#B8C8C6', '#2C383B', '#DDDEE2', '#778B88',
                    '#9DB0AD'],
    'kendrick': ['#CACAD9', '#3E404E', '#AA232A', '#1E1E25', '#703C49', '#4D2B34', '#8E5867', '#AEA3AB', '#E3E3EF',
                 '#F2090A'],
    'kendrick2': ['#4C8AAC', '#DFDFDF', '#282935', '#5C7668', '#376F93', '#C5C6C5', '#67A5C3', '#86968F', '#28587B',
                  '#485E55'],
    'kendrick3': ['#9AA6A4', '#3F2818', '#987952', '#CED1CF', '#111112', '#B9A57E', '#765F48', '#653718', '#7F857F',
                  '#574736'],
    'aventura': ['#3B4E42', '#BEC7BA', '#C06B49', '#101A15', '#7E8E7F', '#4F6254', '#E6ECE7', '#9DA897', '#202B21',
                 '#2F3B30'],
    'radiohead': ['#CCCDC4', '#2E1D1C', '#ABB0AF', '#5D6C82', '#F9F8F0', '#8A311E', '#090908', '#E3E6E5', '#8A9298',
                  '#424757'],
    'frank_ocean': ['#E2E2E2', '#616267', '#372019', '#90583F', '#BB7454', '#FDFDFD', '#583A2D', '#B2AEAD', '#1A0E0D',
                    '#5B5854'],
    'alvaro_diaz': ['#33423B', '#B8D7F1', '#7F8998', '#596043', '#EDF8FC', '#9DA2AE', '#67B2F3', '#BB5550', '#465262',
                    '#5F6E83'],
    'alvaro_diaz2': ['#0059C6', '#EE580A', '#08CA09', '#0D1110', '#EDB413', '#0F3D77', '#63776C', '#DADBD9', '#147413',
                     '#7C4C14'],
    'sen_senra': ['#989C96', '#7A5B3A', '#C3C2C0', '#8E7350', '#B6B7B2', '#1C1712', '#828278', '#616259', '#523926',
                  '#D7D4D0'],
    'bad_bunny': ['#F5B21C', '#F3BBBA', '#DC190A', '#5EAC50', '#E16C7F', '#82BCCB', '#503B2F', '#E1681D', '#C2CAEF',
                  '#D69499'],
    'rosalia': ['#A5B1BF', '#AE9262', '#E3DFD9', '#8192AF', '#BCA98B', '#C8CBCD', '#F4F4F3', '#69502B', '#92743F',
                '#DFC9B0'],
    'rosalia2': ['#FEFEFE', '#BA2421', '#D2997D', '#3D3834', '#E26561', '#EBD1C6', '#A37C69', '#E5393E', '#E4B79E',
                 '#735950']
}


def color_gradient_generator(palette_name, color_count=None, palette_type=None):
    """
    Generates a color gradient (discrete or continuous) from an album palette
    :param palette_name:
    :param color_count:
    :param palette_type:
    :return:
    """
    current_palette = []

    if palette_name in palettes:
        current_palette = palettes[palette_name]
    else:
        return []  # TODO: Replace with exceptions? Or just return empty list?

    if color_count is None:
        color_count = len(current_palette)

    if palette_type is None:
        # If colour count is less than the number of colours in the palette (10), then it is a discrete palette
        if color_count < len(current_palette):
            palette_type = 'discrete'
        else:
            palette_type = 'continuous'

    if palette_type == 'discrete' and color_count > len(current_palette):
        raise ValueError('The colour count is greater than the number of colours in the palette')

    # Decide if this is for seaborn, matplotlib, ggplot, plotly, etc.

    if palette_type == 'discrete':
        return current_palette[:color_count]
    else:
        return [c.hex_l for c in list(Color(current_palette[0]).range_to(Color(current_palette[2]), color_count))]
