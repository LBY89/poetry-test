#reshuffle data structure, adding 'clickable' and 'non_clickable', del 'dev' and 'dependencies'
def deal_clickables(subArray): 
    pkg_name_array = [item['name'] for item in subArray]

    for item in subArray:

        if 'dev' in item and 'dependencies' not in item:
            clickable = []
            non_clickable = []
            # generate an list of strings of pkg
            item_array = item['dev'][1:-1].replace('"', '').split(',')
            item_array = item_array[:1] + [i.lstrip() for i in item_array[1:]]
            item_array = [i[:-10] if "(" and ")" in i else i for i in item_array ]
            
            for i in range(len(pkg_name_array)):
                for j in range(len(item_array)):
                    if pkg_name_array[i] == item_array[j]:
                        clickable.append(item_array[j])
                        
            item["clickable"] = clickable

            for i in item_array:
                if i not in clickable:
                    non_clickable.append(i)
            
            item["non_clickable"] = non_clickable

            del item['dev']

        elif 'dependencies' in item and 'dev' not in item:
            #print('dependencies',item['dependencies'])
            clickable = []
            non_clickable = []
            item_keys = item['dependencies'].keys()
            for i in range(len(pkg_name_array)):
                if pkg_name_array[i] in item_keys:
                    clickable.append(pkg_name_array[i])
            
            for i in item_keys:
                if i not in clickable:
                    non_clickable.append(i)

            item["clickable"] = clickable
            item["non_clickable"] = non_clickable

            del item['dependencies']
        
        elif 'dev' in item and 'dependencies' in item:
            #print('item', item)
            clickable = []
            non_clickable = []

            item_array = item['dev'][1:-1].replace('"', '').split(',')
            item_array = item_array[:1] + [i.lstrip() for i in item_array[1:]]
            item_array = [i[:-10] if "(" and ")" in i else i for i in item_array ]
            
            merge_array = item_array + list(item['dependencies'].keys())
            
            
            for i in range(len(pkg_name_array)):
                for j in range(len(merge_array)):
                    if pkg_name_array[i] == merge_array[j]:
                        clickable.append(merge_array[j])
                    
            #print('clickable',clickable)
            item["clickable"] = clickable
            
            for j in merge_array:
                if j not in clickable:
                    non_clickable.append(j)
            

            item["non_clickable"] = non_clickable          
            
            del item['dependencies']
            del item['dev']

    return subArray

def get_index_positions(list_of_elems, element):#get each sliced array chunck's index, using '[[package]]' as identifier
    index_pos_list = []
    index_pos = 0
    while True:
        try:
            index_pos = list_of_elems.index(element, index_pos)
            index_pos_list.append(index_pos)
            index_pos += 1
        except ValueError as e:
            break

    return index_pos_list

def deal_depenencies(small_list):
    depend_dict = {}
    for chunk in small_list:
        if "dependencies" in chunk and "=" not in chunk:
            
            small_list = small_list[small_list.index(chunk)+1: ]
            for junk in small_list:
                if "[package" in junk:
                    break

                depend_dict[junk[:junk.index("=")-1]] = junk[junk.index("=")+2:].replace('"', '')
            
    return depend_dict
    
# THIS IS the Main function!!!
def toml_parser(filename):
    fileData = {}
    fileArray = []
    result_array = []

    with open(filename, encoding = "ISO-8859-1") as file:

        for line in file:
            line = line.replace("\n", "")
            fileArray.append(line)

    fileArray = list(filter(None, fileArray))
    #get each array chunck's index, using '[[package]]' as identifier
    package_index = get_index_positions(fileArray, "[[package]]")
    #get an array of arrays, each array has all the strings that represents this particular package's information.
    new_file_array = [(fileArray+[''])[slice(ix,iy)] for ix, iy in zip([0]+package_index, package_index+[-1])][1:]
    
    for i in range(len(new_file_array)):
        
        small_dict = {}
        
        for chunk in new_file_array[i]:
            equal_sign_left = chunk[chunk.index("=")+2:]
            if "name" in chunk:
                small_dict["name"] = equal_sign_left.replace('"', '')# put in a varaible
            elif "description" in chunk:
                small_dict["description"] = equal_sign_left.replace('"', '')
            elif "dev =" in chunk:
                small_dict["dev"] = equal_sign_left.replace("'", "")
            elif "dependencies"  in chunk:
                small_dict["dependencies"] = deal_depenencies(new_file_array[i])
        
        result_array.append(small_dict)

    #construct a subArray inside which each item has "dev" or "dependencies"

    subArray = []
    for item in result_array:
        if 'dev' in item or 'dependencies' in item:
            subArray.append(item)
    
    for i in range(len(result_array)):
        for j in range(len(subArray)):
            if 'dev' in subArray[j]:
                if result_array[i]['name'] in subArray[j]['dev']:
                    result_array[i]['reverseDep'] = subArray[j]['name']
            elif 'dependencies' in subArray[j]:
                if result_array[i]['name'] in subArray[j]['dependencies']:
                    result_array[i]['reverseDep'] = subArray[j]['name']
            elif 'dev' and 'dependencies' in subArray[j]:
                if result_array[i]['name'] in subArray[j]['dependencies'] or result_array[i]['name'] in subArray[j]['dev']:
                    result_array[i]['reverseDep'] = subArray[j]['name']

    # deal_clickable restructure each package obj, where 'dev' and 'dependencies' properties were deleted, 
    #'clickable' and 'non_clicable' properties added
    fileData["package"] = deal_clickables(result_array)

    return fileData