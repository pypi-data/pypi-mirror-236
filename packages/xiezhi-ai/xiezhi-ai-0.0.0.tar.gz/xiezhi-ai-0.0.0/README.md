### xiezhi: The First One-dimensional Anomaly Detection Tool

### Install

pip install xiezhi-ai

### Usage
The inputs include data, beta, and alpha.

data: The current version only supports the detection of one-dimensional data, so the data should be a list. 

beta and alpha are set between 0 and 1 and beta is smaller than alpha, if there are few anomalies, beta and alpha can be set close to 1; 
otherwize, it should be set close to 0.5. If the number of anomalies are unknown, then both of beta and alpha should be close to 0.5. 

Below is the example:

```python
import xiezhi as xz

data=[1,2,3,4,5,6,7,9,10,20] # here 20 is the anomaly
benign_data=xz(data,0.7,0.9) # xiezhi will return the benign data
```