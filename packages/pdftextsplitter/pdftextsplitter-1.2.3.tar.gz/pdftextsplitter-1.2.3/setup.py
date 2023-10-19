from distutils.core import setup
setup(
  name = 'pdftextsplitter',                                                            # Name of the package
  packages = ['pdftextsplitter', 'pdftextsplitter.TextPart', 'pdftextsplitter.Tests', 'pdftextsplitter.Tests.Tools'], # Each folder to copy must be in here; first = same as package name.
  version = '1.2.3',                                                                # Speaks for itself, keep in sync with the textsplitter-class!
  license='MIT',                                                                    # Most commonly used licenses: https://help.github.com/articles/licensing-a-repository
  description = 'This packages can read PDF documents and automatically recognise chapter-titles, enumerations and other elements in the text and summarize the document part-by-part',
  author = 'Unit Data en Innovatie, Ministerie van Infrastructuur en Waterstaat, Netherlands',
  author_email = 'dataloket@minienw.nl',                                            # Contact email address
  url = 'https://gitlab.com/datainnovatielab/public/pdftextsplitter/dist/',       # Link to the repository.
  download_url = 'https://gitlab.com/datainnovatielab/public/pdftextsplitter/dist/',
  keywords = ['NLP', 'PDF', 'Text recognition', 'Structure recognition', 'ChatGPT'],
  install_requires=[                                                                # the list of dependencies: other packages that your package needs to function.
          'setuptools>=59.6.0',
          'wheel>=0.41.1',
          'build>=0.10.0',
          'numpy>=1.25.2',
          'pandas>=2.0.3',
          'matplotlib>=3.7.2',
          'pillow>=10.0.0',
          'PyPDF2>=3.0.1',
          'openai>=0.27.8',
          'tiktoken>=0.4.0',
          'pymupdf>=1.22.2,<=1.22.5',
          'pdfminer.six>=20221105',
          'thefuzz>=0.19.0',
          'pytest>=7.3.0,<=7.4.0',
          'coverage>=7.3.0',
          'pylint>=2.17.5',
      ],
  classifiers=[
    'Development Status :: 3 - Alpha',                                              # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package
    'Intended Audience :: Developers',                                              # The intended audience for the package
    'Topic :: Software Development :: Build Tools',                                 # Better to keep this as it is.
    'License :: OSI Approved :: MIT License',                                       # Should be the same as the previous license choice.
    'Programming Language :: Python :: 3.10',                                       # Specification of which python versions are supported.
  ],
)
