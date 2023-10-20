# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['abses', 'abses.algorithms', 'abses.tools']

package_data = \
{'': ['*']}

install_requires = \
['fiona>=1.9.4.post1,<2.0.0',
 'hydra-core>=1.3.2,<2.0.0',
 'mesa-geo>=0.5.0,<0.6.0',
 'netcdf4>=1.6.2,<2.0.0',
 'pint>=0.20.1,<0.21.0',
 'prettytable>=3.6.0,<4.0.0',
 'xarray>=2023.8.0,<2024.0.0']

setup_kwargs = {
    'name': 'abses',
    'version': '0.2.0a0',
    'description': 'ABSESpy makes it easier to build artificial Social-ecological systems with real GeoSpatial datasets and fully incorporate human behaviour.',
    'long_description': '![ABSES_banner](https://songshgeo-picgo-1302043007.cos.ap-beijing.myqcloud.com/uPic/CleanShot%202023-10-19%20at%2019.08.12@2x.png)\n\n\n<div style="text-align: center;">\n    <!-- License Badge -->\n    <a href="http://www.apache.org/licenses/">\n        <img src="https://img.shields.io/github/license/songshgeo/absespy" alt="license">\n    </a>\n    <!-- Downloads Badge -->\n    <img src="https://img.shields.io/github/downloads/songshgeo/absespy/total" alt="downloads">\n    <!-- Code Size Badge -->\n    <img src="https://img.shields.io/github/languages/code-size/songshgeo/absespy" alt="codesize">\n    <!-- Tag Badge -->\n    <img src="https://img.shields.io/github/v/tag/songshgeo/absespy" alt="tag">\n    <br>\n    <!-- Website Badge -->\n    <a href="https://cv.songshgeo.com/">\n        <img src="https://img.shields.io/badge/Website-SongshGeo-brightgreen.svg" alt="github">\n    </a>\n    <!-- Stars Badge -->\n    <img src="https://img.shields.io/github/stars/songshgeo/absespy?style=social" alt="stars">\n    <!-- Twitter Badge -->\n    <a href="https://twitter.com/shuangsong11">\n        <img src="https://img.shields.io/twitter/follow/shuangsong11?style=social" alt="twitter">\n    </a>\n</div>\n\n<!-- Language: [English Readme](#) | [简体中文](README_ch) -->\n\nAn Agent-Based computational framework makes modeling artificial **[Social-ecological systems](https://songshgeo.github.io/ABSESpy/docs/about/)** easier.\n\n## Why `ABSESpy`?\n\nAgent-based model (ABM) is essential for social-ecological systems (SES) research. `ABSESpy` is designed for modeling **couples humans and nature systems** by:\n\n- Allow users to develop modules separately and coupling them together.\n- Automatically portray interactions between social actors and natural cells with `Networkx`\n- By applying a [human behavior modeling framework]((https://songshgeo.github.io/ABSESpy/docs/background/#human-behaviour-framework)), users can define, select, and track agents of the model in more intuitive ways.\n- Manage and test complex parameters [with a `yaml` file](https://songshgeo.github.io/ABSESpy/tutorial/notebooks/parameters/).\n- access information between cells and social actors by their locations\n- Auto-update real-world datasets and relate the ticks counter to the real-world time.\n## Basic Usage & Documents\n\nInstall with pip or your favorite PyPI package manager.\n\n```\npip install abses\n```\n\nAccess the [Documentation here](https://songshgeo.github.io/ABSESpy/).\n\n<img src="https://songshgeo-picgo-1302043007.cos.ap-beijing.myqcloud.com/uPic/DQg0xJ.jpg" alt="Drawing" style="width: 600px;"/>\n\n## Get in touch\n\n- **For enthusiastic developers and contributors**, all contributions, bug reports, bug fixes, documentation improvements, enhancements, and ideas are welcome.\n- **SES researchers** are welcome to use this package in social-ecological system (SES) studies. It would be appreciated if you contribute a published model to our gallery.\n\nIf you need any help when using `ABSESpy`, don\'t hesitate to get in touch with us through:\n\n- Ask usage questions ("How to do?") on\xa0[_GitHub_\xa0Discussions](https://github.com/SongshGeo/ABSESpy/discussions).\n- Report bugs, suggest features, or view the source code\xa0[on\xa0_GitHub_ Issues](https://github.com/SongshGeo/ABSESpy/issues).\n- Use the [mailing list](https://groups.google.com/g/absespy) for less well-defined questions or ideas or to announce other projects of interest to `ABSESpy` users.\n\n## License\n\nCopyright 2023, `ABSESpy` [Shuang Song](https://cv.songshgeo.com/)\n\nLicensed under the Apache License, Version 2.0 (the "License"); you may not use this file except in compliance with the License. You may obtain a copy of the License at\n\n[https://www.apache.org/licenses/LICENSE-2.0](https://www.apache.org/licenses/LICENSE-2.0)\n\nUnless required by applicable law or agreed to in writing, software distributed under the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the License for the specific language governing permissions and limitations under the License.\n\n`ABSESpy` bundles portions of `Mesa`, `mesa-geo`, `pandas`, `NumPy`, and `Xarray`; the full text of these licenses are included in the licenses directory.\n\n## Thanks to all contributors\n\n<a href="https://github.com/ABSESpy/ABSESpy/graphs/contributors">\n  <img src="https://contrib.rocks/image?repo=ABSESpy/ABSESpy" />\n</a>\n',
    'author': 'Shuang Song',
    'author_email': 'songshgeo@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4',
}


setup(**setup_kwargs)
