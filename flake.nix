{
  description = "Python bindings for libghostty-vt";

  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixpkgs-unstable";
    flake-utils.url = "github:numtide/flake-utils";
    ghostty = {
      url = "github:ghostty-org/ghostty";
      inputs.nixpkgs.follows = "nixpkgs";
    };
  };

  outputs = { self, nixpkgs, flake-utils, ghostty }:
    flake-utils.lib.eachDefaultSystem (system:
      let
        pkgs = nixpkgs.legacyPackages.${system};
        python = pkgs.python313;

        libghostty-vt = ghostty.packages.${system}.libghostty-vt;
      in
      {
        packages = {
          inherit libghostty-vt;

          libghostty-vt-debug = ghostty.packages.${system}.libghostty-vt-debug;
          libghostty-vt-releasesafe = ghostty.packages.${system}.libghostty-vt-releasesafe;
        };

        devShells.default = pkgs.mkShell {
          packages = [
            python
            pkgs.uv
            pkgs.ruff
            libghostty-vt
          ];

          env = {
            LIBGHOSTTY_VT_PATH = "${libghostty-vt}/lib/libghostty-vt.so.0";
            LD_LIBRARY_PATH = pkgs.lib.makeLibraryPath (with pkgs; [
              glib
              libGL
              fontconfig
              freetype
              libX11
              libXext
              libXrender
              libxcb
              libxcb-wm
              libxcb-image
              libxcb-keysyms
              libxcb-render-util
              dbus
              libxkbcommon
              wayland
            ]);
          };

          shellHook = ''
            echo "libghostty-py dev shell"
            echo "libghostty-vt: ${libghostty-vt}/lib/libghostty-vt.so.0"
          '';
        };
      }
    );
}
