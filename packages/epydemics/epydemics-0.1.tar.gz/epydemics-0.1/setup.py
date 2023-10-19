from setuptools import setup, find_packages
import yaml

def extract_dependencies_from_yaml(yaml_file_path):
    with open(yaml_file_path, 'r') as file:
        env = yaml.safe_load(file)
        # Extract dependencies, ignoring any version specifications
        dependencies = [pkg.split('=')[0] for pkg in env['dependencies']]
    return dependencies

# Use the function to get the list of dependencies
dependencies = extract_dependencies_from_yaml('./ideal.yaml')

setup(
    name='epydemics',
    version='0.1',  # Start with a small version number, you can increment this as you make changes
    packages=find_packages(),  # Automatically discover and include all packages in the package directory
    install_requires=dependencies,  # Install any additional dependencies that are needed
    author='Juliho David Castillo Colmenares',
    author_email='juliho.colmenares@gmail.com',
    description='A module for modeling and analyzing epidemic data.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',  # If using a markdown README file
    url='https://github.com/julihocc/epydemics',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',  # Choose the appropriate license
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',  # Specify a minimum Python version
)
