Package Documentation
=====================

With this library you can map your dictionaries easily, you just need to
pass it:

1- output: the dictionary you want to receive, the variables you want to
map must go with {}

.. code:: python

        from DictMaper import MapDict
        result = MapDict(
            output={
                "{var_1}": "Hi! {var_2}, welcome to {company_name}"
                "company name":"{company_name}"
            }
            ......
        )

2- context: context is the data from which the information will be
obtained:

.. code:: python

        from DictMaper import MapDict
        result = MapDict(
            output={
                "{var_1}": "Hi! {var_2}, welcome to {company_name}"
                "company name":"{company_name}"
            }
            context={
                "user": {
                  "name":"user name",
                  "email":"test_email@..."
                }
                "company":{
                 "information":{
                    "name":"Company name",
                    "id":"1234"
                    }
                }
           }
        )    

3- vars: vars are the variables you want to map to your output and the
value is where they are located within context:

.. code:: python

        from DictMaper import MapDict
        result = MapDict(
            output={
                "{var_1}": "Hi! {var_2}, welcome to {company_name}",
                "company":"{company_name}"
            }
            context={
                "user": {
                  "name":"user name",
                  "email":"test_email@..."
                },
                "company":{
                 "information":{
                    "name":"Company name",
                    "id":"1234"
                    }
                }
           }
           vars={
             "var_1": "user.email",
             "var_2": "user.name",
             "company_name": "company.information.name"
           }
        )

That's all, process the data making .process() and as a result you will
have:

``python     from DictMaper import MapDict     result = MapDict(...).process()     {         "test_email@...": "Hi! user name, welcome to Company name",         "company":"Company name"     }``
