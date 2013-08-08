### SSL configuration instructions

* For pdfprocess-test
    * cd /etc/nginx/ssl/; mv server-test.crt server.crt
* Edit /etc/nginx/sites-enabled/default
    * Uncomment the last server section
    * Change the root
        * root /usr/share/nginx/www;
    * Set SSL options
        * ssl_certificate /etc/nginx/ssl/server.crt;
        * ssl_certificate_key /etc/nginx/ssl/server.key;
        * ssl_verify_depth 3;

### etc/nginx/README.md
