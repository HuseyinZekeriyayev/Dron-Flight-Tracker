import csv
import math
import matplotlib.pyplot as plt

t, e, n, alt = [], [], [], []
with open('flight_log.csv') as f:
    for row in csv.DictReader(f):
        t.append(float(row['time_s']))
        e.append(float(row['utm_e']))
        n.append(float(row['utm_n']))
        alt.append(float(row['alt_m']))

# Trim the idle time on the ground after landing
last_airborne = max(i for i, a in enumerate(alt) if a > 2)
end = min(last_airborne + 10, len(t))
t, e, n, alt = t[:end], e[:end], n[:end], alt[:end]

# Simple flight statistics
dist = sum(math.hypot(e[i] - e[i-1], n[i] - n[i-1]) for i in range(1, len(e)))
print(f"Duration:     {t[-1]:.0f} s")
print(f"Max altitude: {max(alt):.0f} m")
print(f"Distance:     {dist/1000:.2f} km")

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(13, 5))

ax1.plot(e, n, linewidth=1.5)
ax1.scatter(e[0], n[0], c='green', label='Start', zorder=3)
ax1.scatter(e[-1], n[-1], c='red', label='End', zorder=3)
ax1.set_xlabel('UTM Easting (m)')
ax1.set_ylabel('UTM Northing (m)')
ax1.set_title('Flight path (WGS84 -> UTM zone 55)')
ax1.axis('equal')
ax1.ticklabel_format(useOffset=False, style='plain')
ax1.tick_params(axis='x', rotation=45)
ax1.legend()
ax1.grid(True)

ax2.plot(t, alt)
ax2.set_xlabel('Time (s)')
ax2.set_ylabel('Relative altitude (m)')
ax2.set_title(f'Altitude profile (max {max(alt):.0f} m)')
ax2.grid(True)

plt.tight_layout()
plt.savefig('flight_plot.png', dpi=150)
print("Saved flight_plot.png")
plt.show()