
# -*- coding: utf-8 -*-

LOG_STDOUT = True

# db config
SQLALCHEMY_DATABASE_URI = 'url to db'
SQLALCHEMY_TRACK_MODIFICATIONS = False
SQLALCHEMY_ECHO = False

# number of records that can be inserted/updated in one call
RESOLVER_MAX_RECORDS_ADD = 100
# number of records that can be deleted in one call
RESOLVER_MAX_RECORDS_DEL = 100

# This is the URL to communicate with resolver_gateway api
RESOLVER_GATEWAY_URL = 'http://localhost:5050/link_gateway/{bibcode}/{link_type}/{url}'

# This is the URL for deterministic links, needs to go to local-config, once deployed, if need to
RESOLVER_DETERMINISTIC_LINKS_BASEURL = '/abs'

# These URLs are used to create links for doi and arXiv sources
RESOLVER_DOI_LINK_BASEURL = 'https://doi.org/{id}'
RESOLVER_ARXIV_LINK_BASEURL = 'http://arxiv.org/abs/{id}'

RESOLVER_DATA_SOURCES = {
    "4TU.ResearchData": {
      "name": "4TU.ResearchData",
      "url": "https://data.4tu.nl/",
    },
    "AcA": {
      "name": "AcA",
      "url": "ftp://ftp.astrouw.edu.pl",
    },
    "AHED": {
      "name": "AHED",
      "url": "https://ahed.nasa.gov/",
    },
    "ALMA": {
      "name": "ALMA",
      "url": "https://almascience.org/",
    },
    "ArcticData": {
      "name": "ArcticData",
      "url": "https://arcticdata.io/",
    },
    "ARI": {
      "name": "ARI",
      "url": "https://zah.uni-heidelberg.de/institutes/ari/",
    },
    "ARTEMIS": {
      "name": "ARTEMIS",
      "url": "http://artemis.ssl.berkeley.edu/",
    },
    "AstroGeo": {
      "name": "AstroGeo",
      "url": "https://www.usgs.gov/centers/astrogeology-science-center",
    },
    "ASU": {
      "name": "ASU",
      "url": "",
    },
    "Astroverse": {
      "name": "Astroverse",
      "url": "https://dataverse.harvard.edu/dataverse/cfa",
    },
    "ATNF": {
      "name": "ATNF",
      "url": "https://atoa.atnf.csiro.au",
    },
    "Author": {
      "name": "Author",
      "url": "",
    },
    "BAS": {
      "name": "BAS",
      "url": "https://data.bas.ac.uk/",
    },
    "BAVJ": {
      "name": "BAVJ",
      "url": "https://www.bav-astro.eu",
    },
    "BICEP2": {
      "name": "BICEP2",
      "url": "http://bicepkeck.org",
    },
    "CADC": {
      "name": "CADC",
      "url": "http://www.canfar.phys.uvic.ca/en",
    },
    "Caltech": {
      "name": "Caltech",
      "url": "https://data.caltech.edu",
    },
    "CDS": {
      "name": "CDS",
      "url": "http://cdsweb.u-strasbg.fr",
    },
    "Chandra": {
      "name": "Chandra",
      "url": "http://cxc.harvard.edu/cda",
    },
    "ClimateDataStore": {
      "name": "ClimateDataStore",
      "url": "https://cds.climate.copernicus.eu/#!/home",
    },
    "CMDN": {
      "name": "CMDN",
      "url": "http://data.cma.cn/en",
    },
    "CXO": {
      "name": "CXO",
      "url": "https://cxc.harvard.edu/cda/",
    },
    "DARTS": {
      "name": "DARTS",
      "url": "https://darts.isas.jaxa.jp/",
    },
    "Dataverse": {
      "name": "Dataverse",
      "url": "",
    },
    "Dryad": {
      "name": "Dryad",
      "url": "https://datadryad.org",
    },
    "dryad": {
      "name": "dryad",
      "url": "https://datadryad.org",
    },
    "EARTHCHEM": {
      "name": "EARTHCHEM",
      "url": "https://www.earthchem.org/",
    },
    "ECMWF": {
      "name": "ECMWF",
      "url": "https://www.ecmwf.int/",
    },
    "EMFISIS": {
      "name": "EMFISIS",
      "url": "https://emfisis.physics.uiowa.edu/",
    },
    "ERGSC": {
      "name": "ERGSC",
      "url": "https://ergsc.isee.nagoya-u.ac.jp/",
    },
    "ESA": {
      "name": "ESA",
      "url": "http://archives.esac.esa.int",
    },
    "ESGF": {
      "name": "ESGF",
      "url": "https://esgf-node.llnl.gov/projects/esgf-llnl/",
    },
    "ESO": {
      "name": "ESO",
      "url": "http://archive.eso.org",
    },
    "ETHZ": {
      "name": "ETHZ",
      "url": "https://www.research-collection.ethz.ch/",
    },
    "FDSN": {
      "name": "FDSN",
      "url": "https://www.fdsn.org/",
    },
    "Figshare": {
      "name": "Figshare",
      "url": "https://figshare.com",
    },
    "figshare": {
      "name": "figshare",
      "url": "https://figshare.com",
    },
    "GCPD": {
      "name": "GCPD",
      "url": "http://obswww.unige.ch/gcpd/",
    },
    "Gemini": {
      "name": "Gemini",
      "url": "https://archive.gemini.edu/searchform",
    },
    "Github": {
      "name": "Github",
      "url": "https://github.com",
    },
    "GRAS": {
      "name": "GRAS",
      "url": "http://moon.bao.ac.cn",
    },
    "GTC": {
      "name": "GTC",
      "url": "http://gtc.sdc.cab.inta-csic.es/gtc/",
    },
    "HEASARC": {
      "name": "HEASARC",
      "url": "https://heasarc.gsfc.nasa.gov/",
    },
    "Herschel": {
      "name": "Herschel",
      "url": "https://www.cosmos.esa.int/web/herschel/home",
    },
    "IBVS": {
      "name": "IBVS",
      "url": "http://ibvs.konkoly.hu/IBVS/IBVS.html",
    },
    "INES": {
      "name": "INES",
      "url": "http://sdc.cab.inta-csic.es/ines/",
    },
    "IRIS": {
      "name": "IRIS",
      "url": "https://ds.iris.edu/ds/",
    },
    "IRSA": {
      "name": "IRSA",
      "url": "https://irsa.ipac.caltech.edu/frontpage/",
    },
    "ISO": {
      "name": "ISO",
      "url": "https://www.cosmos.esa.int/web/iso",
    },
    "JOSS": {
      "name": "JOSS",
      "url": "https://joss.theoj.org/",
    },
    "JWST": {
      "name": "JWST",
      "url": "http://www.stsci.edu/jwst",
    },
    "KOA": {
      "name": "KOA",
      "url": "https://koa.ipac.caltech.edu",
    },
    "LAADS": {
      "name": "LAADS",
      "url": "https://ladsweb.modaps.eosdis.nasa.gov/",
    },
    "LASP": {
      "name": "LASP",
      "url": "https://lasp.colorado.edu/home/",
    },
    "LPL": {
      "name": "LPL",
      "url": "https://www.lpl.arizona.edu/",
    },
    "MAST": {
      "name": "MAST",
      "url": "http://archive.stsci.edu",
    },
    "MetOffice": {
      "name": "MetOffice",
      "url": "https://www.metoffice.gov.uk/",
    },
    "MIT": {
      "name": "MIT",
      "url": "https://web.mit.edu/",
    },
    "NASA": {
      "name": "NASA",
      "url": "https://data.nas.nasa.gov",
    },
    "NCAR": {
      "name": "NCAR",
      "url": "https://ncar.ucar.edu/",
    },
    "NED": {
      "name": "NED",
      "url": "https://ned.ipac.caltech.edu",
    },
    "NExScI": {
      "name": "NExScI",
      "url": "https://exoplanetarchive.ipac.caltech.edu",
    },
    "NOAA": {
      "name": "NOAA",
      "url": "https://www.ncdc.noaa.gov/",
    },
    "NOAO": {
      "name": "NOAO",
      "url": "https://www.noao.edu",
    },
    "OSF": {
      "name": "OSF",
      "url": "https://osf.io/",
    },
    "PANGAEA": {
      "name": "PANGAEA",
      "url": "https://www.pangaea.de",
    },
    "pangaea": {
      "name": "pangaea",
      "url": "https://www.pangaea.de",
    },
    "PASA": {
      "name": "PASA",
      "url": "http://www.publish.csiro.au",
    },
    "PDG": {
      "name": "PDG",
      "url": "http://pdglive.lbl.gov",
    },
    "PDS": {
      "name": "PDS",
      "url": "https://pds.jpl.nasa.gov",
    },
    "PDSS": {
      "name": "PDSS",
      "url": "https://pds.jpl.nasa.gov",
    },
    "PIK": {
      "name": "PIK",
      "url": "https://dataservices.gfz-potsdam.de/portal/",
    },
    "protocols": {
      "name": "protocols",
      "url": "https://www.protocols.io",
    },
    "ScienceBase": {
      "name": "ScienceBase",
      "url": "https://www.sciencebase.gov/catalog/",
    },
    "SIMBAD": {
      "name": "SIMBAD",
      "url": "http://simbad.u-strasbg.fr",
    },
    "Spitzer": {
      "name": "Spitzer",
      "url": "https://irsa.ipac.caltech.edu/Missions/spitzer.html",
    },
    "TDR": {
      "name": "TDR",
      "url": "https://dataverse.tdl.org/",
    },
    "THEMIS": {
      "name": "THEMIS",
      "url": "http://themis.ssl.berkeley.edu/index.shtml",
    },
    "TNS": {
      "name": "TNS",
      "url": "https://wis-tns.weizmann.ac.il",
    },
    "UNAVCO": {
      "name": "UNAVCO",
      "url": "https://www.unavco.org/",
    },
    "Vizier": {
      "name": "Vizier",
      "url": "http://vizier.u-strasbg.fr",
    },
    "XMM": {
      "name": "XMM",
      "url": "http://nxsa.esac.esa.int",
    },
    "Zenodo": {
      "name": "Zenodo",
      "url": "https://zenodo.org",
    },
}

