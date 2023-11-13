import setuptools

# print(setuptools.find_packages())
setuptools.setup(
    name='xquantipy',
    version='0.2.1',
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
        'beautifulsoup4',
        'matplotlib',
        'numpy',
        'pandas',
        'pipreqs',
        'plotly',
        'pytest',
        'python_dateutil',
        'Requests',
        'seaborn',
        'setuptools',
        'statsmodels',
        'yfinance',
    ],
)