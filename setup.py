from setuptools import setup, find_packages


setup(
    name="uc_solver",
    version="0.9.0",
    packages=find_packages(),
    install_requires=[
        "knapsack-pip",
        "pydantic",
        "click",
        "pyyaml",
        "tabulate",
        "mealpy",
    ],
    extras_require={
        "dev": [
            "black",
        ],
    },
    entry_points={"console_scripts": ["uc_solver = uc_solver.cli:solve"]},
)
