# coding = utf-8
import os, sys, bencodepy, hashlib, base64, getopt, csv

# shell

def getConfig():
    torrentFile = ''
    torrentsDir = ''
    output = 'result.csv'
    try:
        optlist, args = getopt.getopt(
            sys.argv[1:], "-f:-d:-o:", ["file=", "dir=", "output="])
        for key, value in optlist:
            if key in ('-f', '--file'):
                torrentFile = value
            elif key in ('-d', '--dir'):
                torrentsDir = value
            elif key in ('-o', '--output'):
                output = value if value.endswith('.csv') else value + '.csv'
        
        return (
            torrentFile,
            torrentsDir,
            output
        )
    except getopt.GetoptError:
        print('wrong options!')

# extract

def getInfos(file_path, file_name=''):
    try:
        file_data = bencodepy.decode_from_file(file_path)
        prefix = 'magnet:?xt=urn:btih:'

        info_key = b'info'

        info = file_data[info_key]

        byte, kb, mb, gb = getFullSize(info)

        name = getName(info, file_path)
        name = name if name else file_name

        hash = getHash(info)
        magnet_link = prefix + hash

        return [file_path, file_name, magnet_link, kb, mb, gb]
    except Exception as e:
        print('file path: %s' % (file_path))
        print(e)
        print('\n')
        return None


def iterateDir(dir):
    dir_list = os.walk(dir)
    result = []
    for root, dirs, files in dir_list:
        for file_name in files:
            if '.torrent' in file_name:
                file_path = os.path.join(root, file_name)
                info = getInfos(file_path, file_name)
                if info:
                    result.append(info)
    return result


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
            full_size += a_file[length_b]
    else:
        print('no length & files')
    size_kb = full_size / 1024
    size_mb = size_kb / 1024
    size_gb = size_mb / 1024
    return str(full_size), str(size_kb), str(size_mb), str(size_gb)


def getHash(info):
    info_hash = bencodepy.encode(info)
    digest = hashlib.sha1(info_hash).digest()
    b32_hash = base64.b32encode(digest).decode()
    return b32_hash


def getName(info, p):
    name_key = b'name'
    name = ''
    if name_key in info:
        try:
            name = info.get(name_key, '').decode('utf-8')
        except Exception:
            try:
                name = info.get(name_key, '').decode('gbk')
            except Exception as e:
                raise e
    return name

# export

def exportCSV(result, file_path):
    header = ['file name', 'manget', 'kb', 'mb', 'gb']
    try:
        with open(file_path, 'w', newline = '') as f:
            writer = csv.writer(f)
            writer.writerow(header)
            for row in result:
                try:
                    # TODO: unicode error
                    writer.writerow(row[1:5])
                except Exception as e:
                    print('file path: %s' % (row[0]))
                    print(e)
                    print('\n')
    except Exception as e:
        print(e)


def exportText(result, file_path):
    try:
        with open(file_path, 'w', newline = '', encoding = 'utf-8') as f:
            result_text = ''
            for line in result:
                result_text += ','.join(line) + '\n'
            f.write(result_text)
    except Exception as e:
        print(e)

# main

def main():
    torrentFile, torrentsDir, output = getConfig()

    if not torrentFile and not torrentsDir:
        print('must specify file path with -d or -f option!')
    else:
        print('extracting...\n')
        if torrentFile:
            result = [getInfos(torrentFile)]
        else:
            result = iterateDir(torrentsDir)

        print('exporting...\n')
        exportCSV(result, output)

        print('done')
                

if __name__ == '__main__':
    main()