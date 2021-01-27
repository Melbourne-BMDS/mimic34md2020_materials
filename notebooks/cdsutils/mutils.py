from jinja2 import Template
import jinja2
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

from IPython.display import display, clear_output, HTML
from ipywidgets import interactive, interact, fixed
import ipywidgets as widgets
import ipywidgets as ipw
from markdown import markdown
import networkx as nx
import ibis

dt1 = Template(
    """
<table>
{% for key, value in data.items() %}
   <tr>
        <th> {{ key }} </th>
        <td> {{ value }} </td>
   </tr>
{% endfor %}
</table>"""
)
dt2 = Template(
    """
<table>
   <tr>
   {% for key,_ in data.items() %}
        <th style="text-align:left"> {{ key }} </th>
   {% endfor %}
   </tr>
   {% for _,value in data.items() %}
        <td style="text-align:left"> {{ value }} </td>
   {% endfor %}
   </tr>
</table>"""
)

t2 = Template(
    """<table>
{%- for row in data|batch(ncols, '&nbsp;') %}
  <tr>
  {%- for column in row %}
    <td>{{ column }}</td>
  {%- endfor %}
  </tr>
{%- endfor %}
</table>"""
)

t3 = Template(
    """
<pre style="white-space: pre !important;"></pre>
{% block content %}
<h3 align="center"> {{title}} </h3>
    <img src="{{ fname }}" alt="image alt text" />
{% endblock %}
"""
)



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
