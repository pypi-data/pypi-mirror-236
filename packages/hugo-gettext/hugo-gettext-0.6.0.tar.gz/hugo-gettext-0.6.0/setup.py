# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['hugo_gettext', 'hugo_gettext.extraction', 'hugo_gettext.generation']

package_data = \
{'': ['*']}

install_requires = \
['markdown-gettext>=0.2.1,<0.3.0',
 'mdit-py-hugo>=0.3.1,<0.4.0',
 'mdit-py-i18n>=0.2.1,<0.3.0',
 'tomlkit>=0.12.1,<0.13.0']

entry_points = \
{'console_scripts': ['hugo-gettext = hugo_gettext.cli:main',
                     'hugo-i18n = hugo_gettext.cli:main']}

setup_kwargs = {
    'name': 'hugo-gettext',
    'version': '0.6.0',
    'description': 'I18n with gettext for Hugo',
    'long_description': '<!--\nSPDX-FileCopyrightText: 2023 Phu Hung Nguyen <phuhnguyen@outlook.com>\nSPDX-License-Identifier: CC-BY-SA-4.0\n-->\n\n# hugo-gettext\n\nI18n with gettext for Hugo.\n\nCurrently compliant with Hugo 0.110.0.\n\n## Install\n\n```bash\npip install hugo-gettext\n```\n\n## Usage\n\nThere are three commands corresponding to three steps that _hugo-gettext_\nsupports:\n- `hugo-gettext extract` extracts messages from source files (files in the\nsource language) to one or many POT files;\n- `hugo-gettext compile` compiles PO files to binary MO files;\n- `hugo-gettext generate` uses MO files to generate target files (files in\ntarget languages).\n\nThese are types of text that _hugo-gettext_ can extract messages from and can\ngenerate in target languages:\n- Front matter and content in content files;\n- Strings in string file (i.e. "translation table") in `i18n` folder\n  - `other` keys\n  - Support `comment`\n- Menu item names, site title, and site description in site config file:\nall in `languages.en` config key:\n  - title: `title`\n  - description: `params.description`\n  - menu: `menu.main.<entry>.name`\n- Data in data files: processed as Markdown (front matter text aren\'t\nprocessed as Markdown).\n\nEach project can specify multiple text domains to work with (i.e. messages are\nextracted to multiple POT files and subsequently multiple PO files are\navailable to use for generation), however all types of text outside content\nfiles always belong to a default domain which is derived from a name that each\nproject must have. Content files can be associated with the default domain or\ncustom domains.\n\n### Directory structure in each step\n\n### Compilation\n- From a folder containing subdirectories with PO files inside,\nin the form of `<dir>/<lang_code>/<domain>.po`\n- To a `locale` folder\n- Structure: `locale/<lang_code>/LC_MESSAGES/<domain>.po`\n\n### Generation\n- Conditions in front matter\n- `hugo_lang_code`s are prepended to absolute links in `aliases` dict in front matter\n- How data file generation works\n- Requirement for a language to be qualified\n(a config block is added and data files are generated, string file is generated anyway):\n  - there\'s no content file to translate but string file is translated, or\n  - there are content files to translate and some files are translated\n- A content file is considered translated if\n  - The front matter is translated, or\n  - There\'s nothing in the content, or\n  - The translation rate of the content is higher than 50%\n\n### Markdown\n\nCommonMark compliant. All core Markdown elements are supported, as well as\ntable, and definition list.\n\nSome notes about how different elements are handled:\n- Inlines: hard line breaks are replaced with <br />, newlines and consecutive spaces are not kept;\n- Content of each HTML block isn\'t parsed into finer tokens but processed as a whole;\n\n#### Shortcodes\n- If the string contains only one shortcode\n- Newlines are kept for arguments quoted with backticks\n- hg_stop shortcode to stop processing a content file\n\n#### Attributes\n\n## Configuration\n- `package`: `Project-Id-Version` in POT metadata\n- `default_domain_name`\n- `report_address` and `team_address`: `Report-Msgid-Bugs-To` and `Language-Team` in POT metadata\n- `excluded_keys`: in front matter\n- `excluded_data_keys`: in data files\n- `rtl_langs`\n- `shortcodes`: can use `*` wildcard to indicate all shortcodes\n\n### Custom functions\nThe path of the file should be passed as an argument to the command line with `-c` or `--customs` option,\nor set in the config file with `customs` key.\n\nThe following functions are called to make `default_domain_name`, `excluded_keys`,\n`report_address`, `team_address`, and `rtl_langs` attributes of `Config`:\n- `get_default_domain_name`: will be called with `package` as an argument, returns `package` by default\n- `get_custom_excluded_keys`: returns an empty set by default\n- `get_pot_fields`: returns a dictionary of `\'report_address\'` and `\'team_address\'` keys\n- `get_rtl_langs`: returns a list of codes of RTL languages\n\nTwo functions are called during the generation step:\n- `load_lang_names`: returns an empty dictionary by default\n- `convert_lang_code`: function to convert gettext language codes to Hugo language codes,\nreturns gettext language codes by default\n\n## Development\n\n- With Conda\n\n```bash\nconda env create -f environment.yml\nconda activate hg\npoetry install\n```',
    'author': 'Phu Hung Nguyen',
    'author_email': 'phuhnguyen@outlook.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/phunh/hugo-gettext',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
