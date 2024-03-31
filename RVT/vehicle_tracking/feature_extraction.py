
from .ReId.load_model import load_model_from_opts
import torch
import torchvision.transforms as transforms
from PIL import Image
import os

opts_path = os.path.join(os.path.dirname(__file__) , 'opts.yaml')
ckpt_path = os.path.join(os.path.dirname(__file__) , 'net_19.pth')

extraction_model = load_model_from_opts(opts_path,ckpt=ckpt_path, remove_classifier=True)



def fliplr(img):
    """flip images horizontally in a batch"""
    inv_idx = torch.arange(img.size(3) - 1, -1, -1).long()
    inv_idx = inv_idx.to(img.device)
    img_flip = img.index_select(3, inv_idx)
    return img_flip


def extract_feature(model, X, device="cuda"):
    """Exract the embeddings of a single image tensor X"""
    if len(X.shape) == 3:
        X = torch.unsqueeze(X, 0)
    X = X.to(device)
    feature = model(X).reshape(-1)

    X = fliplr(X)
    flipped_feature = model(X).reshape(-1)
    feature += flipped_feature

    fnorm = torch.norm(feature, p=2)
    return feature.div(fnorm)

data_transforms = transforms.Compose([
    transforms.Resize((224, 224), interpolation=3),
    transforms.ToTensor(),
    transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
])



def get_score(query_feature, image_feature):
    # similarity of two features vectors for reid
    query_feature = query_feature
    image_feature = image_feature
    score = torch.dot(query_feature, image_feature).detach().numpy()

    return score


def getSimilarity(image1,image2):

    query_image = torch.unsqueeze(data_transforms(image1), 0)
    query_feature = extract_feature(extraction_model, query_image, device="cpu")
    query_image2 = torch.unsqueeze(data_transforms(image2), 0)
    query_feature2 = extract_feature(extraction_model, query_image2, device="cpu")
    return get_score(query_feature,query_feature2)

def compare_images(image1, image2):
    return getSimilarity(image1, image2)

def compare_images_from_path(image1, image2):
    print(image1, image2)

    img1 = Image.open(image1).convert('RGB')
    img2 = Image.open(image2).convert('RGB')

    return getSimilarity(img1, img2)