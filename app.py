# -*- coding:utf-8 -*-
# 引入flask框架，jsonify格式转换，网络请求request库，jieba库，数据库连接pymysql，flask_cors跨域处理
import datetime
import json
import logging

from flask import Flask, jsonify, request
import pymysql
from flask_cors import *
# 初始化flask
import requests

app = Flask(__name__)
# 设置全局跨域处理

cors = CORS(app, resources={r"/*": {"origins": "*"}})

# 学生注册判断接口
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

# 老师注册判断接口
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

# 更新学生或教师信息
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

# 通过openid获取学生/教师信息
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

# 老师获取课程列表
@app.route('/getTeacherClass', methods=['post'])
def getTeacherClass():
    db = pymysql.connect(host='121.36.46.96',
                         port=3306,
                         user='root',
                         password='151874DZlw',
                         db='sign_in')
    data = request.get_data()
    json_data = json.loads(data.decode("UTF-8"))
    teacher_openid = json_data.get("openid")
    sql_openid = "select * from sign_class where teacher_openid='%s'" % teacher_openid
    try:
        cur = db.cursor()
        if (cur.execute(sql_openid)):
            result = {'msg': '课程查询成功！', 'status': 200, 'data':cur.fetchall()}
        else:
            result = {'msg': '未创建任何课程！', 'status': 201}
    except Exception as e:
        print('异常信息' + e.msg)
        result = {'msg': '查询失败！', 'status': 404}
    db.close()
    returnData = jsonify(result)
    return returnData

# 学生获取打卡课程列表
@app.route('/getStudentSignClass', methods=['post'])
def getStudentSignClass():
    db = pymysql.connect(host='121.36.46.96',
                         port=3306,
                         user='root',
                         password='151874DZlw',
                         db='sign_in')
    data = request.get_data()
    json_data = json.loads(data.decode("UTF-8"))
    student_id = json_data.get("openid")
    sql_openid = "select * from sign_history where student_id='%s' and sign_status=TRUE and student_status=FALSE" % student_id
    try:
        cur = db.cursor()
        if (cur.execute(sql_openid)):
            result = {'msg': '课程查询成功！', 'status': 200, 'data':cur.fetchall()}
        else:
            result = {'msg': '没有需要打卡的课程！', 'status': 201}
    except Exception as e:
        print('异常信息' + e.msg)
        result = {'msg': '查询失败！', 'status': 404}
    db.close()
    returnData = jsonify(result)
    return returnData


# 学生获取课程列表
@app.route('/getStudentClass', methods=['post'])
def getStudentClass():
    db = pymysql.connect(host='121.36.46.96',
                         port=3306,
                         user='root',
                         password='151874DZlw',
                         db='sign_in')
    data = request.get_data()
    json_data = json.loads(data.decode("UTF-8"))
    student_id = json_data.get("openid")
    sql_openid = "select * from sign_my_class where student_id='%s'" % student_id
    try:
        cur = db.cursor()
        if (cur.execute(sql_openid)):
            result = {'msg': '课程查询成功！', 'status': 200, 'data':cur.fetchall()}
        else:
            result = {'msg': '未添加课程！', 'status': 201}
    except Exception as e:
        print('异常信息' + e.msg)
        result = {'msg': '查询失败！', 'status': 404}
    db.close()
    returnData = jsonify(result)
    return returnData

# 学生搜索课程
@app.route('/searchClass', methods=['post'])
def searchClass():
    db = pymysql.connect(host='121.36.46.96',
                         port=3306,
                         user='root',
                         password='151874DZlw',
                         db='sign_in')
    data = request.get_data()
    json_data = json.loads(data.decode("UTF-8"))
    class_id = json_data.get("class_id")
    sql_openid = "select * from sign_class where id='%s'" % class_id
    try:
        cur = db.cursor()
        if (cur.execute(sql_openid)):
            result = {'msg': '课程查询成功！', 'status': 200, 'data':cur.fetchall()}
        else:
            result = {'msg': '未找到课程！', 'status': 201}
    except Exception as e:
        print('异常信息' + e.msg)
        result = {'msg': '查询失败！', 'status': 404}
    db.close()
    returnData = jsonify(result)
    return returnData

