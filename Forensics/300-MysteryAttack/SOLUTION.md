Solution
========

The file contains a list of bytes that represent an TCP/IP packet. This packet represents a Xmas attack (Christmas): flags F, P and U are set.

It can be read with the following command:


```
$ scapy
>>> Ether(('0adc27b619b40af933fabd4908004500002836e300002506fc4bac1e0042341e8223b3348011bd4b0250000000005029040056380000').decode('hex')).show()
###[ Ethernet ]###
  dst= 0a:dc:27:b6:19:b4
  src= 0a:f9:33:fa:bd:49
  type= 0x800
###[ IP ]###
     version= 4L
     ihl= 5L
     tos= 0x0
     len= 40
     id= 14051
     flags=
     frag= 0L
     ttl= 37
     proto= tcp
     chksum= 0xfc4b
     src= 172.30.0.66
     dst= 52.30.130.35
     \options\
###[ TCP ]###
        sport= 45876
        dport= 32785
        seq= 3175809616
        ack= 0
        dataofs= 5L
        reserved= 0L
        flags= FPU
        window= 1024
        chksum= 0x5638
        urgptr= 0
        options= {}
```


Flag
----

`xmas`