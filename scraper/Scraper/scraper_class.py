class Recipe_Scraper():
    urlList:list[str] = []
    def __init__(self) -> None:
        raise NotImplementedError()
        
    
    def get_formatted_recipes(self):
        raise NotImplementedError()
        
    def get_formatted_recipe(self,url:str):
        raise NotImplementedError()
        
        