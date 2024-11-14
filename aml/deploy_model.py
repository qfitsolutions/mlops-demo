from azureml.core import Workspace, Model, Environment
from azureml.core.model import InferenceConfig
from azureml.core.webservice import AciWebservice, Webservice

# Connect to your workspace
ws = Workspace.from_config()

# Get the registered model
model = Model(ws, name='iris-classifier')

# Define the environment using the YAML file
env = Environment.from_conda_specification(name='iris-env', file_path='env.yml')

# Create inference configuration
inference_config = InferenceConfig(entry_script='score.py', environment=env)

# Define deployment configuration
aci_config = AciWebservice.deploy_configuration(cpu_cores=1, memory_gb=1)

# Deploy the model as a web service
service = Model.deploy(
    workspace=ws,
    name='iris-service',
    models=[model],
    inference_config=inference_config,
    deployment_config=aci_config
)

service.wait_for_deployment(show_output=True)

print(f"Service deployed at {service.scoring_uri}")