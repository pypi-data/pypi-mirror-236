import uvicorn
from fastapi import APIRouter, Request
from bbat.web.url_to_sql.query import Query
from bbat.db.aio_mysql import Mysql

router = APIRouter()

def get_router(host="localhost", port=3306, user="root", password="123456", database="project"):
    db = Mysql(host, port, database, user, password)
    router.db = db
    return router, db


def success(data, msg="success"):
    return {"code": 0, "data": data, "msg": msg}


def error(msg="error"):
    return {"code": -1, "data": {}, "msg": msg}

# @router.on_event("startup")
# async def startup():
#     router.db = init_db(**router.db_config)

# get方法查询函数
@router.get("/hyper/{table}")
async def query(table, request: Request):
    db = router.db
    query_string = request.query_params

    result = {}
    query = Query(table, query_string)

    sql = query.to_sql()
    # 1.主表查询
    data = await db.query(sql)
    # 根据field定义，做数据处理
    data = query.data_convert(query.fields, data)
    # 2.统计查询
    count_sql = query.to_count_sql()
    info = await db.fetch(count_sql)
    result["meta"] = {"total": info["cnt"]}
    # 3.子表查询
    for relation in query.relation:
        # master表外键所有id
        idhub = set([str(i[relation.master_key]) for i in data])
        if len(idhub) == 0:
            continue
        ids = ",".join([f"'{i}'" for i in idhub])
        # 查子表数据
        sql = relation.to_sql(f"{relation.relate_key} IN ({ids})")
        relation_data = await db.query(sql)
        query.data_convert(relation.fields, relation_data)
        # 合并数据
        relation.merge_table_data(data, relation_data)

    result["list"] = data
    return success(result)


# POST,PUT方法，插入和更新数据，有查询条件触发更新
@router.api_route("/hyper/{table}", methods=["POST", "PUT"])
async def post(table, request: Request):
    db:Mysql = router.db
    query_string = request.query_params

    data = await request.json()
    if not data:
        return error("ERROR: data is null")
    # 有query触发更新
    query = Query(table, query_string)
    if query_string:
        sql = query.to_update_sql(data)
        result = await db.execute(sql)
        return success(data)
    else:
        # sql = query.to_insert_sql(data)
        # result = await db.execute(sql)
        result = await db.insert(table, data)
        if not result:
            return error(result)
        data['id'] = result
        return success(data)


# delete data
@router.delete("/hyper/{table}")
async def delete(table, request: Request):
    db = router.db
    query_string = request.query_params

    # 有query触发更新
    query = Query(table, query_string)
    if query_string:
        result = await db.execute(query.to_delete_sql())
        return success(result)
    else:
        return error("ERROR: No query string")


# 查所有表
@router.get("/scheme/table")
async def get_tables(db: str):
    db = router.db
    database = db
    tables = await db.tables(database=database)
    return success(tables)


# 查表结构
@router.get("/scheme/table_field")
async def table_struct(name: str):
    db = router.db
    # 指定表
    table = name
    if not table:
        raise ValueError("No table")
    table_info = await db.table_fields(name=table)
    return success(table_info)


# 创建表
@router.post("/scheme/table")
async def create_table(name: str):
    db = router.db
    table = name
    res = await db.create_table(table)
    return success(res)


# 添加字段
@router.post("/scheme/table_field")
async def add_field(request: Request):
    db = router.db
    json = await request.json()
    table = json.get("table")
    field = json.get("field")
    type = json.get("type")

    if not all([table, field, type]):
        return ValueError("Invalid data")
    res = await db.add_field(table=table, field=field, type=type)
    return success(res)


# 删除字段
@router.delete("/scheme/table_field")
async def del_field(request: Request):
    db = router.db
    json = await request.json()
    table = json.get("table")
    field = json.get("field")

    if not all([table, field, type]):
        return ValueError("Invalid data")
    res = await db.drop_field(table=table, field=field)
    return success(res)


# if __name__ == "__main__":
#     uvicorn.run(
#         "db_server:router",
#         host="0.0.0.0",
#         port=8000,
#         reload=True,
#     )
