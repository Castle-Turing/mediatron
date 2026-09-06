{
  description = "Mediatron — the surface the castle shows its pages on";

  inputs.nixpkgs.url = "github:NixOS/nixpkgs/nixos-unstable";

  outputs =
    { nixpkgs, ... }:
    let
      system = "x86_64-linux";
      pkgs = nixpkgs.legacyPackages.${system};
    in
    {
      formatter.${system} = pkgs.nixfmt;
      # packages.mediatron and packages.mediatron-render land with task
      # 0001; this flake exists first so `nix flake check` is green from
      # the founding commit and every later change is a diff against a
      # working baseline.
    };
}
