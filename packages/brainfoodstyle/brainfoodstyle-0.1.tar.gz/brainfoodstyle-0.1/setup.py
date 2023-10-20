from setuptools import setup

readme = open("./README.md", "r")


setup(
    name='brainfoodstyle',
    packages=['bfstyle'],  # this must be the same as the name above
    version='0.1',
    description='Librería de estilo plots Brain Food',
    long_description=readme.read(),
    long_description_content_type='text/markdown',
    author='J. Ignacio del Rio',
    author_email='jorge.delrio@ug.uchile.cl',
    # use the URL to the github repo
    #url='https://github.com/nelsonher019/nelsonsaludo',
    #download_url='https://github.com/nelsonher019/nelsonsaludo/tarball/0.1',
    keywords=['brainfood', 'style', 'plot'],
    classifiers=[ ],
    license='MIT',
    include_package_data=True
)