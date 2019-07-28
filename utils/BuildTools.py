from pydash import objects, arrays
import json


def buildTop(data):
    '''
    构建swagger顶层目录结构
    :param data: swagger原始返回的信息
    :return:返回顶层元组信息
    '''
    dataObj = json.loads(data)
    tags = objects.get(dataObj, 'tags', [])
    tops = arrays.compact(tags)
    tops = arrays.mapcat(tops, lambda item: objects.assign(objects.clone(item), {'child': []}))

    return tops;


def getTagsFromPath(path):
    wayKey = ['get', 'post', 'patch', 'put', 'delete']

    for key in wayKey:
        if objects.get(path, key) != None:
            return path[key]['tags'][0]
    return None


def buildChild(data, tags):
    '''
    构建child接口组
    :param data: 原始数据
    :param tasg: buildTop构建的tags组
    :return: 带有child信息的tags组
    '''
    dataObj = json.loads(data)
    tagsObj = objects.clone_deep(tags)

    #         tagsIndex = arrays.find_index(tagsObj, lambda tagItem: tagItem[''] == item[''])

    # 遍历 tags ,嵌套遍历paths将对应的连接挂在到tags下的child中

    paths = objects.get(dataObj, 'paths')
    for tag in tagsObj:
        for path in paths:
            if tag['name'] == getTagsFromPath(paths[path]):
                tag['child'].append(paths[path])

    arrays.mapcat(tagsObj, lambda tag: tag)
    return tagsObj
