from setuptools import setup

setup(
    name='pydead',
    version='1.1.1',
    author='Sergey Petrov',
    author_email='srgypetrov@ya.ru',
    url='https://github.com/SrgyPetrov/pydead',
    description='Utility for searching of unused code in python projects',
    packages=['src'],
    scripts=['pydead'],
    classifiers=[
        'Environment :: Console',
        'Intended Audience :: Developers',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Topic :: Software Development',
        'Topic :: Utilities',
    ]
)
