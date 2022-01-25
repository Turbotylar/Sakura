{ pkgs ? import <nixpkgs> {} }:
with pkgs.python39Packages;
  pkgs.mkShell {
    nativeBuildInputs = with pkgs; [
      python39
      python39Packages.sqlalchemy
      (python39Packages.discordpy.overrideAttrs (old: rec {
        version = "7c571b7fb693ea26f29f793049a161bc538ce7a5";
        src = fetchFromGitHub {
          owner = "Pycord-Development";
          repo = "pycord";
          rev = "${version}";
          sha256 = "sha256-+MI4pVUWQLNgvjo2XX9M5rMgZ8xaVK/ygGlF3asUOGo=";
        };

        patches = [];
      }))
      python39Packages.pyowm
      python39Packages.alembic
      python39Packages.psycopg2
      python39Packages.spotipy
    ];
}