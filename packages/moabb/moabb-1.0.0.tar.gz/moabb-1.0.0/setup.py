# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['moabb',
 'moabb.analysis',
 'moabb.datasets',
 'moabb.datasets.compound_dataset',
 'moabb.evaluations',
 'moabb.paradigms',
 'moabb.pipelines',
 'moabb.tests']

package_data = \
{'': ['*'],
 'moabb': ['results/GridSearch_WithinSession/FakeDataset-imagery-10-2-2-lefthandrighthand-c3czc4/1/session_0/FakePipeline/*',
           'results/GridSearch_WithinSession/FakeDataset-imagery-10-2-2-lefthandrighthand-c3czc4/1/session_1/FakePipeline/*',
           'results/GridSearch_WithinSession/FakeDataset-imagery-10-2-2-lefthandrighthand-c3czc4/10/session_0/FakePipeline/*',
           'results/GridSearch_WithinSession/FakeDataset-imagery-10-2-2-lefthandrighthand-c3czc4/10/session_1/FakePipeline/*',
           'results/GridSearch_WithinSession/FakeDataset-imagery-10-2-2-lefthandrighthand-c3czc4/2/session_0/FakePipeline/*',
           'results/GridSearch_WithinSession/FakeDataset-imagery-10-2-2-lefthandrighthand-c3czc4/2/session_1/FakePipeline/*',
           'results/GridSearch_WithinSession/FakeDataset-imagery-10-2-2-lefthandrighthand-c3czc4/3/session_0/FakePipeline/*',
           'results/GridSearch_WithinSession/FakeDataset-imagery-10-2-2-lefthandrighthand-c3czc4/3/session_1/FakePipeline/*',
           'results/GridSearch_WithinSession/FakeDataset-imagery-10-2-2-lefthandrighthand-c3czc4/4/session_0/FakePipeline/*',
           'results/GridSearch_WithinSession/FakeDataset-imagery-10-2-2-lefthandrighthand-c3czc4/4/session_1/FakePipeline/*',
           'results/GridSearch_WithinSession/FakeDataset-imagery-10-2-2-lefthandrighthand-c3czc4/5/session_0/FakePipeline/*',
           'results/GridSearch_WithinSession/FakeDataset-imagery-10-2-2-lefthandrighthand-c3czc4/5/session_1/FakePipeline/*',
           'results/GridSearch_WithinSession/FakeDataset-imagery-10-2-2-lefthandrighthand-c3czc4/6/session_0/FakePipeline/*',
           'results/GridSearch_WithinSession/FakeDataset-imagery-10-2-2-lefthandrighthand-c3czc4/6/session_1/FakePipeline/*',
           'results/GridSearch_WithinSession/FakeDataset-imagery-10-2-2-lefthandrighthand-c3czc4/7/session_0/FakePipeline/*',
           'results/GridSearch_WithinSession/FakeDataset-imagery-10-2-2-lefthandrighthand-c3czc4/7/session_1/FakePipeline/*',
           'results/GridSearch_WithinSession/FakeDataset-imagery-10-2-2-lefthandrighthand-c3czc4/8/session_0/FakePipeline/*',
           'results/GridSearch_WithinSession/FakeDataset-imagery-10-2-2-lefthandrighthand-c3czc4/8/session_1/FakePipeline/*',
           'results/GridSearch_WithinSession/FakeDataset-imagery-10-2-2-lefthandrighthand-c3czc4/9/session_0/FakePipeline/*',
           'results/GridSearch_WithinSession/FakeDataset-imagery-10-2-2-lefthandrighthand-c3czc4/9/session_1/FakePipeline/*',
           'results/Models_WithinSession/FakeDataset-imagery-10-2-2-lefthandrighthand-c3czc4/1/session_0/FakePipeline/*',
           'results/Models_WithinSession/FakeDataset-imagery-10-2-2-lefthandrighthand-c3czc4/1/session_0/Log '
           'Variance LDA/*',
           'results/Models_WithinSession/FakeDataset-imagery-10-2-2-lefthandrighthand-c3czc4/1/session_1/FakePipeline/*',
           'results/Models_WithinSession/FakeDataset-imagery-10-2-2-lefthandrighthand-c3czc4/1/session_1/Log '
           'Variance LDA/*',
           'results/Models_WithinSession/FakeDataset-imagery-10-2-2-lefthandrighthand-c3czc4/10/session_0/FakePipeline/*',
           'results/Models_WithinSession/FakeDataset-imagery-10-2-2-lefthandrighthand-c3czc4/10/session_0/Log '
           'Variance LDA/*',
           'results/Models_WithinSession/FakeDataset-imagery-10-2-2-lefthandrighthand-c3czc4/10/session_1/FakePipeline/*',
           'results/Models_WithinSession/FakeDataset-imagery-10-2-2-lefthandrighthand-c3czc4/10/session_1/Log '
           'Variance LDA/*',
           'results/Models_WithinSession/FakeDataset-imagery-10-2-2-lefthandrighthand-c3czc4/2/session_0/FakePipeline/*',
           'results/Models_WithinSession/FakeDataset-imagery-10-2-2-lefthandrighthand-c3czc4/2/session_0/Log '
           'Variance LDA/*',
           'results/Models_WithinSession/FakeDataset-imagery-10-2-2-lefthandrighthand-c3czc4/2/session_1/FakePipeline/*',
           'results/Models_WithinSession/FakeDataset-imagery-10-2-2-lefthandrighthand-c3czc4/2/session_1/Log '
           'Variance LDA/*',
           'results/Models_WithinSession/FakeDataset-imagery-10-2-2-lefthandrighthand-c3czc4/3/session_0/FakePipeline/*',
           'results/Models_WithinSession/FakeDataset-imagery-10-2-2-lefthandrighthand-c3czc4/3/session_0/Log '
           'Variance LDA/*',
           'results/Models_WithinSession/FakeDataset-imagery-10-2-2-lefthandrighthand-c3czc4/3/session_1/FakePipeline/*',
           'results/Models_WithinSession/FakeDataset-imagery-10-2-2-lefthandrighthand-c3czc4/3/session_1/Log '
           'Variance LDA/*',
           'results/Models_WithinSession/FakeDataset-imagery-10-2-2-lefthandrighthand-c3czc4/4/session_0/FakePipeline/*',
           'results/Models_WithinSession/FakeDataset-imagery-10-2-2-lefthandrighthand-c3czc4/4/session_0/Log '
           'Variance LDA/*',
           'results/Models_WithinSession/FakeDataset-imagery-10-2-2-lefthandrighthand-c3czc4/4/session_1/FakePipeline/*',
           'results/Models_WithinSession/FakeDataset-imagery-10-2-2-lefthandrighthand-c3czc4/4/session_1/Log '
           'Variance LDA/*',
           'results/Models_WithinSession/FakeDataset-imagery-10-2-2-lefthandrighthand-c3czc4/5/session_0/FakePipeline/*',
           'results/Models_WithinSession/FakeDataset-imagery-10-2-2-lefthandrighthand-c3czc4/5/session_0/Log '
           'Variance LDA/*',
           'results/Models_WithinSession/FakeDataset-imagery-10-2-2-lefthandrighthand-c3czc4/5/session_1/FakePipeline/*',
           'results/Models_WithinSession/FakeDataset-imagery-10-2-2-lefthandrighthand-c3czc4/5/session_1/Log '
           'Variance LDA/*',
           'results/Models_WithinSession/FakeDataset-imagery-10-2-2-lefthandrighthand-c3czc4/6/session_0/FakePipeline/*',
           'results/Models_WithinSession/FakeDataset-imagery-10-2-2-lefthandrighthand-c3czc4/6/session_0/Log '
           'Variance LDA/*',
           'results/Models_WithinSession/FakeDataset-imagery-10-2-2-lefthandrighthand-c3czc4/6/session_1/FakePipeline/*',
           'results/Models_WithinSession/FakeDataset-imagery-10-2-2-lefthandrighthand-c3czc4/6/session_1/Log '
           'Variance LDA/*',
           'results/Models_WithinSession/FakeDataset-imagery-10-2-2-lefthandrighthand-c3czc4/7/session_0/FakePipeline/*',
           'results/Models_WithinSession/FakeDataset-imagery-10-2-2-lefthandrighthand-c3czc4/7/session_0/Log '
           'Variance LDA/*',
           'results/Models_WithinSession/FakeDataset-imagery-10-2-2-lefthandrighthand-c3czc4/7/session_1/FakePipeline/*',
           'results/Models_WithinSession/FakeDataset-imagery-10-2-2-lefthandrighthand-c3czc4/7/session_1/Log '
           'Variance LDA/*',
           'results/Models_WithinSession/FakeDataset-imagery-10-2-2-lefthandrighthand-c3czc4/8/session_0/FakePipeline/*',
           'results/Models_WithinSession/FakeDataset-imagery-10-2-2-lefthandrighthand-c3czc4/8/session_0/Log '
           'Variance LDA/*',
           'results/Models_WithinSession/FakeDataset-imagery-10-2-2-lefthandrighthand-c3czc4/8/session_1/FakePipeline/*',
           'results/Models_WithinSession/FakeDataset-imagery-10-2-2-lefthandrighthand-c3czc4/8/session_1/Log '
           'Variance LDA/*',
           'results/Models_WithinSession/FakeDataset-imagery-10-2-2-lefthandrighthand-c3czc4/9/session_0/FakePipeline/*',
           'results/Models_WithinSession/FakeDataset-imagery-10-2-2-lefthandrighthand-c3czc4/9/session_0/Log '
           'Variance LDA/*',
           'results/Models_WithinSession/FakeDataset-imagery-10-2-2-lefthandrighthand-c3czc4/9/session_1/FakePipeline/*',
           'results/Models_WithinSession/FakeDataset-imagery-10-2-2-lefthandrighthand-c3czc4/9/session_1/Log '
           'Variance LDA/*'],
 'moabb.tests': ['None/GridSearch_CrossSession/FakeDataset/1/C/*',
                 'None/GridSearch_CrossSession/FakeDataset/2/C/*',
                 'None/GridSearch_CrossSubject/FakeDataset/C/*',
                 'None/GridSearch_WithinSession/FakeDataset/subject1/session_0/C/*',
                 'None/GridSearch_WithinSession/FakeDataset/subject1/session_1/C/*',
                 'None/GridSearch_WithinSession/FakeDataset/subject2/session_0/C/*',
                 'None/GridSearch_WithinSession/FakeDataset/subject2/session_1/C/*',
                 'res_test/GridSearch_CrossSession/FakeDataset/1/C/*',
                 'res_test/GridSearch_CrossSession/FakeDataset/2/C/*',
                 'res_test/GridSearch_CrossSubject/FakeDataset/C/*',
                 'res_test/GridSearch_WithinSession/FakeDataset/subject1/session_0/C/*',
                 'res_test/GridSearch_WithinSession/FakeDataset/subject1/session_1/C/*',
                 'res_test/GridSearch_WithinSession/FakeDataset/subject2/session_0/C/*',
                 'res_test/GridSearch_WithinSession/FakeDataset/subject2/session_1/C/*',
                 'test_pipelines/*']}