# 老师创建课程
@app.route('/createClass', methods=['post'])
def createClass():
    db = pymysql.connect(host='121.36.46.96',
                         port=3306,
                         user='root',
                         password='151874DZlw',
                         db='sign_in')
    data = request.get_data()
    json_data = json.loads(data.decode("UTF-8"))
    teacher_openid = json_data.get("openid")
    classname = json_data.get("classname")
    teacher_name = json_data.get("name")
    status=False
    values = (teacher_openid, classname, status,teacher_name)
    sql = 'insert into sign_class (teacher_openid, classname, status,teacher_name) values(%s, %s, %s,%s)'
    try:
        cur = db.cursor()
        if(classname != ''):
            cur.execute(sql, values)
            db.commit()
            result = {'msg': '注册成功！', 'status': 200}
        else:result = {'msg': '课程名字为空！', 'status': 404}
    except Exception as e:
        print('异常信息'+e.msg)
        result = {'msg': '创建失败！', 'status': 404}
    db.close()
    returnData = jsonify(result)
    return returnData

# 老师删除课程
@app.route('/deleteClass', methods=['post'])
def deleteClass():
    db = pymysql.connect(host='121.36.46.96',
                         port=3306,
                         user='root',
                         password='151874DZlw',
                         db='sign_in')
    data = request.get_data()
    json_data = json.loads(data.decode("UTF-8"))
    teacher_openid = json_data.get("openid")
    id = json_data.get("id")
    values = (teacher_openid, id)
    sql = "delete from sign_class where id='%s'"%id
    sql_student = "delete from sign_my_class where class_id='%s'"%id
    try:
        cur = db.cursor()
        if(id != ''):
            cur.execute(sql)
            cur.execute(sql_student)
            db.commit()
            result = {'msg': '删除成功！', 'status': 200}
        else:result = {'msg': '课程名字为空！', 'status': 404}
    except Exception as e:
        print('异常信息'+e.msg)
        result = {'msg': '删除失败！', 'status': 404}
    db.close()
    returnData = jsonify(result)
    return returnData

# 老师更新课程/状态
@app.route('/updateClass', methods=['post'])
def updateClass():
    db = pymysql.connect(host='121.36.46.96',
                         port=3306,
                         user='root',
                         password='151874DZlw',
                         db='sign_in')
    data = request.get_data()
    json_data = json.loads(data.decode("UTF-8"))
    classname = json_data.get("classname")
    id = json_data.get("id")
    status=json_data.get("status")
    if(status):
        sql = "update sign_class set classname='%s',status=TRUE where id='%s'"%(classname,id)
        sql_student = "update sign_my_class set class_name='%s', status=TRUE where class_id='%s'" % (classname, id)
    else:
        sql = "update sign_class set classname='%s',status=FALSE where id='%s'" % (classname, id)
        sql_student = "update sign_my_class set class_name='%s', status=FALSE where class_id='%s'" % (classname, id)
    try:
        cur = db.cursor()
        if(id != ''):
            cur.execute(sql)
            cur.execute(sql_student)
            db.commit()
            result = {'msg': '修改成功！', 'status': 200}
        else:result = {'msg': '课程名字为空！', 'status': 404}
    except Exception as e:
        print('异常信息'+e.msg)
        result = {'msg': '创建失败！', 'status': 404}
    db.close()
    returnData = jsonify(result)
    return returnData

