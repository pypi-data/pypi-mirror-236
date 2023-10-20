



class ApiContext:
    def context(api_name):
      
        file_context= """ 
            import requests
            from core import BafLog

            YOUR_API_ENDPOINT = "https://fakerapi.it/api/v1/texts?_quantity=1&_characters=500"  # Placeholder email API endpoint

            def {api_name}('Pass any required parameters here e.g., user_id=None'):

                logger = BafLog

                
                params = ' Pass any required parameters here e.g., {'user_id': user_id}'
                response = requests.get(YOUR_API_ENDPOINT, params=params)

                # Handle API response
                if response.status_code != 200:
                    logger.error(f"Error fetching last email for user {user_id}. API response: {response.text}")
                    raise Exception(f"Error fetching last email. API responded with: {response.text}")

                your_data_variable = response.json()
                return your_data_variable
        """

        return file_context.replace("{api_name}", api_name)