



class LlmContext:
    @staticmethod
    def snake_to_camel(word):
        """
        Convert snake_case or a single word to CamelCase.
        """
        return ''.join(x.capitalize() for x in word.split('_'))
    
    def context(llm_name):
        camel_case_name = LlmContext.snake_to_camel(llm_name)
        file_context= """ 
        from core import BafLog
        from config import Config
        # Optionally, import any other required modules or packages
        # E.g., from api import YourLLMAPI


        class {llm_name}:
            def __init__(self):
                self.logger = BafLog

                # Initialize your LLM API config here
               

            def process(self,message,prompt):
            
                if not prompt:
                    self.logger.error("No prompt provided for OpenAI LLM.")
                    raise ValueError("A prompt is required for processing.")

                try:
                    # use your LLM API and pass in the prompt and message to process here
                    response = 'Use your LLM API here e.g., YourLLMAPI.process(prompt,message)'
                    return response
                    # Response should be a string e.g., "This is a response from the LLM API."

                except Exception as e:
                    self.logger.error(f"Error processing with OpenAI LLM: {str(e)}")
                    return {
                        'message': "Error processing with OpenAI LLM.",
                        'status': "error"
                    }


        """

        return file_context.replace("{llm_name}", camel_case_name)