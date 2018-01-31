# liwc-py

![RTD](https://media.readthedocs.org/static/projects/badges/passing.svg)

Requires a version of the LIWC dictionary in .dic format. Still very much work in process. Results might differ (albeit marginally) from the commercial LIWC software.

For the full documentation [look here](http://pyliwc.readthedocs.io/en/latest/)
## Installation

```
pipenv install -e git+https://github.com/dfederschmidt/pyliwc#egg=pyliwc
```


## Usage 

### Initialization

```python
liwc = LIWC("./LIWC2015.dic")
```

### Process Text

```python
liwc = LIWC("./LIWC2015.dic")
liwc_scores = liwc.process_text("My text to be analyzed")
```

### Process Pandas Series

```python
import pandas as pd 

liwc = LIWC("./LIWC2015.dic")
series = pd.Series(["Hello World", "Good Morning"])

liwc.process_series(series)

# OR (in case of large series)

liwc.process_series_mp(series)

```