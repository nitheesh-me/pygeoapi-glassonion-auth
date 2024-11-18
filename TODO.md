sign-in methods:

Username and Password: Traditional email and password authentication.
Single Sign-On (SSO): Integration with SSO providers like Okta, OneLogin, and Auth0.
Social Authentication: Sign in with Google, GitHub, and other social accounts.
SAML 2.0: Security Assertion Markup Language for enterprise-level authentication.
LDAP: Lightweight Directory Access Protocol for directory-based authentication.
SSPI: Security Support Provider Interface for Windows-based authentication.

Auth:
- API keys : Used for programmatic access to the platform.
- Token Based Authentication: Secure token-based authentication for APIs. (user specific)
- OAuth: Authorization framework for third-party applications.
- JWT: JSON Web Tokens for stateless authentication.
- Two-Factor Authentication: Two-factor authentication for an additional layer of security.

New:
- Service Accounts: Service accounts for machine-to-machine communication.
- Biometric Authentication: Fingerprint, face, and voice recognition for mobile apps.
- Smart Cards: Physical smart cards for secure authentication.
- Kerberos: Network authentication protocol for secure communication.
- Passwordless Authentication: Authentication without a password using email or SMS. (Magic links)
- Captcha: Automated Turing test to prevent spam and abuse.
- WebAuthn: Web Authentication API for secure public key authentication.
- U2F: Universal 2nd Factor for hardware-based two-factor authentication.

- Role-Based Access Control (RBAC): Access control based on user roles and permissions.
- Attribute-Based Access Control: Access control based on user attributes and policies.

- Security Headers: HTTP headers for security policies like Content Security Policy (CSP) and HTTP Strict Transport Security (HSTS).
- Content Security Policy (CSP): Security policy to prevent cross-site scripting (XSS) and other code injection attacks.
- HTTP Strict Transport Security (HSTS): Security policy to enforce HTTPS connections.
- Cross-Origin Resource Sharing (CORS): Security policy to allow or restrict cross-origin requests.
- Subresource Integrity (SRI): Security feature to validate external resources like scripts and stylesheets.

How to add auth to a service that doesn't have auth?


```
To use in django one can consider the following to get all above mentioned features:
- Django Rest Framework
- Django Allauth
- Django OAuth Toolkit
- Django Simple JWT
- Django Two Factor Authentication