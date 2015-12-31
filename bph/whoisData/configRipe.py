configItem = lambda keyFilePath, requestUrl, resultFilePath:{"keys": keyFilePath, "url": requestUrl, "result" :resultFilePath}

config ={
  "inetnum": configItem("inetnumKeyList", "http://rest.db.ripe.net/ripe/inetnum/", "inetnumResult")
}
