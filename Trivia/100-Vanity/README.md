T100 - Vanity
===============

What's the vanity name of the vulnerability for which the fix includes the following diff:

```
 +      p=value;
 +      q=value+strlen(value);
 +      for (p+=strspn(p,whitelist); p != q; p+=strspn(p,whitelist))
 +        *p=\'_\';
 +      break;
 ```


--
**Pixels Camp 2016**
