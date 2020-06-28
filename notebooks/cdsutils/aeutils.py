from IPython.display import clear_output, display, HTML
import ipywidgets as ipw
import numpy as np
import io
import os
import pyarrow as pa
import pandas as pd
import altair as alt
from collections import defaultdict
from .description import drg, table_text
from . import cases, CASE_DATADIR
from markdown import markdown

# alt.renderers.enable("mimetype")

_debug = ipw.Label(value="")


def du(msg):
    _debug.value = _debug.value + " " + msg


GRAPH_WIDTH = 800
GRAPH_HEIGHT = 300
global_debugs = {}

table_out = ipw.Output()
counts_out = ipw.Output()
histo_out = ipw.Output(
    layout=ipw.Layout(
        width="100%",
        min_height="%dpix" % (GRAPH_HEIGHT + 50),
        max_height="%dpix" % (GRAPH_HEIGHT + 100),
        border="solid",
        align="center",
    )
)


def read_data():
    def concat_data(case_data):
        dw = defaultdict(list)
        for k, v in case_data.items():
            for kk, vv in v.items():
                dw[kk].append(vv)
        return {k: pd.concat(v) for k, v in dw.items()}

    case_data = {}
    fails = []
    for c in cases:
        with open(os.path.join(CASE_DATADIR, "%d.feather" % c), "rb") as f0:
            try:
                case_data[c] = pa.deserialize(f0.read())
            except pa.ArrowInvalid:
                fails.append(c)
    return concat_data(case_data)


def get_case_options(data, table=None):
    if table == None:
        table = list(data.keys())[0]
    options = list(data[table].subject_id.unique())
    options.sort()
    return options


def get_table_options(data):

    table_options = list(data.keys())
    table_options.sort()
    return table_options


def get_column_options(data):
    column_options = {t: list(data[t].columns) for t in data.keys()}
    for k, v in column_options.items():
        v.sort()
    return column_options


def plt_nominal(df, vizvar):
    if fillna.value == "Yes":
        tmp = df.fillna("Missing")
    else:
        tmp = df

    tmp = {
        s: tmp[tmp.subject_id == s][vizvar]
        .value_counts()
        .to_frame()
        .reset_index()
        .rename(columns={"index": vizvar, vizvar: "counts"})
        for s in df.subject_id.unique()
    }
    for k, v in tmp.items():
        v["subject_id"] = k
    try:
        tmp = pd.concat(tmp.values())
    except:
        tmp = pd.DataFrame(columns=["subject_id", "counts", vizvar])

    c = (
        alt.Chart(tmp)
        .mark_bar()
        .encode(
            x="sum(counts):Q",
            y=alt.Y("%s:N" % vizvar, axis=alt.Axis(labelAngle=45)),
            color=alt.Color("subject_id:N"),
        )
        .properties(width=GRAPH_WIDTH, height=GRAPH_HEIGHT)
    )
    return c


def plt_numeric(df, vizvar):
    du("in plt_numeric")
    c0 = (
        alt.Chart(df)
        .transform_filter("isValid(datum.subject_id)")
        .transform_density(
            vizvar, groupby=["subject_id"], as_=[vizvar, "density"], counts=False
        )
        .mark_area(opacity=0.3)
        .encode(x="%s:Q" % vizvar, y="density:Q", color=alt.Color("subject_id:N"))
        .properties(width=GRAPH_WIDTH, height=GRAPH_HEIGHT)
    )
    return c0


def tidy_data(data, cases, dfilter, dfilter_value, pop):
    tmp = data[data["subject_id"].isin(cases)]
    if dfilter_value:
        tmp = tmp[tmp[dfilter] == dfilter_value]
    return tmp[["subject_id", pop]]


def get_plts(df):

    du("cat_qua=%s" % cat_qua.value)
    # if cat_qua.value == "Quantitative":
    if df.dtypes[viz_select.value] in {np.dtype("float64")}:
        du("plotting numeric")
        return plt_numeric(df, viz_select.value)
    else:
        return plt_nominal(df, viz_select.value)


@histo_out.capture(clear_output=True)
def draw_plot(c):
    display(c)


@histo_out.capture(clear_output=True)
def _draw_plot(c):
    with io.StringIO() as f:
        c.save(f, format="html")
        f.seek(0)
        html1 = f.read()
    display(HTML(html1))


