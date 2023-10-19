from setuptools import setup

setup(
    name='pera-transcript',
    version='0.1.2',    
    description='A tool to generate the unofficial transcript automatically for undergraduate students at University of Peradeniya.',
    url='https://github.com/sathiiii/pera-transcript',
    author='Sathira Silva',
    author_email='sathirasofte@gmail.com',
    license='MIT License',
    packages=['pera_transcript'],
    install_requires=['pyyaml',   
                      'bs4',
                      'requests'               
                      ],
    entry_points={
        'console_scripts': ['autogen_transcript=pera_transcript.autogen_transcript:main']
    },

    classifiers=[
        'Development Status :: 1 - Planning',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: MIT License',  
        'Operating System :: POSIX :: Linux',        
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
    ],
)