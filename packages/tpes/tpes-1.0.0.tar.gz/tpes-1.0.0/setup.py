from distutils.core import setup
setup(
  name = 'tpes',
  packages = ["tpes", "tpes.todo", "tpes.data", "tpes.views", "tpes.tui", "tpes.ui"],
  version = '1.0.0',
  description = 'TPES is system which can plan and estimate tasks given workflow diagrams',
  author = 'Stefan Nožinić',
  author_email = 'stefan@lugons.org',
  url = 'https://github.com/fantastic001/tpes',
  download_url = 'https://github.com/fantastic001/tpes/tarball/1.0.0',
  keywords = ["workflow"], 
  package_dir = {'tpes': 'tpes/'},
  classifiers = [],
  entry_points = {
    "console_scripts": [
      "tpes = tpes.__main__:main",
      "tpestui = tpes.tui.__main__:main"
    ]
  },
  install_requires=[
    "lxml",
    "dacite",
    "TatSu",
    "jinja2",
    "easy_widgets",
    "urwid"
  ] # dependencies listed here 
)
