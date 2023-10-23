from setuptools import setup #type: ignore

setup(
    name='chadhmm',
    packages = ['chadhmm','chadhmm/hmm','chadhmm/hsmm'],
    version='0.2.1',
    description='Package for Hidden (Semi-)Markov Models',
    author='GarroshIcecream',
    author_email='ad.pesek13@gmail.com',
    url='https://github.com/GarroshIcecream/ChadHMM',
    download_url = 'https://github.com/GarroshIcecream/ChadHMM/archive/refs/tags/v0.2.tar.gz',
    license='MIT',
    keywords=['Hidden Markov Models','Hidden Semi-Markov Models','hsmm','hmm','Gaussian Mixture Models', 'gmm'],
    install_requires=['torch','matplotlib','scikit-learn','numpy','prettytable'],
    classifiers=[
        'Development Status :: 1 - Planning',
        'Programming Language :: Python :: 3',
        'Operating System :: OS Independent',
        'Intended Audience :: Science/Research',
    ]
)