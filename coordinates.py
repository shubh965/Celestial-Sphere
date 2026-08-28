import numpy as np
import numpy.ma as ma
from astroquery.gaia import Gaia
from astropy.coordinates import SkyCoord, Distance, get_sun, get_body
from astropy.time import Time
import astropy.units as u

def sphere_coordinates():
    theta = np.linspace(0, 2*np.pi, 200) 
    phi = np.linspace(-np.pi/2, np.pi/2, 200)
    theta_grid, phi_grid = np.meshgrid(theta, phi)

    x_sphere = np.cos(phi_grid) * np.cos(theta_grid) 
    y_sphere = np.cos(phi_grid) * np.sin(theta_grid)
    z_sphere = np.sin(phi_grid)

    sphere_xyz = np.array([x_sphere, y_sphere, z_sphere])

    return sphere_xyz, theta

def grid_coordinates():
    ra_line_x, ra_line_y, ra_line_z = [], [], []
    dec_curve = np.linspace(-np.pi / 2, np.pi / 2, 500)

    for ra_val in np.radians(range(0, 360, 10)):
        ra_line_x.extend(np.cos(dec_curve) * np.cos(ra_val))
        ra_line_y.extend(np.cos(dec_curve) * np.sin(ra_val))
        ra_line_z.extend(np.sin(dec_curve))
        ra_line_x.append(None)
        ra_line_y.append(None)
        ra_line_z.append(None)

    dec_line_x, dec_line_y, dec_line_z = [], [], []
    ra_curve = np.linspace(0, 2 * np.pi, 500)

    for dec_val in np.radians(range(-80, 90, 10)):
        r = np.cos(dec_val)
        dec_line_x.extend(r * np.cos(ra_curve))
        dec_line_y.extend(r * np.sin(ra_curve))
        dec_line_z.extend(np.full_like(ra_curve, np.sin(dec_val)))
        dec_line_x.append(None)
        dec_line_y.append(None)
        dec_line_z.append(None)

    grid_xyz = {
        "ra_x" : ra_line_x,
        "ra_y" : ra_line_y,
        "ra_z" : ra_line_z,
        "dec_x" : dec_line_x,
        "dec_y" : dec_line_y,
        "dec_z" : dec_line_z
    }

    return grid_xyz
    
def equator_coordinates(theta):
    x_equator = np.cos(theta) 
    y_equator = np.sin(theta)
    z_equator = np.zeros_like(theta)

    equator_xyz = np.array([x_equator, y_equator, z_equator])

    return equator_xyz

def poles_coordinates():
    x_poles = np.array([0, 0])
    y_poles = np.array([0, 0])
    z_poles = np.array([1, -1])
    
    poles_xyz = np.array([x_poles, y_poles, z_poles])

    return poles_xyz


def solar_ecliptic_coordinates(theta):
    eps = np.radians(23.44)

    x_solar_ecliptic = np.cos(theta)
    y_solar_ecliptic = np.sin(theta) * np.cos(eps)
    z_solar_ecliptic = np.sin(theta) * np.sin(eps)

    solar_ecliptic_xyz = np.array([x_solar_ecliptic, y_solar_ecliptic, z_solar_ecliptic])

    return solar_ecliptic_xyz

def sun_moon_coordinates(time):
    sun = get_sun(time)
    s_ra, s_dec = sun.ra.rad, sun.dec.rad
    sun_x = np.cos(s_dec) * np.cos(s_ra)
    sun_y = np.cos(s_dec) * np.sin(s_ra)
    sun_z = np.sin(s_dec)

    moon = get_body('moon', time)
    m_ra, m_dec = moon.ra.rad, moon.dec.rad
    moon_x = np.cos(m_dec) * np.cos(m_ra)
    moon_y = np.cos(m_dec) * np.sin(m_ra)
    moon_z = np.sin(m_dec)

    sun_moon_xyz = np.array([[sun_x, moon_x], [sun_y, moon_y], [sun_z, moon_z]])

    return sun_moon_xyz

def stars_coordinates(num, max_mag, time):
    print("Fetching Star Data...")

    job = Gaia.launch_job(
        f'''
        SELECT TOP {num} source_id, ra, dec, parallax, pmra, pmdec, ref_epoch, radial_velocity, phot_g_mean_mag 
        FROM gaiadr3.gaia_source as dr3
        WHERE phot_g_mean_mag < {max_mag}
        AND parallax > 0
        AND pmra IS NOT NULL
        AND pmdec IS NOT NULL
        ORDER BY phot_g_mean_mag
        '''
    )

    print("Star data fetched.")

    catalog = job.get_results()

    plx_arcsec = np.array(catalog['parallax'])
    valid_plx = np.where(plx_arcsec > 0, plx_arcsec, np.nan) * u.arcsec
    distance = Distance(parallax = valid_plx, allow_negative = False)

    ra = np.deg2rad(catalog['ra']) * u.rad
    dec = np.deg2rad(catalog['dec']) * u.rad

    rv = catalog['radial_velocity']
    rv_clean = np.where(ma.getmaskarray(rv) | np.isnan(rv), 0.0, rv) * u.km / u.s

    star_coord = SkyCoord(
        ra = ra,
        dec = dec,
        frame = 'icrs',
        distance = distance,
        pm_ra_cosdec = catalog['pmra'],
        pm_dec = catalog['pmdec'],
        radial_velocity = rv_clean,
        obstime = Time(catalog['ref_epoch'], format = 'jyear', scale = 'tcb')
    )

    star_coord_today = star_coord.apply_space_motion(time)

    star_cart = star_coord_today.cartesian

    r = star_cart.norm()
    x_star = star_cart.x / r
    y_star = star_cart.y / r
    z_star = star_cart.z / r

    star_xyz = np.array([x_star, y_star, z_star])

    return star_xyz, np.array(catalog['phot_g_mean_mag'])
