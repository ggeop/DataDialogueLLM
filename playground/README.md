To use this Dockerfile:

Build the Docker image:
```
docker build -t jupyter-notebook-persistent .
```

Create two Docker volumes for persisting data:
```
docker volume create jupyter-notebooks
docker volume create jupyter-model
```

Run the container with the volumes:
```
docker run --name local-jupyter-notebook -p 8888:8888 -v jupyter-notebooks:/data/notebooks -v jupyter-model:/data/model jupyter-notebook-persistent 
```

This setup provides several benefits:

The model will only be downloaded once and stored in the jupyter-model volume.
All your notebooks will be saved in the jupyter-notebooks volume.
When you stop and restart the container, all your data (notebooks, model, and Hugging Face cache) will be preserved.

To stop the container, you can use docker stop <container_id>. To start it again, use the same docker run command as above. Your data will persist between sessions.

**Note: The first time you run the container, it may take some time to download the model. Subsequent starts will be much faster.**


## Training
Spider dataset: https://yale-lily.github.io/spider