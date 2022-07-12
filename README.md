# Online SHOP Application
 This is a blog application built with Python(Django), HTML and CSS.

## Installation
- Fork the project to your account then clone it.
- Create a virtual environment with `pipenv shell` then install the project packages with `pipenv sync`
- You can convert a Pipfile and Pipfile.lock into a requirements.txt file using `pipenv lock -r` and install in the virtual environment with `pip install -r requirements.txt`

<!--
NB: 
- The project uses a PotsgreSQL Database.
- The App uses trigram similarity so create the extenstion in your db.
```bash
$ psql <db_name>;
$ CREATE EXTENSION pg_trgm;
```
-->
## Features
- The cart is persisted in the session so that the cart items are maintained during a user's visit.
- The App uses celery to add asynchronous tasks to the application. This helps with making the app run smoothly with tasks being executed with urgency.
- The App uses custom context processor to make the cart available to all the templates.
- The payment method of choice is Braintree. It's used by Uber and Airbnb.
- Admin can generate Invoices as PDF if there are unpaid transactions and print them.
- The shop has coupons which can be applied either when taking order or when checking out.

<!-- ![alt text for screen readers](./static/images/search.png "Search Module"). -->


## Contributing
Pull requests are welcome.

Please make sure to update tests as appropriate.

## License
&copy; [MIT](https://choosealicense.com/licenses/mit/)
