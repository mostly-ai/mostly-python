# swagger_client.ConnectorApi

All URIs are relative to */*

Method | HTTP request | Description
------------- | ------------- | -------------
[**create_connector**](ConnectorApi.md#create_connector) | **POST** /connectors | Create a new connector
[**delete_connector**](ConnectorApi.md#delete_connector) | **DELETE** /connectors/{connectorId} | Deletes a connector
[**get_connector_by_id**](ConnectorApi.md#get_connector_by_id) | **GET** /connectors/{connectorId} | Read a connector by ID
[**get_connector_locations**](ConnectorApi.md#get_connector_locations) | **GET** /connectors/{connectorId}/locations | Read locations from connector
[**get_connectors**](ConnectorApi.md#get_connectors) | **GET** /connectors | List connectors
[**list_objects**](ConnectorApi.md#list_objects) | **GET** /connectors/{connectorId}/list | List object from a connector.
[**test_connection**](ConnectorApi.md#test_connection) | **POST** /connectors/test | Test the connection of a connector
[**test_connection_by_id**](ConnectorApi.md#test_connection_by_id) | **POST** /connectors/{connectorId}/test | Test the connection of a connector
[**update_connector_by_id**](ConnectorApi.md#update_connector_by_id) | **PUT** /connectors/{connectorId} | Updates a connector or creates a new one with a specified ID

# **create_connector**
> Connector create_connector(body)

Create a new connector

### Example
```python
from __future__ import print_function
import time
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = swagger_client.ConnectorApi()
body = swagger_client.Connector() # Connector | Data for creating a new connector

try:
    # Create a new connector
    api_response = api_instance.create_connector(body)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling ConnectorApi->create_connector: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | [**Connector**](Connector.md)| Data for creating a new connector | 

### Return type

[**Connector**](Connector.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json, application/problem+json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **delete_connector**
> delete_connector(connector_id)

Deletes a connector

### Example
```python
from __future__ import print_function
import time
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = swagger_client.ConnectorApi()
connector_id = swagger_client.ConnectorId() # ConnectorId | The unique identifier of the connector

try:
    # Deletes a connector
    api_instance.delete_connector(connector_id)
except ApiException as e:
    print("Exception when calling ConnectorApi->delete_connector: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **connector_id** | [**ConnectorId**](.md)| The unique identifier of the connector | 

### Return type

void (empty response body)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/problem+json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_connector_by_id**
> Connector get_connector_by_id(connector_id)

Read a connector by ID

### Example
```python
from __future__ import print_function
import time
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = swagger_client.ConnectorApi()
connector_id = swagger_client.ConnectorId() # ConnectorId | The unique identifier of the connector

try:
    # Read a connector by ID
    api_response = api_instance.get_connector_by_id(connector_id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling ConnectorApi->get_connector_by_id: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **connector_id** | [**ConnectorId**](.md)| The unique identifier of the connector | 

### Return type

[**Connector**](Connector.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json, application/problem+json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_connector_locations**
> list[str] get_connector_locations(connector_id)

Read locations from connector

A location can be database, schema or dataset depending on the type of connector.

### Example
```python
from __future__ import print_function
import time
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = swagger_client.ConnectorApi()
connector_id = swagger_client.ConnectorId() # ConnectorId | The unique identifier of the connector

try:
    # Read locations from connector
    api_response = api_instance.get_connector_locations(connector_id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling ConnectorApi->get_connector_locations: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **connector_id** | [**ConnectorId**](.md)| The unique identifier of the connector | 

### Return type

**list[str]**

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json, application/problem+json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_connectors**
> InlineResponse200 get_connectors(page=page, size=size, sort=sort, filter=filter)

List connectors

### Example
```python
from __future__ import print_function
import time
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = swagger_client.ConnectorApi()
page = 1 # int | The number of items to skip before starting to collect the result set (optional) (default to 1)
size = 50 # int | The numbers of items to return (optional) (default to 50)
sort = 'createdAt:desc' # str | Fields and direction used for sorting connectors.  Can include multiple fields (e.g., \"name:desc\" or \"type:asc;createdAt:desc\")  (optional) (default to createdAt:desc)
filter = 'filter_example' # str | Filter by a keyword (optional)

try:
    # List connectors
    api_response = api_instance.get_connectors(page=page, size=size, sort=sort, filter=filter)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling ConnectorApi->get_connectors: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **page** | **int**| The number of items to skip before starting to collect the result set | [optional] [default to 1]
 **size** | **int**| The numbers of items to return | [optional] [default to 50]
 **sort** | **str**| Fields and direction used for sorting connectors.  Can include multiple fields (e.g., \&quot;name:desc\&quot; or \&quot;type:asc;createdAt:desc\&quot;)  | [optional] [default to createdAt:desc]
 **filter** | **str**| Filter by a keyword | [optional] 

### Return type

[**InlineResponse200**](InlineResponse200.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json, application/problem+json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **list_objects**
> list[str] list_objects(connector_id, path=path)

List object from a connector.

Reading an object is only possible from object storages.

### Example
```python
from __future__ import print_function
import time
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = swagger_client.ConnectorApi()
connector_id = swagger_client.ConnectorId() # ConnectorId | The unique identifier of the connector
path = 'path_example' # str |  (optional)

try:
    # List object from a connector.
    api_response = api_instance.list_objects(connector_id, path=path)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling ConnectorApi->list_objects: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **connector_id** | [**ConnectorId**](.md)| The unique identifier of the connector | 
 **path** | **str**|  | [optional] 

### Return type

**list[str]**

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json, application/problem+json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **test_connection**
> test_connection(body)

Test the connection of a connector

### Example
```python
from __future__ import print_function
import time
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = swagger_client.ConnectorApi()
body = swagger_client.Connector() # Connector | Data for testing connector

try:
    # Test the connection of a connector
    api_instance.test_connection(body)
except ApiException as e:
    print("Exception when calling ConnectorApi->test_connection: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | [**Connector**](Connector.md)| Data for testing connector | 

### Return type

void (empty response body)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/problem+json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **test_connection_by_id**
> test_connection_by_id(connector_id, body=body)

Test the connection of a connector

### Example
```python
from __future__ import print_function
import time
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = swagger_client.ConnectorApi()
connector_id = swagger_client.ConnectorId() # ConnectorId | The unique identifier of the connector
body = swagger_client.Connector() # Connector | Data for testing connector (optional)

try:
    # Test the connection of a connector
    api_instance.test_connection_by_id(connector_id, body=body)
except ApiException as e:
    print("Exception when calling ConnectorApi->test_connection_by_id: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **connector_id** | [**ConnectorId**](.md)| The unique identifier of the connector | 
 **body** | [**Connector**](Connector.md)| Data for testing connector | [optional] 

### Return type

void (empty response body)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/problem+json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **update_connector_by_id**
> Connector update_connector_by_id(body, connector_id)

Updates a connector or creates a new one with a specified ID

### Example
```python
from __future__ import print_function
import time
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = swagger_client.ConnectorApi()
body = swagger_client.Connector() # Connector | Data for creating a new connector or updating a connector
connector_id = swagger_client.ConnectorId() # ConnectorId | The unique identifier of the connector

try:
    # Updates a connector or creates a new one with a specified ID
    api_response = api_instance.update_connector_by_id(body, connector_id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling ConnectorApi->update_connector_by_id: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | [**Connector**](Connector.md)| Data for creating a new connector or updating a connector | 
 **connector_id** | [**ConnectorId**](.md)| The unique identifier of the connector | 

### Return type

[**Connector**](Connector.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json, application/problem+json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

