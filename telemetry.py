import csv
import time
from pymavlink import mavutil
from pyproj import Transformer

m = mavutil.mavlink_connection('tcp:127.0.0.1:5762')
m.wait_heartbeat()
print("Connected to vehicle, system id:", m.target_system)

transformers = {}

def to_utm(lat, lon):
    zone = int((lon + 180) // 6) + 1
    epsg = (32600 if lat >= 0 else 32700) + zone
    if epsg not in transformers:
        transformers[epsg] = Transformer.from_crs(4326, epsg, always_xy=True)
    e, n = transformers[epsg].transform(lon, lat)
    return e, n, zone

t0 = time.time()
with open('flight_log.csv', 'w', newline='') as f:
    w = csv.writer(f)
    w.writerow(['time_s', 'lat', 'lon', 'alt_m', 'utm_e', 'utm_n', 'utm_zone'])
    try:
        while True:
            msg = m.recv_match(type='GLOBAL_POSITION_INT', blocking=True)
            lat, lon = msg.lat / 1e7, msg.lon / 1e7
            alt = msg.relative_alt / 1000
            e, n, zone = to_utm(lat, lon)
            t = time.time() - t0
            w.writerow([round(t, 2), lat, lon, alt, round(e, 1), round(n, 1), zone])
            f.flush()
            print(f"t={t:6.1f}s lat={lat:.6f} lon={lon:.6f} alt={alt:5.1f}m UTM{zone} E={e:.1f} N={n:.1f}")
    except KeyboardInterrupt:
        print("Stopped. Log saved to flight_log.csv")