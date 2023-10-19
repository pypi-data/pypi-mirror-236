import requests
import json
from typing import Any
from ...utils._stdout import print_output
import pandas as pd

class RESTServer():
  """RESTServer to make calls to a ai server instance

  Example:

  ```python
  >>> import ai_server

  # define access keys
  >>> loginKeys = {"secretKey":"<your_secret_key>","accessKey":"<your_access_key>"}

  # create connection object by passing in the secret key, access key and base url for the api
  >>> server_connection = ai_server.RESTServer(access_key=loginKeys['accessKey'], secret_key=loginKeys['secretKey'], base='<Your deployed server Monolith URL>')
  ```
  """
  # register the server for proxy call
  da_server = None

  def __init__(self, access_key:str = None, secret_key:str = None, base:str = None):
    """
    Args:
        access_key (`str`):
            A user's access key is a unique identifier used for authentication and authorization. It will allow users or applications to access specific resources or perform designated actions within an ai-server instance.
        secret_key (`str`):
            A user's confidential and securely stored piece of information that complements an access key, used in cryptographic processes to validate identity and ensure secure communication
        base (`str`):
            main url to access the server api
    """
    self.access_key = access_key
    self.secret_key = secret_key
    self.main_url = base
    self.login()
    self.connected = True
    self.open_insights = set()
    self.cur_insight = self.make_new_insight() # automatically create an insight for the user
    RESTServer.da_server = self
    self.monitors = {}
    
  def login(self):
    """
    register / validate the users secret & access key combination. 
    
    Store the cookies to be used for other api calls after authentication
    """
    import base64
    combined = self.access_key + ":" + self.secret_key
    combined_enc = base64.b64encode(combined.encode('ascii'))
    headers = {'authorization': f"Basic {combined_enc.decode('ascii')}"}
    headers.update({'disableRedirect':'true'})
    #login url
    api_url = "/auth/whoami"
    url = self.main_url + api_url

    self.r = requests.get(url, headers=headers)
    self.r.raise_for_status()

    # display the login response
    print_output(self.r.json())
    self.cookies = self.r.cookies
    # display the cookies
    print_output(self.cookies)
    
  
  def make_new_insight(self) -> str:
    """
    create a new temporal space to operate within the ai-server. An insight is directoly associated with a user
    """
    if not self.connected:
      return "Please login"
    
    pixel_payload = {}
    pixel_payload.update({'expression':'META | true', 'insightId':'new'})
    api_url = "/engine/runPixel"
    response = requests.post(self.main_url + api_url, cookies = self.cookies, data=pixel_payload)

    # raise HTTP error if one occurs
    response.raise_for_status()

    json_output = response.json()
    # display the pixel response
    print_output(json_output)
    
    self.cur_insight = json_output['insightID']
    self.open_insights.add(self.cur_insight)

    print_output(f"Current open insights are -- {self.open_insights}")

    return self.cur_insight
  
  def run_pixel(self, 
                payload:str = None, 
                insight_id:str | None = None, 
                full_response:bool = False):
    '''
    /api/engine/runPixel is the AI server's primary endpoint that consumes a flexible payload. The payload must contain two parameters, namely:
      1.) expression - The @payload passed is placed here and must comply and be defined in the Server's DSL (Pixel) which dictates what action should be taken
      2.) insightId - the temporal workspace identifier which isoloates the actions being performed

    Args:
      payload (`str`):
          DSL (Pixel) instruction on what specific action should be performed 
      insight_id (`str`):
          Unique identifier for the temporal worksapce where actions are being isolated

          insight_id Options are:

            - insight_id = '' -> Creates a temporary one time insight created but is not stored /     cannot be referenced for future state
            - insight_id = 'new' -> Creates a new insight which can be referenced in the same sesssion
            - insight_id = '<uuid/guid string>' -> Uses an existing insight id that exists in the user session

      full_response (`bool`):
          Indicate whether to return the full json response or only the actions output
    '''
    # going to create an insight if insight not available
    if not self.connected:
      return "Please login"
    
    if insight_id is None:
      insight_id = self.cur_insight
       # still null :(
      if insight_id is None:
        print_output("insight_id and self.cur_insight are both undefined. Creating new insight")
        self.cur_insight = self.make_new_insight()
        insight_id = self.cur_insight

    print_output(f"Current insight_id is set to {insight_id}")

    pixel_payload = {}
    pixel_payload.update({'expression':payload})
    pixel_payload.update({'insightId':insight_id})

    api_url = "/engine/runPixel";
    response = requests.post(self.main_url + api_url, cookies = self.cookies, data=pixel_payload)
    if full_response:
      return response.json()
    else:
      return self.get_pixel_output(response.json())
    
  def get_pixel_output(self, payload:dict = None) -> Any | list:
    '''
    Utility method to grab the output of runPixel call
    '''
    print_output(payload)
    main_output = payload['pixelReturn'][0]['output']
    if isinstance(main_output, list):
      output = main_output[0]
    else:
      output = main_output
    return output
    
  def logout(self):
    '''Close the connection'''
    # define the logout endpoint
    api_url = "/logout/all"

    # make the request
    requests.get(self.main_url + api_url, cookies = self.cookies)

    # reset the connection attributes for the class
    self.cookies = None
    self.connected = False

  def send_request(self, input_payload:dict) -> None:
    '''
    Constructs the payload for various server resources such as ModelEngine, StorageEngine and DatabaseEngine when the server is an instance of RESTServer

    Args:
      input_payload (`dict`):
          the actual payload being sent to the AI Server
    '''
    
    # this is a synchronous call
    # but I dont want to bother the server proxy and leave it as is
    epoc = input_payload['epoc']

    input_payload_message = json.dumps(input_payload)
    print_output(input_payload_message)

    # escape the quotes
    #input_payload_message = json.dumps(input_payload_message)
    # RemoteEngineRun is responsible for handling ModelEngine, StorageEngine and DatabaseEngine via RESTServer
    func = "RemoteEngineRun(payload=\"<e>" + input_payload_message + "</e>\");"
    output_payload_message = self.run_pixel(payload=func, insight_id=input_payload['insightId'])
    if epoc in self.monitors:
      condition = self.monitors[epoc]
      self.monitors.update({epoc: output_payload_message})
  
  def get_open_insights(self) -> list:
    '''
    Utility method to get a list of insight IDs the user has created after the connection was made
    '''
    # MyOpenInsights is pre0defined server level reactor to handle the action of getting the insightIds
    open_insights = self.run_pixel(payload = 'MyOpenInsights();')
    
    # keep track of the open insights within the python object itself
    self.open_insights = set(open_insights)

    # return a list of insight ids
    return open_insights
  
  def drop_insights(self, insight_ids: str | list) -> None:
    '''
    Utility method close given insight(s)

    Args:
      insight_ids (`str` | `list`):
          a single insight or a list of insights the user wishes to close

    By Default, the current / working insight is set to the first insight in open_insights
    '''
    if isinstance(insight_ids,list):
      for id in insight_ids:
         self.run_pixel(insight_id = id,payload = 'DropInsight();')
         self.open_insights.discard(id)
    else:
      self.run_pixel(insight_id = insight_ids,payload = 'DropInsight();')
      self.open_insights.discard(insight_ids)

    if (len(self.open_insights) > 0):
       self.cur_insight = self.open_insights[0]
    else:
       self.cur_insight = None

  def import_data_product(self, 
                          project_id:str = None, 
                          insight_id:str = None, 
                          sql:str = None) -> pd.DataFrame | None:
        '''
        If an insight is saved, the data within it becomes a data product and is accessible via a REST API

        Args:
        project_id (`str`):
            Given project/app unique identifier 
        insight_id (`str`):
            Shared insight indentifier.
        sql (`bool`):
            SQL statement that is executable on the frames within the data product

        Returns:
          Pandas Dataframe based on the SQL statement
        '''
        if project_id == None:
            project_id = input('Please enter the Project ID: ')
        if insight_id == None:
            insight_id = input('Please enter the Insight ID: ')

        base_url = self.main_url + '/project-' + project_id + '/jdbc_json?insightId=' + insight_id + '&open=true&sql='
        
        if sql == None:
            sql = input('Please enter the SQL: ')

        dataProductUrl = base_url + sql
        response = requests.get(dataProductUrl, cookies = self.cookies).json()
      
        try:
            return pd.DataFrame(response['dataArray'], columns=response['columns'])
        except:
            try:
                return pd.DataFrame(response['data'], columns=response['columns'])
            except:
                return None