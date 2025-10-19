{
  buildPythonApplication ? (import <nixpkgs> { }).python3Packages.buildPythonApplication
, setuptools ? (import <nixpkgs> { }).python3Packages.setuptools
, matplotlib ? (import <nixpkgs> { }).python3Packages.matplotlib
, numpy ? (import <nixpkgs> { }).python3Packages.numpy
, pandas ? (import <nixpkgs> { }).python3Packages.pandas
, tetex ? (import <nixpkgs> { }).tetex
, ...
}:

buildPythonApplication {
  pname = "plots-python-env";
  version = "1.0";

  src = ./.;

  pyproject = true;
  build-system = [ setuptools ];

  propagatedBuildInputs = [
    tetex
    matplotlib
    numpy
    pandas
  ];
}