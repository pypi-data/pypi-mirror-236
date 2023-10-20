from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='mattutils',
    version= '1.0.5',
    author='Mattli',
    author_email='matt.li76@icloud.com',
    description='userful tools for data science projects',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='https://github.com/mattli/deeplearning',

    packages=find_packages(),    # include_package_data=True,
    install_requires=[
        'python-box==6.0.2',
        'ensure==1.0.2',
        'pyYAML',
        'joblib',
    ],
    # entry_points={
    #     'console_scripts': [
    #         'command_name=mattli-ds.command_line_interface:main',
    #     ]
    # },
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Operating System :: OS Independent",
    ],
)
