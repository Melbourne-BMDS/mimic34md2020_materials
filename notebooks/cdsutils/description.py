drg = """<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>subject_id</th>
      <th>hadm_id</th>
      <th>itemid</th>
      <th>cost_weight</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>1766</td>
      <td>28166</td>
      <td>60433</td>
      <td>0.72</td>
    </tr>
    <tr>
      <th>1</th>
      <td>2284</td>
      <td>916</td>
      <td>60614</td>
      <td>1.59</td>
    </tr>
    <tr>
      <th>2</th>
      <td>2284</td>
      <td>1121</td>
      <td>60175</td>
      <td>5.37</td>
    </tr>
    <tr>
      <th>3</th>
      <td>4727</td>
      <td>15510</td>
      <td>60002</td>
      <td>3.43</td>
    </tr>
    <tr>
      <th>4</th>
      <td>4785</td>
      <td>14029</td>
      <td>60691</td>
      <td>3.60</td>
    </tr>
    <tr>
      <th>5</th>
      <td>4785</td>
      <td>16326</td>
      <td>60691</td>
      <td>3.60</td>
    </tr>
    <tr>
      <th>6</th>
      <td>6973</td>
      <td>10690</td>
      <td>60749</td>
      <td>2.46</td>
    </tr>
    <tr>
      <th>7</th>
      <td>6973</td>
      <td>10796</td>
      <td>60144</td>
      <td>1.03</td>
    </tr>
    <tr>
      <th>8</th>
      <td>6973</td>
      <td>13386</td>
      <td>60750</td>
      <td>1.67</td>
    </tr>
    <tr>
      <th>9</th>
      <td>8292</td>
      <td>1301</td>
      <td>60017</td>
      <td>1.24</td>
    </tr>
    <tr>
      <th>10</th>
      <td>9969</td>
      <td>9434</td>
      <td>60017</td>
      <td>1.22</td>
    </tr>
    <tr>
      <th>11</th>
      <td>9969</td>
      <td>28067</td>
      <td>60002</td>
      <td>3.46</td>
    </tr>
    <tr>
      <th>12</th>
      <td>10299</td>
      <td>25055</td>
      <td>60775</td>
      <td>19.80</td>
    </tr>
    <tr>
      <th>13</th>
      <td>11401</td>
      <td>14545</td>
      <td>60648</td>
      <td>2.41</td>
    </tr>
    <tr>
      <th>14</th>
      <td>14125</td>
      <td>27857</td>
      <td>60691</td>
      <td>3.60</td>
    </tr>
    <tr>
      <th>15</th>
      <td>15239</td>
      <td>15328</td>
      <td>60002</td>
      <td>3.73</td>
    </tr>
    <tr>
      <th>16</th>
      <td>17805</td>
      <td>6832</td>
      <td>60691</td>
      <td>3.60</td>
    </tr>
    <tr>
      <th>17</th>
      <td>18514</td>
      <td>6660</td>
      <td>60778</td>
      <td>12.02</td>
    </tr>
    <tr>
      <th>18</th>
      <td>19754</td>
      <td>3097</td>
      <td>60272</td>
      <td>1.00</td>
    </tr>
    <tr>
      <th>19</th>
      <td>19754</td>
      <td>10739</td>
      <td>60783</td>
      <td>2.53</td>
    </tr>
    <tr>
      <th>20</th>
      <td>19847</td>
      <td>27993</td>
      <td>60144</td>
      <td>1.04</td>
    </tr>
    <tr>
      <th>21</th>
      <td>21372</td>
      <td>18307</td>
      <td>60829</td>
      <td>1.59</td>
    </tr>
    <tr>
      <th>22</th>
      <td>22498</td>
      <td>25008</td>
      <td>60181</td>
      <td>3.95</td>
    </tr>
    <tr>
      <th>23</th>
      <td>27421</td>
      <td>33509</td>
      <td>60335</td>
      <td>5.12</td>
    </tr>
    <tr>
      <th>24</th>
      <td>29657</td>
      <td>34701</td>
      <td>61002</td>
      <td>5.79</td>
    </tr>
    <tr>
      <th>25</th>
      <td>29839</td>
      <td>35178</td>
      <td>60038</td>
      <td>4.70</td>
    </tr>
  </tbody>
</table>
"""
table_text = {
    "census_events": """This table describes change of location events during the patient's hospitilazations, that is the admission to and discharge from a particular ICU unit. (Remember that these data are for ICU patients only).""",
    "chart_events": """## `chart_events`

This table describes when values are added into the patient's chart, usually by a nurse or a respiratory therapist. Examples of these values would include vitals (pulse, respiration rate, blood pressure) or the results of lab tests (for example, blood Potassium levels). `chart_events` have names (`label`) and are grouped into `categories`

### Key columns:

* `label`: This is the name given to the chart event. Most interesting plots would be created by filtering the data based on particular chart event names, like `Arterial BP`

* `value1`: chart events with categorical outcomes have their value stored in the `value1` column. An example of categorical values are those associated with the `label` `Behavior` which has values
    * `Angry`
    * `Anxious`
    * `Appropriate`
    * `Calm`
    * `Restless`
    * `Sedated`
    * `Sleeping`

* `value1num`: chart events with numerical outcomes have their numeric value stored in `value1num`. Example: `label` `Glucose (70-105)` has numeric values ranging from around 100 to 180.
* `value2num`: Some chart events include two values. A good example of this is blood pressure, which stores the systolic values in `value1num` and the diastolic values in `value2num`""",
    "demographic_events": """## `demographic_events`

This table records demographic dat at the time of admission, plus also describes the route for admission (e.g. `EMERGENCY ROOM ADMIT`, `ELECTIVE`)""",
    "icustay_events": """## `icustay_events`

This table provides information about when and where patients were in a particular ICU.
""",
    "io_events": """## `io_events`

This table provides information about patient input and output in terms volumes, primarily fluids.

### Key columns:

* `category`: The general category of `io_events` including `IV Infusions`, `Missing` (not specified), `PO/Gastric`, and `Tube Feeding`
* `label`: The spcecific name of an `io_event` such as `Urine Out Foley`
* `volume`: The numeric value of the volume. The units of measurement are provided in the column `volumeuom`.""",
    "lab_events": """## `lab_events`

This table provides the results of lab tests, such as blood chemistry or hematology tests. A question to consider: are these values or some of these values duplicated in `chart_events`?

### Key columns:

* `test_name`: The local institution, human name for the test
* `loinc_description`: The LOINC standard name for the test.
* `value`: categorical value results
* `valuenum`: numeric value results
* `flag`: was the test normal or abnormal. Normal test values have a missing value `None`.
* `category`: general categories of the tests
* `fluid`: tissue/fluid source for the test.""",
    "med_events": """## `med_events`

This table provides information about medications administered to the patient. Almost all the medications in the selected patients are administered with a `route` value of `IV Drip`.

### Key columns:

* `medname`: The name of the medication.
* `cgid`: The ID of the caregiver administering the medication. """,
    "microbiology_events": """## `microbiology_events`

This table records results of testing for the presence of particular bacteria and their sensitivity to particular antibiotics. The table needs to be understood in terms of three columns simultaneously, as the results are reported in terms of the presence of an organism `organism_name` and how that organism reacts to a particular antibiotic `antibiotic.` The nature of that reaction is providing in `interpretation`: the organism is either sensitive `S` (is killed by the antibiotic) or resistant `R` (is immune to the antibiotic). If no organisms are identified, all the values are missing.""",
    "note_events": """## `note_events`

This table stores all the written documentation about a patient. There are three `categories` of notes `Nursing/Other` these are the most common, `RADIOLOGY_REPORT` reports created by radiologists interpreting medical imaging procedures, `DISCHARGE_SUMMARY` the detailed note created when a patient is discharged (including when they die). Even though discharge summaries are created at the *end* of the hospitalization, in the database they are dated at the beginning of the hospitalization. Common `Other` notes are respiratory therapist notes.""",
    "procedure_events": """## `procedure_events`

This table records when billable procedures were performed, seemingly distinct from radiology procedures.

### Key columns:

* `description`: the name of the procedure.""",
}
