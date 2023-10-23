from setuptools import setup, find_packages
from HTTP.version import (__version__)


setup(
    name='CD_HTTP',
    version=__version__,
    description='An HTTP wrapper around the wonderful requests library to make it easier for new users and old.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='codedocta',
    author_email='codedocta@gmail.com',
    url='https://codedocta.com',
    packages=find_packages(),
    install_requires=[
        'requests~=2.31.0',
    ],
    classifiers=[
        # For a list of valid classifiers, see https://pypi.org/classifiers/
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Intended Audience :: Education',
        'Intended Audience :: End Users/Desktop',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
    ],
    project_urls={
        'Bug Reports': 'https://github.com/codedocta/CD_HTTP/issues',  # Replace with your issues URL
        'Source': 'https://github.com/codedocta/CD_HTTP/',  # Replace with your repository URL
    },

)
