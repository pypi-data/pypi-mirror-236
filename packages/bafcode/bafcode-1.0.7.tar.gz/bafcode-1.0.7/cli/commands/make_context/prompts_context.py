



class PromptContext:
    @staticmethod
    def snake_to_camel(word):
        """
        Convert snake_case or a single word to CamelCase.
        """
        return ''.join(x.capitalize() for x in word.split('_'))
    

    
    
    def context(prompt_name):
        camel_case_name = PromptContext.snake_to_camel(prompt_name)
        file_context= """ 
        from core import BafLog
        # Optionally, import any other required modules or packages


        class {prompt_name}: # Replace {prompt_name} with the name of your prompt
           
             def {function}(data):
      prompt = {string}

      

            {prompt_name} Data:
            {data}


           {string}
      
      return prompt.format(data=data)

        """

        return file_context.format(prompt_name=camel_case_name, string='"""',function=prompt_name)