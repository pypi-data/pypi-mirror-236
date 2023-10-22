from setuptools import setup

setup(
    name="mypackage-theacodes",  # Replace "mypackage-theacodes" with your desired package name
    version="0.1",
    description="Progetto di Produzione del Software",
    author="Simone",
    author_email="s.madaghiele@campus.unimib.it",
    url="https://gitlab.com/MarcecaManu/test_runner",
    packages=["mypackage"],
    install_requires=[
        # List your project's dependencies here (use a list of strings, not a filename)
        "requirements.txt",

        # Add more dependencies as needed
    ],
)
