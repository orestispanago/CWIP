### 1. `seed-* [cnt]` may not start counting from 0.

#### Example
File: `KSA CWIP Files/Fall 2024/CS4 - 448/CWIP-R03_20241026144050.csv`

Column: `seed-b [cnt]` 

To count the flares correctly, the offset has to be subracted from the max column value.


### 2. `Altitude (m)` starts above 100 m or may have large negative values.

The altitude is not a suitable indicator to determine 
flight time (engine off - engine on) or 
air time (landing - take off).


### 3. `Man - Acquire (0/1)` does not always work.

This column is described as: "Flag high when new "Zero" command is received"

There are several cases where LWC is zeroed but the flag does not change to 1.


### 4. `lat [deg]` or `lon [deg]` may contain NaN.
Coordinates may be missing in a few rows, resulting in seed events without coordinates.