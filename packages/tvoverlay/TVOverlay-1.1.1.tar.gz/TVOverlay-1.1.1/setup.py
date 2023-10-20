# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['tvoverlay']

package_data = \
{'': ['*']}

install_requires = \
['httpx>=0.23,<1']

setup_kwargs = {
    'name': 'tvoverlay',
    'version': '1.1.1',
    'description': 'Python API for sending notifications to TVOverlay for Android TV',
    'long_description': '# TVOverlay Notifications\n\n### Python API for TVOverlay Notification\n\n<p align="center">\n<picture><img src="https://github.com/gugutab/TvOverlay/blob/main/images/readme_main.png?raw=true" alt="TvOverlay" width="600"></picture>\n<br>\n<a href="https://play.google.com/store/apps/details?id=com.tabdeveloper.tvoverlay">\n<img src="https://github.com/gugutab/TvOverlay/blob/main/images/playstore.png?raw=true" width="300" /></a>\n<a href="https://play.google.com/store/apps/details?id=com.tabdeveloper.tvoverlayremote">\n<img src="https://github.com/gugutab/TvOverlay/blob/main/images/playstore_remote.png?raw=true" width="300" /></a>\t\n</p>\n\nSource: https://github.com/gugutab/TvOverlay\n\n## Usage\n\n- Install the application on your TV\n- Get the IP of the TV unit\n\n```python\nfrom tvoverlay import Notifications\nnotify = Notifications("192.168.1.10")\n\ntry:\n    await notify.async_connect()\nexpect ConnectError:\n    return False\nawait notify.async_send(\n    "message text",\n    title="Title text",\n)\n```\n\n## Optional parameters\n\n```json\n{\n    "message": "Message",\n    "title": "Title",\n    "id": "test1",\n    "appTitle": "Postman",\n    "appIcon": "mdi:unicorn",\n    "color": "#FFC107",\n    "image": "https://picsum.photos/200/100",\n    "smallIcon": "mdi:bell",\n    "largeIcon": "mdi:home-assistant",\n    "corner": "bottom_end",\n    "seconds": 20\n}\n```\n',
    'author': 'Hareesh M U',
    'author_email': 'hareesh.mu@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/hareeshmu/TVOverlay',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
