# tts-convert
A simple text-to-speech request API with Django/DRF, that allows users to create, get, and delete conversion requests. The endpoint is authenticated with DRF's TokenAuthentication, and users are only able to access their own requests. Data validation is implemented with DRF serializers.

### Assumptions:
 - The implemented ConversionRequest model is very bare-bones, but still contains the basic fields needed to track the request. With more exact specification, the model is easy to extend to whatever is needed out of it.
 - Given the implemented fields, only the `text_to_convert`-field needs to be specified by the user (after the patch-endpoint is implemented, that is)
 - `results` (output) type was not specified. TextField gives the freedom to include e.g. a download link or id there.
 - The specification sounds like the ConversionRequest could be run as a background task and later on the results could be fetched, but being able to modify the request doesn't really fit that...

### How to run:
Currently there are no users, and thus no easy way to acquire api tokens. However, the tests should give an overview that the api endpoint is authenticated, and that the users can only access their own requests.

* requirements (built with): python 3.7, Django 3.2.25, djangorestframework 3.15.1
* clone the repo, cd to app/, run  `python manage.py test` to run the tests

### Other implementation notes

* the Django way of doing things doesn't give much leeway here (think views/models/serializers etc.)
* naming things is th hardest thing in programming - current naming is just the first iteration
* the user input given to the ConversionRequest is not sanitized at all
* access control could be a bit prettier and be based on for example a company that a user is associated with, so all users from one company could see each others requests
* the ConversionRequest id that is exposed should be uuid or similar, instead of exposing sequential db ids
* decided to go with TokenAuthentication, because that fits the already mentioned "background task" feel.


