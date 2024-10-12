from pysnmp.entity import engine, config
from pysnmp.carrier.asyncore.dgram import udp
from pysnmp.entity.rfc3413 import ntfrcv

def trap_receiver(snmpEngine, stateReference, contextEngineId, contextName, varBinds, cbCtx):
    print("Received Trap message:")
    for name, val in varBinds:
        print(f"{name.prettyPrint()} = {val.prettyPrint()}")

snmpEngine = engine.SnmpEngine()
config.addTransport(
    snmpEngine, udp.domainName + (1,), udp.UdpTransport().openServerMode(("0.0.0.0", 162))
)
config.addV1System(snmpEngine, "my-area", "public")
ntfrcv.NotificationReceiver(snmpEngine, trap_receiver)

snmpEngine.transportDispatcher.jobStarted(1)
try:
    snmpEngine.transportDispatcher.runDispatcher()
except:
    snmpEngine.transportDispatcher.closeDispatcher()
    raise
