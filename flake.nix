{
  description = "conda-store";

  inputs = {
    nixpkgs = { url = "github:nixos/nixpkgs/nixpkgs-unstable"; };
  };

  outputs = inputs@{ self, nixpkgs, ... }: {
    devShell.x86_64-linux =
      let
        pkgs = import nixpkgs { system = "x86_64-linux"; };

        pythonPackages = pkgs.python3Packages;

        sse-starlette = pythonPackages.buildPythonPackage rec {
          pname = "sse-starlette";
          version = "1.1.6";

          src = pythonPackages.fetchPypi {
            inherit pname version;
            sha256 = "sha256-hDC7hucNFbVKTIqMP1sapditrR5CMbkRq3ax8uILT+E=";
          };

          propagatedBuildInputs = [
            pythonPackages.starlette
          ];
        };
      in pkgs.mkShell {
        buildInputs = [
          pythonPackages.ipykernel
          pythonPackages.fastapi
          pythonPackages.uvicorn
          pythonPackages.watchfiles
        ];

        shellHook = ''
        '';
      };
  };
}
