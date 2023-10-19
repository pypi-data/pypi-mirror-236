from transformers import PreTrainedModel, PretrainedConfig

class HuggingFaceConfig(PretrainedConfig):
    model_type = 'ai_server_model'

    def __init__(self, important_param=3, **kwargs):
        super().__init__(**kwargs)
        self.important_param = important_param

class HuggingFacePretrainedModel(PreTrainedModel):
    config_class = HuggingFaceConfig
    
    def __init__(self, model_engine, **kwargs):
        super().__init__()
        self.server_connection = None
        self.model = model_engine
        
    def forward(self, input, **kwargs):
        return self.model.ask(question = input, **kwargs)
