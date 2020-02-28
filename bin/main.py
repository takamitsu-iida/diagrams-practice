#!/usr/bin/env python
# -*- coding: utf-8 -*-

#
# 標準ライブラリのインポート
#
import argparse
import logging
import os
import sys

try:
  from diagrams import Diagram
  from diagrams.aws.compute import EC2
  from diagrams.aws.database import RDS
  from diagrams.aws.network import ELB
except ImportError as e:
  logging.exception(e)
  sys.exit(-1)


def here(path=''):
  """相対パスを絶対パスに変換して返却します"""
  return os.path.abspath(os.path.join(os.path.dirname(__file__), path))

# アプリケーションのホームディレクトリは一つ上
app_home = here("..")

# 自身の名前から拡張子を除いてプログラム名を得る
app_name = os.path.splitext(os.path.basename(__file__))[0]

# ディレクトリ
conf_dir = os.path.join(app_home, "conf")
data_dir = os.path.join(app_home, "data")

# libフォルダにおいたpythonスクリプトをインポートできるようにするための処理
# このファイルの位置から一つ
if not here("../lib") in sys.path:
  sys.path.append(here("../lib"))

if not here("../lib/site-packages") in sys.path:
  sys.path.append(here("../lib/site-packages"))


if __name__ == '__main__':


  def main():
    """メイン関数

    Returns:
      int -- 正常終了は0、異常時はそれ以外を返却
    """

    # 引数処理
    parser = argparse.ArgumentParser(description='main script.')
    parser.add_argument('-d', '--dump', action='store_true', default=False, help='Dump')
    args = parser.parse_args()

    if args.dump:
      dump()

    with Diagram("Web Service", show=False):
      ELB("lb") >> EC2("web") >> RDS("userdb")

    return 0

  # 実行
  sys.exit(main())
