from setuptools import setup

REQUIREMENTS = [
    'beautifulsoup4',
    'matplotlib',
    'numpy',
    'pandas',
    'requests'
]

setup(
    name='pe_detection',
    version='0.0036',
    description="""\
Tools for PE detection work.
""",
    author='Laurence Dyer',
    author_email='ljdyer@gmail.com',
    url='https://github.com/ljdyer/pe-detection',
    packages=['pe_detection.tools'],
    install_requires=REQUIREMENTS
)
