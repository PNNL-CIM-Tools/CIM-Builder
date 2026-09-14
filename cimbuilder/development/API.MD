


```opendss
New linecode.mtx601 nphases=3 BaseFreq=60 
~ rmatrix = (0.3465 | 0.1535 0.3375 | 0.1580 0.1560 0.3414 ) 
~ xmatrix = (1.0179 | 0.3849 1.0478 | 0.4236 0.5017 1.0348 ) 
~ cmatrix = (0 | 0 0 | 0 0 0) 
~ units=mi normamps=730
```

```python
builder = object_builder.PerLengthSequenceImpedanceBuilder()
mtx601 = builder.new_object(name = 'mtx601', conductorCount = 3)
mtx601.new_phase_impedance_data(row = 1, column = 1, fromPhase = 'A', toPhase = 'A', r = '0.3465 ohm/mile', x = '1.0179 ohm/mile')
mtx601.new_phase_impedance_data(row = 1, column = 2, fromPhase = 'A', toPhase = 'B', r = '0.1535 ohm/mile', x = '0.3849 ohm/mile')
mtx601.new_phase_impedance_data(row = 2, column = 2, fromPhase = 'B', toPhase = 'B', r = '0.3375 ohm/mile', x = '1.0478 ohm/mile')
# add remaining rows
```


