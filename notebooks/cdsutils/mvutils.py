import pandas as pd
import os
import pyarrow as pa
import pandas as pd
import altair as alt
from IPython.display import display, clear_output
import numpy as np
from pprint import pformat as pf
from altair import datum


def read_data():
    with open(
        os.path.join(
            "/", "home", "shared", "mimic2_data", "timeseries_detailed.feather"
        ),
        "rb",
    ) as f0:
        case_data = pa.deserialize(f0.read())
        # delete case 17805 not working for unknownr reason
        del case_data[17805]
    return case_data


def clean_data(data):
    udata = data.fillna(value={"provider": "", "location": ""})

    udata["detail"] = udata["detail"].apply(
        lambda x: "" if x == None or "nan" in x or "None" in x else x
    )
    udata["provider"] = data["provider"].apply(
        lambda x: "" if x == None or "nan" in x or "None" in x else x
    )
    return udata


def aggv2s(rslts):
    _str = ""
    for r in rslts:
        if isinstance(r[1], int):
            _str = _str + "| %s:%d" % (r[0], r[1])
        elif isinstance(r[1], float):
            _str = _str + "| %s:%3.2f" % (r[0], r[1])
        else:
            _str = _str + "| %s:%s" % (r[0], r[1])
    return _str


def aggregate_events(df, c):
    rslts = (
        df[["detail", "key_value"]]
        .apply(lambda r: (r.detail, r.key_value), axis=1)
        .to_list()
    )
    rslts.sort(key=lambda x: x[0])
    tmp2 = df.drop(["detail", "key_value"], axis=1).iloc[0, :]
    tmp2.loc["sub_category"] = c
    return tmp2.append(pd.Series({"key_value": aggv2s(rslts), "detail": c}))


def aggregate_merge_events(_df):
    cats = _df.sub_category.unique()
    rslts = []
    for cat in cats:
        if cat == None:
            df = _df[_df.sub_category.isna()]
            cat = "Other"
        else:
            df = _df[_df.sub_category == cat]
        tmp = [df[df.event_time == t] for t in df.event_time.unique()]
        rslts.extend([aggregate_events(t, cat) for t in tmp])

    return pd.DataFrame(pd.concat(rslts, axis=1)).transpose()


def extract_categories(dfs, cats):
    return {c: df[df.mimic_category.isin(cats)] for c, df in dfs.items()}


def prep_data(cdata):
    vdata = {k: clean_data(v) for k, v in cdata.items()}

    chart_events = pd.concat(extract_categories(vdata, ["chart_events"]).values())
    note_events = pd.concat(extract_categories(vdata, ["note_events"]).values())
    io_events = pd.concat(extract_categories(vdata, ["io_events"]).values())
    other_events = pd.concat(
        extract_categories(
            vdata, ["med_events", "microbiology_events", "procedure_events"]
        ).values()
    )

    chart_events = aggregate_merge_events(chart_events)
    io_events = aggregate_merge_events(io_events)
    return pd.concat(
        [chart_events, note_events, io_events, other_events], axis=0, sort=False
    )


def get_graph(events):

    MARK_SIZE = 100
    selection = alt.selection_interval(bind="scales", resolve="global")
    color_provider = alt.Color("provider:N")
    cce = (
        alt.Chart(events)
        .mark_circle(opacity=0.4, stroke="black", size=MARK_SIZE, strokeWidth=1)
        .encode(
            alt.X("event_time:T", axis=alt.Axis(labelAngle=45)),
            alt.Y("sub_category:N", axis=alt.Axis(labelAngle=-25)),
            color=color_provider,
            tooltip=["key_value", "location", "provider"],
        )
        .properties(width=850, height=300)
        .add_selection(selection)
        .transform_filter(datum.mimic_category == "chart_events")
    )

    cio = (
        alt.Chart(events)
        .mark_circle(opacity=0.4, stroke="black", strokeWidth=1, size=MARK_SIZE)
        .encode(
            alt.X("event_time:T", axis=alt.Axis(labelAngle=45)),
            alt.Y("sub_category:N", axis=alt.Axis(labelAngle=-25)),
            color=color_provider,
            tooltip=["key_value", "location", "provider"],
        )
        .properties(width=850, height=300)
        .add_selection(selection)
        .transform_filter(datum.mimic_category == "io_events")
    )

    cne = (
        alt.Chart(events)
        .mark_circle(opacity=0.4, stroke="black", strokeWidth=1, size=MARK_SIZE,)
        .encode(
            alt.X("event_time:T", axis=alt.Axis(labelAngle=45)),
            alt.Y("sub_category:N", axis=alt.Axis(labelAngle=-25)),
            color=color_provider,
            tooltip=["detail", "location", "provider"],
        )
        .properties(width=850, height=125)
        .add_selection(selection)
        .transform_filter(datum.mimic_category == "note_events")
    )

    cot = (
        alt.Chart(events)
        .mark_circle(opacity=0.4, stroke="black", strokeWidth=1, size=MARK_SIZE,)
        .encode(
            alt.X("event_time:T", axis=alt.Axis(labelAngle=45)),
            alt.Y("mimic_category:N", axis=alt.Axis(labelAngle=-25)),
            color=color_provider,
            tooltip=["key_value", "detail", "provider"],
        )
        .properties(width=850, height=125)
        .add_selection(selection)
        .transform_filter(
            (datum.mimic_category == "microbiology_events")
            | (datum.mimic_category == "med_events")
            | (datum.mimic_category == "procedure_events")
        )
    )

    plt = alt.vconcat(cce, cio, cne, cot)
    return plt


def plot_case(cdata):
    return get_graph(prep_data(cdata))
