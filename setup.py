from setuptools import setup

REQUIREMENTS = [
    'beautifulsoup4',
    'matplotlib',
    'numpy',
    'pandas',
    'requests',
    'scikit-learn==1.0.2',
    'more_itertools'
]

setup(
    name='pe_detection',
    version='0.0083',
    description="""\
Tools for PE detection work.
""",
    author='Laurence Dyer',
    author_email='ljdyer@gmail.com',
    url='https://github.com/ljdyer/pe-detection',
    packages=['pe_detection.tools', 'pe_detection.learn.naive_bayes'],
    install_requires=REQUIREMENTS
)
