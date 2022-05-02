# -*- coding: utf-8 -*-
import os, sys, zipfile, unicodedata, fcntl, time, asyncio
from subprocess import Popen, PIPE, STDOUT

def main(path):
    # エラーチェック
    if len(path) != 1:
        sys.exit("Usage: %s <filename>" % sys.argv[0])
    if not os.path.exists(path[0]):
        sys.exit("no such file or folder %s" % sys.argv[1])

    # 対象がファイルかフォルダかで処理を分ける
    if os.path.isfile(path[0]):
        #print "this is file"
        zip_path = zipFile4Win(os.path.abspath(path[0]))
    elif os.path.isdir(path[0]):
        # 後続の処理のために絶対パスを渡す
        zip_path = zipFolder4Win(os.path.abspath(path[0]))

    # zipファイル作成後にパスワードを設定するか確認
    answer = input("Do you want to set password? [Y/n]").lower()

    if answer in ['', 'y', 'ye', 'yes']:
        # zipcloakをasyncioで実行
        asyncio.run(encrypt_zip('zipcloak', [zip_path]))

        print("Completed!")
    else:
        print("Completed!")

def zipFile4Win(path):
    dirpath, filename = os.path.split(path)
    # filenameから名前と拡張子を分離
    file, ext = os.path.splitext(filename)
    zip_path = os.path.join(dirpath, file) + ".zip"


    # Python3 以降はstr型は全てUnicodeとして扱われるようになったため、decode不要となった
    # filename = unicode_name ということ

    # zipファイルを作成
    with zipfile.ZipFile(zip_path, "w", compression=zipfile.ZIP_DEFLATED) as archive:
        archive.write(filename, arcname=filename)

    return zip_path

def zipFolder4Win(path):
    # 圧縮するファイルの配列
    zip_targets = []
    base = os.path.basename(path)
    zip_path = os.path.abspath('%s.zip' % base)

    for root, dirs, files in os.walk(path):
        for filename in files:
            if filename == ".DS_Store":
                continue
            # file_pathはroot(引数で与えたディレクトリ)/filename(rootに含まれるファイル名)という形式
            file_path = os.path.join(root, filename)
            if file_path == zip_path:
                continue
            # アーカイブするときの名称を作成
            # Python3 以降はstr型は全てUnicodeとして扱われるようになったため、decode不要となった
            # archive_name = unicode_name ということ
            archive_name = os.path.relpath(file_path, os.path.dirname(path))

            zip_targets.append((file_path, archive_name))

    # zipファイルを作成
    with zipfile.ZipFile(zip_path, "w", compression=zipfile.ZIP_DEFLATED) as archive:
        for file_path, archive_ename in zip_targets:
            archive.write(file_path, arcname=archive_name)

    return zip_path

async def encrypt_zip(cmd: str, args: list[str]) -> None:
    proc = await asyncio.create_subprocess_exec(cmd, *args)
    await proc.communicate()
    print(f'{cmd} {" ".join(args)} exited with {proc.returncode}')

if __name__ == "__main__":
    main(sys.argv[1:])
