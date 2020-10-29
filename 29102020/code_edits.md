### Edits to Code

There are two code edits that I made:

1. The first is related to computing ages. This is probably related to MIMIC III's large time shifts. (May not be necessary from discussion below.)
1. Pandas can read gzipped file, which will save you a lot of disk space, if you keep everything compressed.

```Python
def compute_age(stay):
    factor = 3600.0*24*365.24 * np.timedelta64(1,'s')
    age = (stay.INTIME.to_datetime64() - stay.DOB.to_datetime64()) / factor
    if age < 0:
        age = 90.0
    return age

def add_age_to_icustays(stays):
    stays['AGE'] = stays.apply(compute_age, axis=1)
    return stays
```

```Python
def dataframe_from_csv(path, header=0, index_col=0):
    if os.path.exists(path+".gz"):
        path = path + ".gz"
    return pd.read_csv(path, header=header, index_col=index_col)
```


### What happens if we run the code?

```bash
python extract_subjects.py /Users/brian/Downloads/mimic-iii-clinical-database-1.4 /tmp/mimic3 -p ../resources/hcup_ccs_2015_definitions.yaml
transfers_START: 61533 58976 46520
stays_START: 61532 57786 46476
transfers_REMOVE PATIENTS AGE < 18: 53333 50743 38552
stays_REMOVE PATIENTS AGE < 18: 53332 49695 38512
stransfers_done
stays_done
all_diagnoses_done
diagnosis_counts_done
all_procedures_done
procedures_counts_done
sys:1: DtypeWarning: Columns (11) have mixed types.Specify dtype option on import or set low_memory=False.
/Users/brian/opt/anaconda3/lib/python3.8/site-packages/numpy/lib/arraysetops.py:569: FutureWarning: elementwise comparison failed; returning scalar instead, but in the future will perform elementwise comparison
  mask |= (ar1 == a)
all_prescriptions_done
extract_subjects.py:88: YAMLLoadWarning: calling yaml.load() without Loader=... is deprecated, as the default Loader is unsafe. Please read https://msg.pyyaml.org/load for full details.
  phenotypes = add_hcup_ccs_2015_groups(diagnoses, yaml.load(open(args.phenotype_definitions, 'r')))
Traceback (most recent call last):
  File "extract_subjects.py", line 89, in <module>
    make_phenotype_label_matrix(phenotypes, stays).to_csv(os.path.join(args.output_path, 'phenotype_labels.csv'),
  File "/Users/brian/Code2/MIMIC-III_ICU_Readmission_Analysis/mimic3-readmission/scripts/mimic3benchmark/preprocessing.py", line 75, in make_phenotype_label_matrix
    phenotypes = phenotypes.loc[stays.ICUSTAY_ID.sort_values()]
  File "/Users/brian/opt/anaconda3/lib/python3.8/site-packages/pandas/core/indexing.py", line 1768, in __getitem__
    return self._getitem_axis(maybe_callable, axis=axis)
  File "/Users/brian/opt/anaconda3/lib/python3.8/site-packages/pandas/core/indexing.py", line 1954, in _getitem_axis
    return self._getitem_iterable(key, axis=axis)
  File "/Users/brian/opt/anaconda3/lib/python3.8/site-packages/pandas/core/indexing.py", line 1595, in _getitem_iterable
    keyarr, indexer = self._get_listlike_indexer(key, axis, raise_missing=False)
  File "/Users/brian/opt/anaconda3/lib/python3.8/site-packages/pandas/core/indexing.py", line 1552, in _get_listlike_indexer
    self._validate_read_indexer(
  File "/Users/brian/opt/anaconda3/lib/python3.8/site-packages/pandas/core/indexing.py", line 1654, in _validate_read_indexer
    raise KeyError(
KeyError: 'Passing list-likes to .loc or [] with any missing labels is no longer supported, see https://pandas.pydata.org/pandas-docs/stable/user_guide/indexing.html#deprecate-loc-reindex-listlike'
(base) bucksaw:scripts brian$

```


### What went wrong?

### [Next steps](customizing_environment.md)
