from flask import Flask, request, jsonify, make_response, render_template
from flask_mysqldb import MySQL
from flask_cors import CORS, cross_origin
from sqlalchemy.sql import func
import cv2 as cv
 

app = Flask(__name__)
CORS(app)

UPLOAD_FOLDER = 'static/uploads/'

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:''@localhost/en_inventory_details'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


#Our DataBase Model
class Inventory(db.Model):
    Inventory_key = db.Column(db.Integer, autoincrement= 1000000000000, primary_key=True)
    Row_Creation_Date = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    Row_update_Date = db.Column(db.DateTime(timezone=True), onupdate=func.now())
    Calling_Function = db.Column(db.String(20))
    Manufacture_Date = db.Column(db.DateTime())
    Product_Id = db.Column(db.String(20))
    Batch_Id = db.Column(db.String(20))

    #function will help us display our output as JSON.
    def json(self):
        return {'Inventory_key': self.Inventory_key, 'Calling_Function': self.Calling_Function, 'Manufacture_Date': self.Manufacture_Date, 'Product_Id': self.Product_Id, 'Batch_Id':self.Batch_Id}


    #Add products
    def add_product(_Calling_Function, _Manufacture_Date, _Product_Id, _Batch_Id):
        '''function to add product to database'''
        # creating an instance of our Product constructor
        new_product = Inventory(Calling_Function=_Calling_Function, Manufacture_Date=_Manufacture_Date, Product_Id=_Product_Id, Batch_Id=_Batch_Id)
        db.session.add(new_product)  # add new product details to database session
        db.session.commit()  # commit changes to session


    # Get All Product details
    def get_all_products():
        '''function to get all products in our database'''
        return [Inventory.json(pr) for pr in Inventory.query.all()]

    #Get single product details
    def get_product(_Inventory_key):
        '''function to get product details using the Inventory_key of the product as parameter'''
        return [Inventory.json(Inventory.query.filter_by(Inventory_key=_Inventory_key).first())]
        # coverts our output to the json format defined earlier
        # the filter_by method filters the query by the Inventory_key
        # since our key is unique we will only get one result
        # the .first() method will get that first value returned as unique and only value
    
    #function to update product on our database
    def update_product(_Inventory_key, _Calling_Function, _Manufacture_Date, _Product_Id, _Batch_Id):
        '''function to update the details of a product using parameters'''
        product_to_update = Inventory.query.filter_by(Inventory_key=_Inventory_key).first()
        product_to_update.Calling_Function = _Calling_Function
        product_to_update.Manufacture_Date = _Manufacture_Date
        product_to_update.Product_Id = _Product_Id
        product_to_update.Batch_Id = _Batch_Id
        db.session.commit()

    #Delete product
    def delete_product(_Inventory_key):
        '''function to delete a product from our database using
           the id of the product as a parameter'''
        Inventory.query.filter_by(Inventory_key=_Inventory_key).delete()
        # filter id and delete
        db.session.commit()  # commiting the new change to our database

    #Get the qr code
    def get_qr_code(_Inventory_key):

        key = Inventory.query.filter_by(Inventory_key=Inventory_key).first()

        if not key:
            return jsonify({'message' : 'No data found!'})

        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,                                                      
            )

        qr.add_data(key.Inventory_key)

        qr.make(fit=True)
        img = qr.make_image(fill_color="black", back_color="white")

        # val = '' #get value as svg to get .svg image(modify the function as per need)

        # if val == svg:
        #     filename = ''.join(random.choice(string.ascii_lowercase) for _ in range(7))+'.svg'
        # else:
        filename = ''.join(random.choice(string.ascii_lowercase) for _ in range(7))+'.png'
        
        img.save(filename)
        new_qr = {'QR_Code_Image': img}

        return new_qr

    
    #Detect the QR Code Image
    def scan_qr(_img, _Inventory_key):
        im = cv.imread(img)
        det = cv.QRCodeDetector()
        retval, points, straight_qrcode = det.detectAndDecode(im)
        if retval == _Inventory_key:
            return retval
        else:
            return retval = False

        
