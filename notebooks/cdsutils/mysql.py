from .mutils import *

sqluser = 'jovyan'
sqlpass = 'jovyan'
dbname = 'mimic'


def get_mimic_connection():
    return \
    ibis.postgres.connect(
    user=sqluser,
    password=sqlpass,
    host='agsfczqlcan.db.cloud.edu.au',
    port=5432,
    database='mimic')

def interval_in_secs(days=0, hours=0, min=0, sec=0):
    return days*24*3600+hours*3600+min*60+sec

def get_tables(conn):
    return pd.read_sql("SHOW TABLES", conn)


def get_table_names(conn):
    return [row["Tables_in_mimic2"] for _, row in get_tables(conn).iterrows()]


def get_table_descriptons(conn):
    return {t: pd.read_sql("DESCRIBE %s" % t, conn) for t in get_table_names(conn)}


def get_table_columns(table_descriptions):
    return {t: set(f["Field"]) for t, f in table_descriptions.items()}

def tview(t,start):
    display(t.limit(5, offset=start).execute())
def itview(t):
    nrows = t.count().execute()
    ipw.interact(tview, t=ipw.fixed(t), 
                 start=ipw.IntSlider(min=0, max=nrows, value=0))
def ddict(d, template=dt1):
    return template.render(data=d)


def view_dict(d, vertical=False):
    if vertical:
        return HTML(ddict(d))
    else:
        return HTML(ddict(d, template=dt2))

def dlist(l, ncols=5, sort=False):

    if sort:
        l.sort()
    return t2.render(data=l, ncols=ncols)


def get_db_graph(tbls, tbl, col):
    tables = [t for t in tbls if col in tbls[t] and t != tbl]
    g = nx.DiGraph()
    g.add_edges_from([(col, t) for t in tables])
    return g


def view_db_graph(tbls, tbl, col):
    g = get_db_graph(tbls, tbl, col)
    ag = nx.nx_pydot.to_pydot(g)
    fname = "%s_%s.png" % (tbl, col)
    ag.write_png(fname)
    return HTML(t3.render(title="(%s, %s)" % (tbl, col), fname=fname))



def view_table(table, conn, schema="mimiciii"):
    t = conn.table(table, schema=schema)
    nrows = t.count().execute()
    @interact(t=fixed(t), num=ipw.IntSlider(min=5, max=20), 
              start=ipw.IntSlider(min=0, max=nrows))
    def _view_table(t, num, start=0):
        return t.limit(num, offset=start).execute()
    
def explore_table(conn, exclude="chartevents_", schema="mimiciii"):
    tables = [t for t in conn.list_tables(schema=schema) if exclude not in t]
    interact(view_table, table=tables, conn= fixed(conn))

def _explore_table(table, conn, schema="mimiciii"):

    t = conn.table(table, schema=schema)
    nrows = t.count().execute()

    slice_start = ipw.IntSlider(min=0, max=nrows, layout=ipw.Layout(width="50%"))
    slice_size = ipw.IntSlider(min=5, max=20, layout=ipw.Layout(width="50%"))

    table_out = ipw.Output(layout=ipw.Layout(width="100%"))
    @table_out.capture(clear_output=True)
    def view_table(change):
        df = t.limit(slice_size.value, offset=slice_start.value).execute()
        display(df)
    view_table(None)
   

## Set call backs
    slice_start.observe(view_table, names="value", type="change")
    slice_size.observe(view_table, names="value", type="change")

    vw = ipw.Label(value="Select Slice Start")
    pw = ipw.Label(value="Select Slice Size")

    return ipw.TwoByTwoLayout(
        top_left = ipw.VBox([ipw.VBox([vw, slice_start]),
                             ipw.VBox([pw, slice_size])]),
        bottom_left = table_out
        )

