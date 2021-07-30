from setuptools import setup

setup(
    name='lf_data_explorer',
    packages=['lf_data_explorer'],
    include_package_data=True,
    install_requires=[
        'Flask',
        'PyYAML',
        'flask-sqlalchemy'
    ]


)