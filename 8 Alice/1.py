from flask import Flask, request, jsonify
import logging, random, os
from geocoder import get_geo_info

app = Flask(__name__)
logging.basicConfig(level=logging.INFO)
sessionStorage = {}

cities = {'токио': ['1', '2'],
          'благовещенск': ['3', '4'],
          'дубай': ['5', '6']}


print(get_geo_info('благовещенск', 'country'))