from setuptools import find_packages, setup

setup(
    name='assert-files',
    packages=find_packages(include=['assert_files']),
    version='0.1.2',
    description='My first Python library',
    long_description='my first Python library',
    long_description_content_type='text/x-rst',
    url='https://github.com/avillanova/assert-files',
    author='avillanova',
    install_requires=['pypdf~=3.16.4'],
    setup_requires=['pytest-runner'],
    tests_require=['pytest'],
    test_suite='tests',
    license='MIT',
    keywords='assert files test automation compare',
    python_requires='>=3',
    classifiers=[
    # How mature is this project? Common values are
    #   3 - Alpha
    #   4 - Beta
    #   5 - Production/Stable
    'Development Status :: 1 - Planning',

    # Indicate who your project is intended for
    'Intended Audience :: Developers',
    'Topic :: Software Development :: Quality Assurance',

    # Pick your license as you wish (should match "license" above)
    'License :: OSI Approved :: MIT License',

    # Specify the Python versions you support here. In particular, ensure
    # that you indicate whether you support Python 2, Python 3 or both.
    'Programming Language :: Python :: 3.9',
    'Programming Language :: Python :: 3.10',
],
)