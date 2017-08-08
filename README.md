Energy_blockchain

本项目是使用fabric 1.0模拟多用户在能源互联网环节中使用能源区块链进行能源交易，利用区块链技术的防篡改性进行交易认证。确保能源交易的可靠性，推动新能源利用率等。

在CC层加入了简单的能源交易智能合约，并将交易数据写入账本以及保存在couchdb中，业务层数据库在本地db.sqlite中，在上层使用python的胶水特性进行连接，前端界面使用vue框架，后台使用flask。

使用说明：
    运行环境为Linux(Ubuntu 16.04):
    Node版本：v6.9.5. Go版本：1.8 Python版本：3.5.2 Docker版本：17.03.1-ce及以上. 并安装docker-compose
    
    设置$GOPATH为/home/leon/workspace.
    需要在https://github.com/hyperledger里获取Fabirc-CA，Fabric. 放入$GOPATH/src/github.com/hyperledger中.
    在Fabirc和Fabric中分别执行 make docke生成docker镜像并修改标签为latest.
    将项目中的fabric-sdk-node 放入 $GOPATH/src/hyperledger/fabric中
    在fabric-sdk-node/energy_blockchain/fabric-sdk-node/test/fixtures 中执行 docker-compose up --force-recreate.
    在fabric-sdk-node/energy_blockchain/fabric-sdk-node/test/integration/e2e 中 执行：
      node create-channel.js
      node join-channel.js
      node install-chaincode.js
      node instantiate-chaincode.js
    完成部署智能合约, 通过使用node upgrade.js更新智能合约（需要在upgrade.js和query1.sh中修改版本号 默认为 'v113'）
    
    运行 python3 energy-hyperledger.py
    运行 python3 app.py 启动Flask后台，交易平台界面地址为 http：//localhost:8080/    
    在Web端进行基于hyperledger的能源管理交易。
    
    第三次更新（Version 1.0）
