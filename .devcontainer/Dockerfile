FROM sphinxdoc/sphinx

WORKDIR /docs

COPY .env /docs

# Install pandoc
RUN apt-get update

# Install cartopy dependencies
RUN apt -y install libgeos-dev \
                   gcc \
                   g++

# Install python sphinx requirements
RUN pip install nbsphinx mpl_sphinx_theme sphinx-autobuild

# Install vizent depdendencies
RUN pip install scipy Pillow cartopy 

# Install vizent gallery dependencies
RUN pip install pandas python-dotenv

# Install jupyter ipykernel
RUN pip install ipykernel
