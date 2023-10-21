# MASO Software Development Kit (SDK)

### Install using pip

```shell
pip install maso-sdk
```

### Get sub-array, or parameter from existing dataset

```python
from masosdk.Dataset import Dataset

# Both API_TOKEN and dataset id can be copied from MASO
API_TOKEN = ''
DATASET_ID = 0

dataset = Dataset(API_TOKEN, id=DATASET_ID)

# get a sub array of the dataset
# pass a list to define the slice of an array, the -1 value stands for NumPy double colon
data = dataset.get_array([-1, -1])

# get a parameter
parameter = dataset.get_parameter('VisuCoreDim')
```

### Create dataset and upload array

```python
import numpy as np
from masosdk.Dataset import Dataset

# Both API_TOKEN and dataset id can be copied from MASO
API_TOKEN = ''

file_name = 'test.npy'

# create dataset in MASO by providing the name and shape kwargs
dataset = Dataset(API_TOKEN, name=file_name, shape=[256, 256, 10])

data = np.zeros((256, 256))

data[30:80, 30:80] = 1

# upload array
# pass a list to define the slice of an array, the -1 value stands for NumPy double colon
dataset.upload_array(data, [-1, -1, 4])
```

### Delete a user dataset

**It is possible to delete only user datasets.**

```python

import numpy as np
from masosdk.Dataset import Dataset

# Both API_TOKEN and dataset id can be copied from MASO
API_TOKEN = ''
DATASET_ID = 0

dataset = Dataset(API_TOKEN, id=DATASET_ID)

# delete dataset
dataset.delete()
```