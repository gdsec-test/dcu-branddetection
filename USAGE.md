# Usage

## 1. Fetch a JWT from SSO

See [this gist](https://github.secureserver.net/gist/clake1/a5781dd5415504dcbbefae406a212b06) on how to get a JWT using a certificate.  See [this confluence page](https://confluence.godaddy.com/pages/viewpage.action?spaceKey=AUTH&title=Token+Service#TokenService-ClientCertAuthentication) for more documentation on the token service.

## 2. Make calls to the API

### API Domains

* branddetection.int.dev-godaddy.com
* branddetection.int.ote-godaddy.com
* branddetection.int.godaddy.com

### Auth header

Send this header in each request.

```http
Authorization: sso-jwt ...
```

### Endpoints

Each endpoint you make a GET request to.

Note both `Hosting()` and `Registrar()` accept an IP address or domain.  Under the hood registrar translates an IP to a domain typically, and hosting translates a domain into an IP address.  So ideally you pass an IP into `Hosting()` and a domain into `Registrar()`

* `/hosting?domain=x`
  * Response: `{'brand': '', 'hosting_company_name': '', 'hosting_abuse_email': '', ip': ''}`
* `/registrar?domain=x`
  * Response: `{'brand': '', 'registrar_name': '', 'registrar_abuse_email': '', 'domain_create_date': '', 'domain_id': ''}`
