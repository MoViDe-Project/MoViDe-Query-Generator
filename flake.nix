{
  description = "Dev shell for the Promi Exercises 2024-25";

  inputs = { nixpkgs.url = "github:nixos/nixpkgs?ref=nixos-unstable"; };

  outputs = { self, nixpkgs }:
    let
      pkgs = nixpkgs.legacyPackages."x86_64-linux";
      pythonPackages = pkgs.python3Packages;

    in {
      devShells."x86_64-linux".default = import ./shell.nix {inherit pkgs;};

      };
    

}

