import pandas as pd
import streamlit as st
import pymongo
import datetime
import os

# app introduction
st.header('Kubernetes Workshop')
st.subheader('Introduction')
st.markdown('Welcome! This is a template application used in the Kubernetes workshop. Here we use streamlit and '
            'mongoDB to create a TODO app: the user can add todos to a list of todos. Each todo has text, is assigned '
            'a category and has a posted date. A user can update or mark as done (hence delete) the TODOs.')

# connect to mongodb
@st.cache_resource
def init_connection():
    return pymongo.MongoClient(os.environ['MONGO_URL'])
    # return pymongo.MongoClient('mongodb://database:27017')

client = init_connection()

st.markdown('After connecting to mongoDB we can create a new database, called `workshop`,'
            'and within it a collection named `todos`')

example_todo = {"description": "Test post",
                 "category": "test",
                 "date_posted": datetime.datetime.utcnow()
                 }

# CREATE AND READ
todos = client['workshop']['todos']
if todos is not None:
    st.success('Workshop database created, collection `todos` initialized!', icon="✅")

todos.insert_one(example_todo)

# show existing documents in collection
st.write("Existing TODOs: ")
cursor = todos.find({})
st.dataframe(pd.DataFrame(list(cursor)))

# UPDATE
st.subheader('Update TODO')
with st.form('update', clear_on_submit = True):
    id_to_update = st.text_input('Copy the id of todo you want to update')
    doc = todos.find_one({"_id": id_to_update})
    st.write(doc)
    update = st.form_submit_button('Update')
    if update:
        todos.update_one({'_id': id_to_update}, { "$set": { 'description': 'Updated' } })


# DELETE
st.subheader('Delete TODO')
with st.form('delete', clear_on_submit = True):
    id_to_delete = st.text_input('Copy the id of todo you want to update')
    delete = st.form_submit_button('Delete')
    if delete:
        todos.delete_one({'_id': id_to_delete})