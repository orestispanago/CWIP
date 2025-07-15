
# CWIP file headers

## FIN file

| **Header**                       | **Units** | **Description**                                      |
|----------------------------------|-----------|------------------------------------------------------|
| $Fin-2                           |           | LWC with Dynamic DryAirTerm applied                  |
| LWC, Dry Air Term                | g/m³      | Dynamic Dry Air Term. Constantly updated from sensor |
| LWC, Power                       | W         | Power, Dynamic DAT                                   |
| Airspeed                         | knots     | TAS in knots                                         |
| Altitude                         | ft        | pressure altitude in feet                            |
| Altitude                         | m         | pressure altitude in meters                          |
| Wire Temp                        | °C        | typically 150C                                       |
| Sideslip Angle                   | deg       | Sideslip Degrees, Corrected                          |
| Sideslip dP                      | mb        | Sideslip differential pressure (+-25mb)              |
| P_Xducer Temp                    | °C        | Pressure Transducer Temp(C)                          |
| Attack dP                        | mb        | Angle of Attack differential Pressure(+-25 mb)       |
| Attack Angle                     | deg       | Angle of Attack (+- 20 deg) from Lenschow, corrected |
| Pitot dP                         | mb        | Differential Pressure Transducer                     |
| Static Pressure                  | mb        | Static Pressure                                      |
| RH                               | %         | Relative Humidity                                    |
| Ambient Temperature              | °C        | Ambient Temperature                                  |
| LWC Slave                        | V         | Slave Coil (mid bridge)/ Return                      |
| LWC Master                       | V         | Master coil (mid bridge) vs Return                   |
| LWC Error                        | V         | Bridge Middle vs Temp Set Point                      |
| LWC Current                      | A         | Bridge Top vs Bridge Middle                          |
| LWC Voltage                      | V         | Bridge Top                                           |
| Fin Fwd Edge Temp                | °C        | Leading edge temperature                             |
| Anti-Ice Relay Monitor           | V         | Anti Ice relay/voltage monitor                       |
| TAS                              | m/s       | Dyn True Air Speed                                   |
| Static Pressure                  | mb        | Dyn Static Pressure                                  |
| Pitot dP                         | mb        | Dyn Pitot Differential Pressure                      |
| Ambient Temperature              | °C        | Dyn Measured Ambient Temperature                     |
| Ambient Temperature, Corrected   | °C        | Dyn Corrected Ambient Temperature                    |
| Air Density                      | kg/m³     | Calculated                                           |
| Man, Acquire                     | 0/1       | Flag high when new "Zero" command is received        |
| Man, LWC                         | g/m³      | LWC Calculated with Manual Dry Air Term              |
| Man, DAT                         | g/m³      | Manually Acquired Dry Air Term                       |
| Man, Power                       | W         | LWC Power                                            |
| Man, TAS                         | m/s       | Manually Acquired TAS                                |
| Man, Altitude                    | mb        | Manually Acquired Altitude                           |
| Man, Pitot dP                    | mb        | Manually Acquired Pitot differential pressure        |
| Man, Temp Ambient                | °C        | Manually Acquired Measured Ambient Temperature       |
| Man, Temp Corrected              | °C        | Manual Corrected Ambient Temperature                 |
| Man, Air Den                     | kg/m³     | Calculated                                           |
| Fixed, LWC                       | g/m³      | LWC calculated with fixed Dry Air Term               |
| Fixed, DAT                       | g/m³      | Dry Air Term with fixed TAS, Alt, and Temp values    |
| Fixed, Power                     | W         | LWC Power                                            |
| Fixed, TAS                       | m/s       | from "Get Data-1" value                              |
| Fixed, Pressure                  | mb        | from "Get Data-1" value                              |
| Fixed, Temperature               | °C        | from "Get Data-1" value                              |
| Fixed, Air Den                   | kg/m³     | Calculated from Fixed parameters                     |
| not used                         |           | not used                                             |
| Raw, Sideslip dP                 | count     | Sideslip Angle differential pressure                 |
| Raw, P_Xducer Temp               | count     | Pressure Transducer Temperature                      |
| Raw, Attack dP                   | count     | Attack Angle differential pressure                   |
| Not Used                         |           | Not used as analog output                            |
| Raw, Pitot dP                    | count     | Pitot differential pressure                          |
| Raw, Static Pressure             | count     | Static Pressure                                      |
| Raw, RH                          | count     | Relative Humidity                                    |
| Raw, Ambient Temp                | count     | Ambient Temperature                                  |
| Raw, Slave Coil V                | count     | Slave coil vs Return                                 |
| Raw, Master Coil V               | count     | Master coil vs + vs Return                           |
| Raw, Master Error V              | count     | Bridge Middle - Temp Set Point                       |
| Raw, Master Current              | count     | Bridge Top - Bridge Middle                           |
| Raw, Master Voltage              | count     | Bridge Top                                           |
| Raw, Fin Fwd Edge Temp           | count     | Fin Leading edge temperature                         |
| Raw, Anti-Ice Voltage            | count     | Anti-ice relay voltage monitor                       |
| LWC Pwr On/Off                   |           | Indicator, Hotwire Enabled (1=yes, 0=no)             |
| AI Pwr On/Off                    |           | Indicator, Anti-Ice (1=Enabled, 0=Disabled)          |
| Slave Failure?                   |           | Indicator, Slave-coil monitor (0 = good, 1 = bad)    |
| IChecksum (CS)                   | hex       | 16-bit checksum in hexadecimal (e.g., 2FD0)          |


