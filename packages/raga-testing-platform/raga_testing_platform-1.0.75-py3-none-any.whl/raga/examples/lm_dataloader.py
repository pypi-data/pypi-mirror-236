import io
import pathlib
import random
from raga import *
import pandas as pd
import datetime
import numpy as np

weather_data = {
    "overcast": "overcast",
    "fog": "fog",
    "cloudy": "overcast",
    "sunny": "clear",
    "clear": "clear",
    "snow": "snow",
    "rain": "rain",
    "partly cloudy": "overcast",
    "light rain": "rain",
    "patchy light rain with thunder": "rain",
    "patchy light rain": "rain",
    "light drizzle": "rain",
    "light freezing rain": "rain",
    "thundery outbreaks possible": "overcast",
    "patchy rain possible": "overcast",
    "patchy light drizzle": "rain",
    "heavy freezing drizzle":"rain",
    "moderate snow": "snow",
    "moderate rain at times": "rain",
    "moderate rain": "rain",
    "moderate or heavy snow showers": "snow",
    "moderate or heavy rain shower": "rain",
    "moderate or heavy rain with thunder":"rain",
    "moderate or heavy freezing rain":"rain",
    "heavy rain":"rain",
    "heavy snow":"snow",
    "mist": "fog",
    "freezing fog":"fog",
    "light snow": "snow",
    "light snow showers": "snow",
    "light sleet showers": "snow",
    "light sleet": "snow",
    "light rain shower": "rain",
    "blowing snow": "snow",
    "patchy light snow":"snow",
    "patchy moderate snow":"snow",
    "ice pellets":"snow",
    "blizzard":"snow",
    "":""
}

def get_timestamp_x_hours_ago(hours):
    current_time = datetime.datetime.now()
    delta = datetime.timedelta(days=90, hours=hours)
    past_time = current_time - delta
    timestamp = int(past_time.timestamp())
    return timestamp

def img_url(x):
    return StringElement(f"https://ragacloudstorage.s3.ap-south-1.amazonaws.com/1/StopSign_Part1_event.json/data_points/{pathlib.Path(x).stem}/{x}")

def event_a_inference(row):
    detections = EventDetectionObject()
    start_frame = row["model_1_outputs"][0]["frame_id"]
    end_frame = row["model_1_outputs"][-1]["frame_id"]
    for index, frame in enumerate(row["event_1_outputs"]):
        for detection in frame["detections"]:
            for ind, count in enumerate(range(int(detection["count"]))):
                id = ind+1
                detections.add(EventDetection(Id=id, StartFrame=start_frame, EndFrame=end_frame, EventType=detection["class"], Confidence=detection["confidence"]))
    return detections


def event_b_inference(row):
    detections = EventDetectionObject()
    start_frame = row["model_2_outputs"][0]["frame_id"]
    end_frame = row["model_2_outputs"][-1]["frame_id"]
    for index, frame in enumerate(row["event_2_outputs"]):
        for detection in frame["detections"]:
            for ind, count in enumerate(range(int(detection["count"]))):
                id = ind+1
                detections.add(EventDetection(Id=id, StartFrame=start_frame, EndFrame=end_frame, EventType=detection["class"], Confidence=detection["confidence"]))
    return detections

def model_a_video_inference(row):
    model_a_inference = VideoDetectionObject()
    for index, frame in enumerate(row["model_1_outputs"]):
        detections = ImageDetectionObject()
        for index, detection in enumerate(frame["detections"]):
            id = index+1
            detections.add(ObjectDetection(Id=id, Format="xywh_normalized", Confidence=detection["confidence"], ClassId=0, ClassName=detection["class"], BBox=detection["bbox"]))
        model_a_inference.add(VideoFrame(frameId=frame["frame_id"], timeOffsetMs=float(frame["time_offset_ms"])*1000, detections=detections))

    return model_a_inference


def model_b_video_inference(row):
    model_a_inference = VideoDetectionObject()
    for index, frame in enumerate(row["model_2_outputs"]):
        detections = ImageDetectionObject()
        for index, detection in enumerate(frame["detections"]):
            id = index+1
            detections.add(ObjectDetection(Id=id, Format="xywh_normalized", Confidence=detection["confidence"], ClassId=0, ClassName=detection["class"], BBox=detection["bbox"]))
        model_a_inference.add(VideoFrame(frameId=frame["frame_id"], timeOffsetMs=float(frame["time_offset_ms"])*1000, detections=detections))

    return model_a_inference


def model_image_inference(row):
    AnnotationsV1 = ImageDetectionObject()
    for index, detection in enumerate(row["detections"]):
        AnnotationsV1.add(ObjectDetection(Id=detection["Id"], ClassId=0, ClassName=detection['ClassName'], Confidence=detection['Confidence'], BBox= detection['BBox'], Format=detection['Format']))
    return AnnotationsV1

