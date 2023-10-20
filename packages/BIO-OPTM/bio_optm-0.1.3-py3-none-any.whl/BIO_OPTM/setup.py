from setuptools import setup, find_packages

setup(name='bioInspiredTools',
      version='1.0',
      description='Collection of tools to build Bio inspired optimization tools',
      author='Gerald Jones',
      author_email='gjones2@vols.utk.edu',

      packages=find_packages(include=[
                                      'GA_TOOLS.*', 
                                      'PSO_TOOLS.*', 
                                      
                                      'GA_TOOLS', 
                                      'PSO_TOOLS', 
                                      ]),
      install_requires=[
        'pandas',
        'numpy',
        'matplotlib',
        'jupyter',
        'torch',
        'gurobipy',
    ]
     )