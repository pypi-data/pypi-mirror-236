from setuptools import setup, find_packages

setup(
    name='min-db',
    version='0.0.3',
    description='mybatis like minimum db utility',
    author='kyon',
    author_email='originky2@gmail.com',
    install_requires=['pydantic', 'oracledb', 'mysql-connector-python',],
    packages=find_packages(exclude=[]),
    python_requires='>=3.10',
    package_data={},
    zip_safe=False,
    classifiers=[
        'Programming Language :: Python :: 3.11',
    ],
)
