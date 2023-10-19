# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['ampel',
 'ampel.contrib.hu',
 'ampel.contrib.hu.alert',
 'ampel.contrib.hu.alert.load',
 'ampel.contrib.hu.ingest',
 'ampel.contrib.hu.t0',
 'ampel.contrib.hu.t2',
 'ampel.contrib.hu.t3',
 'ampel.contrib.hu.t3.complement',
 'ampel.contrib.hu.t3.tns',
 'ampel.contrib.hu.test',
 'ampel.contrib.hu.util']

package_data = \
{'': ['*'],
 'ampel.contrib.hu.t2': ['data/*'],
 'ampel.contrib.hu.test': ['test-data/*']}

install_requires = \
['adjustText>=0.7.3,<0.8.0',
 'ampel-alerts>=0.8.5,<0.9.0',
 'ampel-interface>=0.8.8,<0.9.0',
 'ampel-lsst>=0.8.6,<0.9.0',
 'ampel-photometry>=0.8.3,<0.9.0',
 'ampel-plot>=0.8.3,<0.9.0',
 'astropy>=5.0,<6.0',
 'backoff>=2,<3',
 'beautifulsoup4>=4.10.0,<5.0.0',
 'corner>=2.2.1,<3.0.0',
 'light-curve>=0.7.3,<0.8.0',
 'more-itertools>=9.0.0,<10.0.0',
 'nltk>=3.7,<4.0',
 'numpy>=1,<2',
 'pandas>=1.3.3,<2.0.0',
 'psutil>=5.9.5,<6.0.0',
 'requests==2.29.0',
 'scikit-learn>=1.1.3,<2.0.0',
 'scipy>=1.4,<2.0',
 'seaborn>=0.12.0,<0.13.0',
 'uncertainties>=3.1.7,<4.0.0',
 'ztfquery>=1.19.1,<2.0.0']

extras_require = \
{':extra == "extcats"': ['extcats>=2.4.2,<3.0.0'],
 ':extra == "ligo"': ['healpy>=1.16.2,<2.0.0'],
 ':extra == "ligo" or extra == "sncosmo"': ['sncosmo>=2.5.0,<3.0.0',
                                            'iminuit>=2.8.0,<3.0.0',
                                            'sfdmap2>=0.2.0,<0.3.0'],
 ':extra == "ligo" or extra == "ztf"': ['ampel-ztf[kafka]>=0.8.6,<0.9.0'],
 'elasticc': ['xgboost>=1.6.2,<2.0.0',
              'astro-parsnip>=1.3.1',
              'timeout-decorator>=0.5,<0.6'],
 'notebook': ['jupyter>=1.0.0,<2.0.0'],
 'slack': ['slack-sdk>=3,<4'],
 'voevent': ['voevent-parse>=1.0.3,<2.0.0']}

setup_kwargs = {
    'name': 'ampel-hu-astro',
    'version': '0.8.3.dev267297206',
    'description': 'Astronomy units for the Ampel system from HU-Berlin',
    'long_description': '<img align="left" src="https://user-images.githubusercontent.com/17532220/213287034-0209aa19-f8a1-418f-a325-7472510542cb.png" width="150" height="150"/>\n<br>\n\n# AMPEL-HU-astro\n<br><br>\n\n\nContributed Ampel units from HU/DESY group\n==========================================\n\nDemo install instructions:\n==========================\n\nCreate environment with python 3.10+ / poetry. Then run:\n\n\n* `git clone https://github.com/AmpelProject/Ampel-HU-astro.git`\n* `cd Ampel-HU-astro/`\n* `poetry install -E "ztf sncosmo extcats notebook"`\n* `cd notebooks`\n* `poetry run jupyter notebook`\n\nThis will allow a number of Demo / access / development notebooks to be run. Note that most of them\nrequires an access token if data is to be retrieved.\n\nContains as of Nov 2022:\n========================\n\nT0\n--\n* SimpleDecentFilter\n* LensedTransientFilter\n* NoFilter\n* RandFilter\n* SEDmTargetFilter\n* SimpleDecentFilter\n* ToOFilter\n* TransientInClusterFilter\n* TransientInEllipticalFilter\n* XShooterFilter\n* RcfFilter\n* RedshiftCatalogFilter\n\nT2\n--\n* T2PanStarrThumbPrint\n* T2PhaseLimit\n* T2PS1ThumbExtCat\n* T2PS1ThumbNedSNCosmo\n* T2PS1ThumbNedTap\n* T2LCQuality\n* T2BrightSNProb\n* T2TNSEval\n* T2InfantCatalogEval\n* T2RunSncosmo\n* T2CatalogMatchLocal\n* T2DigestRedshifts\n* T2RunPossis\n* T2RunTDE\n* T2RunParsnip\n* T2RunSnoopy\n* T2MatchBTS\n* T2NedTap\n* T2NedSNCosmo\n* T2PropagateStockInfo\n* T2GetLensSNParameters\n* T2LSPhotoZTap\n* T2ElasticcRedshiftSampler\n* T2TabulatorRiseDecline\n* T2XgbClassifier\n* T2ElasticcReport\n* T2FastDecliner\n\nT3\n--\n* TransientInfoPrinter\n* TransientViewDumper\n* ChannelSummaryPublisher\n* SlackSummaryPublisher\n* RapidBase\n* RapidSedm\n* RapidLco\n* TNSTalker\n* TNSMirrorUpdater\n* TransientTablePublisher\n* HealpixCorrPlotter\n* PlotLightcurveSample\n* ElasticcClassPublisher\n* VOEventPublisher\n',
    'author': 'Valery Brinnel',
    'author_email': 'None',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://ampelproject.github.io',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.10,<3.12',
}


setup(**setup_kwargs)
