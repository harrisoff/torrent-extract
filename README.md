# Torrent Extract

批量解析种子文件，获取文件名、磁链与文件大小，导出为 csv 文件。

## 安装

```shell
pip install -r requirements.txt
```

## 使用

### 选项

- `-f`/`--file=`，单个种子文件的路径
- `-d`/`--dir=`，种子文件的目录路径，用于批量转换
- `-o`/`--output=`，输出文件路径

### 说明

- `-f` 和 `-d` 至少需要一个，同时给出时，`-f` 会覆盖 `-d`
- 设置 `-d` 时，会深度遍历目录，只匹配 `.torrent` 格式的文件，包括隐藏的文件
- `-o` 可选，自动为文件名添加 `.csv` 后缀

### 示例

```shell
# 单个文件
python extract.py -f sample.torrent
# 文件夹下的多个文件
python extract.py -d ./torrents
# 输出到指定目录
python extract.py -d ./torrents -o C:/result.csv
```

## 依赖

- [bencodepy](https://github.com/eweast/BencodePy)

## 福利

1. 高清下载吧 2019-09-18 蓝光原盘磁链 4726 条
2. MP4吧 2014-2016 磁链 4995 条

## TODO LIST

- [ ] 导出到 csv 文件时 unicode 编码的文件名乱码