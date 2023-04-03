import pandas as pd
import streamlit as st
import pymongo
import datetime
import os
from bson.objectid import ObjectId

# app introduction
st.header('Kubernetes Workshop')
st.subheader('Introduction')
st.markdown('Welcome! This is a template application used in the Kubernetes workshop. Here we use streamlit and '
            'mongoDB to create a TODO app: the user can add todos to a list of todos. Each todo has text, is assigned '
            'a category and has a posted date. A user can update or mark as done (hence delete) the TODOs.')
st.write(os.environ['MONGO_URL'])
# connect to mongodb
@st.cache_resource
def init_connection():
    return pymongo.MongoClient(os.environ['MONGO_URL'])

client = init_connection()

st.markdown('After connecting to mongoDB we can create a new database, called `workshop`,'
            'and within it a collection named `todos`')

todos = client['workshop']['todos']
if todos is not None:
    st.success('Workshop database created, collection `todos` initialized!', icon="✅")

example_todo = {"description": "Test post",
                 "category": "test",
                 "date_posted": datetime.datetime.utcnow()
                 }

# INSERT
st.subheader('Insert TODO')
with st.form('insert', clear_on_submit=True):
    todo_description = st.text_input('Description', 'Insert text here')
    todo_category = st.selectbox('Select the todo category:', ('CHM', 'MIT', 'Harvard'))
    insert = st.form_submit_button("Insert")
    if insert:
        todos.insert_one({"description": todo_description,
                          "category": todo_category,
                          "date_posted": datetime.datetime.utcnow()
                          })
# show existing documents in collection
st.write("Existing TODOs: ")
cursor = todos.find({})
st.dataframe(pd.DataFrame(list(cursor)), use_container_width=True)


col1, col2 = st.columns(2)

with col1:
    # UPDATE
    st.subheader('Update TODO')
    with st.form('update', clear_on_submit=True):
        id_to_update = st.selectbox('Select the id of todo you want to update',
                                    [str(id) for id in todos.distinct('_id')])
        doc = todos.find_one({"_id": ObjectId(id_to_update)})
        if doc is not None:
            new_description = st.text_input('New description here', doc['description'])
            new_category = st.text_input('New category here', doc['category'])
        update = st.form_submit_button('Update')
        if update:
            todos.update_one({'_id': ObjectId(id_to_update)}, {"$set": {'description': new_description,
                                                                        'category': new_category}})


with col2:
    # DELETE
    st.subheader('Delete TODO')
    with st.form('delete', clear_on_submit=True):
        id_to_delete = st.selectbox('Select the id of todo you want to delete',
                                    [str(id) for id in todos.distinct('_id')])
        delete = st.form_submit_button('Delete')
        if delete:
            todos.delete_one({'_id': ObjectId(id_to_delete)})
