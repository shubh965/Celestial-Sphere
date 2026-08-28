# Celestial Sphere 3D

An interactive 3D astronomical visualization tool built with **Python**, **Plotly**, and **Astropy**. This project renders the celestial sphere in real time, projecting real stellar catalog data from **ESA Gaia DR3**, celestial coordinates (Right Ascension & Declination), the celestial equator, poles, the ecliptic, and the current positions of the Sun and Moon.



## Features

- **Interactive 3D Visualization**: Rotate, pan, and zoom through the celestial sphere with dark space-themed aesthetics powered by Plotly 3D.
- **Real Star Catalog Integration (Gaia DR3)**: Queries live star data using ADQL via `astroquery.gaia`, pulling positions, parallax, proper motion, and radial velocities.
- **Stellar Space Motion Propagation**: Applies space motion to stars using Astropy's `apply_space_motion` to propagate star positions accurately to any target epoch/time.
- **Magnitude-Based Star Scaling**: Calculates visual marker sizes dynamically based on stellar magnitudes ($10 \times 10^{-\text{mag}/5}$), giving a realistic apparent brightness effect.
- **Celestial Reference Systems**:
  - **Coordinate Grid**: 10° intervals for Right Ascension (RA) lines and Declination (Dec) parallels.
  - **Celestial Equator & Poles**: Visual references for Earth's equatorial projection and the North/South Celestial Poles.
  - **Ecliptic Plane**: The apparent annual path of the Sun, inclined at Earth's axial obliquity ($\sim 23.44^\circ$).
- **Solar System Ephemerides**: Calculates real-time or historical 3D positions of the **Sun** and **Moon** using Astropy coordinate frames.
- **Standalone HTML Export**: Automatically exports the interactive 3D model to `celestial_sphere.html` for offline viewing or web sharing.

## How It Works

1. **Coordinate Calculations (`coordinates.py`)**:
   - Computes unit sphere mesh points and grid lines for Right Ascension ($\alpha$) and Declination ($\delta$).
   - Calculates the solar ecliptic tilted at $\varepsilon = 23.44^\circ$.
   - Queries `gaiadr3.gaia_source` with filters for valid parallax and proper motions.
   - Converts astronomical coordinates from ICRS to 3D Cartesian coordinates on the unit sphere ($x, y, z$).
   - Queries real-time Sun and Moon ephemeris via `astropy.coordinates.get_sun` and `astropy.coordinates.get_body`.

2. **3D Scene Rendering (`plotting.py`)**:
   - Builds 3D traces using `plotly.graph_objects` (`Surface` and `Scatter3d`).
   - Applies custom colors, hover labels, and magnitude-weighted star radii.

3. **Orchestration & Display (`main.py`)**:
   - Merges all traces into a single `go.Figure` with a customized dark space scene layout and exports to HTML.

## Project Structure

```text
Celestial Sphere/
├── assets/
│   ├── celestial_sphere.html
├── main.py
├── coordinates.py
├── plotting.py
├── requirements.txt
├── LICENCE.md
├── .gitignore
└── README.md
```


## Prerequisites & Installation

Ensure you have Python 3.8+ installed. Then clone the repository and install the required packages:

```bash
git clone <repo-url>
cd celestial-sphere
pip install -r requirements.txt
```


## Configuration

You can customize the parameters at the top of `Celestial Sphere/main.py`:

```python
# Number of stars to query from Gaia DR3
STAR_NUM = 2000

# Maximum magnitude threshold (lower = brighter stars only)
STAR_MAG = 5

# Target epoch (None defaults to datetime.now())
TIME = None  # Eg. Time("2026-01-01 00:00:00")
```


## License

This project is open-source and available under the [MIT License](LICENSE).
