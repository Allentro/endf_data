from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

long_description = ''
  
setup(
        name ='endf_decay',
        version ='1.0.0',
        author ='Ross Allen',
        author_email ='rossallen1996@gmail.com',
        #url ='https://github.com/Vibhu-Agarwal/vibhu4gfg',
        description ='Command line tool for ENDF data',
        long_description = long_description,
        #long_description_content_type ="text/markdown",
        license ='MIT', 
        install_requires = ['argparse'],
        #packages = find_packages(),
        entry_points ={
            'console_scripts': [
                'endf_data = endf_decay.endf_decay:main'
            ]
        },
        classifiers =(
            "Programming Language :: Python :: 3",
            "License :: OSI Approved :: MIT License",
            "Operating System :: OS Independent",
        ),
        #eywords ='geeksforgeeks gfg article python package vibhu4agarwal',
        python_requires='>=3.6', 
        zip_safe = False
)