#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import re
import sys
import time
import serial
import socket
import configparser
import win32print
import datetime
import json
import webbrowser
import pdfkit
import tempfile
import logging

import serial.tools.list_ports
from time import sleep
from flask import Flask, redirect, request, make_response
from flask_cors import CORS

app = Flask(__name__, static_url_path='')
CORS(app, supports_credentials=True)


@app.route('/', methods=['GET'])
def index():
    return redirect('/index.html')


@app.route('/get/config', methods=['GET'])
def get_config():
    port, rate, timeout = config()
    version = get_conf('base', 'version')
    data = [{'port': port, 'rate': rate, 'timeout': timeout, 'version': version}]
    return str(data)


@app.route('/test', methods=['POST'])
def test():
    try:
        port = request.values.get('port')
        rate = int(request.values.get('rate'))
        timeout = float(request.values.get('timeout'))
        ser = serial.Serial(port, rate, timeout=timeout)
        if ser.isOpen():
            return 'success'
    except Exception as e:
        return str(e)


@app.route('/set/config', methods=['POST'])

def set_config():
    try:
        port = request.values.get('port')
        rate = request.values.get('rate')
        timeout = request.values.get('timeout')
        conf = "base"
        logger("[SET CONF]:" + conf)
        set_conf(conf, 'port', port)
        set_conf(conf, 'rate', rate)
        set_conf(conf, 'timeout', timeout)
        logger("[SET CONF]:" + str(port) + "  " + str(rate) + "  " + str(timeout))
        return redirect("/index.html")
    except Exception as e:
        return str(e)


@app.route('/get/all/printer', methods=['GET'])
def get_all_printer_conf():
    data = []
    for item in get_printer_selections():
        if 'base' != item:
            logger(item)
            temple_code = get_conf(item, 'temple_code')
            printer_name = get_conf(item, 'printer_name')
            page_height = get_conf(item, 'page_height')
            page_width = get_conf(item, 'page_width')
            margin_top = get_conf(item, 'margin_top')
            margin_right = get_conf(item, 'margin_right')
            margin_bottom = get_conf(item, 'margin_bottom')
            margin_left = get_conf(item, 'margin_left')
            printer = {
                'temple_code': temple_code,
                'printer_name': printer_name,
                'page_height': page_height,
                'page_width': page_width,
                'margin_top': margin_top,
                'margin_right': margin_right,
                'margin_bottom': margin_bottom,
                'margin_left': margin_left
            }
            data.append(printer)
    response = make_response(json.dumps(data))
    response.headers['Access-Control-Allow-Origin'] = '*'
    return response


@app.route('/syn/printer', methods=['POST'])
def syn_printer_conf():
    try:
        logger(request.data)
        json_data = json.loads(request.json)
        temple_code = json_data["temple_code"]
        if temple_code == "base":
            response = make_response("Invalid temple code: " + temple_code)
            response.headers['Access-Control-Allow-Origin'] = '*'
            return response
        selections = temple_code
        printer_name = json_data["printer_name"]
        page_height = json_data["page_height"]
        page_width = json_data["page_width"]
        margin_top = json_data["margin_top"]
        margin_right = json_data["margin_right"]
        margin_bottom = json_data["margin_bottom"]
        margin_left = json_data["margin_left"]
        set_conf(selections, "temple_code", temple_code)
        set_conf(selections, "printer_name", printer_name)
        set_conf(selections, "page_height", page_height)
        set_conf(selections, "page_width", page_width)
        set_conf(selections, "margin_top", margin_top)
        set_conf(selections, "margin_right", margin_right)
        set_conf(selections, "margin_bottom", margin_bottom)
        set_conf(selections, "margin_left", margin_left)
        response = make_response('success')
    except Exception as e:
        logger("[SET CONFIG EXCEPTION] " + str(e))
        response = make_response("[SET CONFIG EXCEPTION] " + str(e))
    response.headers['Access-Control-Allow-Origin'] = '*'
    return response


