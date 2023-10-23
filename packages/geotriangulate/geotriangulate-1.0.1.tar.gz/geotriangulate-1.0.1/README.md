# geotriangulate

geotriangulate is a Python library for finding object location by triangulation method.

## Installation

Just save geotriangulate.py to any convenient location and import it



## Usage

```python
import geotriangulate

# Creates a new measurement with longitude lon, latitude lat, azimuth alpha
meas = Measurement(lon, lat, alpha)

# Creates a new target object
targobj = TargObj()

''' Adds measurement meas of the target object. returns the id assigned to the measurement. 
If the new measurement does not provide any additional information, None is returned

'''
meas_id = targobj.AddMeasurement(meas)

# Deletes the measurement by id. If there is no measurement with such an id, an error is thrown
targobj.DeleteMeasurement(meas_id)

# Access to the current average location of the object
targobj.CurMedPos

```


## License

[MIT](https://choosealicense.com/licenses/mit/)
