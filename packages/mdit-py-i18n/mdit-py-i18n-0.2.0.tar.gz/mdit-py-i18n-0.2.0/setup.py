# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['mdit_py_i18n']

package_data = \
{'': ['*']}

install_requires = \
['Pygments>=2.16.1,<3.0.0', 'markdown-it-py[plugins]>=3.0.0,<4.0.0']

setup_kwargs = {
    'name': 'mdit-py-i18n',
    'version': '0.2.0',
    'description': 'Markdown i18n and l10n using markdown-it-py',
    'long_description': "<!--\nSPDX-FileCopyrightText: 2023 Phu Hung Nguyen <phuhnguyen@outlook.com>\nSPDX-License-Identifier: CC-BY-SA-4.0\n-->\n\n# mdit-py-i18n\n\nMarkdown i18n and l10n using markdown-it-py.\n\nCommonMark compliant. All core Markdown elements are supported, as well as\ntable, and definition list. Front matter handlers are left for users to\nimplement.\n\n## Install\n\n```bash\npip install mdit-py-i18n\n```\n\n## Notes\n\nSome notes about how different elements are handled:\n- Inlines: hard line breaks are replaced with `<br />`, newlines and\nconsecutive spaces are not kept;\n- Content of each HTML block isn't parsed into finer tokens but processed\nas a whole;\n- Fenced code blocks: disabled by default. When enabled, only `//` and `#`\nsingle comments are processed;\n\n## Usage\n\n### Extraction\n- Implement `I18NEntryProtocol` and `DomainExtractionProtocol`\n- Subclass `RendererMarkdownI18N`\n\n### Generation\n- Implement `DomainGenerationProtocol`\n- Subclass `RendererMarkdownL10N`\n\n## Development\n\n### Environment\n\n- With Conda\n\n```bash\nconda env create -f environment.yml\nconda activate mpi\npoetry install\n```",
    'author': 'Phu Hung Nguyen',
    'author_email': 'phuhnguyen@outlook.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/phunh/mdit-py-i18n',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
