from setuptools import setup
from setuptools import find_packages

setup( 
    name='cashflex', 
    version='1.0.1', 
    description='Cashflex Money Manager', 
    author='Gary Barnes', 
    author_email='gary.barnes2023@gmail.com', 
    python_requires='>=3.10',
    packages=['cashflex'],
    include_package_data=True,
    install_requires=[ 
        'matplotlib>=3.8', 
    ],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: End Users/Desktop',
        'License :: Free for non-commercial use',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Topic :: Office/Business :: Financial :: Accounting',
    ],
    project_urls={
        'Documentation': 'https://github.com/gary-1959/cashflex/blob/main/README.md',
        'Source': 'https://github.com/gary-1959/cashflex',
        'Tracker': 'https://github.com/gary-1959/cashflex/issues',
    },
) 