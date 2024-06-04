# Job feature list

|Column|Description|Type|Anonymized|
|------|-----------|----|----------|
|jid|The id assigned to the job when it is submitted|object|true|
|usr|The username of the user submitting the job|object|true|
|jnam|The name of the job|object|true|
|cnumr|Number of cores requested for the job|int64|false|
|cnumat|Number of cores allocated to the job|int64|false|
|cnumut|Number of cores used by the job|int64|false|
|nnumr|Number of nodes requested for the job|int64|false|
|adt|Arrival datetime (submission time)|object|false|
|qdt|Time of insertion in the job queue|object|false|
|schedsdt|Time of completed scheduling choice|object|false|
|deldt|Time of job deletion|object|false|
|ec|Job exit code|int64|false|
|elpl|Elapsed time limit, the time limit set to the job duration|float64|false|
|sdt|Start datetime|object|false|
|edt|End datetime|object|false|
|nnuma|Number of nodes allocated to the job|int64|false|
|idle_time_ave|Average idle time of the job|float64|false|
|nnumu|Number of nodes used by the job|int64|false|
|perf1|Number of execution cycles|float64|false|
|perf2|FP_FIXED_OPS_SPEC|float64|false|
|perf3|FP_SCALE_OPS_SPEC|float64|false|
|perf4|BUS_READ_TOTAL_MEM|float64|false|
|perf5|BUS_WRITE_TOTAL_MEM|float64|false|
|perf6|Number of sleep cycles|float64|false|
|mszl|Memory size limit for the job|float64|false|
|pri|Priority|int64|false|
|econ|Energy consumption|float64|false|
|avgpcon|Average node power consuption|float64|false|
|minpcon|Minimum node power consuption|float64|false|
|maxpcon|Maximum node power consuption|float64|false|
|msza|Memory size allocated|uint64|false|
|mmszu|Memory size used|float64|false|
|uctmut|User cpu time total use|float64|false|
|sctmut|System cpu time total use|float64|false|
|usctmut|Total cpu time use|float64|false|
|jobenv_req|Job environment requested|object|true|
|freq_req|Node frequency requested|int64|false|
|freq_alloc|Node frequency allocated|int64|false|
|flops|Number of floating point operations per second|float64|false|
|mbwidth|Memory bandwidth|float64|false|
|opint|Operational intensity|float64|false|
|pclass|Performance class, either compute-bound or memory-bound|object|false|
|embedding|Sensitive data encoding with Sentence-Bert|object|false|
|exit state|Exit state of the job execution, either completed or failed|object|false|
|duration|Duration of the job execution in seconds|float64|false|