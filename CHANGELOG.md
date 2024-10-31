## 0.4.4 (2024-10-31)

### Feat

- allow snake_case (alongside camelCase) for config dict (#73)
- **api**: clone generators (#71)

## 0.4.3 (2024-10-03)

### Feat

- **api**: introduce similarity metrics

## 0.4.2 (2024-09-20)

### Fix

- **base**: return ListItems for list calls (#69)

## 0.4.1 (2024-09-20)

## 0.4.0 (2024-09-05)

### Feat

- **api**: introduce language models (#63)

### Fix

- **base**: repr pydantic model without deprecation warning (#66)

### Refactor

- **admin**: drop support for usage report (#65)
- **computes**: simplify interface for computes (#64)

## 0.3.13 (2024-08-19)

### Feat

- **api**: computes

## 0.3.12 (2024-08-12)

### Feat

- **api**: usage report (#60)

## 0.3.11 (2024-07-15)

### Feat

- **api**: allow `columns` to be provided as list[str] instead of list[dict[str, str]] in `mostly.train` (#59)

## 0.3.10 (2024-07-03)

### Feat

- **api**: add fairness parameters for SD generation
- **api**: add import / export for generators
- **api**: added total_rows and total_datapoints for synthetic dataset tables

## 0.3.9 (2024-06-10)

### Feat

- **api**: return URL when calling .open()
- **api**: add mostly.about() for retrieving platform info / version

## 0.3.8 (2024-05-28)

### Feat

- support shortLivedFileTokens for synthetic data download

## 0.3.7 (2024-05-23)

### Fix

- **utils**: _harmonize_sd_config to handle generator carefully (#40)

## 0.3.6 (2024-05-21)

### Feat

- **api**: make progress bar optional (#36)
- **api**: support endpoint for probing data (#25)

## 0.3.5 (2024-05-13)

### Feat

- **api**: support endpoint for fetching table schema (#28)
- **api**: support of value ranges and AUTO encoding type (#23)

## 0.3.4 (2024-04-26)

### Feat

- **api**: add connector usage (#21)

## 0.3.3 (2024-04-19)

### Feat

- **api**: add search_term parameter for lists (#15)

## 0.3.2 (2024-04-19)

### Feat

- **api**: allow setting ssl verify (#11)
- **api**: add an api call for GET /users/me (#10)

### Refactor

- **shares**: remove redundant imports (#14)

## 0.3.0 (2024-03-19)

### Refactor

- **shares**: url with resourceType, ver 0.3.0: (#8)

## 0.2.0 (2024-03-08)
