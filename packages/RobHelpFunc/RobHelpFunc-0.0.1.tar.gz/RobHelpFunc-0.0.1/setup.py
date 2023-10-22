from setuptools import setup, find_packages

setup(
    name='RobHelpFunc',
    version='0.0.1',
    author='Robert Metzger',
    description='A collection of helper functions',
    license='GNU',
    url='https://github.com/UzumymW839/RobHelpFunc',
    packages=find_packages(),
    install_requires=[
        'pandas >= 2.1.1',
        'numpy >= 1.26.1',
        'matplotlib >= 3.8.0',
        'scikit-learn >= 1.3.1',
        'scipy >= 1.11.3',
    ],
)