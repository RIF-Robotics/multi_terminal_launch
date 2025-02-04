import sys
import argparse
import subprocess
import time
import yaml

def main(args):
    with open(args.launch_file, "r") as stream:
        try:
            info = yaml.safe_load(stream)
        except yaml.YAMLError as exc:
            print(exc)
            return -1

    # Run the system commands if they exist
    try:
        pre_commands = info['pre_commands']

        for pre_command in pre_commands:
            subprocess.call([f'{pre_command}'], shell=True)
    except KeyError:
        pass

    try:
        pre_terminal_command = info['pre_terminal_command']
    except KeyError:
        pre_terminal_command = None

    for terminal in info['terminals']:
        title = terminal['title']
        cmd = terminal['cmd']

        subprocess.call([f'gnome-terminal --title="{title}"'], shell=True)

        # Get the window ID
        result = subprocess.run([f'xdotool search --sync {title}'], shell=True, stdout=subprocess.PIPE)
        window_id = result.stdout.decode('utf-8').strip('\n')

        terminal['window_id'] = window_id # Save the window ID for when we close it later

        result = subprocess.run([f'xdotool windowactivate --sync {window_id}'],shell=True)
        time.sleep(0.2) # The --sync doesn't seem to work all the time

        if pre_terminal_command is not None:
            result = subprocess.run([f'xdotool type --clearmodifiers "{pre_terminal_command}"; xdotool key Return;'],shell=True)

        result = subprocess.run([f'xdotool type --clearmodifiers "{cmd}"'],shell=True)
        if terminal['autorun']:
            result = subprocess.run(['xdotool key Return'],shell=True)

        print('-'*10)
        print(terminal)


    print('='*10)
    print('Type [ENTER] to close terminals: ')
    user_input = input()

    for terminal in info['terminals']:
        window_id = terminal['window_id']
        print('killing window_id: ', window_id)

        result = subprocess.run([f'xdotool windowactivate --sync {window_id}'],shell=True)
        result = subprocess.run([f'xdotool key --clearmodifiers ctrl+c'],shell=True)

        time.sleep(0.5)

        result = subprocess.run([f'xdotool windowclose {window_id}'],shell=True)

    # Run the system commands if they exist
    try:
        post_commands = info['post_commands']

        for post_command in post_commands:
            subprocess.call([f'{post_command}'], shell=True)
    except KeyError:
        pass


def get_args_parser():
    parser = argparse.ArgumentParser(description='Multiple terminal launch')
    parser.add_argument('launch_file', type=str,
                        help='Launch configuration file')
    return parser


def main_cli():
    sys.exit(main(get_args_parser().parse_args()))
