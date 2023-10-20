# simple-wkt

## Description

`simple-wkt` provides a basic suite of WKT models to make creating or validating WKT data easier.

Project uses [Shapely](https://pypi.org/project/shapely/) lib to parse WKT strings into simple objects.

## Examples

```python
wkt_data: WKTObject = parse_wkt("POINT (0 0)")
print(wkt_data.type) # Point
print(wkt_data.coordinates) # [0.0, 0.0]
print(wkt_data) # type='Point' coordinates=[0.0, 0.0] 

# Transforming to a Shapely lib object 
shapely_wkt = wkt_data.to_shapely()
```