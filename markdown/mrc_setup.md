# Setting Up a Jupyter Notebook/Lab on MRC

The Melbourne Research Cloud provides instructions (sort of) for creating a Jupyter notebook server. From my initial exploration, it does not seem to support Jupyterlab yet. You can find their instructions [here](https://docs.cloud.unimelb.edu.au/guides/application_rstudio/), although they are setting up an R-Studio server.

The default allocation provided to you as a student (and me as well) is fairly spartan and we do not have extra disk (so we can't create a persistent volume).

We can create a key pair. This will allow us to securely connect to our instance with ssh.

## [Create a key pair](https://docs.cloud.unimelb.edu.au/training/first_instance/#create_keypair)

Once you've created the key pair, the private half of the pair will automatically be downloaded to your computer. The file will have the anem of your key pair (e.g. MIMIC34MD) and will end in `.pem`. I put these files in a special directory in my home directory ($HOME/.ssh)

## [Create a Jupyter Notebook Server](https://youtu.be/Rkkqv-cXhIw)
