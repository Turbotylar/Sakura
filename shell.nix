{ pkgs ? import <nixpkgs> {} }:
with pkgs.python39Packages;
  pkgs.mkShell {
    nativeBuildInputs = with pkgs; [
      python39
      (python39Packages.discordpy.overrideAttrs (old: rec {
        version = "groups";#"f51a1ae6b2751b53fe46256a930773b3549cd3f5";
        src = fetchFromGitHub {
          owner = "Pycord-Development";
          repo = "pycord";
          rev = "${version}";
          sha256 = "sha256-L2SCd8TXqM4dJjF3kb20qRXbGhBkcUAgoFKrRh3sP2o=";
        };

        patches = [];
      }))
      (buildPythonPackage rec {
        pname = "SQLAlchemy";
        version = "1.4.27";
        src = fetchPypi {
          inherit pname version;
          sha256 = "sha256-12g1na6zqGZE84VMZlnkSWo+a7orRlHsyHznrUFbMgw=";
        };
        checkInputs = [
          pytestCheckHook
          pytest_xdist
          mock
        ] ++ lib.optional (!isPy3k) pysqlite;

        pytestFlagsArray = [ "-n auto" ];

        postInstall = ''
          sed -e 's:--max-worker-restart=5::g' -i setup.cfg
        '';

        propagatedBuildInputs = [
          (
            buildPythonPackage rec {
              pname = "greenlet";
              version = "1.0.0";
              disabled = isPyPy;  # builtin for pypy

              src = fetchPypi {
                inherit pname version;
                sha256 = "1y6wbg9yhm9dw6m768n4yslp56h85pnxkk3drz6icn15g6f1d7ki";
              };

              propagatedBuildInputs = [ six ];
            }
          )
        ];


        dontUseSetuptoolsCheck = true;
      })
      python39Packages.pyowm
      python39Packages.alembic
      python39Packages.psycopg2
    ];
}