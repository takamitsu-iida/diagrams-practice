# Python diagrams practice

```bash
brew install graphviz
```

```bash
pip install diagrams
```

## 接続のオペレーター

使えるオペレータは `>>`, `<<`, `-` の3個。

`>>` は左から右への接続、`<<`は逆に右から左への接続、`-`は向きのない接続。

```python
from diagrams import Diagram
from diagrams.aws.compute import EC2
from diagrams.aws.database import RDS
from diagrams.aws.network import ELB
from diagrams.aws.storage import S3

with Diagram("Web Services", show=False):
    ELB("lb") >> EC2("web") >> RDS("userdb") >> S3("store")
    ELB("lb") >> EC2("web") >> RDS("userdb") << EC2("stat")
    (ELB("lb") >> EC2("web")) - EC2("web") >> RDS("userdb")
```

定義した順番と逆の順番に描画される。

`>>` と `-` を同時に使うときは演算子の強度に注意が必要。予想外の動きをするときは()を使って調整する。

## 向き

directionには`TB`, `BT`, `LR`, `RL`を指定する。デフォルトは`LR`で、左から右に向かって描画する。
