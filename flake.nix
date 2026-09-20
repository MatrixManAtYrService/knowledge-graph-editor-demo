{
  description = "London Underground demo graph for knowledge-graph-editor — the dev shell just provides uv";

  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixos-unstable";
    flake-utils.url = "github:numtide/flake-utils";
  };

  outputs = { self, nixpkgs, flake-utils }:
    flake-utils.lib.eachDefaultSystem (system:
      let
        pkgs = import nixpkgs { inherit system; };
      in
      {
        devShells.default = pkgs.mkShell {
          packages = [ pkgs.uv ];

          shellHook = ''
            echo "kge demo — run:  uv run kge serve   then open http://localhost:8151"
          '';
        };
      });
}
