import numpy as np
import plotly.graph_objects as go
from datetime import datetime
from astropy.time import Time
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import coordinates
import plotting

STAR_NUM = 2000
STAR_MAG = 5
TIME = None

def main(star_num, star_mag, time):
    if time is None:
        time = Time(datetime.now())
    
    sphere_xyz, theta = coordinates.sphere_coordinates()
    grid_xyz = coordinates.grid_coordinates()
    equator_xyz = coordinates.equator_coordinates(theta)
    poles_xyz = coordinates.poles_coordinates()
    solar_ecliptic_xyz = coordinates.solar_ecliptic_coordinates(theta)
    sun_moon_xyz = coordinates.sun_moon_coordinates(time)
    stars_xyz, phot_g_mean_mag = coordinates.stars_coordinates(star_num, star_mag, time)

    fig = go.Figure()

    surfacecolor = np.ones_like(sphere_xyz[0])

    sphere = plotting.plot_sphere(sphere_xyz, surfacecolor)
    equator = plotting.plot_equator(equator_xyz)
    poles = plotting.plot_poles(poles_xyz)
    ra_grid, dec_grid = plotting.plot_grid(grid_xyz)
    ecliptic = plotting.plot_solar_ecliptic(solar_ecliptic_xyz)
    sun, moon = plotting.plot_sun_moon(sun_moon_xyz)
    stars = plotting.plot_stars(stars_xyz, phot_g_mean_mag)

    fig.update_layout(
        title = {
            "text" : "Celestial Sphere",
            "font" : {
                "family" : "Arial",
                "size" : 24,
                "color" : "white"
            },
            "y" : 0.99,
            "x" : 0.5,
            "xanchor" : "center",
            "yanchor" : "top"
        },
        template = "plotly_dark",
        scene = dict(
            xaxis = dict(visible = False),
            yaxis = dict(visible = False),
            zaxis = dict(visible = False),
            aspectmode = 'cube',
            bgcolor = 'rgb(5, 5, 15)',
            camera = dict(
                eye = dict(x = 1.6, y = 1.6, z = 1.2)
            )
        ),
        margin = dict(l = 0, r = 0, b = 0, t = 30)
    )

    fig.add_trace(sphere)
    fig.add_trace(equator)
    fig.add_trace(ecliptic)
    fig.add_trace(ra_grid)
    fig.add_trace(dec_grid)
    fig.add_trace(poles)
    fig.add_trace(sun)
    fig.add_trace(moon)
    fig.add_trace(stars)

    fig.write_html("celestial_sphere.html")
    fig.show()

if __name__ == "__main__":
    main(STAR_NUM, STAR_MAG, TIME)
