from ipywidgets import interact, fixed
from IPython.display import clear_output, display, HTML
import ipywidgets as ipw
import numpy as np
import warnings
import io
import os
from markdown import markdown
import pyarrow as pa
import pandas as pd
import altair as alt
from .description import drg, table_text
from . import cases, CASE_DATADIR

# alt.renderers.enable("mimetype")

GRAPH_WIDTH = 400
GRAPH_HEIGHT = 300

em_table_out = ipw.Output()
em_counts_out = ipw.Output()
em_plots_out1 = ipw.Output(
    layout=ipw.Layout(
        width="100%",
        min_height="%dpix" % (GRAPH_HEIGHT + 50),
        max_height="%dpix" % (GRAPH_HEIGHT + 100),
        border="solid",
        align="center",
    )
)


def read_data():
    em_case_data = {}
    fails = []
    for c in cases:
        with open(os.path.join(CASE_DATADIR, "%d.feather" % c), "rb") as f0:
            try:
                em_case_data[c] = pa.deserialize(f0.read())
            except pa.ArrowInvalid:
                fails.append(c)
    return em_case_data


def get_em_case_options(em_case_data):
    em_case_options = list(em_case_data.keys())
    em_case_options.sort()
    return em_case_options


def get_em_table_options(em_case_data, case=None):
    if case == None:
        case = list(em_case_data.keys())[0]
    em_table_options = list(em_case_data[case].keys())
    em_table_options.sort()
    return em_table_options


def get_em_column_options(em_case_data, case=None):
    if case == None:
        case = list(em_case_data.keys())[0]
    em_column_options = {t: em_case_data[case][t].columns for t in em_table_options}
    for k, v in em_column_options.items():
        v.sort_values()
    return em_column_options


def plt_nominal(df, vizvar):

    tmp = df[vizvar].fillna("Missing").value_counts().to_frame().reset_index()
    c0 = (
        alt.Chart(tmp)
        .mark_bar()
        .encode(
            x=alt.X("index:N", axis=alt.Axis(labelAngle=45)),
            y=alt.Y("%s:Q" % vizvar, axis=alt.Axis(labelAngle=-25)),
        )
        .properties(width=GRAPH_WIDTH, height=GRAPH_HEIGHT)
    )
    c1 = (
        alt.Chart(df.fillna("Missing"))
        .mark_circle()
        .encode(
            x=alt.X("event_time:T", axis=alt.Axis(labelAngle=45)),
            y=alt.Y("%s:N" % vizvar, axis=alt.Axis(labelAngle=-25)),
            tooltip=["event_time:T", "%s:N" % vizvar],
        )
        .add_selection(
            alt.selection_interval(encodings=["x"], bind="scales", resolve="global")
        )
        .properties(width=GRAPH_WIDTH, height=GRAPH_HEIGHT)
    )
    return c0, c1


def plt_numeric(df, vizvar):
    c0 = (
        alt.Chart(df)
        .mark_bar()
        .encode(x=alt.X("%s:Q" % vizvar, bin=alt.Bin(maxbins=100)), y="count()")
        .properties(width=GRAPH_WIDTH, height=GRAPH_HEIGHT)
    )

    c1 = (
        alt.Chart(df)
        .mark_line(point=True)
        .encode(
            x=alt.X("event_time:T", axis=alt.Axis(labelAngle=45)),
            y=alt.Y("%s:Q" % vizvar, axis=alt.Axis(labelAngle=-25)),
            tooltip=["event_time:T", "%s:Q" % vizvar],
        )
        .add_selection(
            alt.selection_interval(encodings=["x"], bind="scales", resolve="global")
        )
        .properties(width=GRAPH_WIDTH, height=GRAPH_HEIGHT)
    )  # .configure_point( size=60)
    return c0, c1


def get_plts(df):

    if df.dtypes[em_viz_select.value] in {np.dtype("float64")}:
        c1, c2 = plt_numeric(df, em_viz_select.value)
    else:
        c1, c2 = plt_nominal(df, em_viz_select.value)
    return c1, c2


@em_plots_out1.capture(clear_output=True)
def _draw_plot(c):

    with io.StringIO() as f:
        c.save(f, format="html")
        f.seek(0)
        html1 = f.read()
    display(HTML(html1))


@em_plots_out1.capture(clear_output=True)
def draw_plot(c):
    display(c)


