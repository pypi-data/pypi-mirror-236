from setuptools import setup, find_packages

setup(
    name="shmaxg_gen",
    version="1.0.0",
    author="Maksim Shirobokov",
    author_email="shmaxg@gmail.com",
    description='A version of genetic algorithm.',
    long_description='A version of genetic algorithm.',
    keywords=['genetic algorithm', 'optimization'],
    packages=find_packages(),
    package_data={'shmaxg_gen': ['/Users/maksimsirobokov/Yandex.Disk.localized/Python/shmaxg_gen/*']},
    include_package_data=True,
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Science/Research",
        "Intended Audience :: Education",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
        "Operating System :: Microsoft :: Windows :: Windows 10",
        "Operating System :: MacOS",
        "Operating System :: POSIX :: Linux",
        "Programming Language :: Python :: 3",
        "Topic :: Scientific/Engineering",
    ]
)
