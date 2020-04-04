{ pkgs, ... }:

{
  imports = [ 
    <nixpkgs/nixos/modules/installer/cd-dvd/sd-image-raspberrypi4.nix>
#    <nixpkgs/nixos/modules/profiles/hardened.nix>
   ];

  boot.vesa = false;

  # Reboot on panic
  boot.kernelParams = [ "panic=1" "boot.panic_on_fail" ];

  networking.hostName = "eupheme";
  networking.wireless.enable = false;
  networking.useDHCP = false;
  networking.interfaces.eth0.ipv4.addresses = [
    {address = "192.168.1.2";
    prefixLength = 24;}
  ];
  networking.defaultGateway = "192.168.1.1";
  networking.nameservers = ["1.1.1.1"];
  networking.networkmanager.enable = true;

  time.timeZone = "Europe/Amsterdam";

  environment.systemPackages = with pkgs; [
    coreutils
    emacs
    git
    htop
    neofetch
    pciutils
    usbutils
    wget
  ];

  # Enable SSH
  services.openssh.enable = true;
  services.openssh.permitRootLogin = "yes";
  

  # Open ports in the firewall
  networking.firewall.allowedTCPPorts = [ 22 80 443 ];
  networking.firewall.allowedUDPPorts = [ 22 ];

  users.users.luis = {
    isNormalUser = true;
    uid = 1000;
    home = "/home/luis";
    extraGroups = [ "wheel" ];
  };

 # This value determines the NixOS release with which your system is to be
  # compatible, in order to avoid breaking some software such as database
  # servers. You should change this only after NixOS release notes say you
  # should.
  system.stateVersion = "19.09"; # Did you read the comment?
  system.autoUpgrade.enable = true;

}
