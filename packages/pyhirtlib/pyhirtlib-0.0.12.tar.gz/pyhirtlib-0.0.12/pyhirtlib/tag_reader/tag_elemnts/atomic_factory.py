from abc import ABC, abstractmethod
from tag_reader.tag_elemnts.tag_element_type import TagElemntType
from tag_reader.tag_elemnts.tag_element_atomic import TagElementAtomic

from tag_reader.tag_layouts import TagLayouts


class BaseAtomicFactory(ABC):
    def __init__(self,) -> None:
        super().__init__()

    @abstractmethod
    def getTagElemnt(self, layout:TagLayouts.C) -> TagElementAtomic :
        pass



    
