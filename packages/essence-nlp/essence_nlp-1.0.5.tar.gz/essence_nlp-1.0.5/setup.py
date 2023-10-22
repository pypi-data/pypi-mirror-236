from setuptools import setup
from setuptools_rust import Binding, RustExtension

setup(
    name="essence_nlp",
    version="1.0.5",
    rust_extensions=[RustExtension("essence_nlp.essence", "src/essence_nlp/essence/Cargo.toml", binding=Binding.PyO3)],
    packages=["essence"],
    zip_safe=False,
)
