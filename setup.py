from setuptools import setup, find_packages

setup(
    name='horiana-rag',
    version='0.1.0',
    description='A Python project for Retrieval-Augmented Generation.',
    packages=find_packages(include=['rag', 'rag.*']),  # Include the `rag` package and subpackages
    install_requires=[
        'PyPDF2',
        'python-docx',
        'scikit-learn',
        'numpy<2',
        'lxml',
        'scipy',
        'pandas',
        'six',
        'biobert-embedding @ git+https://github.com/lukalafaye/biobert_embedding'
        ],
    extras_require={
        'dev': [
            'pytest',
            'flake8',
            'black',
            'twine'
        ]
    },
#    entry_points={
#        'console_scripts': [
#            'preprocess=rag.preprocess:main',  # Entry point updated to call `main` function
#            'embed=rag.embed:main',  # Entry point updated to call `main` function
#            'query=rag.query:main',  # Entry point updated to call `main` function
#        ],
#    },
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.10',
    ],
    python_requires='>=3.10',
)