# to allow for case insensitive search
# add any new data subtype as follows:
# if all upper case then key and value listed all upper case
# if case sensitive key is upper case and value is case senstive so list as new_sub_type.upper():new_sub_type
RESOLVER_DATA_TYPES = {
    'AcA'.upper():'AcA', 'ALMA':'ALMA', 'ARI':'ARI', 'Astroverse'.upper():'Astroverse', 'ATNF':'ATNF',
    'Author'.upper():'Author', 'BAVJ':'BAVJ', 'BICEP2':'BICEP2', 'CADC':'CADC', 'CDS':'CDS',
    'Chandra'.upper():'Chandra', 'Dryad'.upper():'Dryad', 'ESA':'ESA', 'ESO':'ESO', 'Figshare'.upper():'Figshare',
    'GCPD':'GCPD', 'Gemini'.upper():'Gemini', 'Github'.upper():'Github', 'GTC':'GTC', 'HEASARC':'HEASARC',
    'Herschel'.upper():'Herschel', 'IBVS':'IBVS', 'INES':'INES', 'IRSA':'IRSA', 'ISO':'ISO', 'JWST':'JWST', 'KOA':'KOA',
    'LPL':'LPL', 'MAST':'MAST', 'NED':'NED', 'NExScI'.upper():'NExScI', 'NOAO':'NOAO', 'PANGAEA':'PANGAEA', 'PASA':'PASA',
    'PDG':'PDG', 'PDS':'PDS', 'protocols'.upper():'protocols', 'SIMBAD':'SIMBAD', 'Spitzer'.upper():'Spitzer',
    'TNS':'TNS', 'Vizier'.upper():'Vizier', 'XMM':'XMM', 'Zenodo'.upper():'Zenodo'
}