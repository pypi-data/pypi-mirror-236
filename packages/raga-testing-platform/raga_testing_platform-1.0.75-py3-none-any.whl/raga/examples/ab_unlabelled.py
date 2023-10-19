from raga import *
import datetime

run_name = f"AB-event-unlabelled-{datetime.datetime.now().strftime('%Y%m%d%H%M%S')}"


filters = Filter()
filters.add(TimestampFilter(gte="nan", lte="na"))

# create test_session object of TestSession instance
test_session = TestSession(project_name="testingProject", run_name = run_name, access_key="LGXJjQFD899MtVSrNHGH", secret_key="TC466Qu9PhpOjTuLu5aGkXyGbM7SSBeAzYH6HpcP", host="http://3.111.106.226:8080")


rules = EventABTestRules() 
rules.add(metric = "difference_percentage", IoU = 0.5, _class = "ALL", threshold = 0.5, conf_threshold=0.5)
rules.add(metric = "difference_count", IoU = 0.5, _class = "ALL", threshold = 0.5, conf_threshold=0.5)

model_comparison_check = event_ab_test(test_session=test_session, 
                                       dataset_name="stopsign-event-video-ds-full-v5",
                                       test_name="AB-test-unlabelled",
                                       modelA = "Production-America-Stop-Event",
                                       modelB = "Complex-America-Stop-Event",
                                       object_detection_modelA="Complex-America-Stop-Model",
                                       object_detection_modelB = "Production-America-Stop-Model",
                                       type = "metadata", 
                                       sub_type = "unlabelled", 
                                       output_type = "event_detection",
                                       rules = rules,
                                       aggregation_level=["weather"], 
                                       filter=filters)

# add payload into test_session object
test_session.add(model_comparison_check)
#run added test
test_session.run()