from setuptools import setup, find_packages

setup(
    name='crypto_game_node',
    version='1.0.0',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'flask',
        'ecdsa',
        'base58',
        'web3',
    ],
    entry_points={
        'console_scripts': [
            'crypto_game_node=main:main',
        ],
    },
)