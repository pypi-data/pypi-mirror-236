from setuptools import setup

setup(
    name='alfa-integrations',
    version='0.0.1',
    packages=['feature_toggle_ui', 'widget_management_ui'],
    url='https://github.com/Dofamin/alfa-integrations',
    license='unlicense',
    author='Filippov Roman',
    author_email='',
    description='Python Wraper for Internals tools',
    install_requires=("pytz", "requests", "urllib3"),
)
