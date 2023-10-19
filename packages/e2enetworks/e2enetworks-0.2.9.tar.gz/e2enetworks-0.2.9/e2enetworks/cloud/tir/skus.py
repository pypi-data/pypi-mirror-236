import requests
from e2enetworks.constants import BASE_GPU_URL, hash_code_to_image_id
from e2enetworks.cloud.tir import client


class Plans:
    def __init__(self):
        client_not_ready = (
            "Client is not ready. Please initiate client by:"
            "\n- Using e2enetworks.cloud.tir.init(...)"
        )
        if not client.Default.ready():
            raise ValueError(client_not_ready)

    def list(self, service, image_id=None):

        if type(service) != str:
            print(f"Service - {service} Should be String")
            return

        if service == "notebook" and type(image_id) != str:
            print(f"Image ID - {image_id} Should be String")
            return
        image = hash_code_to_image_id.get(image_id)
        image = image if image else ""
        url = f"{BASE_GPU_URL}gpu_service/sku/?image_id={image}&service={service}&"
        req = requests.Request('GET', url)
        response = client.Default.make_request(req)
        if response.status_code == 200:
            skus = response.json()["data"]
            print("SKU_ID  SERIES  CPU  GPU  MEMORY  SKU_TYPE SKU_NAME")
            print("CPU PLANS")
            for sku in skus["CPU"]:
                if sku.get("is_inventory_available"):
                    print(f"{sku.get('sku_id')}       {sku.get('series')}  "
                          f"   {sku.get('cpu')}  {sku.get('gpu')}  {sku.get('memory')}  {sku.get('sku_type')}  "
                          f"{sku.get('name')} ")
            print("GPU PLANS")
            for sku in skus["GPU"]:
                if sku.get("is_inventory_available"):
                    print(f"{sku.get('sku_id')}       {sku.get('series')}     {sku.get('cpu')}  {sku.get('gpu')}  "
                          f"  {sku.get('memory')}  {sku.get('sku_type')}  {sku.get('name')}")

    @staticmethod
    def help():
        print("Sku Class Help")
        print("\t\t================")
        print("\t\tThis class provides functionalities to interact with Plans.")
        print("\t\tAvailable methods:")

        print("\t\t1. list(service, image_id): Lists all Plans for given image_id and service.\n")
        print("\t\t Allowed Services List - ['notebook', 'inference_service', 'pipeline']")
        # Example usages
        print("\t\tExample usages:")
        print("\t\tskus = Plans()")
        print("\t\tskus.list('inference')")
