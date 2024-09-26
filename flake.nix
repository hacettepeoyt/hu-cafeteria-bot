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
        version = "2.3";
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

    nixosModules = { lib, config, pkgs, ... }: let
      cfg = config.services.hu-cafeteria-bot;
      configFormat = pkgs.formats.toml { };
      configFile = configFormat.generate "hu-cafeteria-bot.toml" cfg.settings;
    in {
      options.services.hu-cafeteria-bot = {
        enable = lib.mkEnableOption "hu-cafeteria-bot";

        environmentFile = lib.mkOption {
          type = lib.types.nullOr lib.types.path;
          example = "/run/agenix/x-config.env";
          default = null;
          description = ''Environment file for providing secrets to the unit.'';
        };

        hostname = lib.mkOption {
          type = lib.types.nullOr lib.types.str;
          example = "hucafeteriabot.example.org";
          default = null;
          description = "Domain of the host for the webhook. Will enable the webhook and an NGINX virtual host for it.";
        };

        settings = lib.mkOption {
          type = lib.types.submodule {
            freeformType = configFormat.type;
            options = {
                TELEGRAM_API_KEY = lib.mkOption {
                  type = lib.types.str;
                  description = "The telegram token fetched from BotFather.";
                };
                IMAGE_CHANNEL_ID = lib.mkOption {
                  type = lib.types.int;
                  description = "The ID of the room to send the menu images to.";
                };
                TEXT_CHANNEL_ID = lib.mkOption {
                  type = lib.types.int;
                  description = "The ID of the room to send the menu text to.";
                };
                LOGGER_CHAT_ID = lib.mkOption {
                  type = lib.types.int;
                  description = "The ID of the room to send errors/admin messages to.";
                };
                SHARE_TIME_HOUR = lib.mkOption {
                  type = lib.types.ints.between 0 23;
                  default = 9;
                  description = "The hour of the time for sharing the menu. Defaults to 9.";
                };
                SHARE_TIME_MINUTE = lib.mkOption {
                  type = lib.types.ints.between 0 59;
                  default = 15;
                  description = "The minute of the time for sharing the menu. Defaults to 15.";
                };
                UPDATE_DB_TIME_HOUR = lib.mkOption {
                  type = lib.types.ints.between 0 23;
                  default = 15;
                  description = "The hour of the time for updating the database. Defaults to 15.";
                };
                UPDATE_DB_TIME_MINUTE = lib.mkOption {
                  type = lib.types.ints.between 0 59;
                  default = 0;
                  description = "The minute of the time for updating the database. Defaults to 0.";
                };
                WEBHOOK_CONNECTED = lib.mkOption {
                  type = lib.types.bool;
                  default = cfg.hostname != null;
                  description = "Whether to use webhook instead of polling for messages. Defaults to true if `services.hu-cafeteria-bot.hostname` is non-null.";
                };
                PORT = lib.mkOption {
                  type = lib.types.port;
                  default = 51413;
                  description = "Port to listen the webhook on. Defaults to 51413.";
                };
                WEBHOOK_URL = lib.mkOption {
                  type = lib.types.str;
                  default = "https://${cfg.hostname}";
                  description = "The URL for the webhook. Defaults to hostname + api key.";
                };
                BACKGROUND_COLORS = lib.mkOption {
                  type = lib.types.listOf lib.types.str;
                  default = [ "#C9D6DF" "#F8F3D4" "#FFE2E2" "#E7D4B5" "#AEDEFC" "#EAFFD0" "#FFD3B4" "#BAC7A7" "#95E1D3" "#FCE38A" "#FFB4B4" ];
                  description = "The list of background colors to be used for menu images. Defaults to the upstream-provided colors.";
                };
                SMTP_HOST = lib.mkOption {
                  type = lib.types.str;
                  description = "Target server address for the SMTP";
                };
                SMTP_PORT = lib.mkOption {
                  type = lib.types.port;
                  default = 587;
                  description = "Target server port for the SMPT. Defaults to 587.";
                };
                SMTP_USERNAME = lib.mkOption {
                  type = lib.types.str;
                  description = "Username for SMTP connection.";
                };
                SMTP_PASSWORD = lib.mkOption {
                  type = lib.types.str;
                  description = "Password for SMPT connection.";
                };
                MAILING_LIST_ADDRESS = lib.mkOption {
                  type = lib.types.str;
                  description = "Mailing list address for delivering menu to.";
                };
            };
          };
          default = { };
        };
      };

      config = lib.mkIf cfg.enable {
        services.nginx = lib.mkIf (cfg.hostname != null) {
          enable = lib.mkDefault true;

          recommendedGzipSettings = lib.mkDefault true;
          recommendedProxySettings = lib.mkDefault true;

          virtualHosts.${cfg.hostname} = {
            forceSSL = lib.mkDefault true;
            enableACME = lib.mkDefault true;

            locations."/".proxyPass = "http://localhost:${toString cfg.settings.PORT}";
          };
        };

        systemd.services.hu-cafeteria-bot = {
          enable = true;
          wantedBy = [ "multi-user.target" ];
          after = [ "network-online.target" ];
          startLimitBurst = 3;
          startLimitIntervalSec = 60;

          serviceConfig = {
            ExecStart = "${self.packages.${pkgs.system}.hu-cafeteria-bot}/bin/hu-cafeteria-bot -c /run/hu-cafeteria-bot/hu-cafeteria-bot.toml -d /var/lib/hu-cafeteria-bot/database.json";
            ExecStartPre = ''
                ${pkgs.envsubst}/bin/envsubst -i ${configFile} -o /run/hu-cafeteria-bot/hu-cafeteria-bot.toml
            '';
            EnvironmentFile = lib.mkIf (cfg.environmentFile != null) cfg.environmentFile;

            Type = "simple";
            Restart = "always";
            DynamicUser = true;
            User = "hu-cafeteria-bot";
            Group = "hu-cafeteria-bot";
            RuntimeDirectory = "hu-cafeteria-bot";
            RuntimeDirectoryMode = "0700";
            StateDirectory = "hu-cafeteria-bot";
            WorkingDirectory = "${self.packages.${pkgs.system}.hu-cafeteria-bot}/lib/hu-cafeteria-bot";

            LockPersonality = true;
            PrivateDevices = true;
            PrivateTmp = true;
            PrivateUsers = true;
            ProtectClock = true;
            ProtectControlGroups = true;
            ProtectHome = true;
            ProtectHostname = true;
            ProtectKernelLogs = true;
            ProtectKernelModules = true;
            ProtectKernelTunables = true;
            ProtectProc = "invisible";
            RestrictNamespaces = true;
            RestrictRealtime = true;
            RestrictSUIDSGID = true;
            SystemCallArchitectures = "native";
            UMask = "0007";
          };
        };
      };
    };
  };
}
