import os
# --- landscape override (YouTube 16:9) ---
LAND_SH = float(os.environ.get("LAND_SH", "28"))
r.resolution_x, r.resolution_y = 1280, 720
cam_d.sensor_fit = "VERTICAL"; cam_d.sensor_height = LAND_SH
print("LANDSCAPE", r.resolution_x, r.resolution_y, LAND_SH)
r.resolution_percentage = int(os.environ.get("LAND_PCT", "100"))
