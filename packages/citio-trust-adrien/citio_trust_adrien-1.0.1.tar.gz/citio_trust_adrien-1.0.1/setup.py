from setuptools import setup
from setuptools.command.install import install
from citio_trust_adrien.display import display_and_save_infos


class PostInstallCommand(install):
    """Post-installation for installation mode."""

    def run(self):
        install.run(self)
        display_and_save_infos()


setup(
    name="citio_trust_adrien",
    packages=["citio_trust_adrien"],
    version="1.0.1",
    license="MIT",
    description="Package created for a presentation about malwares.",
    author="ADRIEN ROBILIARD",
    author_email="adrien@cit.io",
    url="https://github.com/adrienrobiliard/citio_trust_Adrien",
    download_url="https://github.com/adrienrobiliard/citio_trust_Adrien/archive/refs/tags/v1.0.1.tar.gz",
    keywords=["CITIO", "DEMO", "MALWARE"],
    classifiers=[
        "Development Status :: 3 - Alpha",  # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package
        "Intended Audience :: Developers",  # Define that your audience are developers
        "Topic :: Software Development :: Build Tools",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",  # Specify which pyhton versions that you want to support
    ],
    cmdclass={
        "install": PostInstallCommand,
    },
)
