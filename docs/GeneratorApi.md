# swagger_client.GeneratorApi

All URIs are relative to */*

Method | HTTP request | Description
------------- | ------------- | -------------
[**add_file_to_generator**](GeneratorApi.md#add_file_to_generator) | **POST** /generators/{generatorId}/file/{filename} | Add a file to a generator
[**create_generator**](GeneratorApi.md#create_generator) | **POST** /generators | Creates a new generator
[**delete_file_from_generator**](GeneratorApi.md#delete_file_from_generator) | **DELETE** /generators/{generatorId}/file/{filename} | Delete file from generator
[**delete_generator**](GeneratorApi.md#delete_generator) | **DELETE** /generators/{generatorId} | Deletes a generator
[**download_generator_configuration**](GeneratorApi.md#download_generator_configuration) | **GET** /generators/{generatorId}/download | Download configuration
[**generators_generator_id_training_download_get**](GeneratorApi.md#generators_generator_id_training_download_get) | **GET** /generators/{generatorId}/training/download | Download the training logs as zip file
[**get_generator_by_id**](GeneratorApi.md#get_generator_by_id) | **GET** /generators/{generatorId} | Read a generator
[**get_generators**](GeneratorApi.md#get_generators) | **GET** /generators | List generators
[**get_training_progress**](GeneratorApi.md#get_training_progress) | **GET** /generators/{generatorId}/training | Read the training progress.
[**start_training**](GeneratorApi.md#start_training) | **POST** /generators/{generatorId}/training | Starts the training of the generator
[**stop_training**](GeneratorApi.md#stop_training) | **DELETE** /generators/{generatorId}/training | Stops the training of the generator
[**update_generator**](GeneratorApi.md#update_generator) | **PUT** /generators/{generatorId} | Updates a generator

# **add_file_to_generator**
> add_file_to_generator(generator_id, filename, body=body)

Add a file to a generator

Creates a new file or appends the existing file

### Example
```python
from __future__ import print_function
import time
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = swagger_client.GeneratorApi()
generator_id = swagger_client.GeneratorId() # GeneratorId | The unique identifier of the generator
filename = swagger_client.FileName() # FileName | 
body = swagger_client.Object() # Object |  (optional)

try:
    # Add a file to a generator
    api_instance.add_file_to_generator(generator_id, filename, body=body)
except ApiException as e:
    print("Exception when calling GeneratorApi->add_file_to_generator: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **generator_id** | [**GeneratorId**](.md)| The unique identifier of the generator | 
 **filename** | [**FileName**](.md)|  | 
 **body** | **Object**|  | [optional] 

### Return type

void (empty response body)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: image/octet-stream
 - **Accept**: application/problem+json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **create_generator**
> Generator create_generator(body=body, copy_from_id=copy_from_id)

Creates a new generator

### Example
```python
from __future__ import print_function
import time
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = swagger_client.GeneratorApi()
body = swagger_client.GeneratorsBody() # GeneratorsBody |  (optional)
copy_from_id = 'copy_from_id_example' # str | Id of generator that should be cloned (optional)

try:
    # Creates a new generator
    api_response = api_instance.create_generator(body=body, copy_from_id=copy_from_id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling GeneratorApi->create_generator: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | [**GeneratorsBody**](GeneratorsBody.md)|  | [optional] 
 **copy_from_id** | **str**| Id of generator that should be cloned | [optional] 

### Return type

[**Generator**](Generator.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json, application/problem+json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **delete_file_from_generator**
> delete_file_from_generator(generator_id, filename)

Delete file from generator

### Example
```python
from __future__ import print_function
import time
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = swagger_client.GeneratorApi()
generator_id = swagger_client.GeneratorId() # GeneratorId | The unique identifier of the generator
filename = swagger_client.FileName() # FileName | 

try:
    # Delete file from generator
    api_instance.delete_file_from_generator(generator_id, filename)
except ApiException as e:
    print("Exception when calling GeneratorApi->delete_file_from_generator: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **generator_id** | [**GeneratorId**](.md)| The unique identifier of the generator | 
 **filename** | [**FileName**](.md)|  | 

### Return type

void (empty response body)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/problem+json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **delete_generator**
> delete_generator(generator_id)

Deletes a generator

### Example
```python
from __future__ import print_function
import time
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = swagger_client.GeneratorApi()
generator_id = swagger_client.GeneratorId() # GeneratorId | The unique identifier of the generator

try:
    # Deletes a generator
    api_instance.delete_generator(generator_id)
except ApiException as e:
    print("Exception when calling GeneratorApi->delete_generator: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **generator_id** | [**GeneratorId**](.md)| The unique identifier of the generator | 

### Return type

void (empty response body)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/problem+json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **download_generator_configuration**
> str download_generator_configuration(generator_id)

Download configuration

### Example
```python
from __future__ import print_function
import time
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = swagger_client.GeneratorApi()
generator_id = swagger_client.GeneratorId() # GeneratorId | The unique identifier of the generator

try:
    # Download configuration
    api_response = api_instance.download_generator_configuration(generator_id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling GeneratorApi->download_generator_configuration: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **generator_id** | [**GeneratorId**](.md)| The unique identifier of the generator | 

### Return type

**str**

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json, application/problem+json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **generators_generator_id_training_download_get**
> str generators_generator_id_training_download_get(generator_id)

Download the training logs as zip file

### Example
```python
from __future__ import print_function
import time
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = swagger_client.GeneratorApi()
generator_id = swagger_client.GeneratorId() # GeneratorId | The unique identifier of the generator

try:
    # Download the training logs as zip file
    api_response = api_instance.generators_generator_id_training_download_get(generator_id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling GeneratorApi->generators_generator_id_training_download_get: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **generator_id** | [**GeneratorId**](.md)| The unique identifier of the generator | 

### Return type

**str**

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/zip, application/problem+json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_generator_by_id**
> Generator get_generator_by_id(generator_id)

Read a generator

### Example
```python
from __future__ import print_function
import time
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = swagger_client.GeneratorApi()
generator_id = swagger_client.GeneratorId() # GeneratorId | The unique identifier of the generator

try:
    # Read a generator
    api_response = api_instance.get_generator_by_id(generator_id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling GeneratorApi->get_generator_by_id: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **generator_id** | [**GeneratorId**](.md)| The unique identifier of the generator | 

### Return type

[**Generator**](Generator.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json, application/problem+json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_generators**
> InlineResponse2001 get_generators(page=page, size=size, sort=sort, filter=filter)

List generators

### Example
```python
from __future__ import print_function
import time
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = swagger_client.GeneratorApi()
page = 1 # int | The number of items to skip before starting to collect the result set (optional) (default to 1)
size = 50 # int | The numbers of items to return (optional) (default to 50)
sort = 'createdAt:desc' # str | Fields and direction used for sorting generators.  Can include multiple fields (e.g., \"name:desc\" or \"status:asc;createdAt:desc\")  (optional) (default to createdAt:desc)
filter = 'filter_example' # str | Filter by a keyword (optional)

try:
    # List generators
    api_response = api_instance.get_generators(page=page, size=size, sort=sort, filter=filter)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling GeneratorApi->get_generators: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **page** | **int**| The number of items to skip before starting to collect the result set | [optional] [default to 1]
 **size** | **int**| The numbers of items to return | [optional] [default to 50]
 **sort** | **str**| Fields and direction used for sorting generators.  Can include multiple fields (e.g., \&quot;name:desc\&quot; or \&quot;status:asc;createdAt:desc\&quot;)  | [optional] [default to createdAt:desc]
 **filter** | **str**| Filter by a keyword | [optional] 

### Return type

[**InlineResponse2001**](InlineResponse2001.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json, application/problem+json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_training_progress**
> JobProgress get_training_progress(generator_id)

Read the training progress.

### Example
```python
from __future__ import print_function
import time
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = swagger_client.GeneratorApi()
generator_id = swagger_client.GeneratorId() # GeneratorId | The unique identifier of the generator

try:
    # Read the training progress.
    api_response = api_instance.get_training_progress(generator_id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling GeneratorApi->get_training_progress: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **generator_id** | [**GeneratorId**](.md)| The unique identifier of the generator | 

### Return type

[**JobProgress**](JobProgress.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json, application/problem+json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **start_training**
> start_training(generator_id)

Starts the training of the generator

### Example
```python
from __future__ import print_function
import time
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = swagger_client.GeneratorApi()
generator_id = swagger_client.GeneratorId() # GeneratorId | The unique identifier of the generator

try:
    # Starts the training of the generator
    api_instance.start_training(generator_id)
except ApiException as e:
    print("Exception when calling GeneratorApi->start_training: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **generator_id** | [**GeneratorId**](.md)| The unique identifier of the generator | 

### Return type

void (empty response body)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/problem+json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **stop_training**
> stop_training(generator_id)

Stops the training of the generator

### Example
```python
from __future__ import print_function
import time
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = swagger_client.GeneratorApi()
generator_id = swagger_client.GeneratorId() # GeneratorId | The unique identifier of the generator

try:
    # Stops the training of the generator
    api_instance.stop_training(generator_id)
except ApiException as e:
    print("Exception when calling GeneratorApi->stop_training: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **generator_id** | [**GeneratorId**](.md)| The unique identifier of the generator | 

### Return type

void (empty response body)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/problem+json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **update_generator**
> Generator update_generator(body, generator_id)

Updates a generator

### Example
```python
from __future__ import print_function
import time
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = swagger_client.GeneratorApi()
body = swagger_client.Generator() # Generator | 
generator_id = swagger_client.GeneratorId() # GeneratorId | The unique identifier of the generator

try:
    # Updates a generator
    api_response = api_instance.update_generator(body, generator_id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling GeneratorApi->update_generator: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | [**Generator**](Generator.md)|  | 
 **generator_id** | [**GeneratorId**](.md)| The unique identifier of the generator | 

### Return type

[**Generator**](Generator.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json, application/problem+json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

