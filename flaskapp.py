import ast
from collections import defaultdict

import pandas as pd
import os
from jinja2 import Template
from flask import Flask, render_template, request, url_for, flash, redirect, session, send_file, Response
import csv,io

info_tag = {}

# List of classes :
list_element = [ "OTHER", 'Thank you','Contact us','Download',
'Sign up','Demo', 'Schedule', 'Webinar', 'Purchase', 'Application','Subscribe','Watch video','Donate','Pricing','Login','Careers','Request a Quote',
'Key pages (product pages, about us, resources, blog)']
info_user={}

## the flask app
app = Flask(__name__,template_folder='template' )


@app.route('/',methods=('GET', 'POST'))
def main():
    if request.method == 'POST':
        name = request.form['name']
        f = request.files['file']
        f.save(f.filename)
        info_user = {'name': name, 'data':f.filename}
        print(info_user)
        if not name:
            return flash('Name is required!')
        elif not f:
            return flash('A file is required!')
        else:
            info_user = str(name) +'-'+ str(f.filename)
            return redirect(url_for('tagging', info_user = info_user))
    else:
        return render_template('main.html')



@app.route('/tagging/<info_user>/', methods=['GET', 'POST'])
def tagging(info_user):
    info_user_2 = info_user.split('-')
    name = info_user.split('-')[1]
    df = pd.read_csv(info_user_2[1])
    df = df.astype(str)
    if 'info' in df.columns:
        df = df.astype(str)
        df_2 = df[df['info'] == 'nan']
        index_to_tag = df_2.index
        number_to_tag = df_2.shape[0]
    else:
        df = df.astype(str)
        df_2 = df
        number_to_tag = df_2.shape[0]
        index_to_tag = df_2.index
    row_index = request.args.get('row_index', 0, type =int)

    if request.method == 'POST':
        if request.form.get('tag'):
            #row_index = request.args.get('row_index', 0, type=int)
            row_index_2 = index_to_tag[row_index-1]

            comment_domain = request.form.get( 'commentdomain')

            # df.loc[row_index-1, 'commentdomain'] = str(comment_domain)
            tag = request.form.get('tag')

            # df.loc[row_index-1, 'tag'] = str(tag)
            comment = request.form.get('comment')
            # print(row_index)
            # df.loc[row_index-1, 'comment'] = str(comment)
            info_tag[row_index_2]={"commentdomain":comment_domain, "tag":tag,"comment":comment}

            #
            # row_index = request.args.get('row_index', 0, type=int)
            # df.to_csv(name)
            number_to_tag = number_to_tag - row_index

        if request.form.get('save'):
            number_to_tag = number_to_tag - row_index
            for el in info_tag.keys():
                df.loc[el]['info'] = info_tag[el]
            df.to_csv(name)
            return redirect(url_for('save_csv', info_user=info_user, number_to_tag=number_to_tag))

    return render_template('index.html',
                           df=df_2,
                           list_element=list_element,
                           row_index=row_index ,
                           info_user=info_user,
                           number_to_tag=number_to_tag,index_to_tag=index_to_tag)


@app.route('/save-csv/<info_user>/<number_to_tag>', methods=['POST',"GET"])
def save_csv(info_user, number_to_tag):
    info_user_2 = info_user.split('-')
    df=pd.read_csv(info_user_2[1])
    s=df.to_csv()
    # Create a string buffer
    buf_str = io.StringIO(s)

    # Create a bytes buffer from the string buffer
    buf_byt = io.BytesIO(buf_str.read().encode("utf-8"))


    response = Response(df ,mimetype='text/csv')
    response.headers.set("Content-Disposition", "attachment", filename="data.csv")
    # Return the CSV data as an attachment
    return send_file(buf_byt,
                     mimetype="text/csv",
                     as_attachment=True,
                     download_name=str(number_to_tag )+'_'+info_user_2[1])


if __name__ == '__main__':

    app.run(debug=True)