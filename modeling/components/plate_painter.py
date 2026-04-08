"""Interactive 96-well plate painter Streamlit component."""

import os
import streamlit.components.v1 as components

_FRONTEND_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                             "_plate_frontend")

_component_func = components.declare_component("plate_painter",
                                               path=_FRONTEND_DIR)


def plate_painter(plate_mrna, plate_cells, groups, cell_types,
                  paint_mode="mrna", active_idx=0, eraser=False,
                  group_colors=None, cell_colors=None,
                  plate_version=0, key=None):
    """Render an interactive 96-well plate for click-to-paint.

    Returns dict with plate_mrna and plate_cells after user clicks,
    or None before any interaction.
    """
    return _component_func(
        plate_mrna=list(plate_mrna),
        plate_cells=list(plate_cells),
        groups=[{"name": g.get("name", ""), "type": g.get("type", "")}
                for g in groups],
        cell_types=[{"name": ct.get("name", "")} for ct in cell_types],
        paint_mode=str(paint_mode),
        active_idx=int(active_idx),
        eraser=bool(eraser),
        group_colors=list(group_colors or []),
        cell_colors=list(cell_colors or []),
        plate_version=int(plate_version),
        key=key,
        default=None,
    )
