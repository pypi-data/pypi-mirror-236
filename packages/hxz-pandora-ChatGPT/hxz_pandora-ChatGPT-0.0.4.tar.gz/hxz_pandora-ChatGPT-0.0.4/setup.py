# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

from src.hxz_pandora import __version__

with open('README.md', 'r', encoding='utf-8') as f:
    long_description = f.read()

with open('requirements.txt', 'r', encoding='utf-8') as f:
    requirements = f.read().split('\n')

with open('requirements_api.txt', 'r', encoding='utf-8') as f:
    requirements_api = f.read().split('\n')

setup(
    name='hxz_pandora-ChatGPT',
    version=__version__,
    python_requires='>=3.7',
    author='shoot82003',
    author_email='shoot82003@qq.com',
    keywords='OpenAI ChatGPT ChatGPT-Plus gpt-3.5-turbo gpt-3.5-turbo-0301',
    description='A command-line interface to ChatGPT',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/shoot82003/hxz_pandora',
    packages=find_packages('src'),
    package_dir={'hxz_pandora': 'src/hxz_pandora'},
    include_package_data=True,
    install_requires=requirements,
    extras_require={
        'api': requirements_api,
        'cloud': ['hxz_pandora-cloud~=0.0.2'],
    },
    entry_points={
        'console_scripts': [
            'hxz_pandora = hxz_pandora.launcher:run',
            'hxz_pandora-cloud = hxz_pandora.cloud_launcher:run',
        ]
    },
    project_urls={
        'Source': 'https://github.com/shoot82003/hxz_pandora',
        'Tracker': 'https://github.com/shoot82003/hxz_pandora/issues',
    },
    classifiers=[
        'Development Status :: 5 - Production/Stable',

        'Environment :: Console',
        'Environment :: Web Environment',

        'Framework :: Flask',

        'Intended Audience :: Developers',
        'Intended Audience :: End Users/Desktop',

        'License :: OSI Approved :: GNU General Public License v2 (GPLv2)',

        'Natural Language :: English',
        'Natural Language :: Chinese (Simplified)',

        'Operating System :: MacOS',
        'Operating System :: Microsoft :: Windows',
        'Operating System :: POSIX :: Linux',

        'Programming Language :: SQL',
        'Programming Language :: JavaScript',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',

        'Topic :: Communications :: Chat',
        'Topic :: Internet :: WWW/HTTP',
    ],
)
