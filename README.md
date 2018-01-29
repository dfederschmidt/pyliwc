# liwc-py

Requires a version of the LIWC dictionary in .dic format.

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