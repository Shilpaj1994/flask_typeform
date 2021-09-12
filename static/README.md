# Simple Flask Application

[toc]

### [Application Link](http://simpleflaskapp-env.eba-j4mmrasx.us-east-2.elasticbeanstalk.com/)



---



## Notes

By creating this simple flask application, I learnt following things:

- How to code the web pages using HTML
- How to link them with Python logic
- How to deploy them on AWS



### Creating Web Pages using HTML

- A `base.html` is used to have a common Header, Footer and Navbar for all the webpages

- In the `Head` tag of the file, we can include the background, font information by referencing the `style.css` file

  ```html
  <link href="{{ url_for('static', filename='css/style.css')}}" rel="stylesheet">
  ```

- Title for the website can also be mentioned in the `Head` tag to have same name across all the pages

- In the `Body` tag, we can include the Navbar, header and footer information which is common for all the pages

- The code lines in the `base.html`

  ```html
  {% block content %}
  {% endblock %}
  ```

  ensures that the code above `{% block content %}` and the code below `{% endblock %}` is common for all the web pages

- Link referencing should be done using `"{{ url_for('about') }}"` to keep the modularity of the website

- For all the other pages, following template is used to include the home page configurations

  ```html
  {% extends 'base.html' %}
  
  {% block content %}
  	<!-- Page Content Goes Here -->
  {% endblock %}
  ```

- [Jinja](https://jinja.palletsprojects.com/en/3.0.x/) is used to include the logical part in the HTML files

- [Bootstrap](https://getbootstrap.com/) is used to refer to all the templates for website components

- Data can be passed between the Python code and HTML code

- Use `{{ variable_name }}` to access the Python objects in HTML file





### Python Logic File

- In the Python file, we have to use `from flask import Flask, render_template, request` to interact with HTML pages and render them
- `application = Flask(__name__)` is used to create instance of the application
- `@application.route('')` decorator is used to assign address to the webpage
- The `methods=['POST']` argument is passed to the decorators to ensure page can only be called after the link from the previous page
- Function name is usually defined as page name
- `render_template()` is used to send the data from Python to HTML
- Objects to be passed to HTML pages are included as keyword arguments in the `render_template()`
- `request.form.get("first_name")` is used to read the data from HTML to Python
- `$ export FLASK_ENV=development` is used in the terminal to set development environment 
- `$ export FLASK_APP=application.py` is used to tell the server which file contains the application
- `$ flask run` or `$ python -m flask run` is used to run the application server





### Deploy Application on AWS

Application can be deployed to AWS by following steps in the below video

<iframe width="1350" height="527" src="https://www.youtube.com/embed/dhHOzye-Rms" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>

