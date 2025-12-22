class Translatable:
    """## Translatable BaseClass
    used in WidgetClass, Translatable inheritance for Forced Polymorphism"""
    def __init__(self, translation_manager, key) -> None:
        if "." in key:
            raise ValueError(f"Argument key does not allow periods, key:{key} is not allowed")
        self._translation_key = key
        "used internally"
        self.translation_manager = translation_manager
        self.translation_manager._text_likes.update({self._get_translation_key(): self}) # good

    def _get_translation_key(self) -> str:
        """helps the TranslationManager find the key more easily"""
        return ""

    def _translate(self, value:str) -> None:
        """Internal helper-function"""
        return