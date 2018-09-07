# coding = utf-8
import os, bencodepy, hashlib, base64


def iterateDir(dir):
    dir_list = os.walk(dir)
    for root, dirs, files in dir_list:
        for file_name in files:
            if '.torrent' in file_name:
                file_path = os.path.join(root, file_name)
                resolveFile(file_path, file_name)


def resolveFile(file_path, file_name=''):
    file_data = bencodepy.decode_from_file(file_path)
    prefix = 'magnet:?xt=urn:btih:'

    info_key = b'info'

    info = file_data[info_key]

    kb, mb, gb = getFullSize(info)

    name = getName(info)
    name = name if name else file_name

    hash = getHash(info)
    magnet_link = prefix + hash

    print('file name  : %s\n'
          'magnet link: %s\n'
          'full size  : %s kb/ %s mb/ %s gb\n'
          % (name, magnet_link, kb, mb, gb)
          )


def getFullSize(info):
    # bytes
    full_size = 0

    files_key = b'files'
    length_key = b'length'

    if length_key in info:
        full_size = info[length_key]
    elif files_key in info:
        files = info[files_key]
        for a_file in files:
            length_b = b'length'
            path_b = b'path'
            # print('  path:', a_file[path_b])
            # print('  length', a_file[length_b])
            full_size += a_file[length_b]
    else:
        print('no length & files')
    size_kb = full_size / 1024
    size_mb = size_kb / 1024
    size_gb = size_mb / 1024
    return size_kb, size_mb, size_gb


def getHash(info):
    info_hash = bencodepy.encode(info)
    digest = hashlib.sha1(info_hash).digest()
    b32_hash = base64.b32encode(digest).decode()
    return b32_hash


def getName(info):
    name_key = b'name'
    name = ''
    if name_key in info:
        name = info.get(name_key, '').decode()
    return name


if __name__ == '__main__':

    # for multiple torrent files
    iterateDir('torrents')

    # for single torrent file
    # resolveFile('test.torrent')
