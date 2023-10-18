"""Monkey Anagram Setup Script

Author: Steve Daulton
"""

from setuptools import setup  # type: ignore

setup(
    name='monkey_anagram',
    version='0.1',
    description='A CLI anagram solver.',
    url='https://github.com/SteveDaulton/Monkey_Anagram',
    author='Steve Daultom',
    license='MIT',
    packages=['monkey_anagram'],
    install_requires=['setuptools',
                      'appdirs'
                      ],
    package_data={
        'monkey_anagram': ['words.txt']},
    entry_points={
        'console_scripts': [
            'monkeygram = monkey_anagram.monkey_anagram_solver:main',
        ],
    },
    zip_safe=False)
