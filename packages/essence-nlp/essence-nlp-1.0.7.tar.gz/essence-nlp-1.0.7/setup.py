from setuptools import setup
from setuptools_rust import Binding, RustExtension

setup(
    name="essence-nlp",
    version="1.0.7",
    rust_extensions=[RustExtension("essence_nlp.essence", "src/essence_nlp/essence/Cargo.toml", binding=Binding.PyO3)],
    packages=["essence_nlp"],
    package_dir={"essence_nlp": "src/essence_nlp"},
    zip_safe=False,
)
