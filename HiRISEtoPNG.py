from osgeo import gdal

# Create an intermediate TIFF file
intermediate_tiff = '/Users/core/Downloads/intermediate_dem.tiff'
driver = gdal.GetDriverByName('GTiff')
if not driver:
    raise RuntimeError("GDAL TIFF driver not available.")

# Create a new dataset for the output TIFF
tiff_data = driver.Create(intermediate_tiff, dem_data.RasterXSize, dem_data.RasterYSize, 1, gdal.GDT_UInt16)
if not tiff_data:
    raise RuntimeError("Failed to create the intermediate TIFF file.")

tiff_band = tiff_data.GetRasterBand(1)
tiff_band.WriteArray(dem_normalized)
tiff_band.FlushCache()
tiff_band.SetNoDataValue(0)  # Set the no-data value if necessary

# Copy the geotransform and projection from the original DEM to preserve spatial referencing
tiff_data.SetGeoTransform(dem_data.GetGeoTransform())
tiff_data.SetProjection(dem_data.GetProjection())

# Close the datasets
tiff_band = None
tiff_data = None

import subprocess

# Specify the output PNG file path
output_png = '/Users/core/Downloads/output_dem.png'

# Construct the gdal_translate command
translate_command = [
    'gdal_translate',
    '-of', 'PNG',
    intermediate_tiff,
    output_png
]

# Execute the command
subprocess.run(translate_command, check=True)

print("Conversion to PNG completed successfully.")
