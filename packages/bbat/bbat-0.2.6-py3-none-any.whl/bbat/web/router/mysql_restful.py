
from fastapi import APIRouter, Request
from bbat.web.url_to_sql.query import Query
from bbat.db.aio_mysql import Mysql
from bbat.web.router.utils import success, error

router = APIRouter()


# get方法查询函数
@router.get("/hyper/{table}")
async def query(table: str, request: Request):
    db: Mysql = request.app.db
    query_string = request.query_params

    result = {}
    query = Query(table, query_string)

    sql = query.to_sql()
    print('>>>', sql)
    # 1.主表查询
    data = await db.query(sql)
    # 根据field定义，做数据处理
    data = query.data_convert(query.fields, data)
    # 2.统计查询
    count_sql = query.to_count_sql()
    info = await db.fetch(count_sql)
    result["total"] = info["cnt"] if info else 0
    result["page_num"] = query.page
    result["page_size"] = query.size
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
    db: Mysql = request.app.db
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
    db: Mysql = request.app.db
    query_string = request.query_params

    # 有query触发更新
    query = Query(table, query_string)
    if query_string:
        result = await db.execute(query.to_delete_sql())
        return success(result)
    else:
        return error("ERROR: No query string")