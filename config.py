
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
      "name": '4TU.ResearchData',
      "url": 'International data repository for science, engineering and design',
    },
    "AcA": {
      "name": 'AcA',
      "url": 'Acta Astronomica Data Files',
    },
    "ALMA": {
      "name": 'ALMA',
      "url": 'Atacama Large Millimeter/submillimeter Array',
    },
    "ArcticData": {
      "name": 'ArcticData',
      "url": 'Arctic Data Center',
    },
    "ARI": {
      "name": 'ARI',
      "url": 'Astronomisches Rechen-Institut',
    },
    "AstroGeo": {
      "name": 'AstroGeo',
      "url": 'USGS Astrogeology Science Center',
    },
    "Astroverse": {
      "name": 'Astroverse',
      "url": 'CfA Dataverse',
    },
    "ASU": {
      "name": 'ASU',
      "url": 'Arizona State University',
    },
    "ATNF": {
      "name": 'ATNF',
      "url": 'Australia Telescope Online Archive',
    },
    "Author": {
      "name": 'Author',
      "url": 'Author Hosted Dataset',
    },
    "BAS": {
      "name": 'BAS',
      "url": 'British Antarctic Survey',
    },
    "BAVJ": {
      "name": 'BAVJ',
      "url": 'Data of the German Association for Variable Stars',
    },
    "BICEP2": {
      "name": 'BICEP2',
      "url": 'BICEP/Keck Data',
    },
    "CADC": {
      "name": 'CADC',
      "url": 'Canadian Astronomy Data Center',
    },
    "Caltech": {
      "name": 'Caltech',
      "url": 'California Institute of Technology',
    },
    "CDS": {
      "name": 'CDS',
      "url": 'Strasbourg Astronomical Data Center',
    },
    "CMDN": {
      "name": 'CMDN',
      "url": 'China Meteorological Data Service Centre',
    },
    "Chandra": {
      "name": 'Chandra',
      "url": 'Chandra X-Ray Observatory',
    },
    "ClimateDataStore": {
      "name": 'ClimateDataStore',
      "url": 'Climate Data Store',
    },
    "DARTS": {
      "name": 'DARTS',
      "url": 'Data ARchives and Transmission System',
    },
    "Dataverse": {
      "name": 'Dataverse',
      "url": 'Dataverse Project',
    },
    "Dryad": {
      "name": 'Dryad',
      "url": 'International Repository of Research Data',
    },
    "EARTHCHEM": {
      "name": 'EARTHCHEM',
      "url": 'Open-access repository for geochemical datasets',
    },
    "ECMWF": {
      "name": 'ECMWF',
      "url": 'European Centre for Medium-Range Weather Forecasts',
    },
    "EMFISIS": {
      "name": 'EMFISIS',
      "url": 'An instrument suite on the Van Allen Probes',
    },
    "ERGSC": {
      "name": 'ERGSC',
      "url": 'ERG Science Center',
    },
    "ESA": {
      "name": 'ESA',
      "url": 'ESAC Science Data Center',
    },
    "ESGF": {
      "name": 'ESGF',
      "url": 'Earth System Grid Federation',
    },
    "ESO": {
      "name": 'ESO',
      "url": 'European Southern Observatory',
    },
    "Figshare": {
      "name": 'Figshare',
      "url": 'Online Open Access Repository',
    },
    "GCPD": {
      "name": 'GCPD',
      "url": 'The General Catalogue of Photometric Data',
    },
    "Github": {
      "name": 'Github',
      "url":
        'Web-based version-control and collaboration platform for software developers.',
    },
    "GRAS": {
      "name": 'GRAS',
      "url": 'Lunar and Planet Exploration Program Ground Application System',
    },
    "GTC": {
      "name": 'GTC',
      "url": 'Gran Telescopio CANARIAS Public Archive',
    },
    "HEASARC": {
      "name": 'HEASARC',
      "url":
        "NASA's High Energy Astrophysics Science Archive Research Center",
    },
    "Herschel": {
      "name": 'Herschel',
      "url": 'Herschel Science Center',
    },
    "IBVS": {
      "name": 'IBVS',
      "url": 'Information Bulletin on Variable Stars',
    },
    "INES": {
      "name": 'INES',
      "url": 'IUE Newly Extracted Spectra',
    },
    "IRSA": {
      "name": 'IRSA',
      "url": 'NASA/IPAC Infrared Science Archive',
    },
    "ISO": {
      "name": 'ISO',
      "url": 'Infrared Space Observatory',
    },
    "JWST": {
      "name": 'JWST',
      "url": 'JWST Proposal Info',
    },
    "KOA": {
      "name": 'KOA',
      "url": 'Keck Observatory Archive',
    },
    "MAST": {
      "name": 'MAST',
      "url": 'Mikulski Archive for Space Telescopes',
    },
    "NED": {
      "name": 'NED',
      "url": 'NASA/IPAC Extragalactic Database',
    },
    "NExScI": {
      "name": 'NExScI',
      "url": 'NASA Exoplanet Archive',
    },
    "NOAO": {
      "name": 'NOAO',
      "url": 'National Optical Astronomy Observatory',
    },
    "PANGAEA": {
      "name": 'PANGAEA',
      "url":
        'Digital Data Library and a Data Publisher for Earth System Science',
    },
    "PASA": {
      "name": 'PASA',
      "url":
        'Publication of the Astronomical Society of Australia Datasets',
    },
    "PDG": {
      "name": 'PDG',
      "url": 'Particle Data Group',
    },
    "PDS": {
      "name": 'PDS',
      "url": 'The NASA Planetary Data System',
    },
    "protocols": {
      "name": 'protocols',
      "url":
        'Collaborative Platform and Preprint Server for Science Methods and Protocols',
    },
    "SIMBAD": {
      "name": 'SIMBAD',
      "url": 'SIMBAD Database at the CDS',
    },
    "Spitzer": {
      "name": 'Spitzer',
      "url": 'Spitzer Space Telescope',
    },
    "TNS": {
      "name": 'TNS',
      "url": 'Transient Name Server',
    },
    "Vizier": {
      "name": 'VizieR',
      "url": 'VizieR Catalog Service',
    },
    "XMM": {
      "name": 'XMM',
      "url": 'XMM Newton Science Archive',
    },
    "Zenodo": {
      "name": 'Zenodo',
      "url": 'Zenodo Archive',
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