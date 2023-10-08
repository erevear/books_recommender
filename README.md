
![kaggle diagrams](https://github.com/erevear/books_recommender/assets/11822655/8ffad140-401b-48b2-a5a0-3295c6f99f86)


This project was completed as part of the KaggleX mentorship program. The goal of this project was to build a general understanding of the tools and processes used to productionize machine learning models. We explored both serving and scaling a prediction service, as well as creating a pipeline for continuous training.

1. Model: We built a two tower retrieval recommendation model that uses the tensorflow-recommenders package. This allows us to use a hybrid content and collaborative filtering system (system based both on the similarities between objects, but also on what users that have liked similar items also like). 
Since we wanted a very simple ui we ended up using a cosine similarity model based only on the book embeddings. The two tower architecture captures semantic similarity between users and items and clusters things together in embedding space. We simply pull out the learned book embeddings and send them to a cosine similarity function when the user inputs a book title.

![kaggle diagrams (1)](https://github.com/erevear/books_recommender/assets/11822655/2a7a972a-7097-4f45-9be0-0d500b0318d0)

2.  Model training: The model training pipeline was built in TFX, and deployed and run in Vertex AI Pipelines via the Kubeflow Dag Runner. Running the pipeline requires a custom Docker image that contains the required TFX recommenders package.
The pipeline pushes the trained model to a GCP Cloud Storage Bucket for the next step.
Note: as the prediction service is using the learned embeddings instead of the model predictions, we use a serving signature to take in the index of the book name and return its embeddings.

![kaggle diagrams (2)](https://github.com/erevear/books_recommender/assets/11822655/60a3a2a7-bff9-4967-88aa-fa94fcf88851)

3. Prediction service: Once the trained model is available we leverage Tensorflow Serving and GKE to create an API that will allow us to access predictions. 
TF Serving is deployed to GKE via its Docker image. We set all of this up through the configs in the K8s_serving folder, which we can load and run in GCP through the console editor. To apply the configs run kubectl apply -f on each file

4. UI: We create another Kubernetes cluster and set of configs to deploy the UI (a Streamlit app) that allows us to interact with our prediction service. The app takes in the name of a book, turns that name into an index number, hits the prediction service with that value to pull in the learned embeddings for the book, then compares it to the rest of the model’s learned book embeddings (which were stored in a pkl file in cloud storage by the model training code). 
Note: typically we would only need to pull in the learned embeddings, however, deploying the service with TF Serving was done for the sake of the exercise.
We then return and graph a list of books similar to the one input by the user
![Uploading giphy.gif…]()

Next steps
Put monitoring in place to flag data drift
Kick off pipeline retraining and rebuild of serving api on data changes
