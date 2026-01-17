from setuptools import setup, find_packages

setup(
    name="2xkoGamePlayAnalyzer",
    version="0.1.0",
    description="A gameplay analyzer for 2XKO fighting game",
    author="Elton Aguiar",
    packages=find_packages(),
    install_requires=[],
    extras_require={
        'dev': [
            'pytest>=7.4.0',
            'pytest-cov>=4.1.0',
        ]
    },
    python_requires='>=3.7',
    entry_points={
        'console_scripts': [
            '2xko-analyzer=analyzer.cli:main',
        ],
    },
)
