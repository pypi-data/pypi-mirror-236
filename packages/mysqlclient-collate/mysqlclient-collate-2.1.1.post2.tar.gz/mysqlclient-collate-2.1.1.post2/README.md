# mysqlclient-collate

**NOTE:** These features have been merged upstream into mysqlclient 2.2.0. This package is now archived. Please switch to `mysqlclient>=2.2` instead.

---

Fork of [mysqlclient](https://github.com/PyMySQL/mysqlclient) which adds support for setting collation via connection options.

Setting collation is necessary for servers that do not use the default, and for Django queries using `CAST` statements, which are prevalent in Wagtail 4. For more background, see the following discussions:

* [mysqlclient bug report](https://github.com/PyMySQL/mysqlclient/pull/564)
* [Wagtail bug report](https://github.com/wagtail/wagtail/issues/9477)

## Usage

Make sure you have MySQL or MariaDB C connector, and a C compiler installed.

**IMPORTANT**: If you already have `mysqlclient` installed, uninstall it before installing this fork. Both projects use the same module name and cannot be installed at the same time.

```
pip uninstall mysqlclient
pip install mysqlclient-collate
```

For use in a Django project, set your database connection as so:

```python
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.mysql",
        "HOST": "",
        "NAME": "",
        "USER": "",
        "PASSWORD": "",
        "OPTIONS": {
            "charset": "utf8mb4",
            "collation": "utf8mb4_unicode_ci",
        },
    }
}
```
