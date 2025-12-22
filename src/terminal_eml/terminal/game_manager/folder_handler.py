import os, shutil, sys

## Simple renaming class ##
class FolderHandler:
    def __init__(self, folder_path:str) -> None:
        self.folder = folder_path
    
    def reselect_folder(self, folder_path:str):
        self.folder = folder_path
    

    def select_destination_target(self, folder_path:str):
        self.destination_target = folder_path

    def select_target(self, target:str):
        self.selected_target = f"{self.folder}/{target}"
    
    # Renamed shutil functions #
    def move_target(self):
        shutil.move(self.selected_target, self.destination_target)
    
    def clone_move_target(self):
        shutil.copy(self.selected_target, self.destination_target)
    
    # Renamed os functions #
    def rename_target(self):
        os.renames(self.selected_target, self.destination_target)
    
    def delete_target(self):
        os.remove(self.selected_target)

def cache(string:str, where:str):
    "where: folder/file ; .cache is added automatically"
    with open(f"{where}.cache", "r") as c:
        if string in c.readlines(): return
    with open(f"{where}.cache", "a") as c:
        c.write(f"\n{string}")