
# -*- coding: utf-8 -*-

LOG_STDOUT = True

# db config
SQLALCHEMY_DATABASE_URI = 'url to db'
SQLALCHEMY_TRACK_MODIFICATIONS = False
SQLALCHEMY_ECHO = False

# number of records that can be inserted/updated in one call
RESOLVER_MAX_RECORDS_ADD = 100

# This is the URL to communicate with resolver_gateway api
RESOLVER_GATEWAY_URL = 'http://localhost:5000/{bibcode}/{link_type}/{url}'
RESOLVER_GATEWAY_URL_TEST = '/{bibcode}/{link_type}/{url}'

# This is the URL for deterministic links, needs to go to local-config, once deployed, if need to
RESOLVER_DETERMINISTIC_LINKS_BASEURL = '/#abs'

# These URLs are used to create links for doi and arXiv sources
RESOLVER_DOI_LINK_BASEURL = 'http://dx.doi.org/{id}'
RESOLVER_ARXIV_LINK_BASEURL = 'http://arxiv.org/abs/{id}'

RESOLVER_DATA_SOURCES = {
    "SIMBAD": {
        "name": "SIMBAD Database at the CDS",
        "url": "http://simbad.u-strasbg.fr",
    },
    "XMM": {
        "name": "XMM Newton Science Archive",
        "url": "http://nxsa.esac.esa.int",
    },
    "NED": {
        "name": "NASA/IPAC Extragalactic Database",
        "url": "https://ned.ipac.caltech.edu",
    },
    "MAST": {
        "name": "Mikulski Archive for Space Telescopes",
        "url": "http://archive.stsci.edu",
    },
    "ISO": {
        "name": "Infrared Space Observatory",
        "url": "https://www.cosmos.esa.int/web/iso",
    },
    "Vizier": {
        "name": "VizieR Catalog Service",
	    "url": "http://vizier.u-strasbg.fr",
    },
    "HEASARC": {
        "name": "NASA's High Energy Astrophysics Science Archive Research Center",
        "url": "https://heasarc.gsfc.nasa.gov/",
    },
    "CDS": {
        "name": "Strasbourg Astronomical Data Center",
        "url": "http://cdsweb.u-strasbg.fr/",
    },
    "ESA": {
        "name": "ESAC Science Data Center",
        "url": "http://archives.esac.esa.int",
    },
    "CXO": {
        "name": "Chandra X-Ray Observatory",
        "url": "http://cxc.harvard.edu/cda",
    },
    "ESO": {
        "name": "European Southern Observatory",
        "url": "http://archive.eso.org",
    },
    "PDG": {
        "name": "Particle Data Group",
        "url": "http://pdglive.lbl.gov",
    },
    "KOA": {
        "name": "Keck Observatory Archive",
        "url": " https://koa.ipac.caltech.edu",
    },
    "NOAO": {
        "name": "National Optical Astronomy Observatory",
        "url": " https://www.noao.edu",
    },
    "Herschel": {
        "name": "Herschel Science Center",
        "url": "https://www.cosmos.esa.int/web/herschel/home",
    },
    "GCPD": {
        "name": "The General Catalogue of Photometric Data",
        "url": "http://obswww.unige.ch/gcpd/",
    },
    "TNS": {
        "name": "Transient Name Server",
        "url": " https://wis-tns.weizmann.ac.il",
    },
    "Spitzer": {
        "name": "Spitzer Space Telescope",
        "url": "https://irsa.ipac.caltech.edu/Missions/spitzer.html",
    },
    "INES": {
        "name": "IUE Newly Extracted Spectra",
        "url": "http://sdc.cab.inta-csic.es/ines/",
    },
    "PDS": {
        "name": "The NASA Planetary Data System",
        "url": " https://pds.jpl.nasa.gov",
    },
    "ATNF": {
        "name": "Australia Telescope Online Archive",
        "url": " https://atoa.atnf.csiro.au",
    },
    "IBVS": {
        "name": "Information Bulletin on Variable Stars",
        "url": "http://ibvs.konkoly.hu/IBVS/IBVS.html",
    },
    "ARI": {
        "name": "Astronomisches Rechen-Institut",
        "url": "https://zah.uni-heidelberg.de/institutes/ari/",
    },
    "NExScI": {
        "name": "NASA Exoplanet Archive",
        "url": " https://exoplanetarchive.ipac.caltech.edu",
    },
    "ALMA": {
        "name": "Atacama Large Millimeter/submillimeter Array",
        "url": "https://almascience.org/",
    },
    "Author": {
        "name": "Author Hosted Dataset",
    },
    "GTC": {
        "name": "Gran Telescopio CANARIAS Public Archive",
        "url": "http://gtc.sdc.cab.inta-csic.es/gtc/",
    },
    "Astroverse": {
        "name": "CfA Dataverse",
        "url": "https://dataverse.harvard.edu/dataverse/cfa",
    },
    "AcA": {
        "name": "Acta Astronomica Data Files",
    },
    "BICEP2": {
        "name": "BICEP/Keck Data",
        "url": " http://bicepkeck.org",
    },
    "Zenodo": {
        "name": "Zenodo Archive",
        "url": "https://zenodo.org",
    },
    "PASA": {
        "name": "Publication of the Astronomical Society of Australia Datasets",
        "url": "http://www.publish.csiro.au",
    },
    "CADC": {
        "name": "Canadian Astronomy Data Center",
        "url": "http://www.canfar.phys.uvic.ca/en",
    },
}