@app.route('/set/printer', methods=['POST'])
def set_printer_conf():
    try:
        logger(request.data)
        temple_code = request.json["temple_code"]
        if temple_code == "base":
            response = make_response("Invalid temple code: " + temple_code)
            response.headers['Access-Control-Allow-Origin'] = '*'
            return response
        selections = temple_code
        printer_name = request.json["printer_name"]
        page_height = request.json["page_height"]
        page_width = request.json["page_width"]
        margin_top = request.json["margin_top"]
        margin_right = request.json["margin_right"]
        margin_bottom = request.json["margin_bottom"]
        margin_left = request.json["margin_left"]
        set_conf(selections, "temple_code", temple_code)
        set_conf(selections, "printer_name", printer_name)
        set_conf(selections, "page_height", page_height)
        set_conf(selections, "page_width", page_width)
        set_conf(selections, "margin_top", margin_top)
        set_conf(selections, "margin_right", margin_right)
        set_conf(selections, "margin_bottom", margin_bottom)
        set_conf(selections, "margin_left", margin_left)
        response = make_response('success')
    except Exception as e:
        logger("[SET CONFIG EXCEPTION] " + str(e))
        response = make_response("[SET CONFIG EXCEPTION] " + str(e))
    response.headers['Access-Control-Allow-Origin'] = '*'
    return response


@app.route('/delete/temple', methods=['POST'])
def delete_printer_conf():
    temple_code = request.json["temple_code"]
    if temple_code == "base":
        return "Invalid temple code: " + temple_code
    else:
        delete_selection(temple_code)
        return "success"


@app.route('/printers', methods=['GET'])
def get_printers():
    index_of_name = 2
    printer = []
    for item in win32print.EnumPrinters(win32print.PRINTER_ENUM_LOCAL):
        printer.append(str(item[index_of_name]))
        logger(str(item[index_of_name]))
    response = make_response(json.dumps(printer))
    response.headers['Access-Control-Allow-Origin'] = '*'
    return response


@app.route('/test/print', methods=['POST'])
def test_print_pdf():
    try:
        content = request.json['content']
        temple_code = request.json['temple_code']
        selections = temple_code
        length_unit = "mm"
        test_printer = get_conf(selections, "printer_name")
        options = {
            'page-height': get_conf(selections, "page_height") + length_unit,
            'page-width': get_conf(selections, "page_width") + length_unit,
            'margin-top': get_conf(selections, "margin_top") + length_unit,
            'margin-right': get_conf(selections, "margin_right") + length_unit,
            'margin-bottom': get_conf(selections, "margin_bottom") + length_unit,
            'margin-left': get_conf(selections, "margin_left") + length_unit,
            'encoding': get_conf("base", "charset")
        }
        print_file = tempfile.TemporaryFile(suffix=".pdf", prefix="sz_").name
        logger(print_file)
        configuration = pdfkit.configuration(wkhtmltopdf='tool\\wkhtmltopdf_x86.exe')
        if bool(sys.maxsize > 2 ** 32):
            configuration = pdfkit.configuration(wkhtmltopdf='tool\\wkhtmltopdf_x64.exe')
        pdfkit.from_string(content, print_file, options=options, configuration=configuration)
        print_executor = os.getcwd() + "\\tool\\SumatraPDF.exe"
        print_to = "-print-to \"" + test_printer + "\""
        logger(print_executor + " " + print_to + " " + print_file)
        os.system(print_executor + " " + print_to + " " + print_file)
        response = make_response("OK")
    except Exception as e:
        logger(str(e))
        response = make_response('[PRINT EXCEPTION]' + str(e))
    return response


