from distutils.core import setup
setup(
  name = 'edempy',         # How you named your package folder (MyLib)
  packages = ['edempy'],   # Chose the same as "name"
  version = '0.1',      # Start with a small number and increase it with every change you make
  license='Apache-2.0',        # Chose a license from here: https://help.github.com/articles/licensing-a-repository
  description = '',   # Give a short description about your library
  author = 'edem-dev',                   # Type in your name
  author_email = 'edem-dev@altair.com',      # Type in your E-Mail
  url = '',   # Provide either the link to your github or to your website
  download_url = '',    # I explain this later on
  keywords = ['DEM'],   # Keywords that define your package best
  install_requires=[],
  classifiers=[
    'Development Status :: 1 - Planning',      # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package
    'Intended Audience :: Developers',      # Define that your audience are developers
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: Apache Software License',   # Again, pick a license
    'Programming Language :: Python :: 3.8',      #Specify which pyhton versions that you want to support
  ],
)