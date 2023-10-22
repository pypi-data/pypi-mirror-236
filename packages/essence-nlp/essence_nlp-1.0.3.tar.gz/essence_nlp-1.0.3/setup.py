from setuptools import setup
from setuptools_rust import Binding, RustExtension

setup(
    name="essence",
    version="0.1",
    rust_extensions=[RustExtension("essence.essence", "essence/Cargo.toml", binding=Binding.PyO3)],
    packages=["essence"],
    zip_safe=False,
)
