import requests
from web3 import Web3
from eth_account import Account

# ======= 配置项 =======
RPC_URL = "https://mainnet.unichain.org"  # 换成你的 RPC 节点
PRIVATE_KEY = "You_PrivateKey"
DIS_AMOUNT = 0.01
SENDER_ADDRESS = Account.from_key(PRIVATE_KEY).address
CONTRACT_ADDRESS = Web3.to_checksum_address("0xfD2424913DfF580A348f39f9A42de5206dbB3662")
CHAIN_ID = 130  # 修改为你链的 chainId（Unichain 主网）

# ======= 读取接收方地址 =======
def load_receivers_from_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    return [
        Web3.to_checksum_address(line.strip())
        for line in lines
        if line.strip()
    ]

receivers = load_receivers_from_file("receivers.txt.txt")
if len(receivers) == 0:
    raise Exception("未读取到接收地址，请检查 receivers.txt.txt 文件！")

print(f"读取到 {len(receivers)} 个接收地址：")
print(receivers)

# ======= 总金额（均分给每个地址） =======
total_amount = Web3.to_wei(DIS_AMOUNT, 'ether')  # 总发送金额，可以自行修改

# ======= 手撸 ABI 编码：sendValue(address[]) =======
function_selector = Web3.keccak(text="sendValue(address[])")[:4]
offset = (32).to_bytes(32, 'big')
array_length = len(receivers).to_bytes(32, 'big')
encoded_addresses = b''.join([b'\x00' * 12 + bytes.fromhex(addr[2:]) for addr in receivers])
data = function_selector + offset + array_length + encoded_addresses
data_hex = Web3.to_hex(data)

# ======= 获取 nonce =======
def get_nonce(address):
    payload = {
        "jsonrpc": "2.0",
        "method": "eth_getTransactionCount",
        "params": [address, "latest"],
        "id": 1
    }
    response = requests.post(RPC_URL, json=payload).json()
    return int(response["result"], 16)

nonce = get_nonce(SENDER_ADDRESS)
gas_price = Web3.to_wei(5, 'gwei')  # 可动态调整
gas_limit = 300000  # 可动态调整

# ======= 构造交易 =======
tx = {
    "nonce": nonce,
    "to": CONTRACT_ADDRESS,
    "value": total_amount,
    "gas": gas_limit,
    "gasPrice": gas_price,
    "data": data_hex,
    "chainId": CHAIN_ID
}

# ======= 签名交易 =======
signed_tx = Account.sign_transaction(tx, private_key=PRIVATE_KEY)
raw_tx_hex = Web3.to_hex(signed_tx.rawTransaction)

# ======= 发送交易 =======
send_payload = {
    "jsonrpc": "2.0",
    "method": "eth_sendRawTransaction",
    "params": [raw_tx_hex],
    "id": 1
}

response = requests.post(RPC_URL, json=send_payload)
print("发送结果:", response.json())
