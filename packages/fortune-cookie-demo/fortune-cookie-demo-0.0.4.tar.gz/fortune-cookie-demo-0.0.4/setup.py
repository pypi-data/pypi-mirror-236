from setuptools import setup, find_packages

# Use https://packaging.python.org/en/latest/guides/tool-recommendations/ to verify the sea of tools
# that exist to help with packaging. For this example we will use setuptools
# Build a wheel with: python setup.py bdist_wheel and install the pre-required package (wheel)


# Read the requirements.txt file and use it to install dependencies
with open('requirements.txt', encoding='utf-8') as f:  # Corrected "encodings" to "encoding"
    install_requires = f.read().splitlines()


setup(
    name='fortune-cookie-demo',
    description='demo python CLI tool to generate random fortunes',
    packages=find_packages(where='src'),
    author='Simrun & Afraa',
    entry_points="""
    [console_scripts]
    fortune=src.main:main
    """,
    #install_requires=['click==7.1.2'],
    install_requires=install_requires,
    version='0.0.4',
    url= "https://github.com/nogibjj/week7_afraa_simrun_fortune_cookie",
)