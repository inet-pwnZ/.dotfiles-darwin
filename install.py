#!/usr/bin/env python

import subprocess
import os
import sys
from os import system
import logging

current_folder = os.path.abspath(os.getcwd())

pip_packages = [
        "powerline-status",
        "psutil"
        ]

brew_dependencies = [
        "mono",
        "gcc",
        "htop",
        "make",
        "python",
        "ruby",
        "go",
        "rust",
        "perl",
        "lua",
        "vim",
        "zsh",
        "nodenv",
        "docker",
        "docker-compose",
        "docker-machine"
        ]

cask_dependencies = [
        "virtualbox",
        "google-chrome",
        "cheatsheet",
        "firefox",
        "slack",
        "visual-studio-code",
        "microsoft-office",
        "skype-for-business",
        "postman",
        "iterm2",
        "docker",
        "whatsapp",
        "discord"
        ]

node_packages = [
        "nodemon",
        "webpack",
        "yarn"
        ]

arrow = '========>'

def Call(arg):
    try:
        cmdArr = arg.split()
        with open(os.devnull, "w") as f: subprocess.call(cmdArr, stdout=f)
    except OSError as e:
        print(e.errno)


def InstallPackages(installCall, arr, options):
    for package in arr:
        print('{0} Installing {1}'.format(arrow, package))
        install = '{0} {1} {2}'.format(installCall, package, options)
        cmdArr = install.split()
        try:
            with open(os.devnull, "w") as f: subprocess.call(cmdArr, stdout=f)
        except subprocess.CalledProcessError as e:
            logging.error('{0} Failed to install {1} with code {2}'.format(arrow, package, e.returncode))

def CallCheck(args, **kwargs):
    try:
        with open(os.devnull, "w") as f: subprocess.call(args, stdout=f)
    except subprocess.CalledProcessError as e:
        logging.critical('{0} {1} is Required'.format(arrow, args))
        sys.exit(e.returncode)

def Install(call):
    try:
        print('{0} Installing {1}'.format(arrow, call))
        cmdArr = call.split()
        with open(os.devnull, "w") as f: subprocess.call(cmdArr, stdout=f)
    except subprocess.CalledProcessError as e:
        logging.error('{0} Failed to install {1}'.format(arrow, call))

def main():
    print("{0} Starting Installation".format(arrow))
    print("{0} Installing Dependencies".format(arrow))

    # check if xcode dev tools are installed becouse of git
    try:
        CallCheck('xcode-select --install')
        Install('xcode-select --install')
    except:
        print("{0} xcode dev tools installed".format(arrow))

    # check if brew is installed
    try:
        print("{0} brew check".format(arrow))
        Call("brew")
    except OSError as e:
        logging.error("{0} brew not found installing brew".format(arrow))
        system('/usr/bin/ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)"')

    # check if git lfs is installed
    try:
        print("{0} git lfs check".format(arrow))
        Call("git lfs")
    except OSError as e:
        logging.error("{0} git lfs not found installing git lfs".format(arrow))
        system('brew install git-lfs')
        system('git lfs install')

    # git submodule pull
    try:
        print("{0} git pull submodules".format(arrow))
        Call('git submodule update --init --recursive')
    except OSError as e:
        logging.error("{0} git pull submodules failed".format(arrow))

    # install brew dependencies
    print("{0} Install brew dependencies".format(arrow))
    InstallPackages('brew install', brew_dependencies, '')

    # install cask dependencies
    print("{0} Install cask dependencies".format(arrow))
    InstallPackages('brew cask install', cask_dependencies, '')

    # install node
    print("{0} Install node".format(arrow))
    Install('nodenv install 12.8.0')
    Install('nodenv global 12.8.0')

    # node packages
    print("{0} Install node packages".format(arrow))
    InstallPackages('npm install', node_packages, '--global')

    # install python packages
    print("{0} Install pip packages".format(arrow))
    InstallPackages('pip3.7 install', pip_packages, '')

    # install fonts
    try:
        ### Fonts https://github.com/gabrielelana/awesome-terminal-fonts
        print("{0} Installing Fonts".format(arrow))
        ### and nerd fonts https://github.com/ryanoasis/nerd-fonts
        FONT="https://github.com/gabrielelana/awesome-terminal-fonts/blob/patching-strategy/patched/SourceCodePro%2BPowerline%2BAwesome%2BRegular.ttf"
        FONT_NAME="SourceCodeProAwesome.ttf"
        system('wget -L ' + FONT + ' -O ' + FONT_NAME + ' > /dev/null 2>&1')
        system('cp ' + current_folder + '/' + FONT_NAME + ' ~/Library/Fonts/' + FONT_NAME)
        system('brew tap homebrew/cask-fonts')
        system('brew cask install font-hack-nerd-font')
    except OSError as e:
        logging.error("{0} Error while installing fonts".format(arrow))

    # cloning dependencies
    try:
        print("Cloning Dependencies".format(arrow))
        system('cp -r ./powerlevel10k ' + current_folder +  '/oh-my-zsh/custom' + '/themes/powerlevel10k')
        system('cp -r zsh-syntax-highlighting ' + current_folder +  '/oh-my-zsh/custom' + '/plugins/zsh-syntax-highlighting')

        ### autosuggest
        system('git clone https://github.com/zsh-users/zsh-autosuggestions ' + current_folder +  '/oh-my-zsh/custom' + '/plugins/zsh-autosuggestions')

        ### fzf docker
        system('git clone https://github.com/pierpo/fzf-docker ' + current_folder +  '/oh-my-zsh/custom' + '/plugins/fzf-docker')
    except OSError as e:
        logging.error("{0} Error while cloning".format(arrow))

    # linking files
    try:
        print("{0} Linking zsh and vim files Symbolic".format(arrow))
        system('ln -s ' + current_folder + '/.zsh/zshrc ~/.zshrc')
        system('ln -s ' + current_folder + '/.dotfiles-vim/ ~/.vim')
        system('ln -s ' + current_folder + '/.vim/vimrc ~/.vimrc')
        system('ln -s ' + current_folder + '/.tmux.conf ~/.tmux.conf')
        system('ln -s ' + current_folder + '/.ssh/config ~/.ssh/config')
        system('ln -s ' + current_folder + '/powerline ~/.config')
    except OSError as e:
        logging.error("{0} Error while settings zsh shell".format(arrow))

    # set default shell
    try:
        print("{0} Set zsh default shell".format(arrow))
        system('chsh -s /usr/local/bin/zsh $(whoami)')
    except OSError as e:
        loggin.error("{0} Error while settings zsh shell".format(arrow))

    if len(sys.argv) > 0:
        if sys.argv[1] == '--all':
            # compile youcompleteme
            try:
                print("{0} Compile YCM".format(arrow))
                system('./.dotfiles-vim/bundle/YouCompleteMe/install.py --all')
            except OSError as e:
                logging.error("{0} Error while compiling ycm".format(arrow))

    print("{0} Installation Done".format(arrow))
    system('zsh')

if __name__ == "__main__":
    CallCheck('git')
    main()