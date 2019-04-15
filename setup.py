import setuptools

import robotframework_rp_tools


with open('README.md', 'r') as fh:
    long_description = fh.read()


with open('install_requires.txt', 'r') as ir:
    install_requires = [item.strip('\n') for item in ir.readlines()]


setuptools.setup(
    name=robotframework_rp_tools.__name__,
    version=robotframework_rp_tools.__version__,
    author=robotframework_rp_tools.__author__,
    author_email=robotframework_rp_tools.__author_email__,
    description='Listener and visitor modules for integration with ReportPortal',
    long_description=long_description,
    url='https://github.com/Shumodan/robotframework_tools',
    long_description_content_type='text/markdown',
    packages=setuptools.find_packages(exclude=['tests']),
    include_package_data=True,
    python_requires='>=3.7',
    install_requires=install_requires,
    classifiers=[
        'Programming Language :: Python :: 3',
        'Topic :: Software Development :: Testing',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Framework :: Robot Framework',
        'Framework :: Robot Framework :: Library',
        'Framework :: Robot Framework :: Tool',
    ],
)
