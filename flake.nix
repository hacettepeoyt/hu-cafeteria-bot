{
  description = "Hacettepe Cafeteria? Yummy :P";

  inputs = {
    nixpkgs.url = "github:nixos/nixpkgs";
  };

  outputs = { self, nixpkgs }:
  let
    forAllSystems = nixpkgs.lib.genAttrs [ "aarch64-linux" "x86_64-linux" ];
  in {
    packages = forAllSystems (system: let
      pkgs = nixpkgs.legacyPackages.${system};
    in {
      default = self.packages.${system}.hu-cafeteria-bot;

      hu-cafeteria-bot = pkgs.stdenv.mkDerivation {
        pname = "hu-cafeteria-bot";
        version = "2.1.1";
        src = ./.;

        buildInputs = with pkgs; [
          python3
          python3Packages.aiohttp
          python3Packages.apscheduler
          python3Packages.pillow
          python3Packages.python-telegram-bot
          python3Packages.pytz
          python3Packages.toml
          python3Packages.tornado
        ];

        installPhase = ''
          mkdir -p $out/{bin,lib/hu-cafeteria-bot}

          cp -r ./* $out/lib/hu-cafeteria-bot
          mv $out/lib/hu-cafeteria-bot/{src,hu-cafeteria-bot}
          cat <<EOF > $out/bin/hu-cafeteria-bot
          #!/bin/sh
          PYTHONPATH="$out/lib/hu-cafeteria-bot:$PYTHONPATH" exec ${pkgs.python3.interpreter} -m hu-cafeteria-bot "\$@"
          EOF
          chmod +x $out/bin/hu-cafeteria-bot
        '';
      };
    });
  };
}
