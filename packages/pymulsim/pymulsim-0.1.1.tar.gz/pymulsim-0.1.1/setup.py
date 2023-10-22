from setuptools import setup

setup(
    name='pymulsim',
    version='0.1.1',    
    description='A package for computing pairwise node similarities between multilayer networks, based on embeddings from Graph Neural Networks.',
    url='https://github.com/pietrocinaglia/pymulsim',
    author='Pietro Cinaglia',
    author_email='cinaglia@unicz.it',
    license='MIT',
    packages=['pymulsim'],
    install_requires=['numpy>=1.23.2',
                      'networkx>=2.8.6',
                      'torch>=2.0.1',
                      'torch_geometric>=2.3.1'            
                      ],
    classifiers=[
        'Development Status :: 1 - Planning',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: MIT License',  
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python :: 3.8',
    ],
)