# AWS MSK Kafka Practice 
## Josue Rojas Noble

### Idea

This repo creates both Producer and Consumer workflows connecting to MSK Kafka, creating a message(Producer) and reading it (Consumer)

#### Requisites

In execution environment:
``` bash
pip install kafka-python
pip install aws-msk-iam-sasl-signer-python
```
In AWS:
- AWS MSK Cluster
- EC2 Instance
  - Docker & Docker compose
  - Jupyterlab + compatible Python version

#### Files
##### Topic.py

This script creates a topic to use with messaging later on.

##### holamundo.py

This script creates a *Producer* and sends a "Hello World" message to the topic created in *Topic.py*

##### consumer.py

This script creates a *Consumer* in order to recieve the "Hello World" message sent via *holamundo.py*

##### delete.py 

This script deletes the topic created before in *Topic.py*
