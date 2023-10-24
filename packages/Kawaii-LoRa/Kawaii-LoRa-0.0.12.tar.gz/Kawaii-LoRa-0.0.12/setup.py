import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="Kawaii-LoRa",
    version="0.0.12",
    packages=setuptools.find_packages(),
    url="https://github.com/LuisTheProgrammer/Kawaii-LoRa",
    author="Luis Di Matteo",
    author_email="luiss.dimatteo@gmail.com",
    description="LoRa communication library for Raspberry Pi",
    long_description=long_description,
    long_description_content_type="text/markdown",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries",
        "Topic :: System :: Hardware",
        "Operating System :: POSIX :: Linux",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.5",
    ],
    # install_requires=["RPi.GPIO", "spidev"],
)
