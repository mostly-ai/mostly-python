# swagger_client.SynthDataApi

All URIs are relative to */*

Method | HTTP request | Description
------------- | ------------- | -------------
[**create_synth_data**](SynthDataApi.md#create_synth_data) | **POST** /synthetic-data | Creates a new SynthData
[**delete_synth_data**](SynthDataApi.md#delete_synth_data) | **DELETE** /synthetic-data/{syntheticDataId} | Deletes a SynthData
[**get_synth_data**](SynthDataApi.md#get_synth_data) | **GET** /synthetic-data | List SynthData
[**get_synth_data_by_id**](SynthDataApi.md#get_synth_data_by_id) | **GET** /synthetic-data/{syntheticDataId} | Read a SynthData
[**get_synth_data_progress**](SynthDataApi.md#get_synth_data_progress) | **GET** /synthetic-data/{syntheticDataId}/generation | Read the synthData progress.
[**start_synth_data**](SynthDataApi.md#start_synth_data) | **POST** /synthetic-data/{syntheticDataId}/generation | Starts the synthData of the generator
[**stop_synth_data**](SynthDataApi.md#stop_synth_data) | **DELETE** /synthetic-data/{syntheticDataId}/generation | Stops the synthData of the generator
[**update_synth_data**](SynthDataApi.md#update_synth_data) | **PUT** /synthetic-data/{syntheticDataId} | Updates a SynthData

# **create_synth_data**
> SyntheticData create_synth_data(body=body, copy_from_id=copy_from_id)

Creates a new SynthData

### Example
```python
from __future__ import print_function
import time
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = swagger_client.SynthDataApi()
body = swagger_client.SyntheticdataBody() # SyntheticdataBody |  (optional)
copy_from_id = 'copy_from_id_example' # str | Id of SynthData that should be cloned (optional)

try:
    # Creates a new SynthData
    api_response = api_instance.create_synth_data(body=body, copy_from_id=copy_from_id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling SynthDataApi->create_synth_data: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | [**SyntheticdataBody**](SyntheticdataBody.md)|  | [optional] 
 **copy_from_id** | **str**| Id of SynthData that should be cloned | [optional] 

### Return type

[**SyntheticData**](SyntheticData.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json, application/problem+json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **delete_synth_data**
> delete_synth_data(synthetic_data_id)

Deletes a SynthData

### Example
```python
from __future__ import print_function
import time
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = swagger_client.SynthDataApi()
synthetic_data_id = swagger_client.SyntheticDataId() # SyntheticDataId | The unique identifier of the synthData

try:
    # Deletes a SynthData
    api_instance.delete_synth_data(synthetic_data_id)
except ApiException as e:
    print("Exception when calling SynthDataApi->delete_synth_data: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **synthetic_data_id** | [**SyntheticDataId**](.md)| The unique identifier of the synthData | 

### Return type

void (empty response body)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/problem+json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_synth_data**
> InlineResponse2002 get_synth_data(page=page, size=size, sort=sort, filter=filter, generatorid=generatorid)

List SynthData

### Example
```python
from __future__ import print_function
import time
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = swagger_client.SynthDataApi()
page = 1 # int | The number of items to skip before starting to collect the result set (optional) (default to 1)
size = 50 # int | The numbers of items to return (optional) (default to 50)
sort = 'date:desc' # str | Fields and direction used for sorting generators.  Can include multiple fields (e.g., \"name:desc\" or \"status:asc;date:desc\")  (optional) (default to date:desc)
filter = 'filter_example' # str | Filter by a keyword (optional)
generatorid = 'generatorid_example' # str | id of used generator. (optional)

try:
    # List SynthData
    api_response = api_instance.get_synth_data(page=page, size=size, sort=sort, filter=filter, generatorid=generatorid)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling SynthDataApi->get_synth_data: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **page** | **int**| The number of items to skip before starting to collect the result set | [optional] [default to 1]
 **size** | **int**| The numbers of items to return | [optional] [default to 50]
 **sort** | **str**| Fields and direction used for sorting generators.  Can include multiple fields (e.g., \&quot;name:desc\&quot; or \&quot;status:asc;date:desc\&quot;)  | [optional] [default to date:desc]
 **filter** | **str**| Filter by a keyword | [optional] 
 **generatorid** | **str**| id of used generator. | [optional] 

### Return type

[**InlineResponse2002**](InlineResponse2002.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json, application/problem+json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_synth_data_by_id**
> SyntheticData get_synth_data_by_id(synthetic_data_id)

Read a SynthData

### Example
```python
from __future__ import print_function
import time
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = swagger_client.SynthDataApi()
synthetic_data_id = swagger_client.SyntheticDataId() # SyntheticDataId | The unique identifier of the synthData

try:
    # Read a SynthData
    api_response = api_instance.get_synth_data_by_id(synthetic_data_id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling SynthDataApi->get_synth_data_by_id: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **synthetic_data_id** | [**SyntheticDataId**](.md)| The unique identifier of the synthData | 

### Return type

[**SyntheticData**](SyntheticData.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json, application/problem+json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_synth_data_progress**
> JobProgress get_synth_data_progress(synthetic_data_id)

Read the synthData progress.

### Example
```python
from __future__ import print_function
import time
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = swagger_client.SynthDataApi()
synthetic_data_id = swagger_client.SyntheticDataId() # SyntheticDataId | The unique identifier of the synthData

try:
    # Read the synthData progress.
    api_response = api_instance.get_synth_data_progress(synthetic_data_id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling SynthDataApi->get_synth_data_progress: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **synthetic_data_id** | [**SyntheticDataId**](.md)| The unique identifier of the synthData | 

### Return type

[**JobProgress**](JobProgress.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json, application/problem+json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **start_synth_data**
> start_synth_data(synthetic_data_id)

Starts the synthData of the generator

### Example
```python
from __future__ import print_function
import time
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = swagger_client.SynthDataApi()
synthetic_data_id = swagger_client.SyntheticDataId() # SyntheticDataId | The unique identifier of the synthData

try:
    # Starts the synthData of the generator
    api_instance.start_synth_data(synthetic_data_id)
except ApiException as e:
    print("Exception when calling SynthDataApi->start_synth_data: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **synthetic_data_id** | [**SyntheticDataId**](.md)| The unique identifier of the synthData | 

### Return type

void (empty response body)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/problem+json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **stop_synth_data**
> stop_synth_data(synthetic_data_id)

Stops the synthData of the generator

### Example
```python
from __future__ import print_function
import time
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = swagger_client.SynthDataApi()
synthetic_data_id = swagger_client.SyntheticDataId() # SyntheticDataId | The unique identifier of the synthData

try:
    # Stops the synthData of the generator
    api_instance.stop_synth_data(synthetic_data_id)
except ApiException as e:
    print("Exception when calling SynthDataApi->stop_synth_data: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **synthetic_data_id** | [**SyntheticDataId**](.md)| The unique identifier of the synthData | 

### Return type

void (empty response body)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/problem+json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **update_synth_data**
> SyntheticData update_synth_data(body, synthetic_data_id)

Updates a SynthData

### Example
```python
from __future__ import print_function
import time
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = swagger_client.SynthDataApi()
body = swagger_client.SyntheticData() # SyntheticData | 
synthetic_data_id = swagger_client.SyntheticDataId() # SyntheticDataId | The unique identifier of the synthData

try:
    # Updates a SynthData
    api_response = api_instance.update_synth_data(body, synthetic_data_id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling SynthDataApi->update_synth_data: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | [**SyntheticData**](SyntheticData.md)|  | 
 **synthetic_data_id** | [**SyntheticDataId**](.md)| The unique identifier of the synthData | 

### Return type

[**SyntheticData**](SyntheticData.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json, application/problem+json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

