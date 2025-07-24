# Error while extending the Hyperledger fabric fabcar example with additional peers
[Link to question](https://stackoverflow.com/questions/51872871/error-while-extending-the-hyperledger-fabric-fabcar-example-with-additional-peer)
**Creation Date:** 1534408508
**Score:** 0
**Tags:** docker, docker-compose, hyperledger-fabric, hyperledger, ibm-blockchain
## Question Body
<p>this is my first post, so I will try to be as detailed as possible and show the steps to reproduce those errors. I want to extend the given Fabcar example with additional peers but I am not able to query/invoke the extended system. If I try to query the System I get the following Error: </p>

<pre>Query has completed, checking results
error from query =  Error: make sure the chaincode fabcar has been successfully instantiated and try again: getccdata mychannel/fabcar responded with error: could not find chaincode with name &apos;fabcar&apos;
    at /home/hyperledger/Dokumente/Hyperledger_test/Fabric-SamplesV4/fabric-samples/fabcar/node_modules/fabric-client/lib/Channel.js:2638:24
    at &lt;anonymous&gt;
</pre>

<p>If I run the docker ps -a command it shows this:</p>

<pre>CONTAINER ID        IMAGE                        COMMAND                  CREATED             STATUS              PORTS                                            NAMES
7eabee4c4eb2        hyperledger/fabric-peer      &quot;peer node start&quot;        39 minutes ago      Up 38 minutes       0.0.0.0:8151-&gt;7051/tcp, 0.0.0.0:8153-&gt;7053/tcp   peer1.org1.example.com
4aaf1b4c063b        hyperledger/fabric-couchdb   &quot;tini -- /docker-ent…&quot;   39 minutes ago      Up 39 minutes       4369/tcp, 9100/tcp, 0.0.0.0:9984-&gt;5984/tcp       couchdb1
831facf5abad        hyperledger/fabric-peer      &quot;peer node start&quot;        39 minutes ago      Up 39 minutes       0.0.0.0:7051-&gt;7051/tcp, 0.0.0.0:7053-&gt;7053/tcp   peer0.org1.example.com
1a9cd9b9f3fb        hyperledger/fabric-orderer   &quot;orderer&quot;                39 minutes ago      Up 39 minutes       0.0.0.0:7050-&gt;7050/tcp                           orderer.example.com
e33bfb4374eb        hyperledger/fabric-couchdb   &quot;tini -- /docker-ent…&quot;   39 minutes ago      Up 39 minutes       4369/tcp, 9100/tcp, 0.0.0.0:5984-&gt;5984/tcp       couchdb
2cfb85e6aa9e        hyperledger/fabric-ca        &quot;sh -c &apos;fabric-ca-se…&quot;   39 minutes ago      Up 39 minutes       0.0.0.0:7054-&gt;7054/tcp                           ca.example.com
</pre>

<p>As you can see, the devpeer is missing, this peer shows up if you build the original Fabcar example.</p>

<p>If I run the docker logs command for peer0 it shows this:</p>

<pre>2018-08-16 07:21:29.804 UTC [ledgermgmt] CreateLedger -&gt; INFO 023 Creating ledger [mychannel] with genesis block
2018-08-16 07:21:29.838 UTC [fsblkstorage] newBlockfileMgr -&gt; INFO 024 Getting block information from block storage
2018-08-16 07:21:30.246 UTC [couchdb] CreateDatabaseIfNotExist -&gt; INFO 025 Created state database mychannel_
2018-08-16 07:21:30.421 UTC [kvledger] CommitWithPvtData -&gt; INFO 026 Channel [mychannel]: Committed block [0] with 1 transaction(s)
2018-08-16 07:21:30.422 UTC [pvtdatastorage] func1 -&gt; INFO 027 Purger started: Purging expired private data till block number [0]
2018-08-16 07:21:30.422 UTC [pvtdatastorage] func1 -&gt; INFO 028 Purger finished
2018-08-16 07:21:30.577 UTC [ledgermgmt] CreateLedger -&gt; INFO 029 Created ledger [mychannel] with genesis block
2018-08-16 07:21:30.726 UTC [cscc] Init -&gt; INFO 02a Init CSCC
2018-08-16 07:21:30.726 UTC [sccapi] deploySysCC -&gt; INFO 02b system chaincode cscc/mychannel(github.com/hyperledger/fabric/core/scc/cscc) deployed
2018-08-16 07:21:30.726 UTC [sccapi] deploySysCC -&gt; INFO 02c system chaincode lscc/mychannel(github.com/hyperledger/fabric/core/scc/lscc) deployed
2018-08-16 07:21:30.727 UTC [qscc] Init -&gt; INFO 02d Init QSCC
2018-08-16 07:21:30.727 UTC [sccapi] deploySysCC -&gt; INFO 02e system chaincode qscc/mychannel(github.com/hyperledger/fabric/core/scc/qscc) deployed
2018-08-16 07:21:36.730 UTC [gossip/election] beLeader -&gt; INFO 02f [60 150 184 106 152 137 128 154 149 235 201 184 164 27 185 56 26 64 112 155 28 70 77 95 96 101 28 51 209 225 187 117] : Becoming a leader
2018-08-16 07:22:57.514 UTC [couchdb] CreateDatabaseIfNotExist -&gt; INFO 030 Created state database mychannel_lscc
2018-08-16 07:22:57.519 UTC [lscc] Invoke -&gt; ERRO 031 error getting chaincode fabcar on channel [mychannel]: could not find chaincode with name &apos;fabcar&apos;
</pre>

<p>My Steps to reproduce this outcome:</p>

<p>Made changes in the basic-network folder:</p>

<ol>
<li><p>Crypto-config.yaml - changed the Template Count value to 2</p></li>
<li><p>Docker-compose.yml - duplicated peer0 and couchdb and changed ports/names</p></li>
</ol>

<pre> peer1.org1.example.com:
    container_name: peer1.org1.example.com
    image: hyperledger/fabric-peer
    environment:
      - CORE_VM_ENDPOINT=unix:///host/var/run/docker.sock
      - CORE_PEER_ID=peer1.org1.example.com
      - CORE_LOGGING_PEER=info
      - CORE_CHAINCODE_LOGGING_LEVEL=info
      - CORE_PEER_LOCALMSPID=Org1MSP
      - CORE_PEER_MSPCONFIGPATH=/etc/hyperledger/msp/peer/
      - CORE_PEER_ADDRESS=peer1.org1.example.com:7051
      # # the following setting starts chaincode containers on the same
      # # bridge network as the peers
      # # https://docs.docker.com/compose/networking/
      - CORE_VM_DOCKER_HOSTCONFIG_NETWORKMODE=${COMPOSE_PROJECT_NAME}_basic
      # - CORE_PEER_TLS_ENABLED=true
      - CORE_PEER_GOSSIP_USELEADERELECTION=true
      - CORE_PEER_GOSSIP_ORGLEADER=false
      - CORE_PEER_PROFILE_ENABLED=true
      # - CORE_PEER_TLS_CERT_FILE=/etc/hyperledger/fabric/tls/server.crt
      # - CORE_PEER_TLS_KEY_FILE=/etc/hyperledger/fabric/tls/server.key
      # - CORE_PEER_TLS_ROOTCERT_FILE=/etc/hyperledger/fabric/tls/ca.crt
      - CORE_PEER_GOSSIP_EXTERNALENDPOINT=peer1.org1.example.com:7051
      - CORE_PEER_GOSSIP_BOOTSTRAP=peer0.org1.example.com:7051
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
      - 8151:7051
      - 8153:7053
    volumes:
        - /var/run/:/host/var/run/
        - ./crypto-config/peerOrganizations/org1.example.com/peers/peer1.org1.example.com/msp:/etc/hyperledger/msp/peer
        - ./crypto-config/peerOrganizations/org1.example.com/users:/etc/hyperledger/msp/users
        - ./config:/etc/hyperledger/configtx
    depends_on:
      - orderer.example.com
      - couchdb1
    networks:
      - basic

  couchdb1:
    container_name: couchdb1
    image: hyperledger/fabric-couchdb
    # Populate the COUCHDB_USER and COUCHDB_PASSWORD to set an admin user and password
    # for CouchDB.  This will prevent CouchDB from operating in an "Admin Party" mode.
    environment:
      - COUCHDB_USER=
      - COUCHDB_PASSWORD=
    ports:
      - 9984:5984
    networks:
      - basic
</pre>

<ol start="3">
<li><p>Run the generate.sh file to create the needed crypto material</p></li>
<li><p>Extend the start.sh file to create the new peer in the whole system</p></li>
</ol>

<pre>

    # don't rewrite paths for Windows Git Bash users
    export MSYS_NO_PATHCONV=1

    docker-compose -f docker-compose.yml down

    docker-compose -f docker-compose.yml up -d ca.example.com orderer.example.com peer0.org1.example.com couchdb

    sleep 0.2

    docker-compose -f docker-compose.yml up -d peer1.org1.example.com couchdb1

    # wait for Hyperledger Fabric to start
    # incase of errors when running later commands, issue export FABRIC_START_TIMEOUT=
    export FABRIC_START_TIMEOUT=10
    #echo ${FABRIC_START_TIMEOUT}
    sleep ${FABRIC_START_TIMEOUT}

    # Create the channel
    docker exec -e "CORE_PEER_LOCALMSPID=Org1MSP" -e "CORE_PEER_MSPCONFIGPATH=/etc/hyperledger/msp/users/Admin@org1.example.com/msp" peer0.org1.example.com peer channel create -o orderer.example.com:7050 -c mychannel -f /etc/hyperledger/configtx/channel.tx
    # Join peer0.org1.example.com to the channel.
    docker exec -e "CORE_PEER_LOCALMSPID=Org1MSP" -e "CORE_PEER_MSPCONFIGPATH=/etc/hyperledger/msp/users/Admin@org1.example.com/msp" peer0.org1.example.com peer channel join -b mychannel.block

    docker exec -e "CORE_PEER_LOCALMSPID=Org1MSP" -e "CORE_PEER_MSPCONFIGPATH=/etc/hyperledger/msp/users/Admin@org1.example.com/msp" peer1.org1.example.com peer channel join -b mychannel.block

</pre>

<ol start="5">
<li><p>Run the start.sh file to bring the system up</p>

<ul>
<li><p>Run docker logs ca.example to get the new ca.example private key and change the old one in the docker-compose.yml file</p></li>
<li><p>Run the start.sh file again, now you should be able to see the new peer in the docker environment</p></li>
<li><p>There is an error with the docker exec command for peer1:</p></li>
</ul></li>
</ol>

<pre>docker exec -e &quot;CORE_PEER_LOCALMSPID=Org1MSP&quot; -e &quot;CORE_PEER_MSPCONFIGPATH=/etc/hyperledger/msp/users/Admin@org1.example.com/msp&quot; peer1.org1.example.com peer channel join -b mychannel.block
2018-08-16 08:06:35.608 UTC [channelCmd] InitCmdFactory -&gt; INFO 001 Endorser and orderer connections initialized
Error: genesis block file not found open mychannel.block: no such file or directory</pre>

<ul>
<li><p>Why is the genesis block for the second peer missing, is it possible that this peer could not access the block?</p>

<ol start="6">
<li><p>Switch into the fabcar folder and run the startFabric.sh file</p></li>
<li><p>Enroll the admin and register the user</p></li>
<li><p>Try to query the new system and you will get the query-error shown above</p></li>
</ol></li>
</ul>

<p>Question: Is there something missing in those steps or why is it not possible to install the chaincode on the peers and run the network properly?</p>

## Answers
### Answer ID: 51874021
<p>mychannel.block is created when you run this command: </p>

<pre><code>    docker exec -e "CORE_PEER_LOCALMSPID=Org1MSP" -e "CORE_PEER_MSPCONFIGPATH=/etc/hyperledger/msp/users/Admin@org1.example.com/msp" peer0.org1.example.com peer channel create -o orderer.example.com:7050 -c mychannel -f /etc/hyperledger/configtx/channel.tx
</code></pre>

<p>mychannel.block is created in peer0.org1.example.com docker container.</p>

<p>When you run this command, it runs from peer1.org1.example.com docker container, so this will not have mychannel.block file , so u have to fetch the file , then run 2nd peer join command.</p>

<pre><code>  docker exec -e "CORE_PEER_LOCALMSPID=Org1MSP" -e "CORE_PEER_MSPCONFIGPATH=/etc/hyperledger/msp/users/Admin@org1.example.com/msp" peer1.org1.example.com peer channel join -b mychannel.block
</code></pre>

<p>fetch command is :</p>

<pre><code> docker exec -e "CORE_PEER_LOCALMSPID=Org1MSP" -e "CORE_PEER_MSPCONFIGPATH=/etc/hyperledger/msp/users/Admin@org1.example.com/msp" peer1.org1.example.com peer channel fetch 0 mychannel.block -o orderer.example.com:7050 -c mychannel
</code></pre>

<p>So add this fetch command before joining 2nd peer(peer1.org1.example.com)</p>

<p>Like this:</p>

<pre><code># Create the channel
    docker exec -e "CORE_PEER_LOCALMSPID=Org1MSP" -e "CORE_PEER_MSPCONFIGPATH=/etc/hyperledger/msp/users/Admin@org1.example.com/msp" peer0.org1.example.com peer channel create -o orderer.example.com:7050 -c mychannel -f /etc/hyperledger/configtx/channel.tx
    # Join peer0.org1.example.com to the channel.
    docker exec -e "CORE_PEER_LOCALMSPID=Org1MSP" -e "CORE_PEER_MSPCONFIGPATH=/etc/hyperledger/msp/users/Admin@org1.example.com/msp" peer0.org1.example.com peer channel join -b mychannel.block

docker exec -e "CORE_PEER_LOCALMSPID=Org1MSP" -e "CORE_PEER_MSPCONFIGPATH=/etc/hyperledger/msp/users/Admin@org1.example.com/msp" peer1.org1.example.com peer channel fetch 0 mychannel.block -o orderer.example.com:7050 -c mychannel
    docker exec -e "CORE_PEER_LOCALMSPID=Org1MSP" -e "CORE_PEER_MSPCONFIGPATH=/etc/hyperledger/msp/users/Admin@org1.example.com/msp" peer1.org1.example.com peer channel join -b mychannel.block
</code></pre>

