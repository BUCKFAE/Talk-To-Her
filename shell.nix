let
  pkgs = import <nixpkgs> { config = { allowUnfree = true; }; };
  python = pkgs.python39;
  pythonPackages = python.pkgs;
in

with pkgs;

mkShell {
  name = "pip-env";
  buildInputs = with pythonPackages; [

    pytest
    setuptools
    wheel
    venvShellHook
    torch-bin
    pyaudio
    flac
    tkinter

    gcc
  ];

  venvDir = "venv";
  src = null;

  shellHook = ''
    alias ide="nohup pycharm-professional . &"
  '';

  postVenv = ''
    unset SOURCE_DATE_EPOCH
    source .env
  '';
  postShellHook = ''
    # Allow the use of wheels.
    unset SOURCE_DATE_EPOCH
    PYTHONPATH=$PWD/$venvDir/${python.sitePackages}:$PYTHONPATH
  '';
}
