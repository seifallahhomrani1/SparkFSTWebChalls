I authored 2 web challenges for Engineers Spark FST event, HackMaze 2.0, which was held yesterday at Université Centrale Tunisie, and they are about the following:

- The first chall, flowers, was about leveraging an LFI to an RCE via php filters.

- The second chall, linktree, was a 2 parts chall:
The first one was a Blind XPATH injection using the contains() function to exfiltrate the admin's password without knowing the password length, nor the chars order.

The second part was about accessing the admin's endpoint by exploiting an SSRF via an OpenRedirection while sending the previously exfiltrated password in the body of a GET request.

Linkedin Post: https://www.linkedin.com/posts/seif-allah-homrani_i-authored-2-web-challenges-for-engineers-activity-7040786657368846336-bPD3?utm_source=share&utm_medium=member_desktop

