from setuptools import setup, find_packages

with open('requirements.txt') as f:
    required = f.read().splitlines()
    
setup(
    name="ai_service_test_23_10_20",
    version='0.0.4',
    author='wj',
    description='PYPI tutorial',
    author_email='hello_world2@helloworld.com',
    url='https://hello2_world.git/hello_world2',
    install_requires=required,
    package_dir = {'':'.'},
    packages=find_packages(include=['lib', 'lib.*', 'src', 'src*', 'utils', 'utils*']),
    python_requires= '>=3.8',
    zip_safe=False,
    package_data={},
    classifiers=[
        "Programming Language :: Python :: 3.8",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: POSIX :: Linux"
    ]
)