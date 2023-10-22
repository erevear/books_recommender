<h2>Bookshelf Insights: Deploying Recommendation Systems with MLOps</h2>



![kaggle diagrams (3)](https://github.com/erevear/books_recommender/assets/11822655/ea44077f-bcc4-48bf-96fb-10883a24036e)


This project was completed as part of the KaggleX mentorship program. The goal of this project was to build a general understanding of the tools and processes used to productionize machine learning models. We explored both serving and scaling a prediction service, as well as creating a pipeline for continuous training.

<b>Model</b><br>
We built a two tower retrieval recommendation model that uses the tensorflow-recommenders package. This allows us to use a hybrid content and collaborative filtering system (system based both on the similarities between objects, but also on what users that have liked similar items also like). 
Since we wanted a very simple ui we ended up using a cosine similarity model based only on the book embeddings. The two tower architecture captures semantic similarity between users and items and clusters things together in embedding space. We simply pull out the learned book embeddings and send them to a cosine similarity function when the user inputs a book title.


![model](https://github.com/erevear/books_recommender/assets/11822655/43b76ec8-f02b-437e-9a4f-01b79bb3c20a)

<b>Model Training</b><br>
The model training pipeline was built in TFX, and deployed and run in Vertex AI Pipelines via the Kubeflow Dag Runner. Running the pipeline requires a custom Docker image that contains the required TFX recommenders package.
The pipeline pushes the trained model to a GCP Cloud Storage Bucket for the next step.
Note: as the prediction service is using the learned embeddings instead of the model predictions, we use a serving signature to take in the index of the book name and return its embeddings.


![kaggle diagrams (2)](https://github.com/erevear/books_recommender/assets/11822655/2a5daecf-50da-4218-b2dd-dbcfb8f8496f)


<b>Prediction Service</b><br>
Once the trained model is available we leverage Tensorflow Serving and GKE to create an API that will allow us to access predictions. 
TF Serving is deployed to GKE via its Docker image. We set all of this up through the configs in the K8s_serving folder, which we can load and run in GCP through the console editor. To apply the configs run kubectl apply -f on each file

<b>Serving Application</b><br>
We create another Kubernetes cluster and set of configs to deploy the UI (a Streamlit app) that allows us to interact with our prediction service. We deploy all of this via Cloudbuild, triggered by pushing to a Github repo.


![kaggle diagrams (3)](https://github.com/erevear/books_recommender/assets/11822655/bfe21e30-7106-4ef4-8904-46f09e09f4a4)


The app takes in the name of a book, turns that name into an index number, hits the prediction service with that value to pull in the learned embeddings for the book, then compares it to the rest of the model’s learned book embeddings (which were stored in a pkl file in cloud storage by the model training code). 
Note: typically we would only need to pull in the learned embeddings, however, deploying the service with TF Serving was done for the sake of the exercise.
We then return and graph a list of books similar to the one input by the user

![sharp object giphy](https://github.com/erevear/books_recommender/assets/11822655/9a343cda-58c1-4883-bc32-74bd548e8807)


<b>Next Steps</b><br>
1. Put monitoring in place to flag data drift
2. Kick off pipeline retraining and rebuild of serving api on data changes
