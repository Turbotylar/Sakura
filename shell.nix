{ pkgs ? import <nixpkgs> {} }:
with pkgs.python3Packages;
  pkgs.mkShell {
    nativeBuildInputs = with pkgs; [
      python3
      (python3Packages.discordpy.overrideAttrs (old: rec {
        version = "f51a1ae6b2751b53fe46256a930773b3549cd3f5";
        src = fetchFromGitHub {
          owner = "Pycord-Development";
          repo = "pycord";
          rev = "${version}";
          sha256 = "sha256-TBwOAFmit+rCGgdpgO9NfErowTb2vHP6rHiZuZZPNM8=";
        };
      }))
      python3Packages.sqlalchemy
      python3Packages.pyowm
      python3Packages.alembic
    ];
}