"""Use the different Scihence styles."""
import logging
import sys
from pathlib import Path
from typing import Any, Self

import matplotlib as mpl
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objects as go
import plotly.io as pio
from matplotlib import font_manager
from PIL import ImageColor

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

THIS_DIR = Path(__file__).parent

for font in font_manager.findSystemFonts([f"{THIS_DIR}/fonts"]):
    font_manager.fontManager.addfont(font)

THIS_MODULE = sys.modules[__name__]
THIS_MODULE.current_style = None


class ColorDict(dict):
    """Dictionary storing colors with their names."""


colors: ColorDict = ColorDict(
    navy="#000035",
    silver="#c0c0c0",
    purple="#552777",
    blue="#aaddff",
    pink="#ffddee",
    brown="#554433",
    red="#ff0000",
    amber="#ffc000",
    green="#00ff00",
    black="#000000",
    white="#ffffff",
)


class ColormapDict(dict):
    """Dictionary storing colormapss with their names."""


colormaps: ColormapDict = ColormapDict(
    light=[colors["navy"], colors["pink"]],
    dark =[colors["blue"], colors["pink"]]
)


def hex_to_rgba(hexadecimal: str, a: float = 0.25) -> str:
    """Convert hexadecimal string to RGBA string with alpha user specified.

    Args:
        hexadecimal: Hexadecimal color including #.
        a: Transparency parameter. Defaults to :code:`0.25`.

    Returns:
        String of the color in the format "RGBA(quadruple)"
    """
    rgba = list(ImageColor.getcolor(hexadecimal, "RGBA"))
    rgba[-1] = round(255 * a)
    return f"RGBA{tuple(rgba)}"


pio.templates["scihence"] = go.layout.Template(
    layout=go.Layout(
        font={"family": "NotoSans: Regular", "size": 12},
        title_font={"family": "NotoSans: Bold", "size": 14},
        plot_bgcolor="rgba(0,0,0,0)",
    )
)
pio.templates["scihence_light"] = go.layout.Template(
    layout=go.Layout(
        font={"color": colors["navy"]},
        title_font={"color": colors["navy"]},
        colorscale={"sequential": colormaps["light"]},
        colorway=colormaps["light"],
        paper_bgcolor=colors["white"],
        xaxis={
            "gridcolor": hex_to_rgba(colors["navy"]),
            "zerolinecolor": hex_to_rgba(colors["navy"]),
        },
        yaxis={
            "gridcolor": hex_to_rgba(colors["navy"]),
            "zerolinecolor": hex_to_rgba(colors["navy"]),
        },
    )
)
px.colors.sequential.scihence_light = colormaps["light"]
pio.templates["scihence_dark"] = go.layout.Template(
    layout=go.Layout(
        font={"color": colors["blue"]},
        title_font={"color": colors["blue"]},
        colorscale={"sequential": colormaps["dark"]},
        colorway=colormaps["dark"],
        paper_bgcolor=colors["navy"],
        xaxis={
            "gridcolor": hex_to_rgba(colors["blue"]),
            "zerolinecolor": hex_to_rgba(colors["blue"]),
        },
        yaxis={
            "gridcolor": hex_to_rgba(colors["blue"]),
            "zerolinecolor": hex_to_rgba(colors["blue"]),
        },
    )
)
px.colors.sequential.scihence_dark = colormaps["dark"]


def use_style(style: str, override_mpl_rcParams: dict[str, Any] | None = None) -> None:
    """Use a Scihence visualisation style.

    Wrap `plt.style.use <https://matplotlib.org/stable/api/style_api.html#matplotlib.style.use>`_
    and plotly style templates to include Scihence styles. If not a Scihence style then the style
    passed will try to set via the usual `plt.style.use <https://matplotlib.org/stable/api/style_api
    .html#matplotlib.style.use>`_ function and plotly will do the same, with errors being
    highlighted if they cannot be found.

    Args:
        style: A style specification. Scihence styles are from {"scihence", "scihence_light",
            "scihence_dark"}.
        override_mpl_rcParams: Extra Matplotlib rcParams to set. Defaults to :code:`None`.

    Examples:
        Using base Scihence theme.
        >>> use_style("scihence")

        Using Scihence light theme.
        >>> use_style("scihence_light")

        Using Scihence dark theme with further Matplotlib alterations.
        >>> use_style("scihence_dark", {"figure.dpi": 300})
    """
    if style[:8] == "scihence":
        base_style = style == "scihence"
        pio.templates.default = f"seaborn+scihence{'' if base_style else f'+{style}'}"
        folder, ext = f"{THIS_DIR}/mplstyles/", ".mplstyle"
        THIS_MODULE.current_style = style
        style = ["seaborn-v0_8", f"{folder}scihence{ext}", f"{folder}{style}{ext}"]
        plt.style.use(style)
    else:
        try:
            pio.templates.default = style
            THIS_MODULE.current_style = None
        except ValueError:
            logger.warning(f"Unknown Plotly style: {style}.")
        try:
            plt.style.use(style)
            THIS_MODULE.current_style = None
        except OSError:
            logger.warning(f"Unknown Matplotlib style: {style}.")
    mpl.rcParams.update({} if override_mpl_rcParams is None else override_mpl_rcParams)


class ScihenceColorMap(mpl.colors.LinearSegmentedColormap):

    def to_list(self: Self) -> list[str]:
        """List the colormap's colors as rgba strings.

        Returns:
            List of colors as rgba strings.
        """
        return [f"rgba{self(i)}" for i in range(self.N)]


def get_cmap(kind: str | None = None, N: int = 256) -> mpl.colors.LinearSegmentedColormap:
    """Build a Scihence themed colormap.

    Create a Scihence matplotlib color spectrum that will match the style of the corresponding
    matplotlib style.

    Args:
        kind: Kind of color map, from {'scihence_light','scihence_dark'}, if None then will use the
            corresponding colormap of the Scihence style that has been set, and will fall back to
            the matplotlib default if it has not been set. Defaults to :code:`None`.
        N: Number of demarcations. Defaults to :code:`256`.

    Returns:
        Matplotlib color map.

    Examples:
        >>> get_cmap("scihence_dark", N=12)
        <matplotlib.colors.LinearSegmentedColormap object at 0x...>
    """
    if kind is None:
        kind = THIS_MODULE.current_style
    if kind in ["scihence_light", "scihence_dark"]:
        return ScihenceColorMap.from_list(f"{kind}", colormaps[kind.split("_")[1]], N)
    return plt.get_cmap(kind, N)
