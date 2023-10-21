from setuptools import setup

readme = open("./README.md", "r")


setup(
    name='bfstyle',
    packages=['bfstyle'],  # this must be the same as the name above
    version='0.5',
    description='Librería de estilo plots Brain Food',
    long_description=readme.read(),
    long_description_content_type='text/markdown',
    author='J. Ignacio del Rio',
    author_email='jorge.delrio@ug.uchile.cl',
    # use the URL to the github repo
    url='https://github.com/ignacio365/BF_plots',
    download_url='https://github.com/ignacio365/BF_plots/tarball/0.5',
    keywords=['brainfood', 'style', 'plot'],
    classifiers=[ ],
    license='MIT',
    include_package_data=True,
    package_data={
        # If any package contains *.ttf , include them:
        '': ['.ttf'],
    },
)