from app import *


# route to get all products
@app.route('/products-detail', methods=['GET'])
def get_products():
    '''Function to get all the products in the database'''
    return jsonify({'Inventory': Inventory.get_all_products()})


# route to get product by Inventory_key
@app.route('/product-detail/<Inventory_key>', methods=['GET'])
def get_product_by_id(Inventory_key):
    return_value = Inventory.get_product(Inventory_key)
    return jsonify(return_value)


# route to add new product
@app.route('/add-products', methods=['POST'])
def add_product():
    '''Function to add new product to our database'''
    request_data = request.get_json()  # getting data from client
    Inventory.add_product(request_data["Calling_Function"], request_data["Manufacture_Date"],
                    request_data["Product_Id"],request_data["Batch_Id"])
    response = Response("Product Details added!", 201, mimetype='application/json')
    return response


# route to update product with PUT method
@app.route('/product/<Inventory_key>', methods=['PUT'])
def update_product(Inventory_key):
    '''Function to edit product data in our database using Inventory_key'''
    request_data = request.get_json()
    Inventory.update_product(Inventory_key, request_data['Calling_Function'], request_data['Manufacture_Date'], request_data['Product_Id'], request_data['Batch_Id'])
    response = Response("Product Details Updated!", status=200, mimetype='application/json')
    return response


# route to delete movie using the DELETE method
@app.route('/movies/<Inventory_key>', methods=['DELETE'])
def remove_product(Inventory_key):
    '''Function to delete product details from our database'''
    Inventory.delete_product(Inventory_key)
    response = Response("Product Data Deleted!", status=200, mimetype='application/json')
    return response


# Generate the QR Code Image from inventory_key and return the image in .svg or .png
@app.route('/unique_qr_code/q=<Inventory_key>', methods=['GET'])
def get_qr_code(Inventory_key):
    return_value = Inventory.get_qr_code(Inventory_key)
    return jsonify(return_value)


#Scanning the Code    
@app.route('/scaning', methods=['POST'])
def scan_qr():
    img  = request.files['image']
    im = cv.imread(img)
    det = cv.QRCodeDetector()
    Inventory_key, points, straight_qrcode =  det.detectAndDecode(im)

    return jsonify({'Inventory_key': Inventory_key})


if __name__ == "__main__":
    app.run(debug=True)