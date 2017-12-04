DROP TABLE IF EXISTS datalinks;
CREATE TABLE datalinks(
      bibcode VARCHAR ,
      link_type VARCHAR,
      link_sub_type VARCHAR,
      url VARCHAR,
      title VARCHAR,
      item_count INTEGER
      );


INSERT INTO public.datalinks VALUES ('2013MNRAS.435.1904M', 'ESOURCE',      'EPRINT_HTML', '{http://arxiv.org/abs/1307.6556}', '{}', 0);
INSERT INTO public.datalinks VALUES ('2013MNRAS.435.1904M', 'ESOURCE',      'EPRINT_PDF',  '{http://arxiv.org/pdf/1307.6556}', '{}', 0);
INSERT INTO public.datalinks VALUES ('2013MNRAS.435.1904M', 'ESOURCE',      'PUB_HTML',    '{http://dx.doi.org/10.1093%2Fmnras%2Fstt1379}', '{}', 0);
INSERT INTO public.datalinks VALUES ('2013MNRAS.435.1904M', 'ESOURCE',      'PUB_PDF',     '{http://mnras.oxfordjournals.org/content/435/3/1904.full.pdf}', '{}', 0);
INSERT INTO public.datalinks VALUES ('2013MNRAS.435.1904M', 'DATA',         'CXO',         '{"http://cda.harvard.edu/chaser?obsid=494"}', '{"Chandra Data Archive ObsIds 494"}', 27);
INSERT INTO public.datalinks VALUES ('2013MNRAS.435.1904M', 'DATA',         'ESA',         '{http://archives.esac.esa.int/ehst/#bibcode=2013MNRAS.435.1904M}', '{"European HST References (EHST)"}', 1);
INSERT INTO public.datalinks VALUES ('2013MNRAS.435.1904M', 'DATA',         'HEASARC',     '{http://heasarc.gsfc.nasa.gov/cgi-bin/W3Browse/biblink.pl?code=2013MNRAS.435.1904M}', '{""}', 1);
INSERT INTO public.datalinks VALUES ('2013MNRAS.435.1904M', 'DATA',         'Herschel',    '{http://herschel.esac.esa.int/hpt/publicationdetailsview.do?bibcode=2013MNRAS.435.1904M}', '{""}', 1);
INSERT INTO public.datalinks VALUES ('2013MNRAS.435.1904M', 'DATA',         'MAST',        '{http://archive.stsci.edu/mastbibref.php?bibcode=2013MNRAS.435.1904M}', '{"MAST References (GALEX EUVE HST)"}', 3);
INSERT INTO public.datalinks VALUES ('2013MNRAS.435.1904M', 'DATA',         'NED',         '{http://$NED$/cgi-bin/nph-objsearch?search_type=Search&refcode=2013MNRAS.435.1904M}', '{"NED Objects (1)"}', 1);
INSERT INTO public.datalinks VALUES ('2013MNRAS.435.1904M', 'DATA',         'SIMBAD',      '{http://$SIMBAD$/simbo.pl?bibcode=2013MNRAS.435.1904M}', '{"SIMBAD Objects (30)"}', 30);
INSERT INTO public.datalinks VALUES ('2013MNRAS.435.1904M', 'DATA',         'XMM',         '{http://nxsa.esac.esa.int/nxsa-web/#obsid=0097820101}', '{"XMM-Newton Observation Number 0097820101"}', 1);
INSERT INTO public.datalinks VALUES ('2017MNRAS.467.3556B', 'PRESENTATION', '',            '{http://www.astro.lu.se/~alexey/animations.html}', '{}', 0);
INSERT INTO public.datalinks VALUES ('1971ATsir.615....4D', 'ASSOCIATED',   '',            '{1971ATsir.615....4D,1971ATsir.621....7D,1971ATsir.624....1D,1973ATsir.759....6D,1974Afz....10..315D,1974ATsir.809....1D,1974ATsir.809....2D,1974ATsir.837....2D,1976Afz....12..665D,1983Afz....19..229D,1983Ap.....19..134D,1984Afz....20..525D,1984Ap.....20..290D}', '{"Part  1","Part  3","Part  5","Part  8","Part  2","Part 11","Part 12","Part 13","Part  4","Part  6","Part  7","Part  9","Part 10"}', 0);
