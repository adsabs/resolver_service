
# -*- coding: utf-8 -*-

LOG_STDOUT = True

# db config
SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:postgres@localhost:5432/test'
SQLALCHEMY_TRACK_MODIFICATIONS = False
SQLALCHEMY_ECHO = False

# number of records that can be inserted/updated in one call
RESOLVER_MAX_RECORDS_ADD = 100
# number of records that can be deleted in one call
RESOLVER_MAX_RECORDS_DEL = 100
# number of records that can be matched (reconciled) in one call
RESOLVER_MAX_RECORDS_RECON = 100

# This is the URL to communicate with resolver_gateway api
RESOLVER_GATEWAY_URL = 'http://localhost:5050/link_gateway/{bibcode}/{link_type}/{url}'

# This is the URL for deterministic links, needs to go to local-config, once deployed, if need to
RESOLVER_DETERMINISTIC_LINKS_BASEURL = '/abs'

# These URLs are used to create links for doi and arXiv sources
RESOLVER_DOI_LINK_BASEURL = 'https://doi.org/{id}'
RESOLVER_ARXIV_LINK_BASEURL = 'http://arxiv.org/abs/{id}'

RESOLVER_DATA_SOURCES = {
    "4TU.ResearchData": {
      "name": "International data repository for science, engineering and design",
      "url": "https://data.4tu.nl/",
    },
    "AcA": {
      "name": "Acta Astronomica Data Files",
      "url": "ftp://ftp.astrouw.edu.pl",
    },
    "AHED": {
      "name": "Astrobiology Habitable Environments Database",
      "url": "https://ahed.nasa.gov/",
    },
    "ALMA": {
      "name": "Atacama Large Millimeter/submillimeter Array",
      "url": "https://almascience.org/",
    },
    "ArcticData": {
      "name": "Arctic Data Center",
      "url": "https://arcticdata.io/",
    },
    "ARI": {
      "name": "Astronomisches Rechen-Institut",
      "url": "https://zah.uni-heidelberg.de/institutes/ari/",
    },
    "ARTEMIS": {
      "name": "Acceleration Reconnection Turbulence & Electrodynamics of Moon Interaction with the Sun",
      "url": "http://artemis.ssl.berkeley.edu/",
    },
    "AstroGeo": {
      "name": "USGS Astrogeology Science Center",
      "url": "https://www.usgs.gov/centers/astrogeology-science-center",
    },
    "ASU": {
      "name": "Arizona State University",
      "url": "",
    },
    "Astroverse": {
      "name": "CfA Dataverse",
      "url": "https://dataverse.harvard.edu/dataverse/cfa",
    },
    "ATNF": {
      "name": "Australia Telescope Online Archive",
      "url": "https://atoa.atnf.csiro.au",
    },
    "Author": {
      "name": "Author Hosted Dataset"
    },
    "BAS": {
      "name": "British Antarctic Survey",
      "url": "https://data.bas.ac.uk/",
    },
    "BAVJ": {
      "name": "Data of the German Association for Variable Stars",
      "url": "https://www.bav-astro.eu",
    },
    "BICEP2": {
      "name": "BICEP/Keck Data",
      "url": "http://bicepkeck.org",
    },
    "CADC": {
      "name": "Canadian Astronomy Data Center",
      "url": "http://www.canfar.phys.uvic.ca/en",
    },
    "Caltech": {
      "name": "California Institute of Technology",
      "url": "https://data.caltech.edu",
    },
    "CDS": {
      "name": "Strasbourg Astronomical Data Center",
      "url": "http://cdsweb.u-strasbg.fr",
    },
    "Chandra": {
      "name": "Chandra X-Ray Observatory",
      "url": "http://cxc.harvard.edu/cda",
    },
    "ClimateDataStore": {
      "name": "Climate Data Store",
      "url": "https://cds.climate.copernicus.eu/#!/home",
    },
    "CMDN": {
      "name": "China Meteorological Data Service Centre",
      "url": "http://data.cma.cn/en",
    },
    "CXO": {
      "name": "Chandra Data Archive",
      "url": "https://cxc.harvard.edu/cda/",
    },
    "DARTS": {
      "name": "Data ARchives and Transmission System",
      "url": "https://darts.isas.jaxa.jp/",
    },
    "Dataverse": {
      "name": "Dataverse",
      "url": "",
    },
    "Dryad": {
      "name": "International Repository of Research Data",
      "url": "https://datadryad.org",
    },
    "EARTHCHEM": {
      "name": "Open-access repository for geochemical datasets",
      "url": "https://www.earthchem.org/",
    },
    "ECMWF": {
      "name": "European Centre for Medium-Range Weather Forecasts",
      "url": "https://www.ecmwf.int/",
    },
    "EMFISIS": {
      "name": "An instrument suite on the Van Allen Probes",
      "url": "https://emfisis.physics.uiowa.edu/",
    },
    "ERGSC": {
      "name": "ERG Science Center",
      "url": "https://ergsc.isee.nagoya-u.ac.jp/",
    },
    "ESA": {
      "name": "ESAC Science Data Center",
      "url": "http://archives.esac.esa.int",
    },
    "ESGF": {
      "name": "Earth System Grid Federation",
      "url": "https://esgf-node.llnl.gov/projects/esgf-llnl/",
    },
    "ESO": {
      "name": "European Southern Observatory",
      "url": "http://archive.eso.org",
    },
    "ETHZ": {
      "name": "ETH Zurich Research Collection",
      "url": "https://www.research-collection.ethz.ch/",
    },
    "FDSN": {
      "name": "International Federation of Digital Seismograph Networks",
      "url": "https://www.fdsn.org/",
    },
    "Figshare": {
      "name": "Online Open Access Repository",
      "url": "https://figshare.com",
    },
    "GCPD": {
      "name": "The General Catalogue of Photometric Data",
      "url": "http://obswww.unige.ch/gcpd/",
    },
    "Gemini": {
      "name": "Gemini Observatory Archive",
      "url": "https://archive.gemini.edu/searchform",
    },
    "Github": {
      "name": "Git Repository Hosting Service",
      "url": "https://github.com",
    },
    "GRAS": {
      "name": "Lunar and Planet Exploration Program Ground Application System",
      "url": "http://moon.bao.ac.cn",
    },
    "GTC": {
      "name": "Gran Telescopio CANARIAS Public Archive",
      "url": "http://gtc.sdc.cab.inta-csic.es/gtc/",
    },
    "HEASARC": {
      "name": "NASA's High Energy Astrophysics Science Archive Research Center",
      "url": "https://heasarc.gsfc.nasa.gov/",
    },
    "Herschel": {
      "name": "Herschel Science Center",
      "url": "https://www.cosmos.esa.int/web/herschel/home",
    },
    "IBVS": {
      "name": "Information Bulletin on Variable Stars",
      "url": "http://ibvs.konkoly.hu/IBVS/IBVS.html",
    },
    "INES": {
      "name": "IUE Newly Extracted Spectra",
      "url": "http://sdc.cab.inta-csic.es/ines/",
    },
    "IRIS": {
      "name": "Incorporated Research Institutions for Seismology",
      "url": "https://ds.iris.edu/ds/",
    },
    "IRSA": {
      "name": "NASA/IPAC Infrared Science Archive",
      "url": "https://irsa.ipac.caltech.edu/frontpage/",
    },
    "ISO": {
      "name": "Infrared Space Observatory",
      "url": "https://www.cosmos.esa.int/web/iso",
    },
    "JOSS": {
      "name": "Journal of Open Source Software",
      "url": "https://joss.theoj.org/",
    },
    "JWST": {
      "name": "JWST Proposal Info",
      "url": "http://www.stsci.edu/jwst",
    },
    "KOA": {
      "name": "Keck Observatory Archive",
      "url": "https://koa.ipac.caltech.edu",
    },
    "LAADS": {
      "name": "Level-1 and Atmosphere Archive & Distribution System Distributed Active Archive Center",
      "url": "https://ladsweb.modaps.eosdis.nasa.gov/",
    },
    "LASP": {
      "name": "Laboratory for Atmospheric and Space Physics",
      "url": "https://lasp.colorado.edu/home/",
    },
    "LPL": {
      "name": "Lunar and Planetary Laboratory",
      "url": "https://www.lpl.arizona.edu/",
    },
    "MAST": {
      "name": "Mikulski Archive for Space Telescopes",
      "url": "http://archive.stsci.edu",
    },
    "MetOffice": {
      "name": "Met Office",
      "url": "https://www.metoffice.gov.uk/",
    },
    "MIT": {
      "name": "Massachusetts Institute of Technology",
      "url": "https://web.mit.edu/",
    },
    "NASA": {
      "name": "NASA Data Portal",
      "url": "https://data.nas.nasa.gov",
    },
    "NCAR": {
      "name": "National Center for Atmospheric Research",
      "url": "https://ncar.ucar.edu/",
    },
    "NED": {
      "name": "NASA/IPAC Extragalactic Database",
      "url": "https://ned.ipac.caltech.edu",
    },
    "NExScI": {
      "name": "NASA Exoplanet Archive",
      "url": "https://exoplanetarchive.ipac.caltech.edu",
    },
    "NOAA": {
      "name": "National Oceanic and Atmospheric Administration",
      "url": "https://www.ncdc.noaa.gov/",
    },
    "NOAO": {
      "name": "National Optical Astronomy Observatory",
      "url": "https://www.noao.edu",
    },
    "OSF": {
      "name": "Open Science Foundation",
      "url": "https://osf.io/",
    },
    "PANGAEA": {
      "name": "Digital Data Library and a Data Publisher for Earth System Science",
      "url": "https://www.pangaea.de",
    },
    "PASA": {
      "name": "Publication of the Astronomical Society of Australia Datasets",
      "url": "http://www.publish.csiro.au",
    },
    "PDG": {
      "name": "Particle Data Group",
      "url": "http://pdglive.lbl.gov",
    },
    "PDS": {
      "name": "The NASA Planetary Data System",
      "url": "https://pds.jpl.nasa.gov",
    },
    "PDSS": {
      "name": "The NASA Planetary Data System",
      "url": "https://pds.jpl.nasa.gov",
    },
    "PIK": {
      "name": "Potsdam Institute for Climate Impact Research",
      "url": "https://dataservices.gfz-potsdam.de/portal/",
    },
    "protocols": {
      "name": "Collaborative Platform and Preprint Server for Science Methods and Protocols",
      "url": "https://www.protocols.io",
    },
    "ScienceBase": {
      "name": "ScienceBase",
      "url": "https://www.sciencebase.gov/catalog/",
    },
    "SIMBAD": {
      "name": "SIMBAD Database at the CDS",
      "url": "http://simbad.u-strasbg.fr",
    },
    "Spitzer": {
      "name": "Spitzer Space Telescope",
      "url": "https://irsa.ipac.caltech.edu/Missions/spitzer.html",
    },
    "TDR": {
      "name": "Texas Data Respository",
      "url": "https://dataverse.tdl.org/",
    },
    "THEMIS": {
      "name": "Time History of Events and Macroscopic Interactions During Substorms",
      "url": "http://themis.ssl.berkeley.edu/index.shtml",
    },
    "TNS": {
      "name": "Transient Name Server",
      "url": "https://wis-tns.weizmann.ac.il",
    },
    "UNAVCO": {
      "name": "UNAVCO",
      "url": "https://www.unavco.org/",
    },
    "Vizier": {
      "name": "VizieR Catalog Service",
      "url": "http://vizier.u-strasbg.fr",
    },
    "XMM": {
      "name": "XMM Newton Science Archive",
      "url": "http://nxsa.esac.esa.int",
    },
    "Zenodo": {
      "name": "Zenodo Archive",
      "url": "https://zenodo.org",
    },
}

# to allow for case insensitive search
# add any new data subtype as follows:
# if all upper case then key and value listed all upper case
# if case sensitive key is upper case and value is case senstive so list as new_sub_type.upper():new_sub_type
RESOLVER_DATA_TYPES = {label.upper():label for label in RESOLVER_DATA_SOURCES.keys()}