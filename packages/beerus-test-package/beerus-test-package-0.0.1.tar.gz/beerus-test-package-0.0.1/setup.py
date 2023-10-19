
import setuptools 
  
with open("README.md", "r") as fh: 
    description = fh.read() 
  
setuptools.setup( 
    name="beerus-test-package", 
    version="0.0.1", 
    author="Beerus", 
    author_email="contact@gfg.com", 
    packages=["utils"], 
    description="A sample test package", 
    long_description=description, 
    long_description_content_type="text/markdown", 
    url="", 
    license='MIT', 
    python_requires='>=3.8', 
    install_requires=[] 
) 