# Team Members

1. Adithya Srinivasa Raghavan - as20373
2. Srikrishna Kumarasamy - sk11595

# ROS Q&A System with Retrieval-Augmented Generation (RAG)

This repository demonstrates the development of a Retrieval-Augmented Generation (RAG) system designed to facilitate question-and-answering (Q&A) across four subdomains of the Robot Operating System (ROS). The project integrates state-of-the-art AI tools for efficient, context-aware Q&A handling.

## Project Highlights

1. **Base Model**: The system leverages the fine-tuned Llama 3.1 - 8b model, stored on Hugging Face. The model was specifically trained on ROS-related Q&A data, utilizing context-target triplets for domain-specific optimization.
2. **Subdomains Covered**:
   - ROS2 Robotics Middleware
   - Nav2 Navigation
   - MoveIt2 Motion Planning
   - Gazebo Simulation
3. **Pipeline Setup**: A modular pipeline was built using ZenML, with components for data scraping, featurization, chunking, storage, and retrieval.
4. **Storage and Retrieval**: MongoDB handles document storage, while QDrant manages vector similarity search for context-aware retrieval.
5. **Interface**: A Gradio-based web UI allows users to input queries and receive detailed, accurate answers.

## Features

- **Fine-Tuning**: Llama 3.1 - 8b was optimized with ROS-related datasets to ensure precise and relevant responses. [Llama 3.1 - 8b on Hugging Face](https://huggingface.co/Srikrishna12/ros_model)
- **Pipeline Architecture**:
  - **MongoDB**: Stores raw and processed data.
  - **QDrant**: Performs dense vector indexing for similarity search.
  - **ZenML**: Orchestrates the end-to-end data processing pipeline.
- **Containerization**: Services are containerized using Docker, ensuring scalability and ease of deployment.
- **User-Friendly UI**: Gradio interface supports interactive Q&A.

## Setup Instructions

1. **Prerequisites**:
   - Docker
   - MongoDB and QDrant
   - Python 3.13
   - ZenML
   - Hugging Face Transformers

2. **Installation**:
   - Clone the repository.
   - Build and start Docker containers using `docker-compose up`.
   - Initialize the MongoDB and QDrant services.

3. **Run the Application**:
   - Use ZenML pipelines to process data and initialize the pipeline.
   - Start the Gradio UI to interact with the Q&A system.