def plt_data():
    df = tidy_data(
        all_data[table_select.value],
        case_select.value,
        column_select.value,
        filter_select.value,
        viz_select.value,
    )
    c = get_plts(df)
    draw_plot(c)


@table_out.capture(clear_output=True)
def view_table():
    df = all_data[table_select.value]
    df = df[df.subject_id.isin(case_select.value)]
    vs = slice_select.value
    display(df[vs : vs + 5])


def comp_view_max():
    df = all_data[table_select.value]
    return max(0, df[df.subject_id.isin(case_select.value)].shape[0] - 5)


def update_view_max():
    slice_select.max = comp_view_max()


def update_table(change):
    table = change.new
    update_case(change)
    # view_table()
    # plt_data()


def update_case(change):
    update_view_max()
    column_select.options = column_options[table_select.value]
    view_table()
    update_column(change)


def set_columns():
    df = all_data[table_select.value]
    df = df[df.subject_id.isin(case_select.value)]
    col = column_select.value
    cslabels = [
        ("%s: %s" % (i[0], i[1]), i[0]) for i in df[col].value_counts().iteritems()
    ]
    cslabels.sort()

    # Update downstream choices
    viz_select.options = column_options[table_select.value]
    cslabels.insert(0, ("None", ""))
    filter_select.options = cslabels


def update_column(change):
    set_columns()
    plt_data()


def update_filter(change):
    plt_data()


def update_viz(change):
    plt_data()


def update_slice(change):
    view_table()


def init_view():
    case_select.value = [case_options[0]]
    table_select.value = table_options[0]
    column_select.options = column_options[table_select.value]
    set_columns()


def on_reset(b):
    init_view()


def update_fill(change):
    plt_data()


def update_mode(change):
    plt_data()


## Readin Data

all_data = read_data()
table_options = get_table_options(all_data)
case_options = get_case_options(all_data)
column_options = get_column_options(all_data)

## Define Widgets


case_select = ipw.SelectMultiple(options=case_options, value=[case_options[0]])
table_select = ipw.Dropdown(options=table_options)
column_select = ipw.Dropdown(options=column_options[table_select.value])
slice_select = ipw.IntSlider(min=0, layout=ipw.Layout(width="100%"))

filter_select = ipw.Dropdown()
viz_select = ipw.Dropdown()
reset = ipw.Button(
    decription="Reset", layout=ipw.Layout(width="100%", align="center")
)  # ,  button_style='danger')
reset.style.button_color = "lightgreen"
fillna = ipw.ToggleButtons(
    options=["Yes", "No"],
    description="Missing",
    disabled=False,
    button_style="",  # 'success', 'info', 'warning', 'danger' or ''
    tooltips=[
        'Missing categorial values will be replaced with "Missing"',
        "Missing values will be ignored",
    ],
    #     icons=['check'] * 3
)
cat_qua = ipw.ToggleButtons(
    options=["Categorical", "Quantitative"],
    description="",
    disabled=False,
    button_style="",  # 'success', 'info', 'warning', 'danger' or ''
    tooltips=["Plot data as categorical values", "Plot data as quantitative values"],
    #     icons=['check'] * 3
)
### Define label widgets

cw = ipw.Label(value="Select case")
tw = ipw.Label(value="Select table")
fw = ipw.Label(value="Select filter variable")
vw = ipw.Label(value="Select filter value")
pw = ipw.Label(value="Select plot variable")

## Set call backs
table_select.observe(update_table, names="value", type="change")
case_select.observe(update_case, names="value", type="change")
column_select.observe(update_column, names="value", type="change")
filter_select.observe(update_filter, names="value", type="change")
viz_select.observe(update_viz, names="value", type="change")
slice_select.observe(update_slice, names="value", type="change")
reset.on_click(on_reset)
fillna.observe(update_fill, names="value", type="change")
cat_qua.observe(update_mode, names="value", type="change")


def get_explorer():
    return ipw.TwoByTwoLayout(
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
        bottom_left=ipw.HBox(
            [ipw.VBox([ipw.HBox([fillna]), histo_out])], layout=ipw.Layout(width="100%")
        ),
    )


def make_description():
    descriptions = ipw.Tab()
    children = [ipw.HTML(value=markdown(table_text[t])) for t in table_options]
    children.append(ipw.HTML(drg))
    tmp = table_options[:]
    tmp.append("DRG")
    for i in range(len(tmp)):
        descriptions.set_title(i, tmp[i])
    descriptions.children = children
    return descriptions