# 老师开始/结束打卡
@app.route('/startOrStopClass', methods=['post'])
def startOrStopClass():
    db = pymysql.connect(host='121.36.46.96',
                         port=3306,
                         user='root',
                         password='151874DZlw',
                         db='sign_in')
    data = request.get_data()
    json_data = json.loads(data.decode("UTF-8"))
    id = json_data.get("id")
    startTag = json_data.get("startTag")
    teacher_id = json_data.get("teacher_id")
    status=json_data.get("status")
    class_name=json_data.get("classname")
    mlat = json_data.get("mlat")
    mlng = json_data.get("mlng")
    startTag=json_data.get("startTag")
    tag=(startTag,mlat,mlng)
    try:
        cur = db.cursor()
        get_id = db.cursor()
        get_data = db.cursor()
        # 先查询是否有学生添加了这个课
        get_student_id = "select student_id from sign_my_class where class_id='%s'" % id
        # 如果有
        if (get_id.execute(get_student_id)):
            temp = get_id.fetchall()
            temp_id_list = []
            for i in temp:
                temp_id_list.append(i[0])
            # 所有学生的student_id存在这个元组中
            student_id_list = tuple(temp_id_list)
            # 如果只有一个人
            if len(student_id_list)==1:
                if(status):
                    sql = "update sign_class set status=TRUE where id='%s'" % id
                    sql_add = "insert into sign_history(`class_id`, `class_name`, `teacher_id`, `teacher_name`," \
                              " `student_id`, `student_name`,`sign_status`,`majorName`,`startTag`,`student_status`,`mlat`,`mlng`,`student_number`) select `class_id`, `class_name`, `teacher_id`, `teacher_name`," \
                              " `student_id`, `student_name`,TRUE,`majorName`, %s ,FALSE,%s,%s,`student_number` from sign_my_class where student_id= '%s' and class_id ='%s'" % (
                              student_id_list[0], id,startTag,mlat,mlng)
                else:
                    sql = "update sign_class set status=FALSE where id='%s'" % id
                    sql_add = "select student_id from sign_my_class where class_id='%s'" % id
                cur.execute(sql)
                if (cur.execute(sql_add, tag)):
                    db.commit()
                    result = {'msg': '开启成功！', 'status': 200}
            # 超过一个人的时候
            else:
                if(status):
                    sql_add = "insert into sign_history(`class_id`, `class_name`, `teacher_id`, `teacher_name`," \
                              " `student_id`, `student_name`,`sign_status`,`majorName`,`startTag`,`student_status`,`mlat`,`mlng`,`student_number`) select `class_id`, `class_name`, `teacher_id`, `teacher_name`," \
                              " `student_id`, `student_name`,TRUE,`majorName`, %s ,FALSE,%s,%s,`student_number` from sign_my_class where student_id in" + str(
                        student_id_list) + "and class_id = " + str(id)
                    sql = "update sign_class set status=TRUE where id='%s'" % id
                    cur.execute(sql)
                    if (cur.execute(sql_add, tag)):
                        db.commit()
                        result = {'msg': '开启成功！', 'status': 200}
                else:
                    sql = "update sign_class set status=FALSE where id='%s'" % id
                    sql_add = "update sign_history set sign_status=FALSE where class_id='%s' and teacher_id='%s' and startTag='%s'" %(id,teacher_id,startTag)
                    cur.execute(sql)
                    cur.execute(sql_add)
                    db.commit()
                    result = {'msg': '关闭成功！', 'status': 200}
        # 没有人添加该课程
        else:
            result = {'msg': '未有学生加入！', 'status': 404}
    except Exception as e:
        print('异常信息'+e.msg)
        result = {'msg': '创建失败！', 'status': 404}
    db.close()
    returnData = jsonify(result)
    return returnData

