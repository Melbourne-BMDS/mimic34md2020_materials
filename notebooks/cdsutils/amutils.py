from ipywidgets import interact, fixed, TwoByTwoLayout
from IPython.display import clear_output, display, HTML
import ipywidgets as ipw
import numpy as np
import warnings
import io
import os
import pyarrow as pa
import pandas as pd
import altair as alt

DATADIR = "/home/shared/mimic_data/case_level"
GRAPH_WIDTH = 400
GRAPH_HEIGHT = 300

cases = (
    21372,
    14125,
    22498,
    10299,
    2284,
    15239,
    4727,
    8292,
    9969,
    17805,
    1766,
    29839,
    29657,
    11401,
    19754,
    4785,
    19847,
    6973,
    27421,
    18514,
)


debug_out = ipw.Output()
_debug = ipw.Label(value="")


def du(msg):
    _debug.value = _debug.value + " " + msg


def read_data():
    case_data = {}
    fails = []
    for c in cases:
        with open(os.path.join(DATADIR, "%d.feather" % c), "rb") as f0:
            try:
                case_data[c] = pa.deserialize(f0.read())
            except pa.ArrowInvalid:
                fails.append(c)
    return case_data


def get_case_options(case_data):
    case_options = list(case_data.keys())
    case_options.sort()
    return case_options


def get_table_options(case_data, case=None):
    if case == None:
        case = list(case_data.keys())[0]
    table_options = list(case_data[case].keys())
    table_options.sort()
    return table_options


def get_column_options(case_data, case=None):
    if case == None:
        case = list(case_data.keys())[0]
    column_options = {t: case_data[case][t].columns for t in table_options}
    for k, v in column_options.items():
        v.sort_values()
    return column_options


def plt_nominal(df, vizvar):

    tmp = df[vizvar].fillna("Missing").value_counts().to_frame().reset_index()
    c0 = (
        alt.Chart(tmp)
        .mark_bar()
        .encode(x="index", y=vizvar)
        .properties(width=GRAPH_WIDTH, height=GRAPH_HEIGHT)
    )
    c1 = (
        alt.Chart(df.fillna("Missing"))
        .mark_circle()
        .encode(x="event_time:T", y=vizvar, tooltip=["event_time:T", "%s:N" % vizvar])
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
        .encode(x=alt.X("%s:Q" % vizvar, bin=True), y="count()")
        .properties(width=GRAPH_WIDTH, height=GRAPH_HEIGHT)
    )

    c1 = (
        alt.Chart(df)
        .mark_line(point=True)
        .encode(
            x="event_time:T",
            y="%s:Q" % (vizvar),
            tooltip=["event_time:T", "%s:Q" % vizvar],
        )
        .add_selection(
            alt.selection_interval(encodings=["x"], bind="scales", resolve="global")
        )
        .properties(width=GRAPH_WIDTH, height=GRAPH_HEIGHT)
    )  # .configure_point( size=60)
    return c0, c1


def get_plts():
    df = case_data[case_select.value][table_select.value]
    df = df[df[column_select.value] == filter_select.value]

    if df.dtypes[viz_select.value] in {np.dtype("float64")}:
        c1, c2 = plt_numeric(df, viz_select.value)
    else:
        c1, c2 = plt_nominal(df, viz_select.value)
    return c1, c2


def draw_plot(c):
    with io.StringIO() as f:
        c.save(f, format="html")
        f.seek(0)
        html1 = f.read()
    with plots_out1:
        display(HTML(html1))


def plt_data():

    c1, c2 = get_plts()
    c = c1 | c2
    draw_plot(c)


def view_table():
    df = case_data[case_select.value][table_select.value]
    vs = slice_select.value
    with table_out:
        clear_output()
        display(df[vs : vs + 5])


def comp_view_max():
    return max(0, case_data[case_select.value][table_select.value].shape[0] - 5)


def update_view_max():
    slice_select.max = comp_view_max()


def update_case(change):
    case = change.new
    update_view_max()
    update_table(change)
    # view_table()
    # plt_data()


def update_table(change):
    update_view_max()
    with debug_out:
        column_select.options = column_options[table_select.value]

    view_table()
    update_column(change)


def set_columns():
    df = case_data[case_select.value][table_select.value]
    col = column_select.value
    cslabels = [
        ("%s: %s" % (i[0], i[1]), i[0]) for i in df[col].value_counts().iteritems()
    ]
    cslabels.sort()

    # Update downstream choices
    viz_select.options = column_options[table_select.value]
    filter_select.options = cslabels


def update_column(change):

    set_columns()
    with counts_out:
        display(df[col].value_counts().to_frame())
    plt_data()


def update_filter(change):
    plt_data()


def update_viz(change):
    plt_data()


def update_slice(change):
    view_table()


def init_view():
    case_select.value = case_options[0]
    table_select.value = table_options[0]
    column_select.options = column_options[table_select.value]
    set_columns()
    view_table()
    plt_data()


def on_reset(b):
    init_view()


## Read in data

case_data = read_data()
case_options = get_case_options(case_data)
table_options = get_table_options(case_data)
column_options = get_column_options(case_data)

## Define Widgets

table_out = ipw.Output()
counts_out = ipw.Output()
plots_out1 = ipw.Output(
    layout=ipw.Layout(
        width="100%",
        min_height="%dpix" % (GRAPH_HEIGHT + 50),
        max_height="%dpix" % (GRAPH_HEIGHT + 100),
        border="solid",
        align="center",
    )
)

case_select = ipw.Dropdown(options=case_options)
table_select = ipw.Dropdown(options=table_options)
column_select = ipw.Dropdown(options=column_options[table_select.value])
slice_select = ipw.IntSlider(min=0, layout=ipw.Layout(width="100%"))

filter_select = ipw.Dropdown()
viz_select = ipw.Dropdown()
reset = ipw.Button(
    decription="Reset", layout=ipw.Layout(width="100%", align="center")
)  # ,  button_style='danger')
reset.style.button_color = "lightgreen"

### Define label widgets

cw = ipw.Label(value="Select case")
tw = ipw.Label(value="Select table")
fw = ipw.Label(value="Select filter variable")
vw = ipw.Label(value="Select filter value")
pw = ipw.Label(value="Select plot variable")

## Set call backs
case_select.observe(update_case, names="value", type="change")
table_select.observe(update_table, names="value", type="change")
column_select.observe(update_column, names="value", type="change")
filter_select.observe(update_filter, names="value", type="change")
viz_select.observe(update_viz, names="value", type="change")
slice_select.observe(update_slice, names="value", type="change")
reset.on_click(on_reset)

explore_mimic = TwoByTwoLayout(
    top_left=ipw.VBox(
        [
            reset,
            ipw.HBox(
                [
                    ipw.VBox([cw, case_select]),
                    ipw.VBox([tw, table_select]),
                    ipw.VBox([fw, column_select]),
                    ipw.VBox([vw, filter_select]),
                    ipw.VBox([pw, viz_select]),
                ]
            ),
            slice_select,
            table_out,
        ],
        layout=ipw.Layout(width="100%", min_height="200px", border="solid"),
    ),
    bottom_left=ipw.HBox([plots_out1]),
    layout=ipw.Layout(width="100%"),
)
