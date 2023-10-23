from tag_reader.tag_elemnts.tag_element_dict import ChildTagElement
from tag_reader.tag_layouts import TagLayouts
from tag_reader.tag_elemnts.tag_element_type import TagElemntType
from tag_reader.tag_elemnts.tag_element import ComplexTagElement, TagElement


class TagElementList(ComplexTagElement):
    def __init__(self, layout: TagLayouts.C) -> None:
        super().__init__(layout)
        self.array : [ChildTagElement]= None
        self.count: int = -1

    def readTagElemnt(self, f, address, field_offset, entry, parent):
        self.array = []
        # self.count
        pass
   

class ResourceHandleTagElement(TagElementList):
    def __init__(self, layout: TagLayouts.C) -> None:
        super().__init__(layout)
        assert layout.T == TagElemntType.ResourceHandle

    def readTagElemnt(self, f, address, field_offset, entry, parent):
        super().readTagElemnt(f, address, field_offset, entry, parent)
        # self.count
        pass

class BlockTagElement(TagElementList):
    def __init__(self, layout: TagLayouts.C) -> None:
        super().__init__(layout)  
        assert layout.T == TagElemntType.Block
    
    def readTagElemnt(self, f, address, field_offset, entry, parent):
        super().readTagElemnt(f, address, field_offset, entry, parent)
        # self.count
        pass

class ArrayTagElement(TagElementList):
    def __init__(self, layout: TagLayouts.C) -> None:
        super().__init__( layout)    
        assert layout.T == TagElemntType.Array


            
