
@app.route('/search', methods=['GET', 'POST'])
def search():

    if request.method == 'POST':
        identifier = request.form.get('identifier')
        q = hub.QueryHub()
        protein_id = identifier
        q.identifier = protein_id
        q.simple_query()

        return redirect(url_for('tasktable'), code=301)
        # redirect(url_for('search_loading', identifier=identifier), code=301)

    return render_template('Search.html')