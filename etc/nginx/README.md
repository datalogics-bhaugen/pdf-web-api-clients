### nginx instructions

As root:

* Edit /etc/nginx/sites-enabled/default
    * Uncomment the last server section
    * Change the root
        * root /usr/share/nginx/www;
    * Set SSL options
        * ssl_certificate /etc/nginx/ssl/server.crt;
            * server-test.crt for _pdfprocess-test_
        * ssl_certificate_key /etc/nginx/ssl/server.key;
        * ssl_verify_depth 3;
* /etc/init.d/nginx start
    * /etc/init.d/nginx testconfig

### etc/nginx/README.md
