from setuptools import setup, find_packages

long_description = 'Package made for testing push notification.'

setup(
    name='gpns',
    version='1.1.1',
    author='Ashish Sahu',
    author_email='ashish.sahu@enfec.com',
    url='https://github.com/enfec/gpns',
    description='Package for test firebase message.',
    long_description=long_description,
    long_description_content_type="text/markdown",
    license='MIT',
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'gpns = gpns.main:cli'
        ]
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    keywords='python package gpns',
    install_requires=[
        'firebase-admin==6.2.0',
        'click==8.1.7',
    ],
    include_package_data=True,
    zip_safe=False
)