def generate_random_list():
    """
    Generate a random list of specified length containing floating-point numbers.

    Args:
        length (int): The number of elements in the list.

    Returns:
        A list of random floating-point numbers.
    """
    list_data = [random.choice([random.uniform(1, 20), random.uniform(1, 20), random.uniform(-10, 20)]), random.choice([random.uniform(1, 20), random.uniform(1, 20), random.uniform(-10, 20)]), random.choice([random.uniform(1, 20), random.uniform(1, 20), random.uniform(-10, 20)])]
    embeddings = ImageEmbedding()
    for embedding in list_data:
        # print(embedding)
        embeddings.add(Embedding(int(embedding)))
    return embeddings


def json_parser(event_1, event_2, model_1, model_2):
    event_1_df = pd.read_json(event_1)
    event_2_df = pd.read_json(event_2)
    model_1_df = pd.read_json(model_1)
    model_2_df = pd.read_json(model_2)

    event_1_df_exploded = event_1_df.explode('inputs')
    event_2_df_exploded = event_2_df.explode('inputs')
    model_1_df_exploded = model_1_df.explode('inputs')
    model_2_df_exploded = model_2_df.explode('inputs')

    attributes = event_2_df["attributes"].apply(pd.Series)

    event_2_df_exploded = pd.concat([event_2_df_exploded, attributes], axis=1)
    event_1_df_exploded.rename(columns={"outputs": "event_1_outputs"}, inplace=True)
    event_2_df_exploded.rename(columns={"outputs": "event_2_outputs"}, inplace=True)
    model_1_df_exploded.rename(columns={"outputs": "model_1_outputs"}, inplace=True)
    model_2_df_exploded.rename(columns={"outputs": "model_2_outputs"}, inplace=True)
    merged_df = pd.merge(event_1_df_exploded, event_2_df_exploded, on='inputs')
    merged_df = pd.merge(merged_df, model_1_df_exploded, on='inputs')
    merged_df = pd.merge(merged_df, model_2_df_exploded, on='inputs', suffixes=[None, "_model_2"])
    data_frame = pd.DataFrame()
    data_frame["videoId"] = merged_df["inputs"].apply(lambda x: StringElement(pathlib.Path(x).stem))
    data_frame["videoUrl"] = merged_df["inputs"].apply(lambda x: img_url(x))
    data_frame["timeOfCapture"] = merged_df.apply(lambda row: TimeStampElement(get_timestamp_x_hours_ago(row.name)), axis=1)
    # data_frame["sourceLink"] = merged_df["inputs"].apply(lambda x: StringElement(x))
    data_frame["dutyType"] = merged_df["dutyType"].apply(lambda x: StringElement(x))
    data_frame["time_of_day"] = merged_df["time_of_day"].apply(lambda x: StringElement(x))
    data_frame["weather"] = merged_df["weather"].apply(lambda x: StringElement(weather_data[str(x).lower()]))
    data_frame["scene"] = merged_df["scene"].apply(lambda x: StringElement(x))
    # data_frame["tags"] = merged_df["tags"].apply(lambda x: StringElement(x))
    # data_frame["Complex-America-Stop-Event"] = merged_df.apply(event_a_inference, axis=1)
    # data_frame["Production-America-Stop-Event"] = merged_df.apply(event_b_inference, axis=1)
    # data_frame["Complex-America-Stop-Model"] = merged_df.apply(model_a_video_inference, axis=1)
    # data_frame["Production-America-Stop-Model"] = merged_df.apply(model_b_video_inference, axis=1)
    return data_frame.iloc[11:13]


pd_video_data_frame = json_parser("./assets/Complex-America-Stop-Event.json", "./assets/Production-America-Stop-Event.json", "./assets/Complex-America-Stop-Model.json", "./assets/Production-America-Stop-Model.json")

# print(pd_video_data_frame)
# # data_frame_extractor(pd_video_data_frame).to_csv("assets/event_ds_pd_10.csv", index=False)


schema = RagaSchema()
schema.add("videoId", PredictionSchemaElement())
schema.add("videoUrl", ImageUriSchemaElement())
schema.add("timeOfCapture", TimeOfCaptureSchemaElement())
# schema.add("sourceLink", FeatureSchemaElement())
schema.add("dutyType", AttributeSchemaElement())
schema.add("time_of_day", AttributeSchemaElement())
schema.add("weather", AttributeSchemaElement())
schema.add("scene", AttributeSchemaElement())
# schema.add("tags", AttributeSchemaElement())
# schema.add("Complex-America-Stop-Event", EventInferenceSchemaElement(model="Complex-America-Stop-Event"))
# schema.add("Production-America-Stop-Event", EventInferenceSchemaElement(model="Production-America-Stop-Event"))


run_name = f"lm_video_loader_failure_mode_analysis_object_detection-{datetime.datetime.now().strftime('%Y%m%d%H%M%S')}"


# create test_session object of TestSession instance
test_session = TestSession(project_name="testingProject", run_name= run_name)

creds = DatasetCreds(arn="arn:aws:iam::527593518644:role/raga-importer")

#create test_ds object of Dataset instance
video_ds = Dataset(test_session=test_session,
                  name="test-lm-loader-19-oct-v4",
                  type=DATASET_TYPE.VIDEO,
                  data=pd_video_data_frame,
                  schema=schema,
                  creds=creds)
#load schema and pandas data frame
video_ds.lightmetrics_data_upload()