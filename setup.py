from setuptools import setup, find_packages

reqs = [
    'requests',
]

setup(
    name='napchart',
    author='Arslan S. Khalilov',
    version='0.0.1',
    license='MIT',
    description='A simple API wrapper for the NAPChart',
    url='https://github.com/Arslan223/NapchartWrapper',
    download_url='https://github.com/Arslan223/NapchartWrapper/archive/refs/tags/v0.0.1-alpha.tar.gz',
    packages=find_packages(),
    long_description=open('README.md').read(),
    install_requires=reqs,
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.8',
    ]
)
