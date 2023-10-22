# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['markdown_gettext']

package_data = \
{'': ['*']}

install_requires = \
['mdit-py-i18n>=0.2.0,<0.3.0', 'polib>=1.2.0,<2.0.0']

extras_require = \
{':python_version >= "3.10"': ['PyYAML>=6.0.1,<7.0.0'],
 ':python_version >= "3.8" and python_version < "3.10"': ['PyYAML>=5.3,<6.0']}

entry_points = \
{'console_scripts': ['markdown-gettext = markdown_gettext.cli:main',
                     'md-gettext = markdown_gettext.cli:main']}

setup_kwargs = {
    'name': 'markdown-gettext',
    'version': '0.2.0',
    'description': 'Markdown i18n with gettext',
    'long_description': "<!--\nSPDX-FileCopyrightText: 2023 Phu Hung Nguyen <phuhnguyen@outlook.com>\nSPDX-License-Identifier: CC-BY-SA-4.0\n-->\n\n# markdown-gettext\n\nA command line program to do i18n and l10n for individual Markdown files.\n\nCommonMark compliant. All core Markdown elements are supported, as well as\nYAML front matter, table, and definition list.\n\n## Install\n\n```bash\npip install markdown-gettext\n```\n\n## Usage\n\nYou can use either `md-gettext` or `markdown-gettext` command\n\n#### Extraction\n```\nmd-gettext extract [-p PACKAGE] [-r REPORT_ADDR] [-t TEAM_ADDR] md pot\n\npositional arguments:\n  md                    path of the Markdown file to extract messages from\n  pot                   path of the POT file to create\n\noptional arguments:\n  -p PACKAGE, --package PACKAGE\n                        the package name in POT metadata\n  -r REPORT_ADDR, --report-addr REPORT_ADDR\n                        the report address in POT metadata\n  -t TEAM_ADDR, --team-addr TEAM_ADDR\n                        the team address in POT metadata\n```\n\n#### Generation\n```\nmd-gettext generate [-l LANG] in-md po out-md\n\npositional arguments:\n  in-md                 path of the source Markdown file\n  po                    path of the PO file containing translations\n  out-md                path of the Markdown file to create\n\noptional arguments:\n  -l LANG, --lang LANG  language of translations\n```\n\n## Notes\n\nSome notes about how different elements are handled:\n- Inlines: hard line breaks are replaced with `<br />`, newlines and\nconsecutive spaces are not kept;\n- Content of each HTML block isn't parsed into finer tokens but processed\nas a whole;\n\n## Development environment\n\n- With Conda\n\n```bash\nconda env create -f environment.yml\nconda activate mg\npoetry install\n```\n",
    'author': 'Phu Hung Nguyen',
    'author_email': 'phuhnguyen@outlook.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/phunh/markdown-gettext',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