# 学生添加课程
@app.route('/studentAddClass', methods=['post'])
def studentAddClass():
    db = pymysql.connect(host='121.36.46.96',
                         port=3306,
                         user='root',
                         password='151874DZlw',
                         db='sign_in')
    data = request.get_data()
    json_data = json.loads(data.decode("UTF-8"))
    teacher_id = json_data.get("teacher_id")
    teacher_name = json_data.get("teacher_name")
    student_id = json_data.get("student_id")
    student_name = json_data.get("student_name")
    student_number = json_data.get("student_number")
    class_id = json_data.get("class_id")
    class_name = json_data.get("class_name")
    majorName = json_data.get("majorName")
    try:
        cur = db.cursor()
        getStatus="select status from sign_class where id='%s'"%class_id
        if(cur.execute(getStatus)):
            if (cur.fetchall()[0][0]):
                status = True
            else:
                status = False
            values = (teacher_id, teacher_name, student_id, student_name, class_id, class_name, majorName, status,student_number)
            sql = 'insert into sign_my_class (teacher_id, teacher_name, student_id, student_name, class_id, class_name, majorName,status,student_number) values(%s, %s, %s,%s,%s, %s, %s,%s,%s)'
            getInClass = "select * from sign_my_class where student_id='%s' and class_id='%s'" % (student_id, class_id)
            if (cur.execute(getInClass)):
                result = {'msg': '已添加过该课程', 'status': 404}
            else:
                if (cur.execute(sql, values)):
                    db.commit()
                    result = {'msg': '添加课程成功', 'status': 200}
                else:
                    result = {'msg': '添加课程失败', 'status': 404}
        else:result = {'msg': '未找到该课程', 'status': 404}
    except Exception as e:
        print('异常信息'+e.msg)
        result = {'msg': '服务器错误！', 'status': 404}
    db.close()
    returnData = jsonify(result)
    return returnData

# 学生删除收藏课程
# 老师删除课程
@app.route('/deleteStudentClass', methods=['post'])
def deleteStudentClass():
    db = pymysql.connect(host='121.36.46.96',
                         port=3306,
                         user='root',
                         password='151874DZlw',
                         db='sign_in')
    data = request.get_data()
    json_data = json.loads(data.decode("UTF-8"))
    student_id = json_data.get("student_id")
    class_id = json_data.get("class_id")
    sql_student = "delete from sign_my_class where student_id='%s' and class_id='%s'"%(student_id,class_id)
    try:
        cur = db.cursor()
        if(class_id != ''):
            cur.execute(sql_student)
            db.commit()
            result = {'msg': '删除成功！', 'status': 200}
        else:result = {'msg': '课程名字为空！', 'status': 404}
    except Exception as e:
        print('异常信息'+e.msg)
        result = {'msg': '删除失败！', 'status': 404}
    db.close()
    returnData = jsonify(result)
    return returnData

# 核心功能！！！打卡
@app.route('/sign_in', methods=['post'])
def sign_in():
    db = pymysql.connect(host='121.36.46.96',
                         port=3306,
                         user='root',
                         password='151874DZlw',
                         db='sign_in')
    data = request.get_data()
    json_data = json.loads(data.decode("UTF-8"))
    student_id = json_data.get("student_id")
    class_id = json_data.get("class_id")
    teacher_id = json_data.get("teacher_id")
    startTag = json_data.get("startTag")
    time = datetime.datetime.now()
    sign_in = "update sign_history set student_status=TRUE, sign_time='%s' where class_id='%s' and teacher_id='%s' and startTag='%s' and student_id='%s'" %(time,class_id,teacher_id,startTag,student_id)
    try:
        cur = db.cursor()
        if (cur.execute(sign_in)):
            db.commit()
            result = {'msg': '课程打卡成功！', 'status': 200}
        else:
            result = {'msg': '课程打卡失败！', 'status': 201}
    except Exception as e:
        print('异常信息' + e.msg)
        result = {'msg': '查询失败！', 'status': 404}
    db.close()
    returnData = jsonify(result)
    return returnData

# 核心功能！！！获取打卡距离判断是否可以打卡
@app.route('/getdistance',methods=['post'])
def getdistance():
    data = request.get_data()
    json_data = json.loads(data.decode("UTF-8"))
    student_id = json_data.get("student_id")
    class_id = json_data.get("class_id")
    lat = json_data.get('lat')
    lng = json_data.get('lng')
    mlat = json_data.get('mlat')
    mlng = json_data.get('mlng')
    print(lat,lng,mlat,mlng)
    url='https://apis.map.qq.com/ws/distance/v1/?mode=walking&from='+str(lat)+','+str(lng)+'&to='+str(mlat)+','+str(mlng)+'&key=PVYBZ-O2ZWG-YLVQS-IEYLV-LQTZF-MPBDO'
    response = requests.get(url)
    dis = response.content.decode('utf-8')
    dis1=json.loads(dis)
    dis1=dis1['result']['elements'][0]['distance']
    result = {'data': dis1, 'status': 200}
    distance = jsonify(result)
    return distance