## ADC file

| **Header**      | **Description**                                          |
|---------------- |----------------------------------------------------------|
| Time            | UTC time in seconds since midnight                       |
| System ID       | 3 digit system ID                                        |
| Update Rate (Hz)| Update Rate as defined in configuration                  |
| DATE            | Date comes through as a 1 for the column                 |
| TIME            | Time, seconds since instrument power on                  |
| C0              | Event Counter 0, 000 to 9999                             |
| C0F             | Counter0 flag goes from 0 to 1 for a configured duration |
| C1              | Event Counter 1, 000 to 9999                             |
| C1F             | Counter1 flag goes from 0 to 1 for a configured duration |
| F0              | Flag0, digital input port can be 1 or 0                  |
| F1              | Flag1, digital input port can be 1 or 0                  |
| F2              | Flag2, digital input port can be 1 or 0                  |
| F3              | Flag3, digital input port can be 1 or 0                  |
| N_ADC           | Number of ADC Channels, 1 to 16                          |
| AD0             | ADC Channel 0 data in Volts                              |
| AD1             | ADC Channel 1 data in Volts                              |
| AD2…AD15        | Remainder of ADC Channels data in Volts                  |
| CS              | 16-bit Check Sum in hex                                  |


## WIND file

| **Data Type** | **Header**        | **Units**       | **Description**                             |
|---------------|-------------------|-----------------|---------------------------------------------|
|**VN-300**     | time              | s               | seconds since 0900 UTC Jan 1st, 1970 × 1000 |
|               | GPStime [nsec]    | ns              | Nanoseconds since 0000 UTC Jan 6th, 1980    |
|               | lat [deg]         | decimal degrees | Latitude                                    |
|               | lon [deg]         | decimal degrees | Longitude                                   |
|               | gps_alt [m]       | meters          | GPS Altitude                                |
|               | gps_gs [m/s]      | m/s             | GPS Ground speed                            |
|               | gps_track [deg]   | degrees         | GPS Track                                   |
|               | yaw [deg]         | degrees         | Yaw Attitude (psi)                          |
|               | pitch [deg]       | degrees         | Pitch Attitude (theta)                      |
|               | roll [deg]        | degrees         | Roll Attitude (phi)                         |
|               | vel_x [m/s]       | m/s             | Velocity x                                  |
|               | vel_y [m/s]       | m/s             | Velocity y                                  |
|               | vel_z [m/s]       | m/s             | Velocity z                                  |
|               | accel_x [m/s²]    | m/s²            | Acceleration x                              |
|               | accel_y [m/s²]    | m/s²            | Acceleration y                              |
|               | accel_z [m/s²]    | m/s²            | Acceleration z                              |
|               | ins_status        | binary          | INS Status                                  |
| **Fin**       | temp_amb [C]      | °C              | Temperature, Ambient                        |
|               | temp_corr [C]     | °C              | Temperature, Corrected                      |
|               | rh [%]            | %               | Relative Humidity                           |
|               | pres_amb [mb]     | mb              | Pressure, Ambient                           |
|               | pres_alt [m]      | m               | Pressure Altitude                           |
|               | tas [m/s]         | m/s             | True Air Speed                              |
|               | attack [deg]      | degrees         | Attack Angle                                |
|               | sideslip [deg]    | degrees         | Sideslip Angle                              |
|               | lwc [g/m³]        | g/m³            | Liquid Water Content                        |
|               | lwc_dat [g/m³]    | g/m³            | LWC Dry Air Term                            |
|               | fin_tmp [C]       | Celsius         | Fin Fwd Edge Temp                           |
| **Calculated**| wind_spd [m/s]    | m/s             | Wind Speed                                  |
|               | wind_dir [deg]    | degrees         | Wind Direction                              |
|               | wind_u [m/s]      | m/s             | u Wind Comp (+ North)                       |
|               | wind_v [m/s]      | m/s             | v Wind Comp (+ East)                        |
|               | wind_w [m/s]      | m/s (not NED)   | w Wind Comp (+ Up)                          |
|               | mag_dec [deg]     | degrees         | Magnetic Declination                        |
|               | mag_hdg [deg]     | degrees         | Magnetic Heading                            |
|               | ss_temp [%]       | %               | Seed Score Temperature                      |
|               | ss_rh [%]         | %               | Seed Score RH                               |
|               | ss_lwc [%]        | %               | Seed Score LWC                              |
|               | ss_updraft [%]    | %               | Seed Score Updraft                          |
|               | ss_extra1 [%]     | TBD             | Seed Score extra 1                          |
|               | ss_extra2 [%]     | TBD             | Seed Score extra 2                          |
|               | ss_extra3 [%]     | TBD             | Seed Score extra 3                          |
|               | ss_total [%]      | %               | Seed Score Total                            |
|               | ss_status [bits]  | binary          | Seed Score Status Word                      |
| **ADC-16A**   | seed-a [cnt], C0  | cnt             | Seeding Event-A                             |
|               | seed-b [cnt], C1  | cnt             | Seeding Event-B                             |
|               | seed-c [flg], C0F | "On" flag       | Seeding Event-C                             |
|               | seed-d [flg], C1F | "On" flag       | Seeding Event-D                             |
|               | Latitude          | degrees         | Latitude                                    |
|               | Longitude         | degrees         | Longitude                                   |
|               | *(unspecified)*   | degrees         | Magnetic Heading                            |


# Issues

### 1. `seed-* [cnt]` counter may not start from 0.

#### Example
File: `KSA CWIP Files/Fall 2024/CS4 - 448/CWIP-R03_20241026144050.csv`

Column: `seed-b [cnt]` 

To count the flares correctly, the offset has to be subracted from the max `seed-* [cnt]` column value.


### 2. `Altitude (m)` starts above 100 m or may have large negative values.

The altitude is not a suitable indicator to determine 
flight time (engine off - engine on) or 
air time (landing - take off).


### 3. `Man - Acquire (0/1)` does not always work.

This column is described as: "Flag high when new "Zero" command is received"

There are several cases where LWC is zeroed but the flag does not change to 1.

### 4. `lat [deg]` or `lon [deg]` may contain NaN.
Coordinates may be missing in a some rows, resulting in non-geolocated seed events.

### 5. Missing records.
Measurements are stored at 1-second intervals, but missing records may cause gaps in the timeseries.
If `seed-* [cnt]` counter increases across non-consecutive seconds, the seed event is not geolocated.