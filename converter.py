import datetime


def time(d: float):
    return datetime.datetime.combine(datetime.date(2024, 8, 1) + datetime.timedelta(days=int(d - 739100)),
                                     datetime.time(hour=(round(24 * (d % 1)))))


def apcpsfc(x):
    "surface total precipitation [kg/m^2]"
    return x[0][0]


def capesfc(x):
    "surface convective available potential energy [j/kg]"
    return x[0][0]


def cinsfc(x):
    "surface convective inhibition [j/kg]"
    return x[0][0]


def dpt2m(x):
    "2 m above ground dew point temperature [k]"
    return x[0][0] - 273.15


def dzdtprs(x):
    "(1000 975 950 925 900.. 10 7 4 2 1) vertical velocity (geometric) [m/s]"
    return x[0][0][0]


def gustsfc(x):
    "surface wind speed (gust) [m/s]"
    return x[0][0]


def hcdcavehcll(x):
    "high cloud layer high cloud cover [%]"
    return x[0][0]


def hgtsfc(x):
    "surface geopotential height [gpm]"
    return x[0][0]


def hgtprs(x):
    "(1000 975 950 925 900.. 10 7 4 2 1) geopotential height [gpm]"
    return x[0][0][0]


def hgtceil(x):
    "cloud ceiling geopotential height [gpm]"
    return x[0][0]


def hpblsfc(x):
    "surface planetary boundary layer height [m]"
    return x[0][0]


def lcdcavelcll(x):
    "low cloud layer low cloud cover [%]"
    return x[0][0]


def lftxsfc(x):
    "surface surface lifted index [k]"
    return x[0][0]


def mcdcavemcll(x):
    "middle cloud layer medium cloud cover [%]"
    return x[0][0]


def no4lftxsfc(x):
    "surface best (4 layer) lifted index [k]"
    return x[0][0]


def prateavesfc(x):
    "surface precipitation rate [kg/m^2/s]"
    return x[0][0] * 3600 * 3


def pressfc(x):
    "surface pressure [pa] "
    return x[0][0] / 133.322


def pres80m(x):
    "80 m above ground pressure [pa]"
    return x[0][0] / 133.322


def prmslmsl(x):
    "mean sea level pressure reduced to msl [pa] "
    return x[0][0] / 133.322


def rhprs(x):
    "(1000 975 950 925 900.. 10 7 4 2 1) relative humidity [%]"
    return x[0][0][0]


def rh2m(x):
    "2 m above ground relative humidity [%]"
    return x[0][0]


def spfhprs(x):
    "(1000 975 950 925 900.. 10 7 4 2 1) specific humidity [kg/kg]"
    return x[0][0]


def spfh2m(x):
    "2 m above ground specific humidity [kg/kg]"
    return x[0][0]


def spfh80m(x):
    "80 m above ground specific humidity [kg/kg]"
    return x[0][0]


def tcdcaveclm(x):
    "entire atmosphere total cloud cover [%]"
    return x[0][0]


def tcdcblcll(x):
    "boundary layer cloud layer total cloud cover [%]"
    return x[0][0]


def tcdcprs(x):
    "(1000 975 950 925 900.. 250 200 150 100 50) total cloud cover [%]"
    return x[0][0][0]


def tcdcccll(x):
    "convective cloud layer total cloud cover [%]"
    return x[0][0]


def tmax2m(x):
    "2 m above ground maximum temperature [k]"
    return x[0][0] - 273.15


def tmin2m(x):
    "2 m above ground minimum temperature [k]"
    return x[0][0] - 273.15


def tmpsfc(x):
    "surface temperature [k]"
    return x[0][0] - 273.15


def tmpprs(x):
    "(1000 975 950 925 900.. 10 7 4 2 1) temperature [k]"
    return x[0][0][0] - 273.15


def tmp2m(x):
    "2 m above ground temperature [k]"
    return x[0][0] - 273.15


def tmp80m(x):
    "80 m above ground temperature [k]"
    return x[0][0] - 273.15


def tmp100m(x):
    "100 m above ground temperature [k]"
    return x[0][0] - 273.15


def ugrdprs(x):
    "(1000 975 950 925 900.. 10 7 4 2 1) u-component of wind [m/s]"
    return x[0][0][0]


def ugrd_1829m(x):
    "1829 m above mean sea level u-component of wind [m/s]"
    return x[0][0]


def ugrd10m(x):
    "10 m above ground u-component of wind [m/s]"
    return x[0][0]


def ugrd20m(x):
    "20 m above ground u-component of wind [m/s]"
    return x[0][0]


def ugrd30m(x):
    "30 m above ground u-component of wind [m/s]"
    return x[0][0]


def ugrd40m(x):
    "40 m above ground u-component of wind [m/s]"
    return x[0][0]


def ugrd50m(x):
    "50 m above ground u-component of wind [m/s]"
    return x[0][0]


def ugrd80m(x):
    "80 m above ground u-component of wind [m/s]"
    return x[0][0]


def ugrd100m(x):
    "100 m above ground u-component of wind [m/s]"
    return x[0][0]


def ugrdpbl(x):
    "planetary boundary layer u-component of wind [m/s]"
    return x[0][0]


def vgrdprs(x):
    "(1000 975 950 925 900.. 10 7 4 2 1) v-component of wind [m/s]"
    return x[0][0][0]


def vgrd_1829m(x):
    "1829 m above mean sea level v-component of wind [m/s]"
    return x[0][0]


def vgrd10m(x):
    "10 m above ground v-component of wind [m/s]"
    return x[0][0]


def vgrd20m(x):
    "20 m above ground v-component of wind [m/s]"
    return x[0][0]


def vgrd30m(x):
    "30 m above ground v-component of wind [m/s]"
    return x[0][0]


def vgrd40m(x):
    "40 m above ground v-component of wind [m/s]"
    return x[0][0]


def vgrd50m(x):
    "50 m above ground v-component of wind [m/s]"
    return x[0][0]


def vgrd80m(x):
    "80 m above ground v-component of wind [m/s]"
    return x[0][0]


def vgrd100m(x):
    "100 m above ground v-component of wind [m/s]"
    return x[0][0]


def vgrdpbl(x):
    "planetary boundary layer v-component of wind [m/s]"
    return x[0][0]


def vissfc(x):
    "surface visibility [m]"
    return x[0][0]