install_requires = \
['PyYAML>=6.0,<7.0',
 'coverage>=7.0.1,<8.0.0',
 'edflib-python>=1.0.6,<2.0.0',
 'h5py<=3.8.0',
 'matplotlib>=3.6.2,<4.0.0',
 'memory-profiler>=0.61.0,<0.62.0',
 'mne-bids>=0.13,<0.14',
 'mne>=1.4,<2.0',
 'numpy>=1.22,<2.0',
 'pandas>=1.5.2,<2.0.0',
 'pooch>=1.6.0,<2.0.0',
 'pyriemann>=0.5,<0.6',
 'pytest>=7.4.0,<8.0.0',
 'requests>=2.28.1,<3.0.0',
 'scikit-learn>=1.2.0,<2.0.0',
 'scipy>=1.9.3,<2.0.0',
 'seaborn>=0.12.1,<0.13.0',
 'tqdm>=4.64.1,<5.0.0',
 'urllib3>=1.26.15,<2.0.0']

extras_require = \
{'carbonemission': ['codecarbon>=2.1.4,<3.0.0'],
 'deeplearning': ['tensorflow>=2.10,<2.13',
                  'keras>=1.11.0',
                  'scikeras>=0.12.0,<0.13.0',
                  'braindecode>=0.7,<0.8',
                  'torch>=1.13.1,<2.0.0',
                  'libclang>=15.0,<16.0']}

