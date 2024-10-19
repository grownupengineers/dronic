from setuptools import setup, find_packages

setup(
    name="dronic",
    version="0.0.1",
    packages=find_packages(include=["dronic"]),
    install_requires=["RestrictedPython", "cryptography"],
    entry_points={
        # utility primarily to run in development mode
        "console_scripts": ["dronic-cli = dronic.main:cli"],
        # internal/core dronic plugins still need to be exported this way, so
        # that the loader picks them up
        "dronic.plugin": ["sh-step = dronic.core.sh:Sh"],
    },
)
