# -*- coding: utf-8 -*-
import os, sys, zipfile
from subprocess import Popen, PIPE, STDOUT

def main(path):
    # エラーチェック
    if len(path) != 1:
        sys.exit("Usage: %s <filename>" % sys.argv[0])
    if not os.path.exists(path[0]):
        sys.exit("no such file or folder %s" % sys.argv[1])

    filepath = os.path.abspath(path[0])
    dirpath, filename = os.path.split(filepath)
    fileraw, ext = os.path.splitext(filename)
    basename = os.path.basename(os.path.join(dirpath, fileraw))
    zippath = os.path.abspath('%s.zip' % basename)

    # zip4winを実行するためのコマンドを作成
    cmd = 'python ' + 'zip_cp932.py ' + filename
    print cmd
    popen = Popen(cmd, shell=True, stdout=PIPE, stdin=PIPE, stderr=STDOUT)
    popen.communicate()

    # zipcloakを実行するためのコマンドを作成
    zipcloak_cmd = 'zipcloak ' + zippath

    # zipの暗号化のためにzipcloakを呼び出す
    p_zipcloak = Popen(zipcloak_cmd, shell=True, stdout=PIPE, stdin=PIPE, stderr=STDOUT)
    p_zipcloak.wait()
    stdout_data, stderr_data = p_zipcloak.communicate()
    print stdout_data, stderr_data

if __name__ == "__main__":
    main(sys.argv[1:])
