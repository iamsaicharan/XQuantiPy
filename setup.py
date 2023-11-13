import setuptools

# print(setuptools.find_packages())
setuptools.setup(
    name='xquantipy',
    version='0.2.0',
    author='Sai Charan Vadakapur',
    description='Module for financial analysis',
    packages=setuptools.find_packages(),
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3',
        'Intended Audience :: Developers',
    ],
    platforms=['any'],
    install_requires=[
        'beautifulsoup4>=4.12.2'
        'matplotlib>=3.8.0'
        'numpy>=1.26.1'
        'pandas>=2.1.2'
        'pipreqs>=0.4.13'
        'plotly>=5.18.0'
        'pytest>=7.4.0'
        'python_dateutil>=2.8.2'
        'Requests>=2.31.0'
        'seaborn>=0.13.0'
        'setuptools>=68.0.0'
        'statsmodels>=0.14.0'
        'yfinance>=0.2.29'
    ],
)