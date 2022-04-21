from flask import Flask, render_template, request, redirect, flash, url_for, session, jsonify
from .. import app

@app.route("/postcodes", methods=["GET"])
def postcodes():
    app.logger.info("Nothing yet")
    return jsonify({"status": "OK"})