@app.route('/print', methods=['POST'])
def print_pdf():
    try:
        json_data = json.loads(request.json)
        content = json_data['content']
        temple_code = json_data['temple_code']
        selections = temple_code
        if selections not in get_printer_selections():
            response = make_response('[ERROR] printer config not exists!!!')
            response.headers['Access-Control-Allow-Origin'] = '*'
            return response
        length_unit = "mm"
        test_printer = get_conf(selections, "printer_name")
        options = {
            'page-height': get_conf(selections, "page_height") + length_unit,
            'page-width': get_conf(selections, "page_width") + length_unit,
            'margin-top': get_conf(selections, "margin_top") + length_unit,
            'margin-right': get_conf(selections, "margin_right") + length_unit,
            'margin-bottom': get_conf(selections, "margin_bottom") + length_unit,
            'margin-left': get_conf(selections, "margin_left") + length_unit,
            'encoding': get_conf("base", "charset")
        }
        print_file = tempfile.TemporaryFile(suffix=".pdf", prefix="sz_").name
        logger(print_file)
        configuration = pdfkit.configuration(wkhtmltopdf='tool\\wkhtmltopdf_x86.exe')
        if bool(sys.maxsize > 2 ** 32):
            configuration = pdfkit.configuration(wkhtmltopdf='tool\\wkhtmltopdf_x64.exe')
        pdfkit.from_string(content, print_file, options=options, configuration=configuration)
        print_executor = os.getcwd() + "\\tool\\SumatraPDF.exe"
        print_to = "-print-to \"" + test_printer + "\""
        logger(print_executor + " " + print_to + " " + print_file)
        os.system(print_executor + " " + print_to + " " + print_file)
        response = make_response("OK")
    except Exception as e:
        logger(str(e))
        response = make_response('[PRINT EXCEPTION]' + str(e))
    response.headers['Access-Control-Allow-Origin'] = '*'
    return response


@app.route('/port', methods=['GET'])
def get_port():
    try:
        plist = list(serial.tools.list_ports.comports())
        if len(plist) <= 0:
            logger("[PORT ERROR] The Serial port can't find!")
            return ""
        else:
            data = ""
            logger("[PORT LEN] " + str(len(plist)))
            for port in plist:
                data += "&" + (port[0])
                logger(port[0])
            logger(data)
            return data.strip("&")
    except Exception as e:
        logger('[PORT EXCEPTION] ' + str(e))
        return ""


@app.route('/data', methods=['GET', 'POST'])
def get_data():
    try:
        port, rate, timeout = config()
        ser = serial.Serial(port, rate, timeout=timeout)
        if ser.isOpen():
            data = ''
            data = data.encode(get_conf('base', 'charset'))
            n = ser.inWaiting()
            count = 10
            while n == 0:
                sleep(0.1)
                count -= 1
                n = ser.inWaiting()
                if count == 0:
                    break
            if n:
                data = data + ser.read(n)
            if ser.isOpen():
                ser.close()
            if len(data) == 0:
                logger('[READ DATA]:NO DATA')
                response = make_response("NO DATA")
            else:
                logger('[READ DATA]:' + str(data))
                pattern = re.compile(r"(\d+\.\d+)")
                values = pattern.findall(str(data))
                if len(values) > 0:
                    response = make_response(values[0])
                else:
                    response = make_response("DATAERROR")
        else:
            response = make_response('PROTCOLSE')
    except UnboundLocalError as a:
        logger('[DATA UnboundLocalError]' + str(a))
        response = make_response('[DATA UnboundLocalError]' + str(a))
    except Exception as se:
        logger('[DATA EXCEPTION]' + str(se))
        response = make_response('[DATA EXCEPTION]' + str(se))
    response.headers['Access-Control-Allow-Origin'] = '*'
    return response


