{ pkgs ? import <nixpkgs> {} }:
with pkgs.python3Packages;
  pkgs.mkShell {
    nativeBuildInputs = with pkgs; [
      python3
      python3Packages.discordpy
      python3Packages.sqlalchemy
      python3Packages.pyowm
      python3Packages.alembic
    ];
}