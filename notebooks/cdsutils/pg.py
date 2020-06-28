from .mutils import *


def get_mimic_connection(sqluser, sqlpass):
    return \
    ibis.postgres.connect(
    user=sqluser,
    password=sqlpass,
    host='agsfczqlcan.db.cloud.edu.au',
    port=5432,
    database='mimic')

def tview(t,start):
    display(t.limit(5, offset=start).execute())
def itview(t):
    nrows = t.count().execute()
    ipw.interact(tview, t=ipw.fixed(t), 
                 start=ipw.IntSlider(min=0, max=nrows, value=0))
def ddict(d, template=dt1):
    return template.render(data=d)




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

