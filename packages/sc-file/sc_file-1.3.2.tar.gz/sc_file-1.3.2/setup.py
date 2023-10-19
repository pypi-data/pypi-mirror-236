# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['scfile',
 'scfile.files',
 'scfile.files.output',
 'scfile.files.source',
 'scfile.utils']

package_data = \
{'': ['*']}

modules = \
['build']
install_requires = \
['lz4[block]>=4.3.2,<5.0.0']

entry_points = \
{'console_scripts': ['build = build:build']}

setup_kwargs = {
    'name': 'sc-file',
    'version': '1.3.2',
    'description': '',
    'long_description': '# Converting STALCRAFT Files Library\n\nLibrary for converting encrypted stalcraft game files, such as models and textures into well-known formats. \\\nYou can use compiled utility from [Releases](https://github.com/onejeuu/sc-file/releases) page.\n\n\n### Formats\n\n`.mcsa` `->` `.obj` \\\n`.mic` `->` `.png` \\\n`.ol` `->` `.dds`\n\n\n## Install:\n\n### Pip\n```console\npip install scfile -U\n```\n\n<details>\n<summary>Manual</summary>\n\n```console\ngit clone git@github.com:onejeuu/sc-file.git\n```\n\n```console\ncd sc-file\n```\n\n```console\npoetry install\n```\n\nOr\n\n```console\npip install -r requirements.txt\n```\n</details>\n\n## Usage:\n\n### Simple\n```python\nfrom scfile import mcsa_to_obj, mic_to_png, ol_to_dds\n\nmcsa_to_obj("path/to/file.mcsa", "path/to/file.obj")\nmic_to_png("path/to/file.mic", "path/to/file.png")\nol_to_dds("path/to/file.ol", "path/to/file.dds")\n```\n\n### Advanced\n```python\nfrom scfile import McsaFile, MicFile, OlFile\nfrom scfile import BinaryReader\n\nwith BinaryReader("path/to/file.ol") as reader:\n    ol = OlFile(reader).to_dds()\n\nwith open("path/to/file.dds", "wb") as fp:\n    fp.write(ol)\n```\n\n### CLI Utility\n\n```console\nSCF.exe --source path/to/file.mcsa\n```\n\n```console\nSCF.exe --source path/to/file.ol --output path/to/file.dds\n```\n\n\n## Build:\n```console\npoetry run build\n```\n',
    'author': 'onejeuu',
    'author_email': 'bloodtrail@beber1k.ru',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'py_modules': modules,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.11,<3.13',
}


setup(**setup_kwargs)
