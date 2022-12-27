from setuptools import setup

REQUIREMENTS = [
    'beautifulsoup4',
    'requests',
    'pandas'
]

setup(
    name='pe_detection',
    version='0.0005',
    description="""\
Tools for PE detection work.
""",
    author='Laurence Dyer',
    author_email='ljdyer@gmail.com',
    url='https://github.com/ljdyer/pe-detection',
    packages=['pe_detection'],
    install_requires=REQUIREMENTS
)
