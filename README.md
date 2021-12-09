1. https://developer.paypal.com/ 
create account for me as a developer  - ordinary paypal account
As A result we can go to https://developer.paypal.com/developer/applications    



There already two basic sandbox account, but we need to add a our new test accounts.

2. Create Business  Account  - that will accept payments


login to this account in the: 
https://www.sandbox.paypal.com/ login page


3. Create personal sandbox account - that will send payments


4. Create APP in paypal sandbox account 



IPN: PayPal can send notifications, that business-account got a new payment
for that we need on OUT application define a url, that will be called by paypal after recieved payment

READ the https://developer.paypal.com/docs/checkout/

Links: 
https://developer.paypal.com/docs/checkout/reference/server-integration/setup-sdk/
https://github.com/paypal/Checkout-Python-SDK


https://stackoverflow.com/questions/67656674/paypal-server-side-integration-in-python
https://developer.paypal.com/demo/checkout/#/pattern/server

https://developer.paypal.com/docs/api/orders/v2/
https://developer.paypal.com/docs/checkout/reference/server-integration/setup-sdk/
https://developer.paypal.com/docs/checkout/reference/upgrade-integration/
https://developer.paypal.com/docs/checkout/reference/server-integration/

add to index.html client_id = client_id (from sandbox.app)
installed https://pypi.org/project/django-cors-headers/
