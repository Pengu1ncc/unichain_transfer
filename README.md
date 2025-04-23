# 🔁 UniChain 多地址 ETH 转账脚本

本脚本通过 Python 使用 `web3.py` 和 `eth-account` 库，  
结合 HTTP `requests` 发送原始 `eth_sendRawTransaction` 请求，  
调用已部署在 UniChain（或其他 EVM 兼容链）上的 `MultiSender` 合约，  
实现 **将一笔 ETH / BNB 均分发送到多个地址**。

## ⚙️ 环境准备

安装必要的 Python 库：

```bash
pip install web3 eth-account requests
```

## 🛠️ 配置项

1. **PRIVATE_KEY** 中填入主钱包
2. **DIS_AMOUNT** 中填入转账金额（合约会自动评分）
3. **receivers.txt** 文件中填入分发钱包