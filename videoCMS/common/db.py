from videoCMS.conf import clct_category

def getCategoryNameById(id):
    return clct_category.find_one({'categoryId':id}).get('categoryName','Not Found')

def getCategoryIdByName(name):
    return clct_category.find_one({'categoryName':name}).get('categoryId','Not Found')

def getCategoryList():
    return clct_category.distinct('categoryName') 

def getCategoryIdMapName():
    ret = clct_category.find({},{'categoryName':1,'categoryId':1})
    result = {}
    for one in ret:
        result[one['categoryId']] = one['categoryName']
    return result