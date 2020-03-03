import importlib
import inspect
import json
import jsondiff

def module_inspection(module_name, inner_class=None):
    mapping = {}
    module = importlib.import_module(module_name)
    if inner_class is None:
        members = inspect.getmembers(module)
        mapping['ModuleName'] = module_name
    else:
        members = eval(f'inspect.getmembers(module.{inner_class})')
        
    mapping['Modules'] = {o[0]:{} for o in members if inspect.ismodule(o[1])}
    mapping['Classes'] = {o[0]:{} for o in members if inspect.isclass(o[1])}
    mapping['Methods'] = {o[0]:{} for o in members if inspect.ismethod(o[1])}
    mapping['Functions'] = {o[0]:{} for o in members if inspect.isfunction(o[1])}
    mapping['Builtins'] = {o[0]:{} for o in members if inspect.isbuiltin(o[1])}
    mapping['GeneratorFunctions'] = {o[0]:{} for o in members if inspect.isgeneratorfunction(o[1])}
    mapping['Generators'] = {o[0]:{} for o in members if inspect.isgenerator(o[1])}
    mapping['CoroutineFunctions'] = {o[0]:{} for o in members if inspect.iscoroutinefunction(o[1])}
    mapping['Coroutines'] = {o[0]:{} for o in members if inspect.iscoroutine(o[1])}
    mapping['Awaitables'] = {o[0]:{} for o in members if inspect.isawaitable(o[1])}
    mapping['AsyncGenerators'] = {o[0]:{} for o in members if inspect.isasyncgen(o[1])}
    mapping['Tracebacks'] = {o[0]:{} for o in members if inspect.istraceback(o[1])}
    mapping['Frames'] = {o[0]:{} for o in members if inspect.isframe(o[1])}
    mapping['Code'] = {o[0]:{} for o in members if inspect.iscode(o[1])}
    mapping['Routines'] = {o[0]:{} for o in members if inspect.isroutine(o[1])}
    mapping['Abstract'] = {o[0]:{} for o in members if inspect.isabstract(o[1])}
    mapping['MethodDescriptor'] = {o[0]:{} for o in members if inspect.ismethoddescriptor(o[1])}
    mapping['DataDescriptor'] = {o[0]:{} for o in members if inspect.isdatadescriptor(o[1])}
    mapping['GetSetDescriptor'] = {o[0]:{} for o in members if inspect.isgetsetdescriptor(o[1])}
    mapping['MemberDescriptor'] = {o[0]:{} for o in members if inspect.ismemberdescriptor(o[1])}

    return mapping

def map_detailing(module_name, mapping, signature=True, doc=True, sourcelines=True, module=True):
        module = importlib.import_module(module_name)
        for entry in mapping:
            if type(mapping[entry]) is not dict:
                continue
            for subentry in mapping[entry]:
                if signature is True:
                    try:
                        mapping[entry][subentry]['Signature'] = str(eval(f'inspect.signature(module.{subentry})'))
                    except:
                        # mapping[entry][subentry]['Signature'] = 'Not Callable'
                        pass
                if doc is True:
                    try:
                        mapping[entry][subentry]['Doc'] = str(eval(f'inspect.getdoc(module.{subentry})'))
                    except:
                        pass
                if sourcelines is True:
                    try:
                        mapping[entry][subentry]['SourceLines'] = str(eval(f'inspect.getsourcelines(module.{subentry})'))
                    except:
                        pass
                if module is True:
                    try:
                        mapping[entry][subentry]['Module'] = str(eval(f'inspect.getmodule(module.{subentry})'))
                    except:
                        pass
        return mapping

def clean_mapping(mapping):
    keys_to_del = []
    for key in mapping:
        if not bool(mapping[key]):
            keys_to_del.append(key)
    for key in keys_to_del:
        del mapping[key]
    
    return mapping

def inner_inspection(module_name, dict_tag, mapping, clean=True):
    for class_inspect in mapping[dict_tag]:
            mapping[dict_tag][class_inspect]['Inner'] = module_inspection(module_name, inner_class=class_inspect)
            mapping[dict_tag][class_inspect]['Inner'] = map_detailing(module_name, mapping[dict_tag][class_inspect]['Inner'])
            if clean is True:
                mapping[dict_tag][class_inspect]['Inner'] = clean_mapping(mapping[dict_tag][class_inspect]['Inner'])
    
    return mapping    

def map_module(module_name, output_name='', inner_mapping=['Modules', 'Classes'], clean=True):
    mapping = module_inspection(module_name)
    mapping = map_detailing(module_name, mapping)

    for tag in inner_mapping:
        mapping = inner_inspection(module_name, tag, mapping, clean=clean)

    if clean is True:
        mapping = clean_mapping(mapping)    

    if output_name == '':
        with open(f'{module_name}_modulemap.json', 'w') as outfile:
            json.dump(mapping, outfile, indent=4)
    else:
        with open(f'{output_name}.json', 'w') as outfile:
            json.dump(mapping, outfile, indent=4)

def compare_module_maps(baseline_map, new_map):
    # TODO Add printing of differences in nice format

    print(f"\n\nBaseline map: {baseline_map}")
    print(f"New map: {new_map}")

    with open(baseline_map, 'r') as json_file:
        baseline_data = json.load(json_file)
    with open(new_map, 'r') as json_file:
        new_data = json.load(json_file)
        
    return jsondiff.diff(baseline_data, new_data)
    