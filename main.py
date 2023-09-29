import configparser
from kubernetes import client, config

def find_ingresses_without_kong_class(kong_ingress_class):
    try:
        # Load the Kubernetes configuration from the default location
        config.load_kube_config()

        # Create a Kubernetes API client
        api_instance = client.NetworkingV1Api()

        # List all Ingress resources in all namespaces
        ingresses = api_instance.list_ingress_for_all_namespaces()

        # Filter Ingress resources without the specified ingress class
        ingresses_without_class = [
            ingress for ingress in ingresses.items if (
                ingress.metadata.annotations and
                kong_ingress_class.lower() not in ingress.metadata.annotations.get("kubernetes.io/ingress.class", "").lower()
            )
        ]

        return ingresses_without_class

    except Exception as e:
        print(f"An error occurred: {str(e)}")

if __name__ == "__main__":
    # Read the configuration file
    config_parser = configparser.ConfigParser()
    config_parser.read("config.ini")

    # Get the ingress class from the configuration
    kong_ingress_class = config_parser.get("IngressFilter", "IngressClass")

    ingresses_without_kong = find_ingresses_without_kong_class(kong_ingress_class)

    if ingresses_without_kong:
        print(f"Ingress resources without '{kong_ingress_class}' in ingress class annotation:")
        for ingress in ingresses_without_kong:
            print(f"- Namespace: {ingress.metadata.namespace}, Name: {ingress.metadata.name}")
    else:
        print(f"No Ingress resources without '{kong_ingress_class}' in ingress class annotation found.")