def plt_data():
    df = em_case_data[em_case_select.value][em_table_select.value]
    df = df[df[em_column_select.value] == em_filter_select.value]
    try:
        df = df.sort_values(by="event_time")
    except:
        pass

    c1, c2 = get_plts(df)
    c = c1 | c2
    draw_plot(c)


@em_table_out.capture(clear_output=True)
def view_table():
    df = em_case_data[em_case_select.value][em_table_select.value]
    vs = em_slice_select.value
    display(df[vs : vs + 5])


def update_view_max():
    em_slice_select.max = max(
        0, em_case_data[em_case_select.value][em_table_select.value].shape[0] - 5
    )


def update_case(change):
    case = change.new
    update_view_max()
    update_table(change)


def update_table(change):
    update_view_max()
    em_column_select.options = em_column_options[em_table_select.value]

    view_table()
    update_column(change)


def set_columns(df):

    col = em_column_select.value
    cslabels = [
        ("%s: %s" % (i[0], i[1]), i[0]) for i in df[col].value_counts().iteritems()
    ]
    cslabels.sort()

    # Update downstream choices
    em_viz_select.options = em_column_options[em_table_select.value]
    em_filter_select.options = cslabels


def update_column(change):
    df = em_case_data[em_case_select.value][em_table_select.value]
    set_columns(df)
    # display(df[col].value_counts().to_frame())
    plt_data()


def update_filter(change):
    plt_data()


def update_viz(change):
    plt_data()


def update_slice(change):
    view_table()


def init_view():
    em_case_select.value = em_case_options[0]
    em_table_select.value = em_table_options[0]
    em_column_select.options = em_column_options[em_table_select.value]
    df = em_case_data[em_case_select.value][em_table_select.value]
    set_columns(df)


def on_em_reset(b):
    init_view()


## Read in data

em_case_data = read_data()
em_case_options = get_em_case_options(em_case_data)
em_table_options = get_em_table_options(em_case_data)
em_column_options = get_em_column_options(em_case_data)

## Define Widgets


em_case_select = ipw.Dropdown(options=em_case_options)
em_table_select = ipw.Dropdown(options=em_table_options)
em_column_select = ipw.Dropdown(options=em_column_options[em_table_select.value])
em_slice_select = ipw.IntSlider(min=0, layout=ipw.Layout(width="100%"))

em_filter_select = ipw.Dropdown()
em_viz_select = ipw.Dropdown()
em_reset = ipw.Button(
    decription="reset", layout=ipw.Layout(width="100%", align="center")
)  # ,  button_style='danger')
em_reset.style.button_color = "lightgreen"

### Define label widgets

cw = ipw.Label(value="Select case")
tw = ipw.Label(value="Select table")
fw = ipw.Label(value="Select filter variable")
vw = ipw.Label(value="Select filter value")
pw = ipw.Label(value="Select plot variable")

## Set call backs
em_case_select.observe(update_case, names="value", type="change")
em_table_select.observe(update_table, names="value", type="change")
em_column_select.observe(update_column, names="value", type="change")
em_filter_select.observe(update_filter, names="value", type="change")
em_viz_select.observe(update_viz, names="value", type="change")
em_slice_select.observe(update_slice, names="value", type="change")
em_reset.on_click(on_em_reset)


def get_case_explorer():
    return ipw.TwoByTwoLayout(
        top_left=ipw.VBox(
            [
                em_reset,
                ipw.HBox(
                    [
                        ipw.VBox([cw, em_case_select]),
                        ipw.VBox([tw, em_table_select]),
                        ipw.VBox([fw, em_column_select]),
                        ipw.VBox([vw, em_filter_select]),
                        ipw.VBox([pw, em_viz_select]),
                    ]
                ),
                em_slice_select,
                em_table_out,
            ],
            layout=ipw.Layout(width="100%", min_height="200px", border="solid"),
        ),
        bottom_left=ipw.HBox([em_plots_out1]),
        layout=ipw.Layout(width="100%"),
    )


def description():
    descriptions = ipw.Tab()
    _to = em_table_options[:]
    children = [ipw.HTML(value=markdown(table_text[t])) for t in _to]
    children.append(ipw.HTML(drg))

    _to.append("DRG")
    for i in range(len(_to)):
        descriptions.set_title(i, _to[i])
    descriptions.children = children
    return descriptions
