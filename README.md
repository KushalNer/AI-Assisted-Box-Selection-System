<h1>AI-Assisted Box Selection System</h1><br>
<h2>Project Overview</h2><br>
<p>We operate an ecommerce platform. When a customer places an order, the warehouse team
needs to know which shipping box should be used. Each product has dimensions and
weight. Each box has internal dimensions, maximum weight capacity, and cost.
</p><br>

<h2>Problem Statment</h2><br>
<p>task is to design and build a small Django-based system that recommends the most
suitable box for an order.</p><br>
<h2>Tech Stack</h2><br>
<p>python<br>Django<br>Django REST Framework<br>SQLlite<br>git<br>Postman</p>

<h2>Project Setup</h2><br>
<p>Clone Repo</p><br>
git clone https://github.com/KushalNer/AI-Assisted-Box-Selection-System.git

<p>Create Virtual Environment</p>
python -m venv venv
source venv/Scripts/activate

<p>Intsall Packages</p>
pip install -r reuirement.txt

<p>Apply Migrations</p>
python manage.py makemigrations
python manage.py migrate 

<p>Run Test</p>
# Run all tests
python manage.py test
# Run service tests
python manage.py test box_selector.test_services
# Run API tests
python manage.py test box_selector.test_api

<p>Start Django Server</p>
python manage.py runserver


<h2>API Documentation</h2>
<h3>Base URL</h3>
<p>http://127.0.0.1:8000/api/</p>

<h3>Product API</h3>
<h4>Create Product:</h4>
<p>method = POST /api/product/</p>
<p>Request Body
{
    "name": "Laptop",
    "length": 30,
    "width": 20,
    "height": 5,
    "weight": "2.00"
}
</p>
<h4>List Product:</h4>
<p>method = GET /api/product/</p>

<h4>Retrive Product:</h4>
<p>method = GET /api/product/{id}/</p>

<h4>Update Product:</h4>
<p>method = PUT /api/product/{id}</p>

<h4>Delete Product</h4>
<p>method = DELETE /api/product/{id}</p>


<h3>Box API</h3>
<h4>Create Box:</h4>
<p>method = POST /api/box/</p>
<p>Request Body
{
    "name": "Small Box",
    "internal_length": 20,
    "internal_width": 15,
    "internal_height": 10,
    "max_weight": "5.00",
    "cost": "20.00"
}
</p>
<h4>List Box:</h4>
<p>method = GET /api/box/</p>

<h4>Retrive Box:</h4>
<p>method = GET /api/box/{id}/</p>

<h4>Update Box:</h4>
<p>method = PUT /api/box/{id}</p>

<h4>Delete Box</h4>
<p>method = DELETE /api/box/{id}</p>

<h3>Box Recommendation API</h3>
<h4>Recommend Box</h4>
<p>Request Body:
{
    "product_ids": [1, 2]
}
</p>