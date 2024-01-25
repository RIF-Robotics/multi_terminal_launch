# Multiple Terminal Launch

## Install dependencies

    sudo apt-get install xdotool

## Install to user folder

    # Make sure pip is upgraded
    pip3 install --upgrade pip

    pip3 install -e .

    # Add local python executables to the PATH in your `.bashrc` file
    PATH="~/.local/bin":${PATH}
