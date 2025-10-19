{
  buildPythonApplication ? (import <nixpkgs> { }).python3Packages.buildPythonApplication
, setuptools ? (import <nixpkgs> { }).python3Packages.setuptools
, matplotlib ? (import <nixpkgs> { }).python3Packages.matplotlib
, numpy ? (import <nixpkgs> { }).python3Packages.numpy
, pandas ? (import <nixpkgs> { }).python3Packages.pandas
, texliveFull ? (import <nixpkgs> { }).texliveFull
, ...
}:

buildPythonApplication {
  pname = "plots-python-env";
  version = "1.0";

  src = ./.;

  pyproject = true;
  build-system = [ setuptools ];

  propagatedBuildInputs = [
    texliveFull
    matplotlib
    numpy
    pandas
  ];
}