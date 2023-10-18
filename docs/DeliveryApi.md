# swagger_client.DeliveryApi

All URIs are relative to */*

Method | HTTP request | Description
------------- | ------------- | -------------
[**create_delivery**](DeliveryApi.md#create_delivery) | **POST** /delivery | Creates a new delivery
[**get_deliveries**](DeliveryApi.md#get_deliveries) | **GET** /delivery | List deliveries of synth data
[**get_delivery_by_id**](DeliveryApi.md#get_delivery_by_id) | **GET** /delivery/{deliveryId} | Read a delivery
[**get_delivery_progress**](DeliveryApi.md#get_delivery_progress) | **GET** /delivery/{deliveryId}/deliver | Read the delivery progress.
[**start_delivery**](DeliveryApi.md#start_delivery) | **POST** /delivery/{deliveryId}/deliver | Starts the delivery of the generator
[**stop_delivery**](DeliveryApi.md#stop_delivery) | **DELETE** /delivery/{deliveryId}/deliver | Stops the delivery of the generator
[**update_delivery**](DeliveryApi.md#update_delivery) | **PUT** /delivery/{deliveryId} | Updates a delivery

# **create_delivery**
> Delivery create_delivery(body=body, synth_data_id=synth_data_id)

Creates a new delivery

### Example
```python
from __future__ import print_function
import time
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = swagger_client.DeliveryApi()
body = swagger_client.DeliveryBody() # DeliveryBody |  (optional)
synth_data_id = 'synth_data_id_example' # str | id of the synth data set (optional)

try:
    # Creates a new delivery
    api_response = api_instance.create_delivery(body=body, synth_data_id=synth_data_id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling DeliveryApi->create_delivery: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | [**DeliveryBody**](DeliveryBody.md)|  | [optional] 
 **synth_data_id** | **str**| id of the synth data set | [optional] 

### Return type

[**Delivery**](Delivery.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json, application/problem+json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_deliveries**
> InlineResponse2003 get_deliveries(synth_data_id)

List deliveries of synth data

### Example
```python
from __future__ import print_function
import time
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = swagger_client.DeliveryApi()
synth_data_id = 'synth_data_id_example' # str | id of the synth data set

try:
    # List deliveries of synth data
    api_response = api_instance.get_deliveries(synth_data_id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling DeliveryApi->get_deliveries: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **synth_data_id** | **str**| id of the synth data set | 

### Return type

[**InlineResponse2003**](InlineResponse2003.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json, application/problem+json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_delivery_by_id**
> Delivery get_delivery_by_id(delivery_id)

Read a delivery

### Example
```python
from __future__ import print_function
import time
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = swagger_client.DeliveryApi()
delivery_id = swagger_client.DeliveryId() # DeliveryId | The unique identifier of the delivery

try:
    # Read a delivery
    api_response = api_instance.get_delivery_by_id(delivery_id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling DeliveryApi->get_delivery_by_id: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **delivery_id** | [**DeliveryId**](.md)| The unique identifier of the delivery | 

### Return type

[**Delivery**](Delivery.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json, application/problem+json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_delivery_progress**
> JobProgress get_delivery_progress(delivery_id)

Read the delivery progress.

### Example
```python
from __future__ import print_function
import time
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = swagger_client.DeliveryApi()
delivery_id = swagger_client.DeliveryId() # DeliveryId | The unique identifier of the delivery

try:
    # Read the delivery progress.
    api_response = api_instance.get_delivery_progress(delivery_id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling DeliveryApi->get_delivery_progress: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **delivery_id** | [**DeliveryId**](.md)| The unique identifier of the delivery | 

### Return type

[**JobProgress**](JobProgress.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json, application/problem+json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **start_delivery**
> start_delivery(delivery_id)

Starts the delivery of the generator

### Example
```python
from __future__ import print_function
import time
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = swagger_client.DeliveryApi()
delivery_id = swagger_client.DeliveryId() # DeliveryId | The unique identifier of the delivery

try:
    # Starts the delivery of the generator
    api_instance.start_delivery(delivery_id)
except ApiException as e:
    print("Exception when calling DeliveryApi->start_delivery: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **delivery_id** | [**DeliveryId**](.md)| The unique identifier of the delivery | 

### Return type

void (empty response body)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/problem+json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **stop_delivery**
> stop_delivery(delivery_id)

Stops the delivery of the generator

### Example
```python
from __future__ import print_function
import time
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = swagger_client.DeliveryApi()
delivery_id = swagger_client.DeliveryId() # DeliveryId | The unique identifier of the delivery

try:
    # Stops the delivery of the generator
    api_instance.stop_delivery(delivery_id)
except ApiException as e:
    print("Exception when calling DeliveryApi->stop_delivery: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **delivery_id** | [**DeliveryId**](.md)| The unique identifier of the delivery | 

### Return type

void (empty response body)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/problem+json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **update_delivery**
> Delivery update_delivery(body, delivery_id)

Updates a delivery

### Example
```python
from __future__ import print_function
import time
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = swagger_client.DeliveryApi()
body = swagger_client.Delivery() # Delivery | 
delivery_id = swagger_client.DeliveryId() # DeliveryId | The unique identifier of the delivery

try:
    # Updates a delivery
    api_response = api_instance.update_delivery(body, delivery_id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling DeliveryApi->update_delivery: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | [**Delivery**](Delivery.md)|  | 
 **delivery_id** | [**DeliveryId**](.md)| The unique identifier of the delivery | 

### Return type

[**Delivery**](Delivery.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json, application/problem+json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

