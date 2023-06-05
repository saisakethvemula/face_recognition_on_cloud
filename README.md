Face Recognition System on Cloud

Real-time face recognition system that uses deepface(tensorflow) algorithm 
to generate fingerprints for each face and marks a subset of these 
fingerprints as fugitives, stored in a database for later use.

The system will be deployed on the cloud by dockerizing the Face 
Recognition System and using a load balancer to orchestrate incoming 
traffic, with each container being a stand-alone unit and the final output 
being an alerting system in case of a match.


Technologies: Python, Docker, AWS