@app.route('/original/data', methods=['GET', 'POST'])
def get_original_data():
    try:
        port, rate, timeout = config()
        ser = serial.Serial(port, rate, timeout=timeout)
        if ser.isOpen():
            data = ''
            data = data.encode(get_conf('base', 'charset'))
            n = ser.inWaiting()
            count = 10
            while n == 0:
                sleep(0.1)
                count -= 1
                n = ser.inWaiting()
                if count == 0:
                    break
            if n:
                data = data + ser.read(n)
            if ser.isOpen():
                ser.close()
            if len(data) == 0:
                logger('[READ DATA]:NO DATA')
                return "NO DATA"
            logger('[READ DATA]:' + str(data))
            return data
        else:
            return 'PROTCOLSE'
    except UnboundLocalError as a:
        logger('[DATA UnboundLocalError]' + str(a))
        return '[DATA UnboundLocalError]' + str(a)
    except Exception as se:
        logger('[DATA EXCEPTION]' + str(se))
        return '[DATA EXCEPTION]' + str(se)


def test_conn(host, port):
    sk = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sk.settimeout(1)
    try:
        sk.connect((host, port))
        logger("[PORT] unavailable ")
        return 0
    except Exception as ae:
        logger("[PORT] available " + str(ae))
        return 1
    sk.close()


def config():
    try:
        path = "./config/app.ini"
        cf = configparser.ConfigParser()
        cf.read(path)
        conf = str(cf.sections()[0])
        logger("[CONF]:" + conf)
        port = cf.get(conf, 'port')
        rate = cf.getint(conf, 'rate')
        timeout = cf.getfloat(conf, 'timeout')
        logger("[CONF]:" + str(port) + "  " + str(rate) + "  " + str(timeout))
        return port, rate, timeout
    except Exception as e:
        logger("[CONF] exception" + str(e))
        return "COM5", 9600, 2


def get_printer_selections():
    try:
        path = "./config/app.ini"
        cf = configparser.ConfigParser()
        cf.read(path)
        return cf.sections()
    except Exception as e:
        logger("[CONF ERROR] " + str(e))
        return "NULL"


def delete_selection(selection):
    path = "./config/app.ini"
    cf = configparser.ConfigParser()
    cf.read(path)
    cf.remove_section(selection)
    with open(path, 'w') as fw:
        cf.write(fw)
    fw.close()


def set_conf(selection, key, value):
    path = "./config/app.ini"
    cf = configparser.ConfigParser()
    cf.read(path)
    if selection not in get_printer_selections():
        logger("new selection: " + selection)
        cf.add_section(selection)
    logger("[SET CONF]: " + selection + " :" + key + " :" + str(value))
    cf.set(selection, key, str(value))
    with open(path, 'w') as fw:
        cf.write(fw)
    fw.close()


def get_conf(selection, key):
    try:
        path = "./config/app.ini"
        cf = configparser.ConfigParser()
        cf.read(path)
        value = cf.get(selection, key)
        return value
    except Exception as e:
        logger("[CONF ERROR] " + str(e))
        return "NULL"


def logger(info):
    today = datetime.date.today()
    logpath = "./log/"
    date_str = str(today.year) + "-" + str(today.month) + "-" + str(today.day)
    if not os.path.exists(logpath):
        os.makedirs(logpath)
    path = logpath + date_str + ".log"
    now = time.strftime("%H:%M:%S")
    with open(path, 'a') as f:
        f.writelines(date_str + " " + now + " " + str(info) + "\n")
        # print(date_str + " " + now + " " + str(info))
    f.close()


if __name__ == '__main__':
    logger("!!!!!!!!!!Do Not Close This Window !!!!!!!!!!!!")
    logger("[VERSION] dev-1.0.0")
    logger("[CHECKING]....")
    port = int(get_conf('base', 'server_port'))
    if test_conn('127.0.0.1', port):
        logger("[DONE] start up...")
        webbrowser.open("http:/127.0.0.1:" + str(port))
        app.run(host="0.0.0.0", port=port)
        # app.run(port=port)
    else:
        logger("[ERROR] local " + str(port) + " port already in use,Please shut it down and restart!!!")
