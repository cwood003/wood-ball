import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib.colors import LinearSegmentedColormap

from plottable import ColDef, Table
from plottable.cmap import normed_cmap
from plottable.formatters import decimal_to_percent
from plottable.plots import circled_image # image

from plottable.cmap import normed_cmap

# example usage
# -------------------------------------------------------
# td = TidyTable()

# cmap = td.cmap
# col_def_dict = {
#     "date": {"textprops": {"ha": "left", "weight": "bold"}, "width": 1},
#     "team": {"textprops": {"ha": "left", "weight": "bold"}, "width": 2},
#     "opponent": {"group": "Matchup Info", "textprops": {"ha": "center"}, "width": 2},
#     "outcome": {"group": "Matchup Info", "textprops": {"ha": "center"}, "width": 0.75},
#     "active": {"group": "Matchup Info", "textprops": {"ha": "center"}, "width": 0.75},
#     "plus_minus": {
#         "group": "Stats",
#         "textprops": {"ha": "center"},
#         "width": 0.75,
#         "border": "left",
#         # Assuming `normed_cmap`, `test_df`, `cmap`, and `num_stds` are defined elsewhere
#         "cmap": normed_cmap(test_df['plus_minus'], cmap=cmap, num_stds=2.5)
#     },
# }
# -------------------------------------------------------

class TidyTable():

    def __init__(self, height: int = 20, width: int = 15, font_size: int = 16):

        self.height = height
        self.width = width
        self.font_size = font_size

        # set wood-ball custom color map
        self.cmap = LinearSegmentedColormap.from_list(
            name="bugw", colors=["#333333", "#353936", "#39483d", "#3d6049", "#3f7653", "#3f8058"], N=256
        )
    
    def create_table_col_defs(self, col_def_dict):
        col_defs = []
        for name, params in col_def_dict.items():
            col_defs.append(ColDef(name=name, **params))
        return col_defs
    
    def create_table(self, data: pd.DataFrame, col_def_dict: dict):

        plt.rcParams["font.family"] = ["Liberation Mono"]
        plt.rcParams["savefig.bbox"] = "tight"
        plt.rcParams["figure.facecolor"] = "#333333"  # Sets the figure background color
        plt.rcParams["axes.facecolor"] = "#333333"    # Sets the axes background color

        fig, ax = plt.subplots(figsize=(self.height, self.width))

        table = Table(
            data,
            column_definitions=self.create_table_col_defs(col_def_dict),
            row_dividers=True,
            # footer_divider=True,
            ax=ax,
            textprops={"fontsize": self.font_size, "color":"#dcdcdc"},
            row_divider_kw={"linewidth": 1, "linestyle": (0, (1, 5)), "color": "#dcdcdc"},
            col_label_divider_kw={"linewidth": 1, "linestyle": "-", "color": "#dcdcdc"},
            column_border_kw={"linewidth": 1, "linestyle": "-", "color": "#dcdcdc"},
        )

        # fig.savefig("wwc_table.png", facecolor=ax.get_facecolor(), dpi=200)
        plt.show()
    
