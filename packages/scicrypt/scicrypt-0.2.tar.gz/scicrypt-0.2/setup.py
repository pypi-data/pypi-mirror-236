from setuptools import setup, find_packages

# Long Description 
def read(name):
    with open(name, "r") as fd:
        return fd.read()
    

setup(
        name="scicrypt",
        version="0.2",
        author="Mdslauddin",
        author_email="mdslauddin285@gmail.com",
        description="Scientific Cryptography",
        long_description=read("../README.md"),
        keywords=["Machine Learning", "Math", "Python", "cryptography"],
        
        python_requires='>=3.9',
        install_requires=[
        'riyazi>=0.17'
        ],
        
        
        url="https://github.com/Mdslauddin/scicrypt-main",
        download_url = "http://pypi.python.org/pypi/Wave/",
        license="MIT",
        packages=find_packages(),
     classifiers=(
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ),
       
)
 
    