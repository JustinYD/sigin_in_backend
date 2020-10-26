# -*- coding:utf-8 -*-
# 引入flask框架，jsonify格式转换，网络请求request库，jieba库，数据库连接pymysql，flask_cors跨域处理
import json
import logging

from flask import Flask, jsonify, request
import pymysql
from flask_cors import *
# 初始化flask
app = Flask(__name__)
# 设置全局跨域处理

cors = CORS(app, resources={r"/*": {"origins": "*"}})
@app.route('/regStu',methods=['post'])
def regStu():
    db = pymysql.connect(host='121.36.46.96',
                         port=3306,
                         user='root',
                         password='151874DZlw',
                         db='sign_in')
    data = request.get_data()
    json_data = json.loads(data.decode("UTF-8"))
    openid = json_data.get("openid")
    student_name = json_data.get("name")
    classname = json_data.get("className")
    stu_number = json_data.get("stuNum")
    sex = json_data.get("sex")
    role = json_data.get("role")
    values = (openid, student_name, classname,stu_number,sex,role)
    sql_openid = "select * from sign_student where openid='%s'" % openid
    sql = 'insert into sign_student (openid, student_name, classname,stu_number,sex,role) values(%s, %s, %s, %s, %s, %s)'
    try:
        cur = db.cursor()
        if (openid != ''):
            if (cur.execute(sql_openid)):
                result = {'msg': '已被注册！', 'status': 201}
            else:
                cur.execute(sql, values)
                db.commit()
                result = {'msg': '注册成功！', 'status': 200}
        else:
            result = {'msg': '参数不完整！', 'status': 404}
    except Exception as e:
        logging.exception(e)
        result={'msg':'注册失败！','status':404}
    db.close()
    returnData=jsonify(result)
    return returnData
@app.route('/regTea', methods=['post'])
def regTea():
    db = pymysql.connect(host='121.36.46.96',
                         port=3306,
                         user='root',
                         password='151874DZlw',
                         db='sign_in')
    data = request.get_data()
    json_data = json.loads(data.decode("UTF-8"))
    openid = json_data.get("openid")
    teacher_name = json_data.get("name")
    phone = json_data.get("tel")
    role = json_data.get("role")
    values = (openid, teacher_name,phone, role)
    sql = 'insert into sign_teacher (openid, teacher_name,phone, role) values(%s, %s, %s, %s)'
    sql_openid = "select * from sign_teacher where openid='%s'"%openid
    try:
        cur = db.cursor()
        if(openid != ''):
            if(cur.execute(sql_openid)):
                result = {'msg': '已注册！', 'status': 201}
            else:
                cur.execute(sql, values)
                db.commit()
                result = {'msg': '注册成功！', 'status': 200}
        else:result = {'msg': '参数不完整！', 'status': 404}
    except Exception as e:
        print('异常信息'+e.msg)
        result = {'msg': '注册失败！', 'status': 404}
    db.close()
    returnData = jsonify(result)
    return returnData
@app.route('/updateInfo', methods=['post'])
def updateInfo():
    db = pymysql.connect(host='121.36.46.96',
                         port=3306,
                         user='root',
                         password='151874DZlw',
                         db='sign_in')
    data = request.get_data()
    json_data = json.loads(data.decode("UTF-8"))
    openid = json_data.get("openid")
    student_name = json_data.get("name")
    classname = json_data.get("className")
    stu_number = json_data.get("stuNum")
    sex = json_data.get("sex")
    role = json_data.get("role")
    teacher_name = json_data.get("name")
    phone = json_data.get("tel")
    if(role=='teacher'):
        values = (teacher_name, phone,openid)
        sql = "update sign_teacher set teacher_name='%s',phone='%s' where openid='%s'"%values
    else:
        values = (student_name, classname,stu_number,sex,openid)
        sql = "update sign_student set student_name='%s', classname='%s',stu_number='%s',sex='%s' where openid='%s'"%values
    try:
        cur = db.cursor()
        cur.execute(sql)
        result = {'msg': '已更新数据！', 'status': 200}
        cur.execute(sql)
        # hh
        db.commit()
    except Exception as e:
        logging.exception(e)
        result = {'msg': '更新失败！', 'status': 404}
    db.close()
    returnData = jsonify(result)
    return returnData
@app.route('/getMyRole', methods=['post'])
def getMyRole():
    db = pymysql.connect(host='121.36.46.96',
                         port=3306,
                         user='root',
                         password='151874DZlw',
                         db='sign_in')
    data = request.get_data()
    json_data = json.loads(data.decode("UTF-8"))
    openid = json_data.get("openid")
    role = json_data.get("role")
    if(role=='teacher'):
        sql = "select * from sign_teacher where openid='%s'" % openid
    else:sql = "select * from sign_student where openid='%s'"%openid
    try:
        cur = db.cursor()
        cur.execute(sql)
        result = {'msg': '获取成功！', 'status': 200, 'data':cur.fetchall()}
    except Exception as e:
        print('异常信息'+e.msg)
        result = {'msg': '注册失败！', 'status': 404}
    db.close()
    returnData = jsonify(result)
    return returnData
#项目启动入口
if __name__ == '__main__':
    app.run(host='0.0.0.0',port=5000)
