{
  description = "Python bindings for libghostty-vt";

  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixpkgs-unstable";
    flake-utils.url = "github:numtide/flake-utils";
    zig = {
      url = "github:mitchellh/zig-overlay";
      inputs.nixpkgs.follows = "nixpkgs";
    };
    ghostty = {
      url = "github:ghostty-org/ghostty";
      inputs.nixpkgs.follows = "nixpkgs";
      inputs.zig.follows = "zig";
    };
  };

  outputs = { self, nixpkgs, flake-utils, zig, ghostty }:
    flake-utils.lib.eachDefaultSystem (system:
      let
        pkgs = import nixpkgs {
          inherit system;
          overlays = [
            (_final: prev: {
              zig_0_15 =
                if prev.stdenv.hostPlatform.isDarwin
                then
                  zig.packages.${system}.brew."0.15.2".overrideAttrs (old: {
                    setupHook = prev.zig_0_15.setupHook;
                    passthru = (old.passthru or {}) // {
                      hook = prev.zig_0_15.hook;
                    };
                  })
                else zig.packages.${system}."0.15.2";
            })
          ];
        };
        python = pkgs.python313;

        zig_0_15 = pkgs.zig_0_15;
        overrideLibghosttyVt = package: (package.override {
          inherit zig_0_15;
        }).overrideAttrs (old: {
          nativeBuildInputs = old.nativeBuildInputs ++ pkgs.lib.optionals pkgs.stdenv.hostPlatform.isDarwin [
            pkgs.zig_0_15.hook
          ];
        });
        libghostty-vt = overrideLibghosttyVt ghostty.packages.${system}.libghostty-vt;
      in
      {
        packages = {
          inherit libghostty-vt;

          libghostty-vt-debug = overrideLibghosttyVt ghostty.packages.${system}.libghostty-vt-debug;
          libghostty-vt-releasesafe = overrideLibghosttyVt ghostty.packages.${system}.libghostty-vt-releasesafe;
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
              dbus
              glib
              libGL
              libXrender
              libxcb
              libxcb-image
              libxcb-keysyms
              libxcb-render-util
              libxcb-wm
              zlib
            ] ++ lib.optionals stdenv.hostPlatform.isLinux [
              fontconfig
              freetype
              libX11
              libXext
              libxkbcommon
              wayland
            ]
          );
          };

          shellHook = ''
            echo "libghostty-py dev shell"
            echo "libghostty-vt: ${libghostty-vt}/lib/libghostty-vt.so.0"
          '';
        };
      }
    );
}
