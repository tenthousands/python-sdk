#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
  FISCO BCOS/Python-SDK is a python client for FISCO BCOS2.0 (https://github.com/FISCO-BCOS/)
  FISCO BCOS/Python-SDK is free software: you can redistribute it and/or modify it under the
  terms of the MIT License as published by the Free Software Foundation. This project is
  distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even
  the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. Thanks for
  authors and contributors of eth-abi, eth-account, eth-hash，eth-keys, eth-typing, eth-utils,
  rlp, eth-rlp , hexbytes ... and relative projects
  @author: kentzhang
  @date: 2019-06
"""
import sys
sys.path.append("./")
from bcos3sdk.bcos3client import Bcos3Client
from client.bcosclient import BcosClient
import os
from client.stattool import StatTool
from client.datatype_parser import DatatypeParser
from client.common.compiler import Compiler
from client_config import client_config
from client.bcoserror import BcosException, BcosError
import traceback
import json
# 从文件加载abi定义
demo_config = client_config
'''
if os.path.isfile(demo_config.solc_path) or os.path.isfile(demo_config.solcjs_path):
    Compiler.compile_file("contracts/HelloWorld.sol")
    Compiler.compile_file("contracts/SimpleInfo.sol")
abi_file = "contracts/SimpleInfo.abi"
data_parser = DatatypeParser()
data_parser.load_abi_file(abi_file)
contract_abi = data_parser.contract_abi
'''
# 以下是查询类的接口，大部分是返回json，可以根据对fisco bcos rpc接口json格式的理解，进行字段获取和转码
"""
useful helper:
int(num,16)  hex -> int
hex(num)  : int -> hex
"""
try:
    client = Bcos3Client()
    
    info = client.getinfo()
    print("client info:", info)
    stat = StatTool.begin()
    print("\n>>---------------------------------------------------------------------")
    res = client.getinfo()
    print("\n>>---------------------------------------------------------------------")
    print("getinfo", json.dumps(res, indent=4))
    print("\n>>---------------------------------------------------------------------")
    try:
        res = client.getBlockNumber()
        print("getBlockNumber", json.dumps(res, indent=4))
    except BcosError as e:
        print("bcos client error,", e.info())
    print("\n>>---------------------------------------------------------------------")
    print("getPeers", client.getPeers())
    print("\n>>---------------------------------------------------------------------")
    print("getBlockByNumber", json.dumps(client.getBlockByNumber(1)))
    print("\n>>---------------------------------------------------------------------")
    blockhash = client.getBlockHashByNumber(1)
    print("getBlockHashByNumber", blockhash)
    print("\n>>---------------------------------------------------------------------")
    block = client.getBlockByHash(blockhash)
    print("getBlockByHash", block)
    if isinstance(block, dict) and "transactions" in block.keys():
        txhash = block["transactions"][0]["hash"]
        print(
            "\n>>---------------------------------------------------------------------"
        )
        print("getTransactionByHash", json.dumps(client.getTransactionByHash(txhash)))
        print(
            "\n>>---------------------------------------------------------------------"
        )

        print("getTransactionReceipt", json.dumps(client.getTransactionReceipt(txhash)))
        print(
            "\n>>---------------------------------------------------------------------"
        )
    print("getTotalTransactionCount", client.getTotalTransactionCount())
    print("\n>>---------------------------------------------------------------------")
    print("getSystemConfigByKey", client.getSystemConfigByKey("tx_count_limit"))
    print("\n>>---------------------------------------------------------------------")

    print("getPbftView", client.getPbftView())
    print("\n>>---------------------------------------------------------------------")
    print("getSealerList", client.getSealerList())
    print("\n>>---------------------------------------------------------------------")
    print("getObserverList", client.getObserverList())
    print("\n>>---------------------------------------------------------------------")
    print("getConsensusStatus", client.getConsensusStatus())
    print("\n>>---------------------------------------------------------------------")
    print("getSyncStatus", client.getSyncStatus())
    print("\n>>---------------------------------------------------------------------")
    print("getGroupPeers", client.getGroupPeers())

    print("\n>>---------------------------------------------------------------------")
    print("getGroupList", client.getGroupList())
    stat.done()
    reqcount = next(client.request_counter)
    print(
        "demo get finish, total request {},usedtime {},avgtime:{}".format(
            reqcount, stat.time_used, (stat.time_used / reqcount)
        )
    )
    client.finish()

except BcosException as e:
    print("demo_get failed, BcosException information: {}".format(e))
    traceback.print_exc()
except BcosError as e:
    print("demo_get failed, BcosError information: {}".format(e))
    traceback.print_exc()
except Exception as e:
    traceback.print_exc()
client.finish()
