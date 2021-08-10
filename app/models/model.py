class Models:
    def get_model_response(self, data_shoes):
        return {
            'info': {
                'count': str(len(data_shoes))
                },
            'results': data_shoes
        }
    
