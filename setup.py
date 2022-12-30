from setuptools import setup

REQUIREMENTS = [
    'beautifulsoup4',
    'requests',
    'pandas'
]

setup(
    name='pe_detection',
    version='0.0028',
    description="""\
Tools for PE detection work.
""",
    author='Laurence Dyer',
    author_email='ljdyer@gmail.com',
    url='https://github.com/ljdyer/pe-detection',
    packages=['pe_detection.tools'],
    install_requires=REQUIREMENTS
)
