from videoCMS.conf import clct_category

def getCategoryNameById(id):
    result = clct_category.find_one({'categoryId':id})
    if not result:
        return 'Not Found'
    return result['categoryName']


def getCategoryIdByName(name):
    result = clct_category.find_one({'categoryName':name})
    if not result:
        return 'Not Found'
    return result['categoryId']

def getCategoryList():
    return clct_category.distinct('categoryName') 

def getCategoryIdMapName():
    ret = clct_category.find({},{'categoryName':1,'categoryId':1})
    result = {}
    for one in ret:
        result[one['categoryId']] = one['categoryName']
    return result