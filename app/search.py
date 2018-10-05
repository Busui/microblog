from flask import current_app


def add_to_index(index, model):
    if not current_app.elasticsearch:
        return
    payload = {}
    for field in model.__searchable__:
        payload[field] = getattr(model, field)
    current_app.elasticsearch.index(index = index, doc_type = index, 
                                    id = model.id, body = payload)


def remove_from_index(index, model):
    if not current_app.elasticsearch:
        return
    current_app.elasticsearch.delete(index = index, doc_type = index, id = model.id)


def query_index(index, query, page, per_page):
    if not current_app.elasticsearch:
        return [], 0
    search = current_app.elasticsearch.search(
        index=index, doc_type=index,
        body={'query': {'multi_match': {'query': query, 'fields': ['*']}},
              'from': (page - 1) * per_page, 'size': per_page})
    ids = [int(hit['_id']) for hit in search['hits']['hits']]
    return ids, search['hits']['total']



# 在目前，query_index返回5个result.  而from参数表示页数，size表示每页大小。
# --------------------------------------------------------------------

# ###  <如何每页大小为5，则只有一页，第二页已经为空了>
# >>> query_index('posts', 'one two three four five', 1, 5)
# ([30, 32, 33, 29, 31], 5)
# >>> query_index('posts', 'one two three four five', 2, 5)
# ([], 5)

# ### <如果每页大小为1， 那么有5页，每页只有一个结果>
# >>> query_index('posts', 'one two three four five', 1, 1)
# ([30], 5)
# >>> query_index('posts', 'one two three four five', 2, 1)
# ([32], 5)
# >>> query_index('posts', 'one two three four five', 3, 1)
# ([33], 5)
# >>> query_index('posts', 'one two three four five', 4, 1)
# ([29], 5)
# >>> query_index('posts', 'one two three four five', 5, 1)
# ([31], 5)

# ### <如果每页大小为2， 那么有3页， 第1,2页有两个结果，最后一页只有一个结果>
# >>> query_index('posts', 'one two three four five', 1, 2)
# ([30, 32], 5)
# >>> query_index('posts', 'one two three four five', 2, 2)
# ([33, 29], 5)
# >>> query_index('posts', 'one two three four five', 3, 2)
# ([31], 5)