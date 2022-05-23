# DISCLAIMER
I won't continue this project as there are already better alternatives out there:
* [nix](https://github.com/nix-community/home-manager)
* [dotbot](https://github.com/anishathalye/dotbot)
* [aconfmgr](https://github.com/CyberShadow/aconfmgr)

# StowY (Stow YAML wrapper)
StowY is a wrapper around [GNU Stow](https://www.gnu.org/software/stow/stow.html)
that adds support for package configuration files written in [YAML](https://yaml.org/).

# Requirements
* `python` version 3.7+
    - `pyyaml`
* `stow`

# Package Configurations
Each package may contain a `package.yaml` configuration file with the following contents:
```yaml
# Controls the `stow --target` option (default=$HOME)
Target: /path/to/target
# Changes the ownership of the packages files (default=$USER)
Owner: root
# Execute any commands at certain hook points
PreStow:  # Executed before any package is stowed
    - pacman -Sy --needed some-arch-package
    - pacman -S --needed --asdeps some-optional-dependency
PostStow:  # Executed after all packages were stowed
    - mkdir ~/.cache/some-arch-package
PreUnstow:  # Executed before any packages are unstowed
    - pacman -Rns some-arch-package; true
    - "pacman -Qdtq | grep -q some-optional-dependency\
      && pacman -Rns some-optional-dependency"
PostUnstow:  # Executed after all packages were stowed
    - rm -rf ~/.cache/some-arch-package
```
Any omitted options assume the default value.

# YAML Pitfalls
* A literal `~` is interpreted as a `null` value in YAML, use `$HOME` or `'~'` instead.
* There are other special character which your values can't begin with.
  If you're unsure, just use quotes.

# Relation to GNU Stow
Since StowY is only a relatively small wrapper around GNU Stow,
packages used by Stow are **fully compatible** with those used by StowY and vice versa.
The only thing to note is that you probably want to add `^/package.yaml` to your `~/.stow-global-ignore`
if you want to use Stow with StowY packages.
StowY is **not a drop-in replacement** for GNU Stow in the sense
that it doesn't support *every* argument that Stow does (because some make no sense with StowY)
and its argument parsing, while trying to replicate Stow's, doesn't work in entirely the same way.

# Further Documentation
* [GNU Stow manual](https://www.gnu.org/software/stow/manual/): `info stow`
* `stowy -h`
* You may also inspect StowY's source code (especially `main.py`), it's not very complex.
