from setuptools import setup

setup(
    name='pydead',
    version='1.0',
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
        'Topic :: Software Development',
        'Topic :: Utilities',
    ]
)