setup_kwargs = {
    'name': 'moabb',
    'version': '1.0.0',
    'description': 'Mother of All BCI Benchmarks',
    'long_description': '# Mother of all BCI Benchmarks\n\n<p align=center>\n  <img alt="banner" src="/images/M.png/">\n</p>\n<p align=center>\n  Build a comprehensive benchmark of popular Brain-Computer Interface (BCI) algorithms applied on an extensive list of freely available EEG datasets.\n</p>\n\n## Disclaimer\n\n**This is an open science project that may evolve depending on the need of the\ncommunity.**\n\n[![Build Status](https://github.com/NeuroTechX/moabb/workflows/Test/badge.svg)](https://github.com/NeuroTechX/moabb/actions?query=branch%3Amaster)\n[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)\n[![PyPI](https://img.shields.io/pypi/v/moabb?color=blue&style=plastic)](https://img.shields.io/pypi/v/moabb)\n[![Downloads](https://pepy.tech/badge/moabb)](https://pepy.tech/project/moabb)\n\n## Welcome!\n\nFirst and foremost, Welcome! :tada: Willkommen! :confetti_ball: Bienvenue!\n:balloon::balloon::balloon:\n\nThank you for visiting the Mother of all BCI Benchmark repository.\n\nThis document is a hub to give you some information about the project. Jump straight to\none of the sections below, or just scroll down to find out more.\n\n- [What are we doing? (And why?)](#what-are-we-doing)\n- [Installation](#installation)\n- [Running](#running)\n- [Supported datasets](#supported-datasets)\n- [Who are we?](#who-are-we)\n- [Get in touch](#contact-us)\n- [Documentation][link_moabb_docs]\n- [Architecture and main concepts](#architecture-and-main-concepts)\n- [Citing MOABB and related publications](#citing-moabb-and-related-publications)\n\n## What are we doing?\n\n### The problem\n\n[Brain-Computer Interfaces](https://en.wikipedia.org/wiki/Brain%E2%80%93computer_interface)\nallow to interact with a computer using brain signals. In this project, we focus mostly on\nelectroencephalographic signals\n([EEG](https://en.wikipedia.org/wiki/Electroencephalography)), that is a very active\nresearch domain, with worldwide scientific contributions. Still:\n\n- Reproducible Research in BCI has a long way to go.\n- While many BCI datasets are made freely available, researchers do not publish code, and\n  reproducing results required to benchmark new algorithms turns out to be trickier than\n  it should be.\n- Performances can be significantly impacted by parameters of the preprocessing steps,\n  toolboxes used and implementation “tricks” that are almost never reported in the\n  literature.\n\nAs a result, there is no comprehensive benchmark of BCI algorithms, and newcomers are\nspending a tremendous amount of time browsing literature to find out what algorithm works\nbest and on which dataset.\n\n### The solution\n\nThe Mother of all BCI Benchmarks allows to:\n\n- Build a comprehensive benchmark of popular BCI algorithms applied on an extensive list\n  of freely available EEG datasets.\n- The code is available on GitHub, serving as a reference point for the future algorithmic\n  developments.\n- Algorithms can be ranked and promoted on a website, providing a clear picture of the\n  different solutions available in the field.\n\nThis project will be successful when we read in an abstract “ … the proposed method\nobtained a score of 89% on the MOABB (Mother of All BCI Benchmarks), outperforming the\nstate of the art by 5% ...”.\n\n## Installation\n\n### Pip installation\n\nTo use MOABB, you could simply do: \\\n`pip install MOABB` \\\nSee [Troubleshooting](#Troubleshooting) section if you have a problem.\n\n### Manual installation\n\nYou could fork or clone the repository and go to the downloaded directory, then run:\n\n1. install `poetry` (only once per machine):\\\n   `curl -sSL https://install.python-poetry.org | python3 -`\\\n   or [checkout installation instruction](https://python-poetry.org/docs/#installation) or\n   use [conda forge version](https://anaconda.org/conda-forge/poetry)\n1. (Optional, skip if not sure) Disable automatic environment creation:\\\n   `poetry config virtualenvs.create false`\n1. install all dependencies in one command (have to be run in the project directory):\\\n   `poetry install`\n\nSee [contributors\' guidelines](CONTRIBUTING.md) for detailed explanation.\n\n### Requirements we use\n\nSee `pyproject.toml` file for full list of dependencies\n\n## Running\n\n### Verify Installation\n\nTo ensure it is running correctly, you can also run\n\n```\npython -m unittest moabb.tests\n```\n\nonce it is installed.\n\n### Use MOABB\n\nFirst, you could take a look at our [tutorials](./tutorials) that cover the most important\nconcepts and use cases. Also, we have a several [examples](./examples/) available.\n\nYou might be interested in [MOABB documentation][link_moabb_docs]\n\n### Moabb and docker\n\nMoabb has a default image to run the benchmark. You have two options to download this\nimage: build from scratch or pull from the docker hub. **We recommend pulling from the\ndocker hub**.\n\nIf this were your first time using docker, you would need to **install the docker** and\n**login** on docker hub. We recommend the\n[official](https://docs.docker.com/desktop/install/linux-install/) docker documentation\nfor this step, it is essential to follow the instructions.\n\nAfter installing docker, you can pull the image from the docker hub:\n\n```bash\ndocker pull baristimunha/moabb\n# rename the tag to moabb\ndocker tag baristimunha/moabb moabb\n```\n\nIf you want to build the image from scratch, you can use the following command at the\nroot. You may have to login with the API key in the\n[NGC Catalog](https://catalog.ngc.nvidia.com/) to run this command.\n\n```bash\nbash docker/create_docker.sh\n```\n\nWith the image downloaded or rebuilt from scratch, you will have an image called `moabb`.\nTo run the default benchmark, still at the root of the project, and you can use the\nfollowing command:\n\n```bash\nmkdir dataset\nmkdir results\nmkdir output\nbash docker/run_docker.sh PATH_TO_ROOT_FOLDER\n```\n\nAn example of the command is:\n\n```bash\ncd /home/user/project/moabb\nmkdir dataset\nmkdir results\nmkdir output\nbash docker/run_docker.sh /home/user/project/moabb\n```\n\nNote: It is important to use an absolute path for the root folder to run, but you can\nmodify the run_docker.sh script to save in another path beyond the root of the project. By\ndefault, the script will save the results in the project\'s root in the folder `results`,\nthe datasets in the folder `dataset` and the output in the folder `output`.\n\n### Troubleshooting\n\nCurrently pip install moabb fails when pip version < 21, e.g. with 20.0.2 due to an `idna`\npackage conflict. Newer pip versions resolve this conflict automatically. To fix this you\ncan upgrade your pip version using: `pip install -U pip` before installing `moabb`.\n\n## Supported datasets\n\nThe list of supported datasets can be found here :\nhttps://neurotechx.github.io/moabb/datasets.html\n\nDetailed information regarding datasets (electrodes, trials, sessions) are indicated on\nthe wiki: https://github.com/NeuroTechX/moabb/wiki/Datasets-Support\n\n### Submit a new dataset\n\nyou can submit a new dataset by mentioning it to this\n[issue](https://github.com/NeuroTechX/moabb/issues/1). The datasets currently on our radar\ncan be seen [here](https://github.com/NeuroTechX/moabb/wiki/Datasets-Support).\n\n## Who are we?\n\nThe founders of the Mother of all BCI Benchmarks are [Alexander Barachant][link_alex_b]\nand [Vinay Jayaram][link_vinay]. This project is under the umbrella of\n[NeuroTechX][link_neurotechx], the international community for NeuroTech enthusiasts. The\nproject is currently maintained by [Sylvain Chevallier][link_sylvain].\n\n### What do we need?\n\n**You**! In whatever way you can help.\n\nWe need expertise in programming, user experience, software sustainability, documentation\nand technical writing and project management.\n\nWe\'d love your feedback along the way.\n\nOur primary goal is to build a comprehensive benchmark of popular BCI algorithms applied\non an extensive list of freely available EEG datasets, and we\'re excited to support the\nprofessional development of any and all of our contributors. If you\'re looking to learn to\ncode, try out working collaboratively, or translate your skills to the digital domain,\nwe\'re here to help.\n\n### Get involved\n\nIf you think you can help in any of the areas listed above (and we bet you can) or in any\nof the many areas that we haven\'t yet thought of (and here we\'re _sure_ you can) then\nplease check out our [contributors\' guidelines](CONTRIBUTING.md) and our\n[roadmap](ROADMAP.md).\n\nPlease note that it\'s very important to us that we maintain a positive and supportive\nenvironment for everyone who wants to participate. When you join us we ask that you follow\nour [code of conduct](CODE_OF_CONDUCT.md) in all interactions both on and offline.\n\n## Contact us\n\nIf you want to report a problem or suggest an enhancement, we\'d love for you to\n[open an issue](../../issues) at this GitHub repository because then we can get right on\nit.\n\nFor a less formal discussion or exchanging ideas, you can also reach us on the [Gitter\nchannel][link_gitter] or join our weekly office hours! This an open video meeting\nhappening on a [regular basis](https://github.com/NeuroTechX/moabb/issues/191), please ask\nthe link on the gitter channel. We are also on [NeuroTechX Slack #moabb\nchannel][link_neurotechx_signup].\n\n## Architecture and Main Concepts\n\n<p align="center">\n  <img alt="banner" src="/images/architecture.png/" width="400">\n</p>\nThere are 4 main concepts in the MOABB: the datasets, the paradigm, the evaluation, and the pipelines. In addition, we offer statistical and visualization utilities to simplify the workflow.\n\n### Datasets\n\nA dataset handles and abstracts low-level access to the data. The dataset will read data\nstored locally, in the format in which they have been downloaded, and will convert them\ninto a MNE raw object. There are options to pool all the different recording sessions per\nsubject or to evaluate them separately.\n\n### Paradigm\n\nA paradigm defines how the raw data will be converted to trials ready to be processed by a\ndecoding algorithm. This is a function of the paradigm used, i.e. in motor imagery one can\nhave two-class, multi-class, or continuous paradigms; similarly, different preprocessing\nis necessary for ERP vs ERD paradigms.\n\n### Evaluations\n\nAn evaluation defines how we go from trials per subject and session to a generalization\nstatistic (AUC score, f-score, accuracy, etc) -- it can be either within-recording-session\naccuracy, across-session within-subject accuracy, across-subject accuracy, or other\ntransfer learning settings.\n\n### Pipelines\n\nPipeline defines all steps required by an algorithm to obtain predictions. Pipelines are\ntypically a chain of sklearn compatible transformers and end with a sklearn compatible\nestimator. See\n[Pipelines](http://scikit-learn.org/stable/modules/generated/sklearn.pipeline.Pipeline.html)\nfor more info.\n\n### Statistics and visualization\n\nOnce an evaluation has been run, the raw results are returned as a DataFrame. This can be\nfurther processed via the following commands to generate some basic visualization and\nstatistical comparisons:\n\n```\nfrom moabb.analysis import analyze\n\nresults = evaluation.process(pipeline_dict)\nanalyze(results)\n```\n\n## Citing MOABB and related publications\n\nTo cite MOABB, you could use the following paper:\n\n> Vinay Jayaram and Alexandre Barachant.\n> ["MOABB: trustworthy algorithm benchmarking for BCIs."](http://iopscience.iop.org/article/10.1088/1741-2552/aadea0/meta)\n> Journal of neural engineering 15.6 (2018): 066011.\n> [DOI](https://doi.org/10.1088/1741-2552/aadea0)\n\nIf you publish a paper using MOABB, please contact us on [gitter][link_gitter] or open an\nissue, and we will add your paper to the\n[dedicated wiki page](https://github.com/NeuroTechX/moabb/wiki/MOABB-bibliography).\n\n## Thank You\n\nThank you so much (Danke schön! Merci beaucoup!) for visiting the project and we do hope\nthat you\'ll join us on this amazing journey to build a comprehensive benchmark of popular\nBCI algorithms applied on an extensive list of freely available EEG datasets.\n\n[link_alex_b]: http://alexandre.barachant.org/\n[link_vinay]: https://ei.is.tuebingen.mpg.de/~vjayaram\n[link_neurotechx]: http://neurotechx.com/\n[link_sylvain]: https://sylvchev.github.io/\n[link_neurotechx_signup]: https://neurotechx.com/\n[link_gitter]: https://app.gitter.im/#/room/#moabb_dev_community:gitter.im\n[link_moabb_docs]: https://neurotechx.github.io/moabb/\n[link_arxiv]: https://arxiv.org/abs/1805.06427\n[link_jne]: http://iopscience.iop.org/article/10.1088/1741-2552/aadea0/meta\n',
    'author': 'Alexandre Barachant',
    'author_email': 'None',
    'maintainer': 'Sylvain Chevallier',
    'maintainer_email': 'sylvain.chevallier@universite-paris-saclay.fr',
    'url': 'https://github.com/NeuroTechX/moabb',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.8,<3.12',
}


setup(**setup_kwargs)
