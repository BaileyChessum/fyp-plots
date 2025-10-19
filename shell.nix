{
  pkgs ? import <nixpkgs> {} 
}:

let 
  my-python = pkgs.python3.withPackages (pp: [
    pp.matplotlib
    pp.numpy
    pp.pandas
    (pp.callPackage ./default.nix { })
  ]);
in
  pkgs.mkShell {
    packages = [
      my-python
      pkgs.tetex
    ];
  }
