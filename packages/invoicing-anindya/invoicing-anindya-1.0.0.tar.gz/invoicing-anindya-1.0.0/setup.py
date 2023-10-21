from setuptools import setup

setup(
    name="invoicing-anindya",
    packages=["invoicing"],
    version="1.0.0",
    license="MIT",
    description="This package can convert a particular format of excel invoices to pdfs. This is an example package from Ardit Sulce's course",
    author="Anindya Dey",
    author_email="email@example.com",
    url="https://example.com",
    keywords=["invoice", "excel", "pdf"],
    install_requires=["fpdf", "openpyxl", "pandas"],
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Build Tools",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
)
