import setuptools

exec(open("cligames/version.py").read())

setuptools.setup(
    name="cligames",
    author="Thomas Brier",
    version=__version__,  #  type: ignore
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(),
    entry_points={"console_scripts": "cligames = cligames.main:run"},
)
