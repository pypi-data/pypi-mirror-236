import spacy
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from transformers import pipeline
import joblib

def classification(customer_feedback):
   classifier = pipeline("zero-shot-classification")
   res = classifier(customer_feedback,
      candidate_labels=["product aspects","customer experience", "issue"],
        )
   joblib.dump(classifier, "feedback_processing.pkl") 
   print("Based on :", res["labels"][0])



# Load GloVe embeddings with spaCy
nlp = spacy.load("en_core_web_md")

def compute(reference_set, reference_set_2, customer_feedback):
  feedback_vector = np.mean([nlp(word).vector for word in customer_feedback.split()], axis=0)
  reference_vector = np.mean([nlp(word).vector for word in reference_set], axis=0)
  reference_vector_2 = np.mean([nlp(word).vector for word in reference_set_2], axis=0)

# Calculate cosine similarity
  similarity = cosine_similarity([feedback_vector], [reference_vector])[0][0]
  similarity_2 = cosine_similarity([feedback_vector], [reference_vector_2])[0][0]
# Set a similarity threshold (adjust as needed)
  threshold = 0.5
  print("score: ", similarity)
  print("score 2: ", similarity_2)
# Filtering based on threshold
  if similarity >= threshold or similarity_2 >= threshold:
    classification(customer_feedback);
  else:
    print("Feedback is vague or useless.")


# Define the customer feedback and the reference set
def for_devices(feedback):
  customer_feedback = feedback

  reference_set = ["device","quality", "performance", "features", "battery", "Connectivity", "update", "build quality"]
  reference_set_2= ["issues", "price", "refund", "logistics"]
  compute(reference_set, reference_set_2, customer_feedback)
 
#The microwave is actually looks very good the color and and the built quality.. the function is very handy and easy for ur instant cook

def for_skincare(feedback):
  customer_feedback = feedback

  reference_set = ["skin care","quality", "skin", "effects", "texture", "fragrance"]
  reference_set_2= ["issues", "price", "refund", "logistics"]

  compute(reference_set, reference_set_2, customer_feedback)

#It is nice but not so good for me . After applying, it gives sweat that's the reason I didn't like this.

def for_clothing(feedback):
  customer_feedback = feedback

  reference_set = ["material","quality", "color", "clothes", "size"]
  reference_set_2= ["issues", "price", "refund", "logistics"]

  compute(reference_set, reference_set_2, customer_feedback)
#It's very pretty and the material is good too. Value for money. Loved the overall product.

def get_started(product_domain, feedback):
   if product_domain == "device" :
      for_devices(feedback)
   elif product_domain == "skin care products":
      for_skincare(feedback)
   elif product_domain == "clothing":
      for_clothing(feedback)
   else:
      print("domain not available") 

     