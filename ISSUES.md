### 1. Column `seed-* [cnt]` may not start counting from 0.

#### Example
File: `KSA CWIP Files/Fall 2024/CS4 - 448/CWIP-R03_20241026144050.csv`

Column: `seed-b [cnt]` 

The correct flares count is calculated using `df["seed-* [cnt]"].diff()>0` 
instead of the max column value.


### 2. Column `Altitude (m)` starts above 100 m or may have large negative values.

The altitude is not a suitable indicator to determine 
flight time (engine off - engine on) or 
air time (landing - take off).