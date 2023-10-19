from .gaas_server_proxy import ServerProxy
from ...utils._stdout import print_output

class DatabaseEngine(ServerProxy):
  
  def __init__(self, engine_id:str = None, insight_id:str = None):
    assert engine_id is not None 
    super().__init__()
    self.engine_id = engine_id
    self.insight_id = insight_id
    print_output("initialized")
   
  def execQuery(self, 
                query:str = None, 
                insight_id:str = None, 
                return_pandas:bool = True, 
                server_output_format:str = 'json'):
    '''
    Connect to a database an execute SQL against it to create a pandas frame

    Args:
        query (`str`):
            A user's access key is a unique identifier used for authentication and authorization. It will allow users or applications to access specific resources or perform designated actions within an ai-server instance.
        insight_id (`str`):
            Unique identifier for the temporal worksapce where actions are being isolated
        return_pandas (`bool`):
            true/false flag for creating a pandas frame
        server_output_format (`str`):
            Define wheter to write the query result to a file or json. *Note*, if file is selected then its only accessible via server UI
    '''
    assert query is not None
    if insight_id is None:
      insight_id = self.insight_id
    assert insight_id is not None
    epoc = super().get_next_epoc()
    fileLoc = super().call(
                      epoc = epoc, 
                      engine_type='database', 
                      engine_id=self.engine_id, 
                      insight_id=insight_id, 
                      method_name='execQuery', 
                      method_args=[query, server_output_format],
                      method_arg_types=['java.lang.String', 'java.lang.String']
                      )
    if isinstance(fileLoc, list) and len(fileLoc) > 0:
      fileLoc = fileLoc[0]
    if return_pandas:
      print_output(f"The output is {fileLoc}")
      import pandas as pd
      print_output(fileLoc)
      if isinstance(fileLoc, dict) and len(fileLoc) > 0:
        rows = []
        # saftey check based on how java gson structure the response
        if 'myArrayList' in fileLoc.keys() and {rows.append(d[key]) if key =='map' else "notMap" for d in fileLoc['myArrayList'] for key in d.keys()} == {None}:
          return pd.DataFrame.from_dict(rows)
      elif isinstance(fileLoc, str):
        return pd.read_json(fileLoc)
      else:
        return fileLoc
    else:
      if isinstance(fileLoc, dict) and len(fileLoc) > 0:
        return fileLoc
      else:  
        return open(fileLoc, "r").read()


  def insertData(self, query:str = None, insight_id:str = None):
    '''
    Connect to a database an execute SQL against it to insert data

    Args:
        query (`str`):
            A SQL statement to insert values into a table
        insight_id (`str`):
            Unique identifier for the temporal worksapce where actions are being isolated
    '''
    assert query is not None
    if insight_id is None:
      insight_id = self.insight_id
    assert insight_id is not None
    epoc = super().get_next_epoc()
    return super().call(
                      epoc = epoc, 
                      engine_type='database', 
                      engine_id=self.engine_id, 
                      insight_id=insight_id, 
                      method_name='insertData', 
                      method_args=[query],
                      method_arg_types=['java.lang.String']
                      )


  def removeData(self, query:str = None, insight_id:str = None):
    '''
    Connect to a database an execute SQL against it to remove data

    Args:
        query (`str`):
            A SQL statement like DELETE FROM diab WHERE age=19
        insight_id (`str`):
            Unique identifier for the temporal worksapce where actions are being isolated
    '''
        
    assert query is not None
    if insight_id is None:
      insight_id = self.insight_id
    assert insight_id is not None
    epoc = super().get_next_epoc()
    return super().call(
                      epoc = epoc, 
                      engine_type='database', 
                      engine_id=self.engine_id, 
                      insight_id=insight_id, 
                      method_name='removeData', 
                      method_args=[query],
                      method_arg_types=['java.lang.String']
                      )

  
    
