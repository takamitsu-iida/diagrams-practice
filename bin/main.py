#!/usr/bin/env python
# -*- coding: utf-8 -*-
# pylint: disable=expression-not-assigned
# pylint: disable=missing-docstring
# pylint: disable=pointless-statement
# pylint: disable=protected-access

import logging
import os
import sys

try:
  from diagrams import Diagram
  from diagrams import Cluster
  from diagrams.aws.compute import EC2
  from diagrams.aws.compute import ECS
  from diagrams.aws.compute import EKS
  from diagrams.aws.compute import Lambda
  from diagrams.aws.database import RDS
  from diagrams.aws.network import ELB
  from diagrams.aws.network import Route53
  from diagrams.aws.database import Redshift
  from diagrams.aws.integration import SQS
  from diagrams.aws.storage import S3

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

  def test1():
    with Diagram("Workers", show=False, direction="TB", filename=sys._getframe().f_code.co_name):
      lb = ELB("lb")
      db = RDS("events")
      lb >> EC2("worker1") >> db
      lb >> EC2("worker2") >> db
      lb >> EC2("worker3") >> db
      lb >> EC2("worker4") >> db
      lb >> EC2("worker5") >> db

  def test2():
    with Diagram("Grouped Workers", show=False, direction="TB", filename=sys._getframe().f_code.co_name):
      ELB("lb") >> [EC2("worker1"),
                    EC2("worker2"),
                    EC2("worker3"),
                    EC2("worker4"),
                    EC2("worker5")] >> RDS("events")

  def test3():
    with Diagram("Simple Web Service with DB Cluster", show=False, filename=sys._getframe().f_code.co_name):
      dns = Route53("dns")
      web = ECS("service")

      with Cluster("DB Cluster"):
        db_master = RDS("master")
        db_master - [RDS("slave1"), RDS("slave2")]

      dns >> web >> db_master

  def test4():
    with Diagram("Event Processing", show=False, filename=sys._getframe().f_code.co_name):
      source = EKS("k8s source")

      with Cluster("Event Flows"):
        with Cluster("Event Workers"):
          workers = [ECS("worker1"), ECS("worker2"), ECS("worker3")]

        queue = SQS("event queue")

        with Cluster("Processing"):
          handlers = [Lambda("proc1"), Lambda("proc2"), Lambda("proc3")]

      store = S3("events store")
      dw = Redshift("analytics")

      source >> workers >> queue >> handlers
      handlers >> store
      handlers >> dw


  def main():
    """メイン関数

    Returns:
      int -- 正常終了は0、異常時はそれ以外を返却
    """

    test1()
    test2()
    test3()
    test4()


    return 0

  # 実行
  sys.exit(main())
