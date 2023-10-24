# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['nicegui_highcharts']

package_data = \
{'': ['*'],
 'nicegui_highcharts': ['lib/highcharts/*', 'lib/highcharts/modules/*']}

install_requires = \
['nicegui>=1.3.18']

setup_kwargs = {
    'name': 'nicegui-highcharts',
    'version': '1.0.0',
    'description': 'Add Highcharts elements to your NiceGUI app.',
    'long_description': "# NiceGUI Highcharts\n\nThis package is an extension for [NiceGUI](https://github.com/zauberzeug/nicegui), an easy-to-use, Python-based UI framework.\nIt provides a `highchart` element based on [Highcharts](https://www.highcharts.com/), the popular JavaScript charting library.\nDue to Highcharts' restrictive license, this element is not part of the NiceGUI package anymore, but can be install separately.\n\n## Installation\n\n```bash\npython3 -m pip install nicegui-highcharts\n```\n\n## Usage\n\nWrite your nice GUI in a file `main.py`:\n\n```py\nfrom nicegui import ui\nfrom nicegui_highcharts import highchart\n\nhighchart({\n    'title': False,\n    'chart': {'type': 'bar'},\n    'xAxis': {'categories': ['A', 'B']},\n    'series': [\n        {'name': 'Alpha', 'data': [0.1, 0.2]},\n        {'name': 'Beta', 'data': [0.3, 0.4]},\n    ],\n})\n\nui.run()\n```\n\nLaunch it with:\n\n```bash\npython3 main.py\n```\n",
    'author': 'Zauberzeug GmbH',
    'author_email': 'info@zauberzeug.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/zauberzeug/nicegui-highcharts',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
