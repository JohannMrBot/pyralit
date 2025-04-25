from setuptools import setup

requirements = [
    'pyramid',
    'pyramid_jinja2',
    'deform>=2.0a2',
    'pyramid_sqlalchemy',
    'pyramid_tm'
]

setup(name='mysite',
      install_requires=requirements,
      entry_points="""\
      [paste.app_factory]
      main = mysite:main
      [console_scripts]
      initialize_db = mysite.scripts.initialize_db:main
      """)