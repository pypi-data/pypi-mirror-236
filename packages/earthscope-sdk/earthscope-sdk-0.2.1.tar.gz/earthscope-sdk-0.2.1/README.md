# EarthScope SDK

An SDK for authenticating with the EarthScope API

## Getting Started

### USAGE

1. **(Optional) Suggest setting up and activating a python virtual environment so as not to clutter your system python**

   ```shell
   python3 -m venv venv
   . venv/bin/activate
   ```

2. **Install earthscope-sdk**

   ```shell
   pip install earthscope-sdk
   ```
   For developers:
   ```bash
   pip -e install earthscope-sdk[dev]
   ```
   
3. **Create/Use required subclasses**
   \
   To use the **Device Authorization Flow** you will need to create a subclass of the DeviceCodeFlow class. Similarly, to use
   the **Machine-to-Machine Client Credentials Flow** you will need to create a subclass of the ClientCredientialFlow class.

   Simple subclasses exist for your use that you can import and use which will allow for locally loading and saving access tokens:
   *DeviceCodeFlowSimple* and *ClientCredentialsFlowSimple* (see below for examples on useage)
   <br/><br/>
   Creating your own subclass:
    \
   Implementing the following methods in the subclass is required:
   * `load_tokens` should implement the ability to load saved tokens
   * `save_tokens` should implement the ability to save tokens locally
   
   additionally for DeviceCodeFlow only:
   * `prompt_user` should provide the user with the SSO authorization uri

   You will need to instantiate your subclass with the following instance attributes:

   For DeviceCodeFlow:
   * `audience`, `domain`, `client_id`, and `scope`.

   For ClientCredentialsFlow:
   * `audience`, `client_credentials`, and `domain`.
   
      where client_credentials contains the machine-to-machine `client_id` and `client_secret`.

   These values are all obtained from [Auth0](https://manage.auth0.com/).
   <br/><br/>
4. **Use the SDK**
   \
   You can now use the subclasses to define actions such as logging in/out, retrieving or refreshing access tokens, etc...
   \
   **NOTE: Never share your access token or refresh tokens**
   
   Additionally, once the subclasses have been instantiated, you can pass your access token as a parameter to retrieve
   your user/anonymous user information using the earthscope_sdk.user.user *get_user* and *lookup_anon* functions.
  
 
5. **Example usage:**
   \
   Note: To see an example of an application using this SDK (and creating custom subclass), check out the [EarthScope CLI Repository](https://gitlab.com/earthscope/public/earthscope-cli).
   <br/><br/>
   How to use the existing simple subclass for device code flow:
   \
   *simple example python code*:
    ```
    import requests
    from pathlib import Path
     
    from earthscope_sdk.auth.device_code_flow import DeviceCodeFlowSimple
    from earthscope_sdk.auth.auth_flow import NoTokensError
    
   # choose where you want the token saved - the default file name is sso_tokens.json
   # if you want to keep the default name, set the path to a directory. Include a file name to rename. 
   token_path = "/Users/my_user/token_dir"
   
   url = "https://data.unavco.org/path/to/data_file"
   # example: "https://data.unavco.org/archive/gnss/rinex/obs/2022/298/ar272980.22d.Z"
   
    # instantiate the device code flow subclass
    device_flow = DeviceCodeFlowSimple(Path(token_path))
    try:
        # get access token from local path
        device_flow.get_access_token_refresh_if_necessary()
    except NoTokensError:
        # if no token was found locally, do the device code flow
        device_flow.do_flow()
    token = device_flow.access_token
     
    # request a file and provide the token in the Authorization header
   file_name = Path(url).name
   directory_to_save_file = Path.cwd() # where you want to save the downloaded file 
   
    r = requests.get(url, headers={"authorization": f"Bearer {token}"})
    if r.status_code == requests.codes.ok:
        # save the file
        with open(Path(directory_to_save_file / file_name), 'wb') as f:
            for data in r:
                f.write(data)
    else:
        #problem occured
        print(f"failure: {r.status_code}, {r.reason}")
     ```
   
   Instantiate the subclass and set the token_path where you want to load/save the token. 
   If you provide only a directory, the file will be saved as sso_tokens.json. 
   We hard-code this variable in this simple example, but we recommend setting this path as an environment variable and 
   reading the environment varibale in your code.


   the **get_access_token_refresh_if_necessary** method will retrieve the token and refresh the token if it is expired. 
   If there is no token, then the **do_flow** method will begin the device code flow and once you complete the flow, 
   the token will be saved at the token_path. You can use the **requests** library to download the file you want 
   (or files in a loop) and pass in the access token in the Authorization header. 
   
Learn more about [data access methods](https://www.unavco.org/data/gps-gnss/data-access-methods/data-access-methods.html).
