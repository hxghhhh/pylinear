  
from setuptools import setup

setup(
    name="pylinear",
    version="0.1",
    py_modules=["linear"],
    include_package_data=True,
    install_requires=["click"],
    entry_points="""
        [console_scripts]
        linear=linear:cli
    """,
)
