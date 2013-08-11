### nginx instructions

As root:

* Edit /etc/nginx/sites-enabled/default
    * Uncomment the last server section
    * Change the root
        * root /usr/share/nginx/www;
    * Set SSL options
        * ssl_certificate /etc/nginx/ssl/server-test.crt;
        * ssl_certificate_key /etc/nginx/ssl/server.key;
        * ssl_verify_depth 3;
* For _pdfprocess_, edit /etc/nginx/sites-enabled/*
    * Remove -test from ssl_certificate and server_name entries
* /etc/init.d/nginx start
    * /etc/init.d/nginx testconfig

### etc/nginx/README.md
