import datetime
from setuptools import setup, find_packages, command
from wheel.bdist_wheel import bdist_wheel
from setuptools.command.sdist import sdist
from pypi.constants import *
import argparse


class Package_Builder:

    @staticmethod
    def update_license(license: str, license_file: str = LICENSE_FILE):
        license_index = {
            'MIT': MIT
        }
        lic = license_index.get(license)

        license_text = lic.LICENSE_TEXT

        license_text = license_text.replace('[<YEAR>]', datetime.date.today().strftime('%Y'))
        license_text = license_text.replace('[<FULLNAME>]', AUTHOR)

        with open(license_file, 'w') as f:
            f.write(license_text)

    @staticmethod
    def get_setup_config(version_file: str = VERSION_FILE):
        def load_version(path: str) -> str:
            with open(path, 'r') as f:
                return f.readline().strip()

        setup_config = {
            'name': NAME,
            'description': DESCRIPTION,
            'long_description': LONG_DESCRIPTION,
            'version': load_version(path=version_file),
            'license': LICENSE,
            'url': HOMEPAGE,
            'author': AUTHOR,
            'author_email': AUTHOR_EMAIL,
            'maintainer': MAINTAINER,
            'maintainer_email': MAINTAINER_EMAIL,
            'long_description_content_type': LONG_DESCRIPTION_CONTENT_TYPE,
            'install_requires': INSTALL_REQUIRES,
            'packages': find_packages(),
            'keywords': KEYWORDS,
            'classifiers': CLASSIFIERS
        }

        sanitized_setup_config = {}
        for k in setup_config.keys():
            if setup_config[k]:
                sanitized_setup_config[k] = setup_config[k]

        return sanitized_setup_config


Package_Builder.update_license(license=LICENSE)

setup(
    **Package_Builder.get_setup_config()
)
