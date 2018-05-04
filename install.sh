#!/bin/sh

### Install Script by Daniel Nehrig inet-pwnZ
### @inetpwnZ // daniel.nehrig@dnehrig.com

# Install Validation
if [ ! -n "$DOTUNIX" ]; then
  DOTUNIX="$(pwd)"
fi

# if [ -d "$DOTUNIX" ]; then
#   printf "You already have DOTUNIX installed.\n"
#   printf "You'll need to remove $DOTUNIX if you want to re-install.\n"
#   exit
# fi

command -v git >/dev/null 2>&1 || {
  echo "Error git is not installed"
  exit 1
}

CURRENT_SHELL=$(expr "$SHELL" : '.*/(.*\)')

# Installing Dependencies
### Brew Install Validation
echo "Enter Permission Credentials"
if ! brew_loc="$(type -p "brew")" || [[ -z $brew_loc ]]; then
  echo "Installing Brew"
  /usr/bin/ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)"
else
  echo "Brew is allready installed"
fi

### Brew Dependencies
brew_depend="vim --with-python@2 mpv mplayer unrar tmux shairport-sync w3m zsh youtube-dl wget wine"
brew_dev_depend="node ruby python mongodb gdb maven mysql go docker docker-compose docker-machine ctags cmake perl lua"
if ! brew_loc="$(type -p "brew")" || [[ ! -z $brew_loc ]]; then
  clear
  echo "Install System Utilitys"
  echo $brew_depend
  brew install $brew_depend
  echo "Install Dev Utilitys"
  echo $brew_dev_depend
  brew install $brew_dev_depend
else
  echo "Brew not found"
fi

### NodeJS NPM Dependencies
node_depend_global="webpack nodemon"
if ! node_loc="$(type -p "npm")" || [[ ! -z $node_loc ]]; then
  clear
  npm install $node_depend_global --global
fi

### Ruby GEM Dependencies
gem_depend="mailcatcher sass"
if ! gem_loc="$(type -p "gem")" || [[ ! -z $gem_loc ]]; then
  clear
  echo "Installing Gem Dependencies"
  echo $gem_depend
  gem install $gem_depend
fi

### Python PIP Dependencies
pip_depend="pylint setuptools unicorn wheel wrapt youtube-dl Pygments powerline-status mercurial pip isort"
if ! python_loc="$(type -p "python")" || [[ ! -z $python_loc ]]; then
  clear
  echo "Installing Pip Dependencies"
  echo $pip_depend
  pip install $pip_depend
else
  echo "Python not found"
fi

# Make ZSH default shell
clear
echo "Making ZSH default shell"
sudo echo "/usr/local/bin/zsh" >> /etc/shells
chsh -s /usr/local/bin/zsh $(whoami)

# Downloading Private Files if Permission granted
### SSH KEYS
if [ -n "$SSH_SERV" ]; then
  clear
  echo "Downloading SSH Keys"
  scp -r $SSH_USER@$SSH_SERV:~/.ssh/$SSH_PRIVATE_KEY ~/.ssh/
fi

### Fonts
clear
echo "Downloading Fonts"
font="https://github.com/gabrielelana/awesome-terminal-fonts/blob/patching-strategy/patched/SourceCodePro%2BPowerline%2BAwesome%2BRegular.ttf"
wget -L $font > /dev/null 2>&1
mv ./SourceCodePro+Powerline+Awesome+Regular.ttf ./fonts/SourceCodeProAwesome.ttf

# Linking Files
clear
echo "Linking Files"
ln -s $pwd/.vim/vimrc ~/.vimrc
ln -s $pwd/.zsh/zshrc ~/.zshrc
