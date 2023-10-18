# SyntheticColumn

## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**id** | [**SyntheticColumnId**](SyntheticColumnId.md) |  | [optional] 
**generator_column_id** | [**SourceColumnId**](SourceColumnId.md) |  | [optional] 
**name** | **str** |  | [optional] 
**generation_method** | **str** |  | [optional] 
**generation_mood** | **str** |  | [optional] 
**rebalanced** | **bool** |  | [optional] 
**imputed** | **bool** |  | [optional] 
**mock_parameters** | **OneOfSyntheticColumnMockParameters** |  | [optional] 
**primary_key_format** | **str** | Applies for primary key column of subject table only. Specifies the format of the key.  | [optional] 
**rare_category_replacement** | **str** | Specifies, if the rare categories will be replaced by a constant _RARE_ or by a sample from non-rare categories.  | [optional] 

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)

