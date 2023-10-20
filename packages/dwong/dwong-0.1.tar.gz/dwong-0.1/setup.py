from setuptools import setup, find_packages

setup(
    name='dwong',
    version='0.1',
    packages=find_packages(),
    install_requires=[
        'numpy>=1.18.0',              
        'keras == 2.13.1',              
        'uproot >= 5.0.7',           
        'sklearn >= 1.2.2',             
       
    ],
    author='Dowling Wong',
    author_email='dowlingwong@brandeis.edu',
    description='Dowling\'s integrated data analysis for DQ experiemnt setup. Include data analysis functions, csv saving tools, Particle ID model, DNN model frame for ID training and EMCal ploting tools',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/Dowling7/dwong',
    license='MIT',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ],
    python_requires='>=3.6',
)
