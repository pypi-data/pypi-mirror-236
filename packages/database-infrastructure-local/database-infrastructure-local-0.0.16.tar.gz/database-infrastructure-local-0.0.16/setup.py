import setuptools

PACKAGE_NAME = "database-infrastructure-local"
package_dir = "circles_number_generator"

with open('README.md') as f:
    readme = f.read()

setuptools.setup(
    name=PACKAGE_NAME,  # https://pypi.org/project/database-infrastructure-local/
    version='0.0.16',
    author="Circles",
    author_email="info@circles.life",
    url="https://github.com/circles-zone/database-infrastructure-local-python-package",
    packages=[package_dir],
    package_dir={package_dir: f'{package_dir}/src'},
    package_data={package_dir: ['*.py']},
    long_description=readme,
    long_description_content_type='text/markdown',
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: Other/Proprietary License",
        "Operating System :: OS Independent",
    ],
    install_requires=[
        "python-dotenv>=1.0.0",
        "pytest>=7.4.0",
        "logger-local>=0.0.66",
        "database-without-orm-local>=0.0.103"
    ]
)

