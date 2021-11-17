# Lightform Data Explorer

## Introduction

This project is a simple data explorer that provides a way of linking data records about material samples.

A project has one or more samples which are processed (cut up, forged, rolled etc.) to make more samples.
Experiments are done on these samples (EBSD, microscopy etc.).
Records and data of the processing and the experiments are uploaded to a data repository (Zenodo in our case).

The problem is that file storage on Zenodo is flat which makes it hard to link between records and explore the 
connections and relations between samples. This data explorer attempts to resolve that. The aim is not to
store data (that is already done by Zenodo) but to record sample-sample relations and sample-experiment 
relations.

## How to use the data explorer

### Intro

This project started off as a full dynamic Python Flask app. The user could install the app on a server, 
have an account, log in and add data. The problem with this is that it requires maintenance and the objective 
of this project is to provide a long term record of samples and experiments. It is hard to maintain things
like websites in academia because the turnover of people is naturally high in a research group.

After realising this, the scope changed somewhat. The data explorer is still a Flask app but the app is only 
run locally to input data. After data is then input, the pages served by Flask are archived to static HTML
pages and are uploaded to a separate GitHub repository. The webpages are then served through GitHub pages.
Hopefully this provides the best of both worlds - a nice dynamic app to input data into but with none of the 
inconvenient faff of having to actually maintain a webserver.

### Setting up a new data explorer

**Note:** If you already have a data explorer set up and just want to edit the data you can skip straight 
to the [updating section](#updating-a-data-explorer-for-the-first-time).

Fork this repository and then clone it to your machine. Make a new virtual environment and install the 
packages in `requirements.txt`. Change the `PROJECT_NAME` variable to a new project name that describes 
your project.

Run the webserver with `flask runserver` and a new database will be initialised in "../../PROJECT_NAME"
relative to the root of where you cloned this repository. Close the flask server and run "freeze.py". Note 
that `freeze.py` has relative references so should be run directly from its containing folder. This will 
generate the static pages in the same folder as the database.

Navigate to the "../../PROJECT_NAME" folder and initialise a new git repository here. Add a .gitigore with

```manage```

in it. This is not essential but will prevent uploading the dynamic pages that for adding the samples.
Set up a new repository on GitHub called "PROJECT_NAME", add it as a remote for this repository and push
to it. Now go into the settings for that project, activate GitHub pages and set it to serve from the 
root of the repository (not the docs folder or ghpages branch). Wait a couple of minutes and the pages 
should be generated.

### Updating a data explorer for the first time

If you want to update an existing data explorer you will need to clone two repositories, this one and the
data one. For this example we will use the TiFUN project as an example. You only need to do this step once,
on subsequent times you want to update the data you can skip straight to the 
[updating data section](#updating-the-data-and-uploading-to-github).

Instructions are provided here for git on the command line but you can use a Git GUI if you prefer.

Find a directory and clone the Flask app:
```
git clone https://github.com/LightForm-group/lightform_data_explorer.git
```
and the data:
```
git clone https://github.com/LightForm-group/tifun-data-explorer.git
```

Change directory to the lightform_data_explorer, make a new Python virtual environment, activate it and install the 
required packages:

```
cd lightform_data_explorer
python -m venv venv
# Windows
./venv/bin/activate
# Mac/unix
source ./venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

Note that activating the environemnet has a different syntax depnding on your operating system.

### Updating the data and uploading to github

If it is not already - activate your virtual environment and then run a Flask server with the command:

```
python run.py
```

This will give you a prompy with a local ip address that will look something like `http://127.0.0.1:5000/`. 
Either click this link or copy and paste into into your web browser. 
At this point you are running a copy of the app on your local machine. You can input new data into the app using 
the `manage` tab in the menu bar. Any data you add will be stored in the `data.db` file in the `tifun-data-explorer` 
folder you cloned earlier.

Once you have finished adding/modifying data, you now need to Freeze the pages you have generated to upload them to 
GitHub. You can kill the Flask server with `CTRL + C`. To freeze the pages, navigate to the `lightform_data_explorer` 
folder and run:

```
python freeze.py
```

This should generate/update the static .html pages in the `tifun-data-explorer` folder. Now commit and push 
the changes to GitHub:

```
cd ../../tifun-data-explorer
git add *
git commit -m "A descriptive message which says what you have added to the data"
git push
```

This pushes the static pages and updated database to GitHub. Give GitHub a few minutes to process them and
the updates should go live on GitHub at the pages URL.

## Development

If you want to modify the app or page templates it may be useful to run Flask with the 
"FLASK_ENV=development" argument as this makes the Flask server give much more helpful error messages and
it only runs a bit slower.