@app.route('/getStudentSignHistory', methods=['post'])
def getStudentSignHistory():
    db = pymysql.connect(host='121.36.46.96',
                         port=3306,
                         user='root',
                         password='151874DZlw',
                         db='sign_in')
    data = request.get_data()
    json_data = json.loads(data.decode("UTF-8"))
    student_id = json_data.get("openid")
    sign_in = "select * from sign_history where student_id='%s'"%student_id
    try:
        cur = db.cursor()
        if (cur.execute(sign_in)):
            result = {'msg': '查询成功！', 'status': 200, 'data':cur.fetchall()}
        else:
            result = {'msg': '查询失败！', 'status': 201}
    except Exception as e:
        print('异常信息' + e.msg)
        result = {'msg': '查询失败！', 'status': 404}
    db.close()
    returnData = jsonify(result)
    return returnData


@app.route('/getItemHistory', methods=['post'])
def getItemHistory():
    db = pymysql.connect(host='121.36.46.96',
                         port=3306,
                         user='root',
                         password='151874DZlw',
                         db='sign_in')
    data = request.get_data()
    json_data = json.loads(data.decode("UTF-8"))
    class_id = json_data.get("class_id")
    teacher_id = json_data.get("teacher_id")
    startTag = "select * from sign_history where class_id='%s' and teacher_id='%s'"%(class_id,teacher_id)
    try:
        cur = db.cursor()
        if (cur.execute(startTag)):
            getTags="select startTag,createtime, count(*) as count from sign_history where class_id='%s' group by startTag having count>0"%class_id
            cur.execute(getTags)
            result = {'msg': '查询成功！', 'status': 200, 'data': cur.fetchall()}
        else:
            result = {'msg': '该课程没有记录！', 'status': 201}
    except Exception as e:
        print('异常信息' + e.msg)
        result = {'msg': '查询失败！', 'status': 404}
    db.close()
    returnData = jsonify(result)
    return returnData

@app.route('/getItemDetail', methods=['post'])
def getItemDetail():
    db = pymysql.connect(host='121.36.46.96',
                         port=3306,
                         user='root',
                         password='151874DZlw',
                         db='sign_in')
    data = request.get_data()
    json_data = json.loads(data.decode("UTF-8"))
    class_id = json_data.get("class_id")
    teacher_id = json_data.get("teacher_id")
    startTag = json_data.get('startTag')
    detail = "select * from sign_history where class_id='%s' and teacher_id='%s' and startTag='%s'"%(class_id,teacher_id,startTag)
    try:
        cur = db.cursor()
        getMajor = db.cursor()
        getStatus = db.cursor()
        if (cur.execute(detail)):
            getTags="select majorName, count(*) as count from sign_history where class_id='%s' and teacher_id='%s' and startTag='%s' group by majorName having count>0"%(class_id,teacher_id,startTag)
            status = "select student_status, count(*) as count from sign_history where class_id='%s' and teacher_id='%s' and startTag='%s' group by student_status having count>0"%(class_id, teacher_id, startTag)
            getMajor.execute(getTags)
            getStatus.execute(status)
            result = {'msg': '查询成功！', 'status': 200, 'data': cur.fetchall(), 'major_data':getMajor.fetchall(), 'status_data':getStatus.fetchall()}
        else:
            result = {'msg': '该课程没有记录！', 'status': 201}
    except Exception as e:
        print('异常信息' + e.msg)
        result = {'msg': '查询失败！', 'status': 404}
    db.close()
    returnData = jsonify(result)
    return returnData

#项目启动入口
if __name__ == '__main__':
    app.run(host='0.0.0.0',port=5000)
