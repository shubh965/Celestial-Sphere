import plotly.graph_objects as go

def plot_sphere(sphere_xyz, surfacecolor):
    sphere = go.Surface(
        x = sphere_xyz[0],
        y = sphere_xyz[1],
        z = sphere_xyz[2],
        surfacecolor = surfacecolor,
        colorscale = [[0, "#040348"], [1, "#040348"]],
        showscale = False,
        opacity = 1,
        name = 'Celestial Sphere',
        hoverinfo = 'skip'
    )

    return sphere

def plot_grid(grid_xyz):
    grid_ra = go.Scatter3d(
        x = grid_xyz['ra_x'],
        y = grid_xyz['ra_y'],
        z = grid_xyz['ra_z'],
        mode = 'lines',
        line = dict(
            color = 'grey',
            width = 3
        ),
        name = 'RA Grid',
        showlegend = False,
        hoverinfo = 'skip'
    )

    grid_dec = go.Scatter3d(
        x = grid_xyz['dec_x'],
        y = grid_xyz['dec_y'],
        z = grid_xyz['dec_z'],
        mode = 'lines',
        line = dict(
            color = 'grey',
            width = 3
        ),
        name = 'Dec Grid',
        showlegend = False
    )

    return grid_ra, grid_dec

def plot_equator(equator_xyz):
    equator = go.Scatter3d(
        x = equator_xyz[0],
        y = equator_xyz[1],
        z = equator_xyz[2],
        mode = 'lines',
        text = "Equator",
        hoverinfo = 'text',
        textposition = 'top center',
        line = dict(
            color = 'white',
            width = 4
        ),
        name = 'Equator',
        showlegend = False
    )

    return equator

def plot_poles(poles_xyz):
    poles = go.Scatter3d(
        x = poles_xyz[0],
        y = poles_xyz[1],
        z = poles_xyz[2],
        mode = 'markers',
        text = ["North Celestial Pole", "South Celestial Pole"],
        hoverinfo = 'text',
        textposition = ['top center', 'bottom center'],
        marker = dict(
            size = 5,
            color = 'white',
            opacity = 1
        ),
        name = 'Poles',
        showlegend = False
    )

    return poles

def plot_solar_ecliptic(solar_ecliptic_xyz):
    solar_ecliptic = go.Scatter3d(
        x = solar_ecliptic_xyz[0],
        y = solar_ecliptic_xyz[1],
        z = solar_ecliptic_xyz[2],
        mode = 'lines',
        text = "Ecliptic",
        hoverinfo = 'text',
        textposition = 'top center',
        line = dict(
            color = 'red',
            width = 2
        ),
        name = 'Solar Ecliptic',
        showlegend = False
    )

    return solar_ecliptic

def plot_sun_moon(sun_moon_xyz):
    sun = go.Scatter3d(
        x = [sun_moon_xyz[0][0]],
        y = [sun_moon_xyz[1][0]],
        z = [sun_moon_xyz[2][0]],
        mode = 'markers',
        name = 'Sun',
        hovertext = 'Sun',
        hoverinfo = 'text',
        marker = dict(
            size=12,
            color='gold',
            opacity=1
        ),
        showlegend = False
    )

    moon = go.Scatter3d(
        x = [sun_moon_xyz[0][1]],
        y = [sun_moon_xyz[1][1]],
        z = [sun_moon_xyz[2][1]],
        mode = 'markers',
        name = 'Moon',
        hovertext = 'Moon',
        hoverinfo = 'text',
        marker = dict(
            size=8,
            color='white',
            opacity=1
        ),
        showlegend = False
    )

    return sun, moon

def plot_stars(stars_xyz, phot_g_mean_mag):
    hover_labels = [f"Magnitude: {mag:.2f}" for mag in phot_g_mean_mag]
    stars = go.Scatter3d(
        x = stars_xyz[0],
        y = stars_xyz[1],
        z = stars_xyz[2],
        mode = 'markers',
        text = hover_labels,
        hoverinfo = "text",
        marker = dict(
            size = 10 * (10 ** (-phot_g_mean_mag / 5)),
            color = "white",
            opacity = 1
        ),
        name = 'Stars',
        showlegend = False
    )

    return stars
