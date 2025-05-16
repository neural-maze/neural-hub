import logging
from functools import lru_cache
from uuid import uuid4

import torch
from facenet_pytorch import MTCNN, InceptionResnetV1  # type: ignore

logger = logging.getLogger(__name__)


@lru_cache(maxsize=1)
def initialize_models() -> tuple[torch.device, MTCNN, InceptionResnetV1]:
    """Initializes and returns the required ML models and device for face recognition.
    
    This function sets up the device (CPU/GPU), initializes the MTCNN model for face detection,
    and loads a pre-trained InceptionResnetV1 model for generating face embeddings.
    
    Returns:
        tuple:
            device (torch.device): The torch device (CPU/GPU) to use for computations
            mtcnn (MTCNN): Initialized MTCNN model for face detection
            resnet (InceptionResnetV1): Pre-trained InceptionResnetV1 model for embeddings
    """
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    mtcnn = MTCNN(image_size=160, margin=0, device=device)
    resnet = InceptionResnetV1(pretrained='vggface2').eval().to(device)
    return device, mtcnn, resnet


def process_single_image(img,  device: torch.device, mtcnn: MTCNN, resnet: InceptionResnetV1) -> None:
    """Process a single image and generates its embedding.
    
    Args:
        img: The celebrity image
        device: Torch device to use
        mtcnn: MTCNN model for face detection
        resnet: ResNet model for embedding generation
    """
    try:
        img_cropped = mtcnn(img)
        img_embedding = resnet(
            img_cropped.unsqueeze(0).to(device)
        ).squeeze(0).cpu().detach().numpy().tolist()
        
        return img_embedding
    
    except Exception as e:
        logger.warning(f"Failed to process image: {str(e)}")
