from typing import List, Callable, Tuple, Optional
import numpy as np
import time
import onnxruntime
import numpy as np
#from PIL import Image
import cv2
import random


# Load the ONNX model
session = onnxruntime.InferenceSession(r'/home/tecologyTrap1/tecology/Trap/best.onnx')

# Define input and output names
input_name = session.get_inputs()[0].name
output_name = session.get_outputs()[0].name


def xywh2xyxy(xywh: np.ndarray) -> np.ndarray:
    """Convert nx4 boxes from [x, y, w, h] to [x1, y1, x2, y2]

    Args:
        xywh (np.ndarray): array of 4 float [center_x, center_y, width, height]

    Returns:
        np.ndarray: array of 4 float [x1, y1, x2, y2] where (x1,y1)==top-left
        and (x2,y2)==bottom-right.
    """
    xyxy = np.copy(xywh)
    xyxy[:, 0] = xywh[:, 0] - xywh[:, 2] / 2  # top left x
    xyxy[:, 1] = xywh[:, 1] - xywh[:, 3] / 2  # top left y
    xyxy[:, 2] = xywh[:, 0] + xywh[:, 2] / 2  # bottom right x
    xyxy[:, 3] = xywh[:, 1] + xywh[:, 3] / 2  # bottom right y
    return xyxy


def nms_np(detections: np.ndarray, scores: np.ndarray, max_det: int,
           thresh: float) -> List[np.ndarray]:
    """Standard Non-Max Supression Algorithm for filter out detections.

    Args:
        detections (np.ndarray): bounding-boxes of shape num_detections,4
        scores (np.ndarray): confidence scores of each bounding box
        max_det (int): Maximum number of detections to keep.
        thresh (float): IOU threshold for NMS

    Returns:
        List[np.ndarray]: Filtered boxes.
    """
    x1 = detections[:, 0]
    y1 = detections[:, 1]
    x2 = detections[:, 2]
    y2 = detections[:, 3]

    areas = (x2 - x1 + 1) * (y2 - y1 + 1)

    # get boxes with more ious first
    order = scores.argsort()[::-1]

    # final output boxes
    keep = []

    while order.size > 0 and len(keep) < max_det:
        # pick maxmum iou box
        i = order[0]
        keep.append(i)

        # get iou
        ovr = get_iou((x1, y1, x2, y2), order, areas, idx=i)

        # drop overlaping boxes
        inds = np.where(ovr <= thresh)[0]
        order = order[inds + 1]

    return np.array(keep)


def get_iou(xyxy: Tuple[np.ndarray], order: np.ndarray, areas: np.ndarray,
            idx: int) -> float:
    """Helper function for nms_np to calculate IoU.

    Args:
        xyxy (Tuple[np.ndarray]): tuple of x1, y1, x2, y2 coordinates.
        order (np.ndarray): boxs' indexes sorted according to there
        confidence scores

        areas (np.ndarray): area of each box
        idx (int): base box to calculate iou for

    Returns:
        float: [description]
    """
    x1, y1, x2, y2 = xyxy
    xx1 = np.maximum(x1[idx], x1[order[1:]])
    yy1 = np.maximum(y1[idx], y1[order[1:]])
    xx2 = np.minimum(x2[idx], x2[order[1:]])
    yy2 = np.minimum(y2[idx], y2[order[1:]])

    max_width = np.maximum(0.0, xx2 - xx1 + 1)
    max_height = np.maximum(0.0, yy2 - yy1 + 1)
    inter = max_width * max_height

    return inter / (areas[idx] + areas[order[1:]] - inter)


