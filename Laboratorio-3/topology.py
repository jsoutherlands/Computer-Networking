#Ejecucion: sudo mn --custom topologia1.py --topo MyTopo --controller remote --switch ovsk --mac
from mininet.topo import Topo
#from mininet.node import RemoteController
#from mininet.net import Mininet


class AnilloSimple(Topo):

    "Topologia numero 1"

    def __init__(self):
        "Creacion de topologia personalizada"
        Topo.__init__(self)
        #net = Mininet(controller = RemoteController)
        #net.addController('c0')
        #Hosts y switches
        
        # Añade 10 hosts
        h01 = self.addHost( 'h1', mac = '00:00:00:00:00:01')
        h02 = self.addHost( 'h2', mac = '00:00:00:00:00:02')
        h03 = self.addHost( 'h3', mac = '00:00:00:00:00:03')
        h04 = self.addHost( 'h4', mac = '00:00:00:00:00:04')
        h05 = self.addHost( 'h5', mac = '00:00:00:00:00:05')
        h06 = self.addHost( 'h6', mac = '00:00:00:00:00:06')
        h07 = self.addHost( 'h7', mac = '00:00:00:00:00:07')
        h08 = self.addHost( 'h8', mac = '00:00:00:00:00:08')
        h09 = self.addHost( 'h9', mac = '00:00:00:00:00:09')
        h0a = self.addHost( 'h10', mac = '00:00:00:00:00:0A')

        # Añade X hosts
        s1 = self.addSwitch( 's1', dpid = '1')
        s2 = self.addSwitch( 's2', dpid = '2')
        s3 = self.addSwitch( 's3', dpid = '3')
        s4 = self.addSwitch( 's4', dpid = '4')
        s5 = self.addSwitch( 's5', dpid = '5')

        # Anade links 
        self.addLink( h01, s1, 0, 1 )
        self.addLink( h02, s1, 0, 2 )
        
        self.addLink( h03, s2, 0, 3 )
        self.addLink( h04, s2, 0, 4 )
        
        self.addLink( h05, s3, 0, 5 )
        self.addLink( h06, s3, 0, 6 )
        
        self.addLink( h07, s4, 0, 7 )
        self.addLink( h08, s4, 0, 8 )

        self.addLink( h09, s5, 0, 9 )
        self.addLink( h0a, s5, 0, 10 )

        self.addLink( s1, s2, 11, 12 )
        self.addLink( s2, s3, 13, 14 )
        self.addLink( s3, s5, 15, 16 )
        self.addLink( s5, s4, 17, 18 )
        self.addLink( s4, s1, 19, 20 )

class DosCaminos(Topo):
     def __init__(self):
        "Creacion de topologia personalizada"
        Topo.__init__(self)

        h1 = self.addHost( 'h1', mac = '00:00:00:00:00:01')
        h2 = self.addHost( 'h2', mac = '00:00:00:00:00:02')
        h3 = self.addHost( 'h3', mac = '00:00:00:00:00:03')
        h4 = self.addHost( 'h4', mac = '00:00:00:00:00:04')
        h5 = self.addHost( 'h5', mac = '00:00:00:00:00:05')
        h6 = self.addHost( 'h6', mac = '00:00:00:00:00:06')
        
        servh7 = self.addHost( 'h7', mac = '00:00:00:00:00:07')
        servh8 = self.addHost( 'h8', mac = '00:00:00:00:00:08')

        s1 = self.addSwitch( 's1', dpid = '1')
        s2 = self.addSwitch( 's2', dpid = '2')
        s3 = self.addSwitch( 's3', dpid = '3')
        s4 = self.addSwitch( 's4', dpid = '4')
        s5 = self.addSwitch( 's5', dpid = '5')

        #Anadir links 
        self.addLink( h1, s1, 0, 1)
        self.addLink( h2, s1, 0, 2)


        
        self.addLink( h3, s2, 0, 3)
        self.addLink( h4, s2, 0, 4)

        
        self.addLink( h5, s3, 0, 5)
        self.addLink( h6, s3, 0, 6)

        
        self.addLink( servh7, s5, 22, 21)
        self.addLink( servh8, s5, 20, 19)

        self.addLink( s1, s2, 7, 8)
        self.addLink( s2, s3, 9, 10)
        self.addLink( s3, s4, 11, 12)
        self.addLink( s4, s5, 13, 14)
        self.addLink( s4, s1, 15, 16)
        self.addLink( s5, s1, 17, 18)
    
topos = {'AnilloSimple': (lambda: AnilloSimple()), 'DosCaminos': (lambda: DosCaminos())}