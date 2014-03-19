import uliweb
from uliweb.utils.setup import setup
import apps

__doc__ = """A Demo for uliweb-redbreast"""

setup(name='YesNoDemo',
    version=apps.__version__,
    description="A Demo for uliweb-redbreast",
    package_dir = {'YesNoDemo':'apps'},
    packages = ['YesNoDemo'],
    include_package_data=True,
    zip_safe=False,
)

