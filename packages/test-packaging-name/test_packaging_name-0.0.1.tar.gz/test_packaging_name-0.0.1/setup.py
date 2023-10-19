from setuptools import setup, find_packages

setup(
    name='test_packaging_name',
    version='0.0.1',
    description="test_packaing_discription",
    author='tester',
    author_email='wjk5848@gmail.com',
    url = 'https://github.com/woorej/packing_test.git',
    install_requires = ['pandas'],
    packages=find_packages(exclude=[]),
    keywords = ['packaging_test', 'wjj'],
    python_requires ='>=3.8',
    package_data={},
    zip_safe=False,
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License'
    ]
)