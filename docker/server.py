import boto3
from flask import Flask, render_template, request, url_for
from botocore.client import Config
import time
from datetime import datetime, timezone

app = Flask(__name__)





dynamodb = boto3.resource('dynamodb', region_name="ca-central-1")
table = dynamodb.Table('message_details')



@app.context_processor
def inject_global_images():
    return dict(images={
        "logo": url_for('static', filename='images/logo.png'),
        "ceo": url_for('static', filename='images/ceo.png'),
        "emp1": url_for('static', filename='images/farmer1.png'),
        "emp2": url_for('static', filename='images/farmer2.png'),
        "emp3": url_for('static', filename='images/farmer3.png'),
        "fruits": url_for('static', filename='images/fruits.png'),
        "vegetables": url_for('static', filename='images/vegetables.png'),
        "nuts": url_for('static', filename='images/nuts.png'),
        
    })


@app.route('/')
def index_page():
    # CALL the helper function here so we get NEW urls
    return render_template('index.html')

@app.route('/about')
def about_page():
    return render_template('about.html')

@app.route("/menu")
def menu_page():
    return render_template('menu.html')

@app.route("/contact")
def contact_page():
    return render_template('contact.html')

@app.route("/contact/success", methods=["POST"])
def received_data():
    timestamp_ms = int(time.time() * 1000)
    now = datetime.now(timezone.utc)
    timestamp_str = now.isoformat()

    # Robust IP Capture
    user_ip = request.headers.get('X-Forwarded-For', request.remote_addr)
    if user_ip and ',' in user_ip:
        user_ip = user_ip.split(',')[0].strip()

    # Get Form Data
    name = request.form.get("name")
    user_email = request.form.get("email")
    phone = request.form.get("phone")
    message = request.form.get("message")
    
    # Static Data
    owner_email = "mohammedabdulfarhan17@gmail.com"
    store_id = 1002

    # Save to DynamoDB
    response = table.put_item(
        Item={
            "time_stamp":timestamp_str,
            "name": name,
            "email": user_email,
            "owner_email": owner_email,
            "phone": phone,
            "message": message,
            "user_ip": user_ip,
            "store_id": str(store_id),
            "message_id": str(timestamp_ms) + str(store_id),
            
        }
    )
    
    # Pass fresh URLs to the contact template again
    return render_template('contact.html', message="Message sent successfully!", status="success")

if __name__ == '__main__':
    app.run(debug=True)