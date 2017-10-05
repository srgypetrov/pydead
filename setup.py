from setuptools import setup

setup(
    name='pydead',
    version='1.2.1',
    author='Sergey Petrov',
    author_email='srgypetrov@ya.ru',
    url='https://github.com/SrgyPetrov/pydead',
    description=('Utility for searching of unused code in python projects, '
                 'such as module’s global classes, functions and names.'),
    packages=['src'],
    install_requires=['Click'],
    entry_points={
        'console_scripts': ['pydead=src.base:check']
    },
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
