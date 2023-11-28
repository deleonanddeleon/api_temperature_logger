from flask import Flask, request, jsonify, render_template
from flask_pymongo import PyMongo

app = Flask(__name__)

# Set up MongoDB connection
app.config['MONGO_URI'] = 'mongodb://localhost:27017/isp_outage_logger_db'
mongo = PyMongo(app)


@app.route('/outages')
def index():
    return render_template('index.html')


# Route to manage All Records from MongoDB
@app.route('/outages/records', methods=['GET', 'POST'])
def manage_records():
    if request.method == 'GET':
        records = mongo.db.outages.find()

        # Convert ObjectId to string in each document and create a new list
        result = []
        for record in records:
            record['_id'] = str(record['_id'])
            result.append(record)

        # Use jsonify with the new list
        return jsonify(result)
    elif request.method == 'POST':
        data = request.get_json()
        mongo.db.outages.insert_one(data)
        # return redirect(url_for('index'))
        return jsonify({'message': 'Item added successfully'})


# Route to manage One Record
@app.route('/outages/records/<int:item_id>', methods=['GET', 'PUT', 'DELETE'])
def manage_record(item_id):
    record = mongo.db.outages.find_one({'id': item_id})
    if not record:
        return jsonify({'error': 'Record not found'}), 404

    if request.method == 'GET':
        record['_id'] = str(record['_id'])
        return jsonify(record)
    elif request.method == 'PUT':
        data = request.get_json()

        # Use update_one to update the document
        result = mongo.db.outages.update_one({'id': item_id}, {'$set': data})

        if result.modified_count == 1:
            return jsonify({'message': 'Item updated'})
        else:
            return jsonify({'message': 'Item not found or not modified'}), 404
    elif request.method == 'DELETE':
        mongo.db.outages.delete_one({'id': item_id})
        return jsonify({'message': 'Item deleted'})


if __name__ == '__main__':
    app.run(debug=True)
