Solution
========

To solve the problem you need to find out that the site is using JWT tokens to authenticate itself, the header is created on the clientside, and the secret for the JWT is the information stored on localStorage.

Then, you can proceed on two ways:

 1. Just set an known token on localStorage, and go to the homepage.
     
     For example, write in the browser console:
     
     ```javascript
     localStorage.user = "89a572794c0a4e608891f31f3f86f85f";
     ```
     <br>
     
 2. View the code that generates the token on `app-services/user.service.js` function `GenAuthorization` and replicate it on your own.


Flag
----

`flag{Y-ARHq29rhchpFJjyJyr} `

