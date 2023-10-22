from setuptools import setup, find_packages

# read the requirements.txt file and use it to install dependencies
with open("requirements.txt") as f:
    install_requires = f.read().splitlines()


setup(
    name="assignment-app",
    description="demo python CLI tool to manage assignments",
    packages=find_packages(),
    author="Ofosu Osei",
    entry_points="""
    [console_scripts]
    assignment=assignment_app.assignment:app
    """,
    install_requires=install_requires,
    version="0.0.1",
    url="https://github.com/Ofosu-Osei",
)
