import logging
import os
import time

import pandas as pd
import requests
import tqdm as tq

logger = logging.getLogger(__name__)


def create_dataset(payload_data, base_url, token):
    """
    Create a new dataset on the Geonadir API.

    Args:
        payload_data (dict): Payload data for creating the dataset.

    Returns:
        str: Dataset ID.

    Raises:
        requests.exceptions.HTTPError: If there's an error creating the dataset.
    """

    reqUrl = f"{base_url}/api/dataset/"

    headers = {
        "Accept": "*/*",
        "Authorization": token,
        "Content-Type": "multipart/form-data; boundary=kljmyvW1ndjXaOEAg4vPm6RBUqO6MC5A"
    }

    payload = ""
    for key, value in payload_data.items():
        payload += f"--kljmyvW1ndjXaOEAg4vPm6RBUqO6MC5A\r\nContent-Disposition: form-data; name=\"{key}\"\r\n\r\n{value}\r\n"
    payload += "--kljmyvW1ndjXaOEAg4vPm6RBUqO6MC5A--\r\n"

    response = requests.post(reqUrl, data=payload, headers=headers, timeout=120)
    response.raise_for_status()

    dataset_id = response.json()["id"]
    return dataset_id


def upload_images(dataset_name, dataset_id, img_dir, base_url, token):
    """
    Upload images from a directory to a dataset.

    Args:
        dataset_name (str): Name of the dataset to upload images to.
        dataset_id (str): ID of the dataset to upload images to.
        img_dir (str): Directory path where the images are located.
        base_url (str): Base url of Geonadir api.
        token (str): User token.

    Returns:
        pd.DataFrame: DataFrame containing upload results for each image.
    """
    file_list = os.listdir(img_dir)
    file_list = [file for file in file_list if file.lower().endswith(('.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tif'))]

    count = 0
    df_list = []

    with tq.tqdm(total=len(file_list), position=0) as pbar:
        for file_path in file_list:

            file_size = os.path.getsize(os.path.join(img_dir, file_path))

            start_time = time.time()
            headers = {
                "authorization": token
            }

            payload = {"project_id": dataset_id}

            with open(os.path.join(img_dir, file_path), "rb") as file:
                response = requests.post(
                    f"{base_url}/api/upload_image/",
                    headers=headers,
                    data=payload,
                    files={"upload_files": file},
                    timeout=180,
                )

            response_code = response.status_code

            end_time = time.time()
            upload_time = end_time - start_time
            df = pd.DataFrame(
                {
                    "Project ID": dataset_id,
                    "Dataset Name": dataset_name,
                    "Image Name": file_path,
                    "Response Code": response_code,
                    "Upload Time": upload_time,
                    "Image Size": file_size
                },
                index=[0]
            )
            df_list.append(df)

            count += 1
            pbar.update(1)

    result_df = pd.concat(df_list, ignore_index=True)
    return result_df


def trigger_ortho_processing(dataset_id, base_url, token):
    headers = {
        "authorization": token
    }

    payload = {
        'dataset_id': (None, str(dataset_id)),
        'flag': (None, 'upload_completed'),
    }

    response = requests.post(
        f"{base_url}/api/utility/dataset-actions/",
        headers=headers,
        files=payload,
        timeout=180,
    )
    response.raise_for_status()


def paginate_dataset_image_images(url, image_names):
    """
    Paginate through the dataset images API response to retrieve all image names.

    Args:
        url (str): URL of the API endpoint.
        image_names (list): List to store the image names.

    Returns:
        list: List of image names.
    """
    response = requests.get(url, timeout=60)
    data = response.json()
    results = data["results"]
    for result in results:
        image_name = result["upload_files"]
        # image_name = re.search(r'([^/]+?)(?:_\d+)?\.JPG', image_url).group(1) + ".JPG"
        image_names.append(image_name)
    next_page = data["next"]
    if next_page:
        paginate_dataset_image_images(next_page, image_names)
    return image_names


def search_datasets(search_str, base_url):
    payload = {
        "search": search_str
    }

    response = requests.get(
        f"{base_url}/api/search_datasets",
        params=payload,
        timeout=180,
    )
    return response.json()


def dataset_info(project_id, base_url):
    payload = {
        "project_id": project_id
    }

    response = requests.get(
        f"{base_url}/api/metadata/",
        params=payload,
        timeout=180,
    )
    return response.json()


def search_datasets_coord(coord, base_url):
    l, r = max(min(coord[0], coord[2]), -180), min(max(coord[0], coord[2]), 180)
    b, t = max(min(coord[1], coord[3]), -90), min(max(coord[1], coord[3]), 90)
    logger.info(f"Querying dataset within ({l}, {b}, {r}, {t})")
    payload = {
        "bbox": f"{coord[0]},{coord[1]},{coord[2]},{coord[3]}"
    }

    response = requests.get(
        f"{base_url}/api/dataset_coords",
        params=payload,
        timeout=180,
    )
    return response.json()
