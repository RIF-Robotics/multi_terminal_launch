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

        result = subprocess.run([f'xdotool type --clearmodifiers "docker exec -it --user ros rtp_humble_nvidia /bin/bash"; xdotool key Return;'],shell=True)
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


def get_args_parser():
    parser = argparse.ArgumentParser(description='Multiple terminal launch')
    parser.add_argument('launch_file', type=str,
                        help='Launch configuration file')
    return parser


def main_cli():
    sys.exit(main(get_args_parser().parse_args()))
