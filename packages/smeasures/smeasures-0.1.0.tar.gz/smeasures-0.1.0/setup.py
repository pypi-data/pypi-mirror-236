from setuptools import setup, find_packages

setup(
    name='smeasures',
    version='0.1.0',
    description='Python package to easily capture respource utilization and time taken for given code block or method.',
    packages=find_packages(),
    install_requires=[
        # List your package dependencies here
        'psutil',
        'time',
        'threading',
        'gc'
    ],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ],
    url='https://github.com/csseeker/smeasures',
    author='Shripad Kandharkar',
    author_email='shripad.kandharkar@gmail.com',
)