def non_max_suppression_np(predictions: np.ndarray,
                           conf_thres: float = 0.25, 
                           iou_thres: float = 0.45, # For NMS
                           agnostic: bool = False,
                           multi_label: bool = True,
                           nms: Callable = nms_np) -> List[np.ndarray]:
    """Runs Non-Maximum Suppression (NMS used in Yolov5) on inference results.

    Args:
        predictions (np.ndarray): predictions from yolov inference

        conf_thres (float, optional): confidence threshold in range 0-1.
        Defaults to 0.25.

        iou_thres (float, optional): IoU threshold in range 0-1 for NMS filtering.
        Defaults to 0.45.

        agnostic (bool, optional): Perform class-agnostic NMS. Defaults to False.

        multi_label (bool, optional): apply Multi-Label NMS. Defaults to False.

        nms (Callable[[np.ndarray, np.ndarray, int, float], List[np.ndarray]]): Base NMS
        function to be applied. Defaults to nms_np.

    Returns:
        List[np.ndarray]: list of detections, on (n,6) tensor per image [xyxy, conf, cls]
    """
    # Settings
    maximum_detections = 300
    max_wh = 4096  # (pixels) minimum and maximum box width and height
    max_nms = 30000  # maximum number of boxes into torchvision.ops.nms()
    time_limit = 60.0  # seconds to quit after

    # number of classes > 1 (multiple labels per box (adds 0.5ms/img))
    multi_label &= (predictions.shape[2] - 5) > 1

    start_time = time.time()
    output = [np.zeros((0, 6))] * predictions.shape[0]
    confidences = predictions[..., 4] > conf_thres

    # image index, image inference
    for batch_index, prediction in enumerate(predictions):

        # confidence
        prediction = prediction[confidences[batch_index]]
        # If none remain process next image
        if not prediction.shape[0]:
            continue

        # Detections matrix nx6 (xyxy, conf, cls)
        prediction = detection_matrix(prediction, multi_label, conf_thres)

        # Check shape; # number of boxes
        if not prediction.shape[0]:  # no boxes
            continue

        # excess boxes
        if prediction.shape[0] > max_nms:
            prediction = prediction[np.argpartition(-prediction[:, 4],
                                                    max_nms)[:max_nms]]

        # Batched NMS
        classes = prediction[:, 5:6] * (0 if agnostic else max_wh)
        indexes = nms(prediction[:, :4] + classes, prediction[:, 4],
                      maximum_detections, iou_thres)

        # pick relevant boxes
        output[batch_index] = prediction[indexes, :]

        # check if time limit exceeded
        if (time.time() - start_time) > time_limit:
            print(f'WARNING: NMS time limit {time_limit}s exceeded')
            break
    return output


def detection_matrix(predictions: np.ndarray, multi_label: bool,
                     conf_thres: float) -> np.ndarray:
    """Prepare Detection Matrix for Yolov5 NMS

    Args:
        predictions (np.ndarray): one batch of predictions from yolov inference.
        multi_label (bool): apply Multi-Label NMS.
        conf_thres (float): confidence threshold in range 0-1.

    Returns:
        np.ndarray: detections matrix nx6 (xyxy, conf, cls).
    """

    # Compute conf = obj_conf * cls_conf
    predictions[:, 5:] *= predictions[:, 4:5]

    # Box (center x, center y, width, height) to (x1, y1, x2, y2)
    box = xywh2xyxy(predictions[:, :4])

    # Detections matrix nx6 (xyxy, conf, cls)
    if multi_label:
        print("Running multilabel")
        i, j = (predictions[:, 5:] > conf_thres).nonzero()#.T()
        predictions = np.concatenate(
            (box[i], predictions[i, j + 5, None], j[:, None].astype('float')),
            1)

    # best class only
    else:
        print("Running best class only")
        j = np.expand_dims(predictions[:, 5:].argmax(axis=1), axis=1)
        conf = np.take_along_axis(predictions[:, 5:], j, axis=1)

        predictions = np.concatenate((box, conf, j.astype('float')),
                                     1)[conf.reshape(-1) > conf_thres]

    return predictions

names = ['butterfly', 'cricket', 'dragonfly']
colors = {name:[random.randint(0, 255) for _ in range(3)] for i,name in enumerate(names)}


def convert_output(output): # This should be loop for multilabel
 
    IDs = [names[int(o[5])] for o in output[0]]
    xmins = [int(o[0]* (4608/640)) for o in output[0]]
    ymins = [int(o[1]* (2592/640)) for o in output[0]]
    xmaxs = [int(o[2]* (4608/640)) for o in output[0]]
    ymaxs = [int(o[3]* (2592/640)) for o in output[0]]
    confs = [round(o[4], 3) for o in output[0]]

    zipped = list(zip(xmins, ymins, xmaxs, ymaxs, confs, IDs))
    print(zipped)

    return zipped


RGB_PALETTE = ((255, 56, 56), (255, 157, 151), (255, 112, 31), (255, 178, 29),
               (207, 210, 49), (72, 249, 10), (146, 204, 23), (61, 219, 134),
               (26, 147, 52), (0, 212, 187), (44, 153, 168), (0, 194, 255),
               (52, 69, 147), (100, 115, 255), (0, 24, 236), (132, 56, 255),
               (82, 0, 133), (203, 56, 255), (255, 149, 200), (255, 55, 199))


