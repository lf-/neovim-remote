#!/usr/bin/env python3

import os
import time
import signal
import subprocess
import nvr

env = os.environ.copy()
env['NVIM_LISTEN_ADDRESS'] = '/tmp/pytest_nvimsock'

def _popen_nvim(**kwargs):
    return subprocess.Popen(['nvim', '-nu', 'NORC', '--headless'], close_fds=True,
                            env=env, **kwargs)

def test_open_and_write_file():
    with _popen_nvim() as proc:
        time.sleep(1)
        argv = ['nvr', '--nostart', '-c', 'e /tmp/pytest_file | %d | exe "norm! iabc" | w']
        nvr.main(argv=argv, env=env)
        proc.send_signal(signal.SIGTERM)

    with open('/tmp/pytest_file') as f:
        assert 'abc\n' == f.read()
    os.unlink('/tmp/pytest_file')

def test_set_vars():
    with _popen_nvim() as proc:
        # XXX: we should find a way to make this wait on neovim opening
        time.sleep(1)
        argv = ['nvr', '--nostart', '-V', 'aaa', 'bbb', '-V', 'ccc', 'ddd', '-c', 'e /tmp/pytest_file | %d | put =g:aaa | put =g:ccc | w']
        nvr.main(argv=argv, env=env)
        proc.send_signal(signal.SIGTERM)

    with open('/tmp/pytest_file') as f:
        assert 'aaaddd\n' == f.read()
    os.unlink('/tmp/pytest_file')
