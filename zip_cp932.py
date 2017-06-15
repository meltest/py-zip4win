# -*- coding: utf-8 -*-
import os, sys, zipfile, unicodedata

def main(path):
    # エラーチェック
    if len(path) != 1:
        sys.exit("Usage: %s <filename>" % sys.argv[0])
    if not os.path.exists(path[0]):
        sys.exit("no such file or folder %s" % sys.argv[1])

    # 対象がファイルかフォルダかで処理を分ける
    if os.path.isfile(path[0]):
        #print "this is file"
        zipFile4Win(os.path.abspath(path[0]))
    elif os.path.isdir(path[0]):
        # 後続の処理のために絶対パスを渡す
        zipFolder4Win(os.path.abspath(path[0]))

def zipFile4Win(path):
    dirpath, filename = os.path.split(path)
    # filenameから名前と拡張子を分離
    file, ext = os.path.splitext(filename)
    zipname = os.path.join(dirpath, file) + ".zip"

    # filenameはstr文字列でありそのままencodeできないため、一度Unicode文字に変換する
    unicode_filename = filename.decode("utf-8")
    # ファイル名に濁点や半濁点などを含む場合、Unicodeに変換しただけでは結合文字となっておりcp932でencodeできずエラーとなる
    # そのためUnicode正規化を行い、結合文字を合成済み文字に変換する
    normalize_unicode_filename = unicodedata.normalize("NFKC", unicode_filename)
    # unicode文字は任意の文字コードでencode可能であり、ここではwindowsで使用されるcp932(shift_jis)を設定
    cp932_filename = normalize_unicode_filename.encode("cp932", "replace")

    #print unicode_filename.encode("cp932")
    #print cp932_filename

    # ZipFileをオープン
    zip = zipfile.ZipFile(zipname, "w", zipfile.ZIP_DEFLATED)
    # ファイルを書き込み(書込元, 書込先)
    zip.write(filename, cp932_filename)
    zip.close

def zipFolder4Win(path):
    # 圧縮するファイルの配列
    zip_targets = []
    base = os.path.basename(path)
    zipfile_path = os.path.abspath('%s.zip' % base)
    print zipfile_path

    for root, dirs, files in os.walk(path):
        for filename in files:
            # file_pathはroot(引数で与えたディレクトリ)/filename(rootに含まれるファイル名)という形式
            file_path = os.path.join(root, filename)
            if file_path == zipfile_path:
                continue
            # アーカイブするときの名称を作成(ここでcp932に変換すればよさそう)
            archive_name = os.path.relpath(file_path, os.path.dirname(path))
            # archive_nameをunicode→cp932に変換
            # ファイル名に濁点や半濁点などを含む場合、Unicodeに変換しただけでは結合文字となっておりcp932でencodeできずエラーとなる
            # そのためUnicode正規化を行い、結合文字を合成済み文字に変換する
            unicode_filename = archive_name.decode("utf-8")
            normalize_unicode_filename = unicodedata.normalize("NFKC", unicode_filename)
            # unicode文字は任意の文字コードでencode可能であり、ここではwindowsで使用されるcp932(shift_jis)を設定
            cp932_filename = normalize_unicode_filename.encode("cp932", "replace")

            zip_targets.append((file_path, cp932_filename))

    # zipファイルの作成
    zip = zipfile.ZipFile(zipfile_path, 'w')
    for file_path, archive_name in zip_targets:
        zip.write(file_path, archive_name)
    zip.close()

if __name__ == "__main__":
    main(sys.argv[1:])
