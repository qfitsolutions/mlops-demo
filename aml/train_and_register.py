from azureml.core import Workspace, Dataset, Experiment, Run
   from azureml.core.model import Model
   from sklearn.datasets import load_iris
   from sklearn.ensemble import RandomForestClassifier
   from sklearn.model_selection import train_test_split
   import joblib

   # Connect to the Azure ML workspace
   ws = Workspace.from_config()

   # Create an experiment
   experiment = Experiment(workspace=ws, name='iris-experiment')

   # Start logging
   run = experiment.start_logging()

   # Load dataset
   data = load_iris()
   X_train, X_test, y_train, y_test = train_test_split(data.data, data.target, test_size=0.3, random_state=42)

   # Train the model
   model = RandomForestClassifier()
   model.fit(X_train, y_train)

   # Save the model
   joblib.dump(model, 'iris_model.pkl')
   print("Model trained and saved.")

   # Register the model
   model = Model.register(
       workspace=ws,
       model_path="iris_model.pkl",
       model_name="iris-classifier"
   )

   print(f"Model registered: {model.name} with ID: {model.id}")

   # End the run
   run.complete()