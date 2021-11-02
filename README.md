# An eCommerce Django Rest API
## Built suing Django and Django Rest for the Backend.

### Features
- **Authentication** using Djoser.
- **Authorization** using Custom permissions and groups, also used Django Rest Permissions.
- **Product Management** using custom code.
- **Category Management** using custom code.
- **Invoice Management** using custom code.
- **Order Management** using custom code.
- **Shipment Management** using custom code.


### Missing Features
- Send Email/create notification to Merchants when Product is edited.
- Send Email/create notification to Merchants when Product review is made or edited.
- Implement weight, age restriction, brand name and capacity for the Product model.
- Implement Shipping based on weight, capacity, price range and/or location of the customer.
- Support for Merchants so that merchants can ask Managers to add categories and get general help. This functions as support. 
- The support will display messages from Merchants in a location only access by managers and if lucky randomly assign task to managers.
- Reporting for customers includes generating pdf of past purchases, shipments and orders.
- Reporting for admin includes get number of daily signups, and other data analytics data for business intelligence.
- Merchants management system (ban, suspend, unsuspend and unban Merchants) for violating usage policy.
- Add or remove Merchants and Managers.
- Add a refferral system using links.
- Implement a loyalty points system / first time buying discount.


### Run the project
- Clone this repository and unzip it to a folder.
- cd into the folder.
- create a python environment and activate it using your desired tool.
- To install all packages run `` python -m pip install -r requirements.txt ``.
- To run the server use `` python manage.py runserver ``

