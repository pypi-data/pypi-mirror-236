# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['protokolo']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'protokolo',
    'version': '0.1.0',
    'description': 'Protokolo is a change log generator.',
    'long_description': "<!--\nSPDX-FileCopyrightText: 2023 Carmen Bianca BAKKER <carmen@carmenbianca.eu>\n\nSPDX-License-Identifier: CC-BY-SA-4.0 OR GPL-3.0-or-later\n-->\n\n# Protokolo\n\nProtokolo is a change log generator.\n\nProtokolo allows you to maintain your change log entries in separate files, and\nthen finally aggregate them into a new section in CHANGELOG just before release.\n\n## Table of Contents\n\n- [Background](#background)\n- [Install](#install)\n- [Usage](#usage)\n- [Maintainers](#maintainers)\n- [Contributing](#contributing)\n- [License](#license)\n\n## Background\n\nChange logs are [a really good idea](https://keepachangelog.com/).\nUnfortunately, they are also a bit of a pain when combined with version control:\n\n- If two pull requests edit CHANGELOG, there is a non-zero chance that you'll\n  need to resolve a conflict when trying to merge them both.\n- Just after you make a release, you need to create a new section in CHANGELOG\n  for your next release. If you forget this busywork, new feature branches will\n  need to create this section, which increases the chance of merge conflicts.\n- If a feature branch adds a change log entry to the section for the next v1.2.3\n  release, and v1.2.3 subsequently releases without merging that feature branch,\n  then merging that feature branch afterwards would still add the change log\n  entry to the v1.2.3 section, even though it should now go to the v1.3.0\n  section.\n\nLife would be a lot easier if you didn't have to deal with these problems.\n\nEnter Protokolo. The idea is very simple: For every change log entry, create a\nnew file. Finally, just before release, compile the contents of those files into\na new section in CHANGELOG, and delete the files.\n\n## Install\n\nTODO\n\n## Usage\n\nTODO\n\n## Maintainers\n\n- Carmen Bianca BAKKER <carmen@carmenbianca.eu>\n\n## Contributing\n\nTODO\n\n## License\n\nAll code is licensed under GPL-3.0-or-later.\n\nAll documentation is licensed under CC-BY-SA-4.0 OR GPL-3.0-or-later.\n\nSome configuration files are licensed under CC0-1.0 OR GPL-3.0-or-later.\n\nThe repository is [REUSE](https://reuse.software)-compliant. Check the\nindividual files for their exact licensing.\n",
    'author': 'Carmen Bianca BAKKER',
    'author_email': 'carmen@carmenbianca.eu',
    'maintainer': 'Carmen Bianca BAKKER',
    'maintainer_email': 'carmen@carmenbianca.eu',
    'url': 'None',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
