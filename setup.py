from setuptools import find_packages, setup

setup(
    name="cli_diary",
    version="0.1.0",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "Click",
    ],
    entry_points={
        "console_scripts": [
            "newdiary = cli_diary.manage:new",
            "deldiary = cli_diary.manage:delete",
            "updtdiary = cli_diary.manage:update",
            "seediary = cli_diary.visualization:see",
        ],
    },
)
