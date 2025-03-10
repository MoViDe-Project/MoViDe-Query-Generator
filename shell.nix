{ pkgs ? import <nixpkgs> {} }:

with pkgs;
  pkgs.mkShell {
    buildInputs = [
    # Defines a python + set of packages.
    (python3.withPackages (ps: with ps; with python3Packages; [
      requests
    ]))
  ];

  # Automatically run jupyter when entering the shell.
  shellHook = "zsh";
  }
