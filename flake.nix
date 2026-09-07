{
  description = "Mediatron — the surface the castle shows its pages on";

  inputs.nixpkgs.url = "github:NixOS/nixpkgs/nixos-unstable";

  outputs =
    { nixpkgs, ... }:
    let
      system = "x86_64-linux";
      pkgs = nixpkgs.legacyPackages.${system};
      python = pkgs.python3;

      mediatron-render = pkgs.stdenv.mkDerivation {
        pname = "mediatron-render";
        version = "0.1.0";
        src = ./src;
        nativeBuildInputs = [ pkgs.makeWrapper ];
        installPhase = ''
          runHook preInstall
          mkdir -p $out/lib/mediatron $out/bin
          cp mediatron_render.py $out/lib/mediatron/
          makeWrapper ${python}/bin/python3 $out/bin/mediatron-render \
            --add-flags "$out/lib/mediatron/mediatron_render.py"
          runHook postInstall
        '';
      };

      mediatron = pkgs.stdenv.mkDerivation {
        pname = "mediatron";
        version = "0.1.0";
        src = ./src;
        nativeBuildInputs = [ pkgs.makeWrapper ];
        installPhase = ''
          runHook preInstall
          mkdir -p $out/lib/mediatron $out/bin $out/share/mediatron
          cp mediatron_render.py mediatron $out/lib/mediatron/
          makeWrapper ${python}/bin/python3 $out/bin/mediatron \
            --add-flags "$out/lib/mediatron/mediatron" \
            --set MEDIATRON_SHARE "$out/share/mediatron" \
            --prefix PATH : ${pkgs.qutebrowser}/bin:${pkgs.xdg-utils}/bin:${pkgs.coreutils}/bin
          cp ${./share/mediatron/open-external} $out/share/mediatron/open-external
          cp ${./share/mediatron/config.example} $out/share/mediatron/config.example
          chmod +x $out/share/mediatron/open-external
          runHook postInstall
        '';
      };
    in
    {
      formatter.${system} = pkgs.nixfmt;
      packages.${system} = {
        inherit mediatron mediatron-render;
        default = mediatron;
      };
    };
}
