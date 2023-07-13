[![Build Status](https://travis-ci.org/adsabs/resolver_service.svg)](https://travis-ci.org/adsabs/resolver_service)
[![Coverage Status](https://coveralls.io/repos/adsabs/resolver_service/badge.svg)](https://coveralls.io/r/adsabs/resolver_service)


# ADS Resolver Service

## Short Summary

This microservice provides links to external resources such as publisher's full text, data links, etc.



## Setup (recommended)

    $ virtualenv python
    $ source python/bin/activate
    $ pip install -r requirements.txt
    $ pip install -r dev-requirements.txt
    $ vim local_config.py # edit, edit
    $ alembic upgrade head # initialize database


    
## Testing

On your desktop run:

    $ py.test
    
    
    
## API

#### Make a GET request with a bibcode to return all links associated with that bibcode:

    curl -H "Authorization: Bearer <your API token>" -X GET https://api.adsabs.harvard.edu/v1/resolver/<bibcode>

For example to return *all* links associated with 2017arXiv170909566R, you would do   

    curl -H "Authorization: Bearer <your API token>" -X GET https://api.adsabs.harvard.edu/v1/resolver/2017arXiv170909566R


#### Make a GET request with a bibcode and link type to return all links of the type specified associated for that bibcode:

    curl -H "Authorization: Bearer <your API token>" -X GET https://api.adsabs.harvard.edu/v1/resolver/<bibcode>/<link_type>

For example to return links for *all*  full text sources, you would do

    curl -H "Authorization: Bearer <your API token>" -X GET https://api.adsabs.harvard.edu/v1/resolver/2013MNRAS.435.1904M/esource

#### Available Link Types:

`<link_type>` is one of the following (case-insensitive):

* **abstract** *Abstract*
* **citations** *Citations to the Article*
* **references** *References in the Article*
* **coreads** *Also-Read Articles*
* **toc** *Table of Contents*
* **openurl**
* **metrics**
* **graphics**
* **esource** *Full text sources*
  * **pub_pdf** *Publisher PDF*
  * **eprint_pdf** *Arxiv eprint*
  * **author_pdf** *Link to PDF page provided by author*
  * **ads_pdf** *ADS PDF*
  * **pub_html** *Electronic on-line publisher article (HTML)*
  * **eprint_html** *Arxiv article*
  * **author_html** *Link to HTML page provided by author*
  * **ads_scan** *ADS scanned article*
  * **gif** *backward compatibility similar to /ads_scan*
  * **preprint** *backward compatibility similar to /eprint_html*
  * **ejournal** *backward compatibility similar to /pub_html*
* **data** *On-line data*
  * **4tu.researchdata** *International data repository for science, engineering and design*
  * **aca** *Acta Astronomica Data Files*
  * **ahed** *Astrobiology Habitable Environments Database*
  * **alma** *Atacama Large Millimeter/submillimeter Array*
  * **arcticdata** *Arctic Data Center*
  * **ari** *Astronomisches Rechen-Institut*
  * **artemis** *Acceleration Reconnection Turbulence & Electrodynamics of Moon Interaction with the Sun*
  * **astrogeo** *USGS Astrogeology Science Center*
  * **astroverse** *CfA Dataverse*
  * **asu** *Arizona State University*
  * **atnf** *Australia Telescope Online Archive*
  * **author** *Author Hosted Dataset*
  * **bas** *British Antarctic Survey*
  * **bavj** *Data of the German Association for Variable Stars*
  * **bicep2** *BICEP/Keck Data*
  * **cadc** *Canadian Astronomy Data Center*
  * **caltech** *California Institute of Technology*
  * **cds** *Strasbourg Astronomical Data Center*
  * **chandra** *Chandra X-Ray Observatory*
  * **climatedatastore** *Climate Data Store*
  * **cmdn** *China Meteorological Data Service Centre*
  * **cxo** *Chandra Data Archive*
  * **darts** *Data ARchives and Transmission System*
  * **dataverse** *Dataverse*
  * **dryad** *International Repository of Research Data*
  * **earthchem** *Open-access repository for geochemical datasets*
  * **ecmwf** *European Centre for Medium-Range Weather Forecasts*
  * **emac** *Exoplanet Modeling and Analysis Center*
  * **emfisis** *An instrument suite on the Van Allen Probes*
  * **ergsc** *ERG Science Center*
  * **esa** *ESAC Science Data Center*
  * **esgf** *Earth System Grid Federation*
  * **eso** *European Southern Observatory*
  * **ethz** *ETH Zurich Research Collection*
  * **fdsn** *International Federation of Digital Seismograph Networks*
  * **figshare** *Online Open Access Repository*
  * **gcpd** *The General Catalogue of Photometric Data*
  * **gemini** *Gemini Observatory Archive*
  * **github** *Git Repository Hosting Service*
  * **gras** *Lunar and Planet Exploration Program Ground Application System*
  * **gsfc** *Goddard Space Flight Center*
  * **gtc** *Gran Telescopio CANARIAS Public Archive*
  * **heasarc** *NASA's High Energy Astrophysics Science Archive Research Center*
  * **herschel** *Herschel Science Center*
  * **ibvs** *Information Bulletin on Variable Stars*
  * **ines** *IUE Newly Extracted Spectra*
  * **iris** *Incorporated Research Institutions for Seismology*
  * **irsa** *NASA/IPAC Infrared Science Archive*
  * **iso** *Infrared Space Observatory*
  * **joss** *Journal of Open Source Software*
  * **jwst** *JWST Proposal Info*
  * **koa** *Keck Observatory Archive*
  * **laads** *Level-1 and Atmosphere Archive & Distribution System Distributed Active Archive Center*
  * **lasp** *Laboratory for Atmospheric and Space Physics*
  * **lpl** *Lunar and Planetary Laboratory*
  * **mast** *Mikulski Archive for Space Telescopes*
  * **mendeley** *Mendeley Data*
  * **metoffice** *Met Office*
  * **mit** *Massachusetts Institute of Technology*
  * **nasa** *NASA Data Portal*
  * **ncar** *National Center for Atmospheric Research*
  * **ned** *NASA/IPAC Extragalactic Database*
  * **nexsci** *NASA Exoplanet Archive*
  * **noaa** *National Oceanic and Atmospheric Administration*
  * **noao** *National Optical Astronomy Observatory*
  * **nrao_prop** *National Radio Astronomy Observatory*
  * **nsidc** *National Snow and Ice Data Center*
  * **osf** *Open Science Foundation*
  * **pangaea** *Digital Data Library and a Data Publisher for Earth System Science*
  * **pasa** *Publication of the Astronomical Society of Australia Datasets*
  * **pdg** *Particle Data Group*
  * **pds** *The NASA Planetary Data System*
  * **pdss** *The NASA Planetary Data System*
  * **pik** *Potsdam Institute for Climate Impact Research*
  * **protocols** *Collaborative Platform and Preprint Server for Science Methods and Protocols*
  * **psa"planetary science archive*
  * **sciencebase** *ScienceBase*
  * **simbad** *SIMBAD Database at the CDS*
  * **spitzer** *Spitzer Space Telescope*
  * **tdr** *Texas Data Respository*
  * **themis** *Time History of Events and Macroscopic Interactions During Substorms*
  * **tns** *Transient Name Server*
  * **unavco** *UNAVCO*
  * **usgs** *United States Geological Survey*
  * **uw** *University of Washington*
  * **vizier** *VizieR Catalog Service*
  * **xmm** *XMM Newton Science Archive*
  * **zenodo** *Zenodo Archive*
* **inspire** *HEP/Spires Information*
* **librarycatalog**
* **presentation** *Multimedia Presentation*
* **associated** *Associated Articles*
    
#### Identification Link Types:

Please note that these links types' endpoints differ slightly from the rest of link types:

    curl -H "Authorization: Bearer <your API token>" -X GET https://api.adsabs.harvard.edu/v1/resolver/<bibcode>/<Identification Link Type>:<id>

where Identification Link Types are: `doi` or `arXiv` and `id` is their respective identification. For example

    curl -H "Authorization: Bearer <your API token>" -X GET https://dev.adsabs.harvard.edu/v1/resolver/2010ApJ...713L.103B/doi:10.1088/2041-8205/713/2/L103
    curl -H "Authorization: Bearer <your API token>" -X GET https://dev.adsabs.harvard.edu/v1/resolver/2018arXiv180303598K/arXiv:1803.03598

#### Insert/Update records in db (internal use only):

    curl -H "Authorization: Bearer <your API token>" -X PUT https://api.adsabs.harvard.edu/v1/resolver/update -d @dataLinksRecordList.json -H "Content-Type: application/json"

where *dataLinksRecordList.json* contains data in the format of protobuf structure *DataLinksRecordList*.



## Maintainer(s)

Golnaz
