# swagger_client.QAReportApi

All URIs are relative to */*

Method | HTTP request | Description
------------- | ------------- | -------------
[**download_data_qa_report**](QAReportApi.md#download_data_qa_report) | **GET** /data-qa-report/{qaReportId}/download | Downloads a QA report of the trained model as .zip file
[**download_model_qa_report**](QAReportApi.md#download_model_qa_report) | **GET** /model-qa-report/{qaReportId}/download | Downloads a QA report of the trained model as .zip file
[**get_data_qa_report**](QAReportApi.md#get_data_qa_report) | **GET** /data-qa-report/{qaReportId} | Read a QA report of the trained model
[**get_model_qa_report**](QAReportApi.md#get_model_qa_report) | **GET** /model-qa-report/{qaReportId} | Read a QA report of the trained model

# **download_data_qa_report**
> str download_data_qa_report(qa_report_id)

Downloads a QA report of the trained model as .zip file

### Example
```python
from __future__ import print_function
import time
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = swagger_client.QAReportApi()
qa_report_id = swagger_client.ModelQAReportId() # ModelQAReportId | The unique identifier of the QA report

try:
    # Downloads a QA report of the trained model as .zip file
    api_response = api_instance.download_data_qa_report(qa_report_id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling QAReportApi->download_data_qa_report: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **qa_report_id** | [**ModelQAReportId**](.md)| The unique identifier of the QA report | 

### Return type

**str**

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/zip, application/problem+json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **download_model_qa_report**
> str download_model_qa_report(qa_report_id)

Downloads a QA report of the trained model as .zip file

### Example
```python
from __future__ import print_function
import time
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = swagger_client.QAReportApi()
qa_report_id = swagger_client.ModelQAReportId() # ModelQAReportId | The unique identifier of the QA report

try:
    # Downloads a QA report of the trained model as .zip file
    api_response = api_instance.download_model_qa_report(qa_report_id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling QAReportApi->download_model_qa_report: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **qa_report_id** | [**ModelQAReportId**](.md)| The unique identifier of the QA report | 

### Return type

**str**

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/zip, application/problem+json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_data_qa_report**
> DataQAReport get_data_qa_report(qa_report_id)

Read a QA report of the trained model

### Example
```python
from __future__ import print_function
import time
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = swagger_client.QAReportApi()
qa_report_id = swagger_client.ModelQAReportId() # ModelQAReportId | The unique identifier of the QA report

try:
    # Read a QA report of the trained model
    api_response = api_instance.get_data_qa_report(qa_report_id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling QAReportApi->get_data_qa_report: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **qa_report_id** | [**ModelQAReportId**](.md)| The unique identifier of the QA report | 

### Return type

[**DataQAReport**](DataQAReport.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json, application/problem+json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_model_qa_report**
> ModelQAReport get_model_qa_report(qa_report_id)

Read a QA report of the trained model

### Example
```python
from __future__ import print_function
import time
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = swagger_client.QAReportApi()
qa_report_id = swagger_client.ModelQAReportId() # ModelQAReportId | The unique identifier of the QA report

try:
    # Read a QA report of the trained model
    api_response = api_instance.get_model_qa_report(qa_report_id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling QAReportApi->get_model_qa_report: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **qa_report_id** | [**ModelQAReportId**](.md)| The unique identifier of the QA report | 

### Return type

[**ModelQAReport**](ModelQAReport.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json, application/problem+json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

