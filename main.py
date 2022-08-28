from cors_handler import fix_cors
from replit import db
from flask import *
import random
import os
import json
from hedera import *

app = Flask(__name__)

def uploadToHedera(bytes):
  transaction = FileCreateTransaction().setKeys(OPERATOR_KEY.getPublicKey()).setContents(bytes).setMaxTransactionFee(Hbar(2))
  file_id = transaction.execute(client).getReceipt(client).fileId.toString()
  return "https://healthsaver.epiccodewizard2.repl.co/" + file_id

@app.route("/save/<email>", methods=["POST"])
@fix_cors
def save(email):
  if email not in db.keys():
    db[email] = []
  tempdata = {}
  tempdata["recordphoto"] = uploadToHedera(request.files["recordphoto"].content)
  tempdata["recordtype"] = request.args.get("recordtype")
  tempdata["recordno"] = request.args.get("recordno")
  db[email].append(tempdata)
  return jsonify(dict(tempdata))

@app.route("/fetch/email/<email>", methods=["GET"])
@fix_cors
def fetch(email):
  if email not in db.keys():
    return jsonify([])
  else:
    findata = []
    index = 0
    for x in db[email]:
      findata.append({"index": index, **dict(x)})
      index += 1
    return jsonify(findata)

@crossdomain(origin="*")
@app.route("/<file_id>", methods=["GET", "POST"])
def return_file(file):
  return FileContentsQuery().setFileId(FileId.fromString(file_id)).execute(client).toByteArray()
 
app.run(host="0.0.0.0")
