from typing import Any
from .gaas_server_proxy import ServerProxy
from ...utils._stdout import print_output

class ModelEngine(ServerProxy):
  
  def __init__(self, engine_id=None, insight_id=None):
    assert engine_id is not None 
    super().__init__()
    self.engine_id = engine_id
    self.insight_id = insight_id
    print_output("initialized")
    
  def embeddings(self, question = None, insight_id=None, param_dict=None):
    '''
    If I model has embeddings enabled, pass in a string to get the embedded response

    Args:
        question (`str`):
            A user's access key is a unique identifier used for authentication and authorization. It will allow users or applications to access specific resources or perform designated actions within an ai-server instance.
        insight_id (`str`):
            Unique identifier for the temporal worksapce where actions are being isolated
        param_dict (`dict`):
            Optional
    '''
    assert question is not None
    if insight_id is None:
      insight_id = self.insight_id
    assert insight_id is not None
    epoc = super().get_next_epoc()
    return super().call(
                      epoc = epoc, 
                      engine_type='Model', 
                      engine_id=self.engine_id, 
                      insight_id=insight_id, 
                      method_name='embeddings', 
                      method_args=[question, insight_id, param_dict],
                      method_arg_types=['java.lang.String', 'prerna.om.Insight', 'java.util.Map']
                      )
    
  def ask(self, 
          question:str = None, 
          context:str = None, 
          insight_id:str = None, 
          param_dict: dict = None
          ) -> list:
    '''
    Connect to a database an execute SQL against it to create a pandas frame

    Args:
        question (`str`):
            The single string question you are asking a an LLM
        context (`str`):
            Set the given context string for an interaction with an LLM
        insight_id (`str`):
            Unique identifier for the temporal worksapce where actions are being isolated
        param_dict (`dict`):
            Additional inference params like temperature, max new tokens and top_k etc

            *NOTE* you can pass in 
            param_dict = {"full_prompt":full_prompt, "temperature":temp, "max_new_tokens":max_token}
            where full_prompt is the an multi faceted prompt construct before sending the payload

            For OpenAI, this would be a list of dictionaris where the only keys within each dictionary are 'role' and 'content'
            For TextGen, this could be a list simialr to OpenAI or a complete string that has all the pieces pre constructed
    Response:
      A list that contains a dictioanry with the answer to the question, insight id and the message id
    '''
    assert question is not None
    if insight_id is None:
      insight_id = self.insight_id
    # should I assert for insight_id as well I think I should
    assert insight_id is not None    
    epoc = super().get_next_epoc()
    return super().call(
                        epoc=epoc, 
                        engine_type='Model', 
                        engine_id=self.engine_id, 
                        method_name='ask', 
                        method_args=[question,context,insight_id, param_dict],
                        method_arg_types=['java.lang.String', 'java.lang.String', 'prerna.om.Insight', 'java.util.Map'],
                        insight_id = insight_id
                        )
  
  def as_pretrained_model(self):
    from .huggingface.pretrain_wrapper import HuggingFaceConfig, HuggingFacePretrainedModel
    return HuggingFacePretrainedModel(config = HuggingFaceConfig(), model_engine = self)

    
    
  