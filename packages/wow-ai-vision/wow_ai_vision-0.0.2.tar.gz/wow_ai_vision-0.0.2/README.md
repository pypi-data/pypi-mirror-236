
## 👋 hello

**We write your reusable computer vision tools.** Whether you need to load your dataset from your hard drive, draw detections on an image or video, or count how many detections are in a zone. You can count on us! 🤝

## 💻 install

Pip install the wow-ai-vision package in a
[**3.11>=Python>=3.8**](https://www.python.org/) environment.

```bash
pip install wow-ai-vision[desktop]
```

Read more about desktop, headless, and local installation in our [guide](https://).

## 🔥 quickstart

### [detections processing](https://)

```python
>>> import wow-ai-vision as sv
>>> from ultralytics import YOLO

>>> model = YOLO('yolov8s.pt')
>>> result = model(IMAGE)[0]
>>> detections = sv.Detections.from_ultralytics(result)

>>> len(detections)
5
```

<details close>
<summary>👉 more detections utils</summary>

- Easily switch inference pipeline between supported object detection/instance segmentation models

    ```python
    >>> import wow-ai-vision as sv
    >>> from segment_anything import sam_model_registry, SamAutomaticMaskGenerator

    >>> sam = sam_model_registry[MODEL_TYPE](checkpoint=CHECKPOINT_PATH).to(device=DEVICE)
    >>> mask_generator = SamAutomaticMaskGenerator(sam)
    >>> sam_result = mask_generator.generate(IMAGE)
    >>> detections = sv.Detections.from_sam(sam_result=sam_result)
    ```

- [Advanced filtering](https://)

    ```python
    >>> detections = detections[detections.class_id == 0]
    >>> detections = detections[detections.confidence > 0.5]
    >>> detections = detections[detections.area > 1000]
    ```

- Image annotation

    ```python
    >>> import wow-ai-vision as sv

    >>> box_annotator = sv.BoxAnnotator()
    >>> annotated_frame = box_annotator.annotate(
    ...     scene=IMAGE,
    ...     detections=detections
    ... )
    ```

</details>

### [datasets processing](https://)

```python
>>> import wow-ai-vision as sv

>>> dataset = sv.DetectionDataset.from_yolo(
...     images_directory_path='...',
...     annotations_directory_path='...',
...     data_yaml_path='...'
... )

>>> dataset.classes
['dog', 'person']

>>> len(dataset)
1000
```

<details close>
<summary>👉 more dataset utils</summary>

- Load object detection/instance segmentation datasets in one of the supported formats

    ```python
    >>> dataset = sv.DetectionDataset.from_yolo(
    ...     images_directory_path='...',
    ...     annotations_directory_path='...',
    ...     data_yaml_path='...'
    ... )

    >>> dataset = sv.DetectionDataset.from_pascal_voc(
    ...     images_directory_path='...',
    ...     annotations_directory_path='...'
    ... )

    >>> dataset = sv.DetectionDataset.from_coco(
    ...     images_directory_path='...',
    ...     annotations_path='...'
    ... )
    ```

- Loop over dataset entries

    ```python
    >>> for name, image, labels in dataset:
    ...     print(labels.xyxy)

    array([[404.      , 719.      , 538.      , 884.5     ],
           [155.      , 497.      , 404.      , 833.5     ],
           [ 20.154999, 347.825   , 416.125   , 915.895   ]], dtype=float32)
    ```

- Split dataset for training, testing, and validation

    ```python
    >>> train_dataset, test_dataset = dataset.split(split_ratio=0.7)
    >>> test_dataset, valid_dataset = test_dataset.split(split_ratio=0.5)

    >>> len(train_dataset), len(test_dataset), len(valid_dataset)
    (700, 150, 150)
    ```

- Merge multiple datasets

    ```python
    >>> ds_1 = sv.DetectionDataset(...)
    >>> len(ds_1)
    100
    >>> ds_1.classes
    ['dog', 'person']

    >>> ds_2 = sv.DetectionDataset(...)
    >>> len(ds_2)
    200
    >>> ds_2.classes
    ['cat']

    >>> ds_merged = sv.DetectionDataset.merge([ds_1, ds_2])
    >>> len(ds_merged)
    300
    >>> ds_merged.classes
    ['cat', 'dog', 'person']
    ```

- Save object detection/instance segmentation datasets in one of the supported formats

    ```python
    >>> dataset.as_yolo(
    ...     images_directory_path='...',
    ...     annotations_directory_path='...',
    ...     data_yaml_path='...'
    ... )

    >>> dataset.as_pascal_voc(
    ...     images_directory_path='...',
    ...     annotations_directory_path='...'
    ... )

    >>> dataset.as_coco(
    ...     images_directory_path='...',
    ...     annotations_path='...'
    ... )
    ```

- Convert labels between supported formats

    ```python
    >>> sv.DetectionDataset.from_yolo(
    ...     images_directory_path='...',
    ...     annotations_directory_path='...',
    ...     data_yaml_path='...'
    ... ).as_pascal_voc(
    ...     images_directory_path='...',
    ...     annotations_directory_path='...'
    ... )
    ```

- Load classification datasets in one of the supported formats

    ```python
    >>> cs = sv.ClassificationDataset.from_folder_structure(
    ...     root_directory_path='...'
    ... )
    ```

- Save classification datasets in one of the supported formats

    ```python
    >>> cs.as_folder_structure(
    ...     root_directory_path='...'
    ... )
    ```

</details>

### [model evaluation](https://roboflow.github.io/wow-ai-vision/metrics/detection/)

```python
>>> import wow-ai-vision as sv

>>> dataset = sv.DetectionDataset.from_yolo(...)

>>> def callback(image: np.ndarray) -> sv.Detections:
...     ...

>>> confusion_matrix = sv.ConfusionMatrix.benchmark(
...     dataset = dataset,
...     callback = callback
... )

>>> confusion_matrix.matrix
array([
    [0., 0., 0., 0.],
    [0., 1., 0., 1.],
    [0., 1., 1., 0.],
    [1., 1., 0., 0.]
])
```

<details close>
<summary>👉 more metrics</summary>

- Mean average precision (mAP) for object detection tasks.

    ```python
    >>> import wow-ai-vision as sv

    >>> dataset = sv.DetectionDataset.from_yolo(...)

    >>> def callback(image: np.ndarray) -> sv.Detections:
    ...     ...

    >>> mean_average_precision = sv.MeanAveragePrecision.benchmark(
    ...     dataset = dataset,
    ...     callback = callback
    ... )

    >>> mean_average_precision.map50_95
    0.433
    ```

</details>

## 🎬 tutorials


## 💜 built with wow-ai-vision


## 📚 documentation



## 🏆 contribution
