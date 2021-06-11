import tempfile
import subprocess as sp
import os
import filecmp
import sys


def run_basic_tests(exec_path, version, port, msg_type):
    address = '127.0.0.1' if version == 'v4' else '::1'
    list_dir = os.listdir('tests/in')
    list_dir = sorted(list_dir)
    for filename in list_dir:
        filename = filename.split('.')[0]
        _, result_file_path = tempfile.mkstemp()

        server = sp.Popen(
            [f'exec {exec_path} {version} {port}'], shell=True, stdout=sp.DEVNULL, stderr=sp.DEVNULL)
        ret = os.system(
            f'python3 client.py {address} {port} {msg_type} < tests/in/{filename}.in > {result_file_path}')
        ret = os.WEXITSTATUS(ret)

        if ret == 0:
            if filecmp.cmp(f'tests/out/{filename}.out', result_file_path, shallow=False):
                print(f'{filename}\t[OK]')
            else:
                print(f'{filename}\t[FAILED] (diff output)')
        else:
            print(
                f'{filename}\t[FAILED] (client exited with non-zero code {ret})')
        os.remove(result_file_path)
        server.kill()


if __name__ == '__main__':
    if len(sys.argv) != 3:
        print(f'usage: python3 {sys.argv[0]} <server> <port>')
        sys.exit(0)
    exec_path = sys.argv[1]
    port = int(sys.argv[2])

    if not exec_path.startswith('/'):
        print('provide the full path to the executable')
        sys.exit(0)

    for address_family in ['v4', 'v6']:
        for msg_type in ['single_msg_single_pkg', 'single_msg_multiple_pkg', 'multiple_msg_single_pkg']:
            print('Testing IP' + address_family, msg_type)
            run_basic_tests(exec_path, address_family, port, msg_type)
