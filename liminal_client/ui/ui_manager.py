from .widget_type import WidgetType

class WidgetManager:
    widgets: dict[int,tuple[WidgetType,list[str],list[str]]] = {}
    idx: int = 0

    @classmethod
    def get_widgets(cls):
        for k,(widget,tags,ids) in cls.widgets.items():
            yield widget,(tags if len(tags) > 0 else "all"), (ids if len(ids) > 0 else "")

    @classmethod
    def add(cls,widget:WidgetType):
        cls.widgets.update({cls.idx:(widget,["all"],[])})
        widget._id = cls.idx
        cls.idx += 1
    
    @classmethod
    def tag(cls,tag:str,w:WidgetType):
        widget,tags,ids = cls.widgets[w._id]
        tags.append(tag)
        cls.widgets[w._id] = (widget,tags,ids)
    @classmethod
    def id(cls,id:str,w:WidgetType):
        widget,tags,ids = cls.widgets[w._id]
        ids.append(id)
        cls.widgets[w._id] = (widget,tags,ids)

    @classmethod
    def get_all_widgets(cls):
        "Returns all widgets"
        for id,(widget,tags,ids) in cls.widgets.items():
            yield id,widget,tags,ids
    @classmethod
    def get_widgets_by_class(cls,c:type[WidgetType]):
        "Returns all instances of class"
        for id,(widget,tags,ids) in cls.widgets.items():
            if isinstance(widget,c):
                yield id,widget,tags,ids
    @classmethod
    def get_widgets_by_tag(cls,tag:str):
        "Returns all instances of widgets with tag"
        for id,(widget,tags,ids) in cls.widgets.items():
            if tag in tags:
                yield id,widget,tags,ids
    @classmethod
    def get_widget_by_id(cls,id:str):
        "Returns first instance of id"
        for _id,(widget,tags,ids) in cls.widgets.items():
            if id in ids:
                return id,widget,tags,ids