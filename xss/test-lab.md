
---

## Description

Stealing cookies is a classic way to exploit XSS. Most web applications use cookies for session handling, so an XSS vulnerability can be used to exfiltrate a victim's cookies to an attacker-controlled destination, then replay them to impersonate the victim.

In practice this technique has some notable limitations:

> - The victim might not be logged in.
> - Many applications hide their cookies from JavaScript using the `HttpOnly` flag.
> - Sessions might be locked to additional factors like the user's IP address.
> - The session might time out before the attacker can hijack it.

This lab is deliberately configured *without* the `HttpOnly` flag, so `document.cookie` is readable from injected JavaScript — which is what makes this attack path work.

---

## Where It Lived

The **comment field** on blog posts. User input (name, email, website, comment) is stored and rendered back on the page with no sanitization or output encoding, allowing arbitrary HTML/JS to execute in the context of anyone who views the post.
