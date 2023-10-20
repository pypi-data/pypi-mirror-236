



class ToolContext:
    @staticmethod
    def snake_to_camel(word):
     formatted_word = word.replace('/', '_')
    
     return ''.join(x.capitalize() for x in formatted_word.split('_'))
    
    def context(tool_name):
        camel_case_name = ToolContext.snake_to_camel(tool_name)
        file_context= """ 
from core import BafLog
# Optionally, import any other required modules or packages
# E.g., from api import YourAPI
# E.g., from prompts import YourPrompt

class {tool_name}: # Replace {tool_name} with the name of your tool
  def __init__(self):
     self.logger = BafLog

  def execute(self, data):
    prompt = 'Use your imported prompt here e.g., YourPrompt.your_function(data)' 
    return prompt


        """

        return file_context.replace("{tool_name}", camel_case_name)