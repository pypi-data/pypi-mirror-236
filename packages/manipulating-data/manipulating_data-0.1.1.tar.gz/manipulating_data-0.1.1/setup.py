from setuptools import setup, find_packages

setup(
    name="manipulating_data",
    version="0.1.1",
    author="Krzysztof Chrzan",
    author_email="krzysztof.a.chrzan@email.com",
    description="A package for manipulating Python data structures.",
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    license='MIT',
    packages=find_packages( include=["manipulating_data", "manipulating_data.*"] ),
    install_requires=["pandas", "numpy"]
)
