# easyGauge

Reusable Streamlit component for quickly deploying Plotly indicator gauge charts.

## Installation instructions

```sh
pip install easyGauge
```

## Usage instructions

```python
import streamlit as st
from easyGauge import easyGauge


number = st.number_input('Insert a number')
easyGauge(number, gSize="FULL", sFix="%")


col1, col2 = st.columns(2)

with col1:
    easyGauge(.55, gSize="MED")

with col2:
    easyGauge(.91, gSize="MED")


col4, col5, col6 = st.columns(3)

with col4:
    easyGauge(
        .49, 
        sFix="%", 
        gSize="MED", 
        gcLow='#6BBEF2', 
        gcMid='#0597F2', 
        gcHigh='#056CF2'
    )

with col5:
    easyGauge(
        .85, 
        sFix="%", 
        gSize="LRG", 
        gcLow='#6BBEF2', 
        gcMid='#0597F2', 
        gcHigh='#056CF2'
    )

with col6:
    easyGauge(
        .63, 
        sFix="%", 
        gSize="MED", 
        gcLow='#6BBEF2', 
        gcMid='#0597F2', 
        gcHigh='#056CF2'
    )