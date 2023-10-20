from setuptools import setup, find_packages

setup(
    name='driwecore',
    version='0.1.1',
    author='Jason Tai',
    description='This Pacakge is commont function that will be use by Drister or similiar team within the internal team',
    url = 'https://github.com/drister-my/driwecore',  
    download_url = 'https://github.com/drister-my/driwecore/archive/refs/tags/v_01.tar.gz',
    packages=find_packages(),
    install_requires=[
        # List your package dependencies here
        'pyjwt', 'google-cloud-secret-manager'
    ],
    classifiers=[
    'Development Status :: 3 - Alpha',      # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package
    'Intended Audience :: Developers',      # Define that your audience are developers
    'Topic :: Software Development :: Build Tools',
    'Programming Language :: Python :: 3',      #Specify which pyhton versions that you want to support
    'Programming Language :: Python :: 3.4',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
  ],
)