def random_color(bgr: bool = True) -> Tuple[int]:
    """Return a random RGB/BGR Color

    Args:
        bgr (bool, optional): whether to return bgr color or rgb.
        Defaults to True.

    Returns:
        Tuple[int]: list of 3 ints representing Color
    """
    color = random.choice(RGB_PALETTE)
    return color[::-1] if bgr else color


def draw_bbox(image: np.ndarray,
              bbox: list,
              title: Optional[str] = None,
              color: Optional[Tuple[int]] = None,
              thickness: Optional[int] = 3) -> None:
    """Draw Bounding Box on the given image (inplace)

    Args:
        image (np.ndarray): image to draw on
        bbox (np.ndarray): coordinates of bbox top-left and right-bottom (x1,y1,x2,y2)
        title (Optional[str], optional): title of the drawn box. Defaults to None.
        color (Optional[Tuple[int]], optional): color of the box. Defaults to None (random color)
        thickness (Optional[int], optional): thickness of the box. Defaults to 2.
    """

    for b in bbox:
        color = random_color()

        # convert cordinates to int
        x1, y1, x2, y2 = b[0], b[1], b[2], b[3]

        # add title
        title = b[5] + ": " + str(round(100*b[4], 2)) + "%"

        scale = min(image.shape[0], image.shape[1]) / (640 / 0.5)
        text_size = cv2.getTextSize(title, 0, fontScale=scale, thickness=1)[0]
        top_left = (x1 - thickness + 1, y1 - text_size[1] - 20)
        bottom_right = (x1 + text_size[0] + 5, y1)

        cv2.rectangle(image, top_left, bottom_right, color=color, thickness=-1)
        cv2.putText(image, title, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX,
                    scale, (255, 255, 255), 2)

        # add box
        cv2.rectangle(image, (x1, y1), (x2, y2), color=color, thickness=thickness)




def letterbox(im, new_shape=(640, 640), color=(114, 114, 114), auto=True, scaleup=True, stride=32):
    # Resize and pad image while meeting stride-multiple constraints
    shape = im.shape[:2]  # current shape [height, width]
    if isinstance(new_shape, int):
        new_shape = (new_shape, new_shape)

    # Scale ratio (new / old)
    r = min(new_shape[0] / shape[0], new_shape[1] / shape[1])
    if not scaleup:  # only scale down, do not scale up (for better val mAP)
        r = min(r, 1.0)

    # Compute padding
    new_unpad = int(round(shape[1] * r)), int(round(shape[0] * r))
    dw, dh = new_shape[1] - new_unpad[0], new_shape[0] - new_unpad[1]  # wh padding

    if auto:  # minimum rectangle
        dw, dh = np.mod(dw, stride), np.mod(dh, stride)  # wh padding

    dw /= 2  # divide padding into 2 sides
    dh /= 2

    if shape[::-1] != new_unpad:  # resize
        im = cv2.resize(im, new_unpad, interpolation=cv2.INTER_LINEAR)
    top, bottom = int(round(dh - 0.1)), int(round(dh + 0.1))
    left, right = int(round(dw - 0.1)), int(round(dw + 0.1))
    im = cv2.copyMakeBorder(im, top, bottom, left, right, cv2.BORDER_CONSTANT, value=color)  # add border
    return im, r, (dw, dh)


def inference(inpImg):
    
    # Add resize step??
    image640 = cv2.resize(inpImg, (640, 640))
    image = image640.transpose((2, 0, 1))
    image = np.expand_dims(image, 0)
    image = np.ascontiguousarray(image)

    im = image.astype(np.float32)
    im /= 255

    inname = [i.name for i in session.get_inputs()]
    inputs = {inname[0]:im}

    # Run the model on the image
    outputs = session.run([output_name], inputs)
    
    # Run NMS on the model output
    nmsOut = non_max_suppression_np(outputs[0])



    #cv2.imwrite("output_image1.jpg", inpImg)
    conOut = convert_output(nmsOut)

    if conOut:
        print("Detections made. Returning box image and coordinates")
        draw_bbox(inpImg, conOut)
        return inpImg, conOut
    else:
        print("No detections made. Returning None.")
        return None
