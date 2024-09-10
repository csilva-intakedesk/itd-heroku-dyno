import shapefile, json
from shapely.geometry import shape, Point
from pyproj import Transformer

def convert_to_geographic(proj_coords, from_epsg, to_epsg=4326):
    """
    Convert projected coordinates to geographic coordinates (longitude, latitude).
    
    Parameters:
    proj_coords : tuple
        The projected coordinates (x, y).
    from_epsg : int
        The EPSG code of the projected coordinate system.
    to_epsg : int, optional
        The EPSG code of the geographic coordinate system (default is 4326, WGS84).
    
    Returns:
    tuple : The geographic coordinates (longitude, latitude).
    """
    # Use Transformer to convert coordinates
    transformer = Transformer.from_crs(f"epsg:{from_epsg}", f"epsg:{to_epsg}", always_xy=True)
    lon, lat = transformer.transform(proj_coords[0], proj_coords[1])
    return lon, lat

def convert_to_projected(geo_coords, from_epsg=4326, to_epsg=3857):
    """
    Convert geographic coordinates (longitude, latitude) to projected coordinates.
    Parameters:
    geo_coords : tuple
        The geographic coordinates (longitude, latitude).
    from_epsg : int
        The EPSG code of the geographic coordinate system (default is 4326, WGS84).
    to_epsg : int, optional
        The EPSG code of the projected coordinate system (default is 3857, Web Mercator).
    
    Returns:
    tuple : The projected coordinates (x, y).
    """
    # Use Transformer to convert coordinates
    transformer = Transformer.from_crs(f"epsg:{from_epsg}", f"epsg:{to_epsg}", always_xy=True)
    x, y = transformer.transform(geo_coords[0], geo_coords[1])
    return x, y

def is_point_in_shapefile(shapefile_path, point, state):
    """
    Check if a point is within any of the shapes in the shapefile using spatial filtering,
    and filter by state.
    Parameters:
    shapefile_path : str
        Path to the shapefile (.shp).
    point : tuple of (longitude, latitude)
        The geographic point to check.
    state : str
        The state to filter shapes by (e.g., "GA").
    
    Returns:
    bool : True if the point is within any shape's bounding box in the specified state, False otherwise
    """
    # Read the shapefile
    sf = shapefile.Reader(shapefile_path)
    
    try:
        # Get the point's longitude and latitude
        x, y = convert_to_projected(point)
        point_proj = Point(x, y)
        
        # Get the field names and find the index of the state field
        fields = sf.fields[1:]  # Skip the first deletion flag field
        field_names = [field[0] for field in fields]
        state_index = field_names.index("State") 
        pws_index = field_names.index("PWSID") 
        
        # Iterate through each shape record
        for shape_record in sf.iterShapeRecords():
            # Check if the shape's state matches the specified state
            if shape_record.record[state_index] == state:
                # Perform a spatial filter on the bounding box of the shape
                # bbox = shape_record.shape.bbox
                polygon = shape(shape_record.shape)
                if polygon.contains(point_proj):
                    record_data = {
                        field_name: str(shape_record.record[i]).encode('utf-8', 'ignore').decode('utf-8')
                        for i, field_name in enumerate(field_names)
                    }
                    # Return the record as a JSON object
                    return record_data
    except KeyError:
        return False
    
    # If the point is not within any shapes in the specified state
    return False
