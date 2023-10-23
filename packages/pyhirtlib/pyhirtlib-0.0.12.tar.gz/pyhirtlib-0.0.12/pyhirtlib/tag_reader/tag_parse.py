from commons.to_debug import NoDataStartedStruct
from commons.exception.read_tag_struct_exception import ReadTagStructException
from tag_reader.tag_elemnts.tag_element_reader import TagElementReader
from tag_reader.tag_elemnts.tag_element import ComplexTagElement, TagElement
from tag_reader.tag_elemnts.tag_element_dict import ChildTagElement, RootTagElement
from tag_reader.headers.tag_struct_table import TagStruct
from tag_reader.tag_elemnts.tag_element_type import BLOCKS, TagElemntType, TagStructType
from tag_reader.tag_layouts import TagLayouts
from tag_reader.tag_file import  TagFile
from events import Event

class TagFileMap:
    def __init__(self):
        self.blocks:{int, ComplexTagElement} = {}
        self.datas = {}
        self.refers = {}
        
class TagParse:
    def __init__(self, group:str):
        self.debug = False
        self.tagFile = TagFile()
        self.tagRootElemnt : RootTagElement= None
        self.reader : TagElementReader = None
        self.tagFile.evetToCall = self.doSomeOn
        self.tagFile.tag_struct_table.AddSubscribersForOnEntryRead(self.onEntryRead)
        self.group = group
        self.xml_template =None
        self.tag_structs_list : {int,TagFileMap} = {}
        self.onFieldRead = Event()
        self.onStructRead = Event()

    def AddSubscribersForOnFieldRead(self, objMethod):
        self.onFieldRead += objMethod

    
    def RemoveSubscribersForOnFieldRead(self, objMethod):
        self.onFieldRead -= objMethod

    def AddSubscribersForOnStructRead(self, objMethod):
        self.onStructRead+= objMethod

    
    def RemoveSubscribersForOnStructRead(self, objMethod):
        self.onStructRead -= objMethod

    def readIn(self, f, p_xml_tamplate = None):
        if p_xml_tamplate is None:
            self.xml_template = TagLayouts.Tags(self.group)
        #self.tag_structs_list[0]=self.xml_template[0]
        self.tagFile.readIn(f)
        
        #tagFile.readInOnlyHeader(f_t)

    def doSomeOn(self, params):
        pass

    def onEntryRead(self, f, entry: TagStruct):
        if not (entry is None):
            if entry.field_data_block_index == -1:
                pass
                #return
            
            tag: ComplexTagElement = None
            if entry.type_id_tg != TagStructType.Root:
                tag = self.tag_structs_list[entry.parent_entry_index].blocks[entry.field_offset]
                if (tag.L.T == TagElemntType.Struct):
                    if entry.type_id_tg != TagStructType.NoDataStartBlock:
                        raise ReadTagStructException(str(f), entry)
                
                if tag.L.E["hash"].upper() != entry.GUID.upper():
                    print("No equal hash")
            else:
                self.tagRootElemnt=RootTagElement(self.xml_template[0])
                tag = self.tagRootElemnt
                tag.readTagElemnt(f, 0, entry.field_data_block.offset_plus, entry, None)
                self.onFieldRead( f, 0, 0, 0, 0, entry, tag)
                

            
            outresult = TagFileMap()
            
            if entry.info.n_childs != -1:
                if tag.L.T == TagElemntType.RootTagInstance:
                    self.readTagDefinition(f, 0, 0,entry,tag.L, tag, outresult,0)
                else:
                    for x in range(entry.info.n_childs): 
                        sub_child_elemnt = ChildTagElement(tag.L)
                        s = self.readTagDefinition(f, x, 0,entry,tag.L, sub_child_elemnt, outresult,int(tag.L.E['size'])*x)
                        tag.array.append(sub_child_elemnt)
            else:
                pass
            self.tag_structs_list[entry.entry_index] = outresult
            if self.debug:
                if tag.L.T == TagElemntType.RootTagInstance:
                    assert(tag.L.E["hash"]==  entry.GUID.upper())
                    assert(entry.type_id_tg == TagStructType.Root)
                else:
                    assert tag.L.E["hash"]==entry.GUID.upper(), f"No equal hash {tag.L.E['hash']} == {entry.GUID.upper()}"
        pass
        
    def readTagDefinition(self,f, i, k, entry: TagStruct, tags: TagLayouts.C, parent: ComplexTagElement,outresult: TagFileMap, field_offset:int = 0) -> int:
        result = 0
        self.onStructRead(i,k,tags,True)
        for address in tags.B:
            child_tag = tags.B[address]
            child_tag_elemt = self.reader.getTagElemnt(child_tag)
            result+= child_tag.S
            parent.dict[child_tag.N] = child_tag_elemt
            child_tag_elemt.readTagElemnt(f, address, field_offset + entry.field_data_block.offset_plus, entry, parent)
            self.onFieldRead(f, address, field_offset, entry, child_tag, parent)
            self.verifyAndAddTagBlocks(outresult, child_tag_elemt, field_offset + address)
            if child_tag.T == TagElemntType.Struct:
                self.readTagDefinition(f, i, k, entry, child_tag, child_tag_elemt, outresult, field_offset + address)
            elif child_tag.T == TagElemntType.Array:
                for _k in range(child_tag.E["count"]):
                    sub_child_elemnt = ChildTagElement(child_tag)
                    self.readTagDefinition(f, i, _k, entry, child_tag, sub_child_elemnt, outresult, field_offset + address)
                    child_tag_elemt.array.append(sub_child_elemnt)
        self.onStructRead(i,k,tags,False)
        return result

    def verifyAndAddTagBlocks(self, tag_maps: TagFileMap, child_item: TagElement, field_offset: int):
        if child_item.L.T == TagElemntType.Data:
            tag_maps.datas[field_offset] = child_item
            return
        elif child_item.L.T == TagElemntType.TagReference:
            tag_maps.refers[field_offset] = child_item
            return
        elif child_item.L.T == TagElemntType.Struct:
            if child_item.L.E["comp"] == "1" : 
                tag_maps.blocks[field_offset] =  child_item
            return
        elif child_item.L.T == TagElemntType.Block:
            tag_maps.blocks[field_offset] =  child_item
            return
        elif child_item.L.T == TagElemntType.ResourceHandle:
            tag_maps.blocks[field_offset] =  child_item
            return
        else:
            return