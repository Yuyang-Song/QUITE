# FabCar Hyperledger Fabric ./startFabric.sh execution is not completely working
[Link to question](https://stackoverflow.com/questions/60333949/fabcar-hyperledger-fabric-startfabric-sh-execution-is-not-completely-working)
**Creation Date:** 1582270171
**Score:** 1
**Tags:** node.js, docker, hyperledger-fabric, hyperledger, hyperledger-chaincode
## Question Body
<p>Im experimenting Hyperledger Fabric FabCar basic example.</p>

<p>Successfully registered admin and user, using registerAdmin.js and registerUser.js. I am currently facing this error after running node query.js.</p>

<pre><code>~/fabric-samples/fabcar$ node query.js 
Store path:/home/****/fabric-samples/fabcar/hfc-key-store
Successfully loaded user1 from persistence
2020-02-21T07:08:00.564Z - error: [Remote.js]: Error: Failed to connect before the deadline URL:grpc://localhost:7051
Query has completed, checking results
error from query =  { Error: Failed to connect before the deadline URL:grpc://localhost:7051
    at checkState (/home/****/fabric-samples/fabcar/node_modules/fabric-client/node_modules/grpc/src/client.js:833:16) connectFailed: true }

</code></pre>

<p>That was mentioned similarly in my previous <a href="https://stackoverflow.com/questions/60163176/error-failed-to-connect-before-the-deadline-urlgrpc-localhost7051">question</a></p>

<p>While checking <em>docker ps -a</em> , I could find the peer got exited</p>

<pre><code>~/fabric-samples/fabcar$ docker ps -a
CONTAINER ID        IMAGE                        COMMAND                  CREATED             STATUS                      PORTS                                        NAMES
1619413cd23c        hyperledger/fabric-peer      "peer node start"        13 minutes ago      Exited (2) 12 minutes ago                                                peer0.org1.example.com
de74d2459574        hyperledger/fabric-couchdb   "tini -- /docker-ent…"   13 minutes ago      Up 13 minutes               4369/tcp, 9100/tcp, 0.0.0.0:5984-&gt;5984/tcp   couchdb
356fb281acbe        hyperledger/fabric-orderer   "orderer"                13 minutes ago      Up 13 minutes               0.0.0.0:7050-&gt;7050/tcp                       orderer.example.com
5e52be445c99        hyperledger/fabric-ca        "sh -c 'fabric-ca-se…"   13 minutes ago      Up 13 minutes               0.0.0.0:7054-&gt;7054/tcp                       ca.example.com

</code></pre>

<p>after checking the workflow I found that the <em>./startFabric.sh</em> execution is not completely running, it got exited after <em>INFO 001 Endorser and orderer connections initialized</em>.</p>

<pre><code>~/fabric-samples/fabcar$ ./startFabric.sh

# don't rewrite paths for Windows Git Bash users
export MSYS_NO_PATHCONV=1

docker-compose -f docker-compose.yml down
Removing network net_basic

docker-compose -f docker-compose.yml up -d ca.example.com orderer.example.com peer0.org1.example.com couchdb
Creating network "net_basic" with the default driver
Creating ca.example.com      ... done
Creating couchdb             ... done
Creating orderer.example.com ... done
Creating peer0.org1.example.com ... done

# wait for Hyperledger Fabric to start
# incase of errors when running later commands, issue export FABRIC_START_TIMEOUT=&lt;larger number&gt;
export FABRIC_START_TIMEOUT=10
#echo ${FABRIC_START_TIMEOUT}
sleep ${FABRIC_START_TIMEOUT}

# Create the channel
docker exec -e "CORE_PEER_LOCALMSPID=Org1MSP" -e "CORE_PEER_MSPCONFIGPATH=/etc/hyperledger/msp/users/Admin@org1.example.com/msp" peer0.org1.example.com peer channel create -o orderer.example.com:7050 -c mychannel -f /etc/hyperledger/configtx/channel.tx
2020-02-21 07:07:06.183 UTC [channelCmd] InitCmdFactory -&gt; INFO 001 Endorser and orderer connections initialized
2020-02-21 07:07:06.222 UTC [channelCmd] InitCmdFactory -&gt; INFO 002 Endorser and orderer connections initialized
2020-02-21 07:07:06.432 UTC [main] main -&gt; INFO 003 Exiting.....
# Join peer0.org1.example.com to the channel.
docker exec -e "CORE_PEER_LOCALMSPID=Org1MSP" -e "CORE_PEER_MSPCONFIGPATH=/etc/hyperledger/msp/users/Admin@org1.example.com/msp" peer0.org1.example.com peer channel join -b mychannel.block
2020-02-21 07:07:06.907 UTC [channelCmd] InitCmdFactory -&gt; INFO 001 Endorser and orderer connections initialized

:~/fabric-samples/fabcar$

</code></pre>

<p>Kindly advise.</p>

<p>*Updated with the Docker logs of the Conatiner:</p>

<pre><code>2020-02-21 08:51:13.123 UTC [nodeCmd] serve -&gt; INFO 001 Starting peer:
 Version: 1.1.0
 Go version: go1.9.2
 OS/Arch: linux/amd64
 Experimental features: false
 Chaincode:
  Base Image Version: 0.4.6
  Base Docker Namespace: hyperledger
  Base Docker Label: org.hyperledger.fabric
  Docker Namespace: hyperledger

2020-02-21 08:51:13.123 UTC [ledgermgmt] initialize -&gt; INFO 002 Initializing ledger mgmt
2020-02-21 08:51:13.123 UTC [kvledger] NewProvider -&gt; INFO 003 Initializing ledger provider
2020-02-21 08:51:13.795 UTC [couchdb] CreateDatabaseIfNotExist -&gt; INFO 004 Created state database _users
2020-02-21 08:51:14.058 UTC [couchdb] CreateDatabaseIfNotExist -&gt; INFO 005 Created state database _replicator
2020-02-21 08:51:14.326 UTC [couchdb] CreateDatabaseIfNotExist -&gt; INFO 006 Created state database _global_changes
2020-02-21 08:51:14.366 UTC [kvledger] NewProvider -&gt; INFO 007 ledger provider Initialized
2020-02-21 08:51:14.366 UTC [ledgermgmt] initialize -&gt; INFO 008 ledger mgmt initialized
2020-02-21 08:51:14.367 UTC [peer] func1 -&gt; INFO 009 Auto-detected peer address: 172.25.0.5:7051
2020-02-21 08:51:14.368 UTC [peer] func1 -&gt; INFO 00a Returning peer0.org1.example.com:7051
2020-02-21 08:51:14.368 UTC [peer] func1 -&gt; INFO 00b Auto-detected peer address: 172.25.0.5:7051
2020-02-21 08:51:14.368 UTC [peer] func1 -&gt; INFO 00c Returning peer0.org1.example.com:7051
2020-02-21 08:51:14.373 UTC [eventhub_producer] start -&gt; INFO 00d Event processor started
2020-02-21 08:51:14.374 UTC [nodeCmd] computeChaincodeEndpoint -&gt; INFO 00e Entering computeChaincodeEndpoint with peerHostname: peer0.org1.example.com
2020-02-21 08:51:14.375 UTC [nodeCmd] computeChaincodeEndpoint -&gt; INFO 00f Exit with ccEndpoint: peer0.org1.example.com:7052
2020-02-21 08:51:14.375 UTC [nodeCmd] createChaincodeServer -&gt; WARN 010 peer.chaincodeListenAddress is not set, using peer0.org1.example.com:7052
2020-02-21 08:51:14.378 UTC [chaincode] NewChaincodeSupport -&gt; INFO 011 Chaincode support using peerAddress: peer0.org1.example.com:7052
2020-02-21 08:51:14.379 UTC [sccapi] registerSysCC -&gt; INFO 012 system chaincode cscc(github.com/hyperledger/fabric/core/scc/cscc) registered
2020-02-21 08:51:14.380 UTC [sccapi] registerSysCC -&gt; INFO 013 system chaincode lscc(github.com/hyperledger/fabric/core/scc/lscc) registered
2020-02-21 08:51:14.380 UTC [sccapi] registerSysCC -&gt; INFO 014 system chaincode escc(github.com/hyperledger/fabric/core/scc/escc) registered
2020-02-21 08:51:14.380 UTC [sccapi] registerSysCC -&gt; INFO 015 system chaincode vscc(github.com/hyperledger/fabric/core/scc/vscc) registered
2020-02-21 08:51:14.380 UTC [sccapi] registerSysCC -&gt; INFO 016 system chaincode qscc(github.com/hyperledger/fabric/core/chaincode/qscc) registered
2020-02-21 08:51:14.382 UTC [gossip/service] func1 -&gt; INFO 017 Initialize gossip with endpoint peer0.org1.example.com:7051 and bootstrap set [127.0.0.1:7051]
2020-02-21 08:51:14.386 UTC [msp] DeserializeIdentity -&gt; INFO 018 Obtaining identity
2020-02-21 08:51:14.389 UTC [gossip/discovery] NewDiscoveryService -&gt; INFO 019 Started { [] [61 97 241 125 96 173 40 203 239 81 147 191 102 161 39 23 0 117 69 217 56 120 139 152 120 223 29 9 23 115 238 6] peer0.org1.example.com:7051 &lt;nil&gt;} incTime is 1582275074389049506
2020-02-21 08:51:14.389 UTC [gossip/gossip] NewGossipService -&gt; INFO 01a Creating gossip service with self membership of { [] [61 97 241 125 96 173 40 203 239 81 147 191 102 161 39 23 0 117 69 217 56 120 139 152 120 223 29 9 23 115 238 6] peer0.org1.example.com:7051 &lt;nil&gt;}
2020-02-21 08:51:14.392 UTC [gossip/gossip] NewGossipService -&gt; WARN 01b External endpoint is empty, peer will not be accessible outside of its organization
2020-02-21 08:51:14.392 UTC [gossip/gossip] start -&gt; INFO 01c Gossip instance peer0.org1.example.com:7051 started
2020-02-21 08:51:14.393 UTC [cscc] Init -&gt; INFO 01d Init CSCC
2020-02-21 08:51:14.393 UTC [sccapi] deploySysCC -&gt; INFO 01e system chaincode cscc/(github.com/hyperledger/fabric/core/scc/cscc) deployed
2020-02-21 08:51:14.394 UTC [sccapi] deploySysCC -&gt; INFO 01f system chaincode lscc/(github.com/hyperledger/fabric/core/scc/lscc) deployed
2020-02-21 08:51:14.395 UTC [escc] Init -&gt; INFO 020 Successfully initialized ESCC
2020-02-21 08:51:14.395 UTC [sccapi] deploySysCC -&gt; INFO 021 system chaincode escc/(github.com/hyperledger/fabric/core/scc/escc) deployed
2020-02-21 08:51:14.395 UTC [sccapi] deploySysCC -&gt; INFO 022 system chaincode vscc/(github.com/hyperledger/fabric/core/scc/vscc) deployed
2020-02-21 08:51:14.396 UTC [qscc] Init -&gt; INFO 023 Init QSCC
2020-02-21 08:51:14.396 UTC [sccapi] deploySysCC -&gt; INFO 024 system chaincode qscc/(github.com/hyperledger/fabric/core/chaincode/qscc) deployed
2020-02-21 08:51:14.396 UTC [nodeCmd] initSysCCs -&gt; INFO 025 Deployed system chaincodes
2020-02-21 08:51:14.397 UTC [nodeCmd] serve -&gt; INFO 026 Starting peer with ID=[name:"peer0.org1.example.com" ], network ID=[dev], address=[peer0.org1.example.com:7051]
2020-02-21 08:51:14.398 UTC [nodeCmd] serve -&gt; INFO 027 Started peer with ID=[name:"peer0.org1.example.com" ], network ID=[dev], address=[peer0.org1.example.com:7051]
2020-02-21 08:51:24.451 UTC [ledgermgmt] CreateLedger -&gt; INFO 028 Creating ledger [mychannel] with genesis block
2020-02-21 08:51:24.488 UTC [fsblkstorage] newBlockfileMgr -&gt; INFO 029 Getting block information from block storage
2020-02-21 08:51:25.005 UTC [couchdb] CreateDatabaseIfNotExist -&gt; INFO 02a Created state database mychannel_
2020-02-21 08:51:25.145 UTC [kvledger] CommitWithPvtData -&gt; INFO 02b Channel [mychannel]: Committed block [0] with 1 transaction(s)
2020-02-21 08:51:25.151 UTC [couchdb] CreateCouchDatabase -&gt; ERRO 02c Error during CouchDB CreateDatabaseIfNotExist() for dbName: mychannel_  error: json: cannot unmarshal string into Go struct field DBInfo.purge_seq of type int
panic: Error during commit to txmgr:json: cannot unmarshal string into Go struct field DBInfo.purge_seq of type int

goroutine 87 [running]:
github.com/hyperledger/fabric/core/ledger/kvledger.(*kvLedger).CommitWithPvtData(0xc420058180, 0xc4215a7200, 0x0, 0x0)
    /opt/gopath/src/github.com/hyperledger/fabric/core/ledger/kvledger/kv_ledger.go:251 +0x921
github.com/hyperledger/fabric/core/ledger/kvledger.(*Provider).Create(0xc4201aa200, 0xc4216da360, 0x27, 0xc421708250, 0x1, 0x1)
    /opt/gopath/src/github.com/hyperledger/fabric/core/ledger/kvledger/kv_ledger_provider.go:107 +0x37f
github.com/hyperledger/fabric/core/ledger/ledgermgmt.CreateLedger(0xc4216da360, 0x0, 0x0, 0x0, 0x0)
    /opt/gopath/src/github.com/hyperledger/fabric/core/ledger/ledgermgmt/ledger_mgmt.go:88 +0x1ac
github.com/hyperledger/fabric/core/peer.CreateChainFromBlock(0xc4216da360, 0x40000000000, 0x10)
    /opt/gopath/src/github.com/hyperledger/fabric/core/peer/peer.go:433 +0x64
github.com/hyperledger/fabric/core/scc/cscc.joinChain(0xc42165d360, 0x9, 0xc4216da360, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0)
    /opt/gopath/src/github.com/hyperledger/fabric/core/scc/cscc/configure.go:212 +0x65
github.com/hyperledger/fabric/core/scc/cscc.(*PeerConfiger).Invoke(0x169e160, 0x166f740, 0xc42032d220, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0)
    /opt/gopath/src/github.com/hyperledger/fabric/core/scc/cscc/configure.go:140 +0xa1e
github.com/hyperledger/fabric/core/chaincode/shim.(*Handler).handleTransaction.func1(0xc4202419d0, 0xc4216bed80)
    /opt/gopath/src/github.com/hyperledger/fabric/core/chaincode/shim/handler.go:329 +0x4f3
created by github.com/hyperledger/fabric/core/chaincode/shim.(*Handler).handleTransaction
    /opt/gopath/src/github.com/hyperledger/fabric/core/chaincode/shim/handler.go:295 +0x49
</code></pre>

## Answers
### Answer ID: 60337321
<p>I solved the above issues, by editing the file <strong><em>start.sh</em></strong> from the path <strong>fabric-samples/basic-network</strong> with the below,</p>

<pre><code># wait for Hyperledger Fabric to start
# incase of errors when running later commands, issue export FABRIC_START_TIMEOUT=&lt;larger number&gt;
#FABRIC_START_TIMEOUT changed to 90 instead of 10
export FABRIC_START_TIMEOUT=90  #default=10
#echo ${FABRIC_START_TIMEOUT}
sleep ${FABRIC_START_TIMEOUT}
</code></pre>

<p>along with that I followed the <a href="https://stackoverflow.com/questions/45856564/error-starting-hyperledger-fabcar-sample-application/45916717">answer</a>,
I included </p>

<blockquote>
  <p>dns_search: .</p>
</blockquote>

<p>to the peer containers in the <strong>docker-compose.yml</strong> file located in <strong>fabric-samples/basic-network</strong> with the below.</p>

<pre><code>peer0.org1.example.com:
    container_name: peer0.org1.example.com
    image: hyperledger/fabric-peer
    dns_search: .
    environment:
      - CORE_VM_ENDPOINT=unix:///host/var/run/docker.sock
      - CORE_PEER_ID=peer0.org1.example.com
      - CORE_LOGGING_PEER=debug
      - CORE_CHAINCODE_LOGGING_LEVEL=DEBUG
      - CORE_PEER_LOCALMSPID=Org1MSP
      - CORE_PEER_MSPCONFIGPATH=/etc/hyperledger/msp/peer/
      - CORE_PEER_ADDRESS=peer0.org1.example.com:7051
      # # the following setting starts chaincode containers on the same
      # # bridge network as the peers
      # # https://docs.docker.com/compose/networking/
      - CORE_VM_DOCKER_HOSTCONFIG_NETWORKMODE=${COMPOSE_PROJECT_NAME}_basic
      - CORE_LEDGER_STATE_STATEDATABASE=CouchDB
      - CORE_LEDGER_STATE_COUCHDBCONFIG_COUCHDBADDRESS=couchdb:5984
      # The CORE_LEDGER_STATE_COUCHDBCONFIG_USERNAME and CORE_LEDGER_STATE_COUCHDBCONFIG_PASSWORD
      # provide the credentials for ledger to connect to CouchDB.  The username and password must
      # match the username and password set for the associated CouchDB.
      - CORE_LEDGER_STATE_COUCHDBCONFIG_USERNAME=
      - CORE_LEDGER_STATE_COUCHDBCONFIG_PASSWORD=
    working_dir: /opt/gopath/src/github.com/hyperledger/fabric
    command: peer node start
    # command: peer node start --peer-chaincodedev=true
    ports:
      - 7051:7051
      - 7053:7053
    volumes:
        - /var/run/:/host/var/run/
        - ./crypto-config/peerOrganizations/org1.example.com/peers/peer0.org1.example.com/msp:/etc/hyperledger/msp/peer
        - ./crypto-config/peerOrganizations/org1.example.com/users:/etc/hyperledger/msp/users
        - ./config:/etc/hyperledger/configtx
    depends_on:
      - orderer.example.com
      - couchdb  # ***i included couchdb***
    networks:
      - basic
</code></pre>

<p>The above edits resolved my issues, and now <strong>./startFabric.sh</strong> and <strong>node query.js</strong> were working properly.</p>

<pre><code>~/fabric-samples/fabcar$ node query.js 
Store path:/home/inforios/fabric-samples/fabcar/hfc-key-store
Successfully loaded user1 from persistence
Query has completed, checking results
Response is  [{"Key":"CAR0", "Record":{"colour":"blue","make":"Toyota","model":"Prius","owner":"Tomoko"}},{"Key":"CAR1", "Record":{"colour":"red","make":"Ford","model":"Mustang","owner":"Brad"}},{"Key":"CAR2", "Record":{"colour":"green","make":"Hyundai","model":"Tucson","owner":"Jin Soo"}},{"Key":"CAR3", "Record":{"colour":"yellow","make":"Volkswagen","model":"Passat","owner":"Max"}},{"Key":"CAR4", "Record":{"colour":"black","make":"Tesla","model":"S","owner":"Adriana"}},{"Key":"CAR5", "Record":{"colour":"purple","make":"Peugeot","model":"205","owner":"Michel"}},{"Key":"CAR6", "Record":{"colour":"white","make":"Chery","model":"S22L","owner":"Aarav"}},{"Key":"CAR7", "Record":{"colour":"violet","make":"Fiat","model":"Punto","owner":"Pari"}},{"Key":"CAR8", "Record":{"colour":"indigo","make":"Tata","model":"Nano","owner":"Valeria"}},{"Key":"CAR9", "Record":{"colour":"brown","make":"Holden","model":"Barina","owner":"Shotaro"}}]

</code></pre>

<p>thanks to Faisal and Aditya Arora for their valuable responses.</p>

