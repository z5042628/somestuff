from flask import Flask, redirect, render_template, request, url_for
from server import app
from random import shuffle

import time

@app.route('/', methods=["GET", "POST"])
def hello():
	final_names = []
	id_names = []
	
	if request.method == "POST":
		'''id_name = []
		for i in range(0, 3):
			inc_name = str("id" + str((i+1)))
			curr_name = request.form[inc_name]
			id_name.insert(i, curr_name)
		#input_id = request.form['username']
		'''
		id_names = request.form.getlist("player_name")
		
		for each_name in id_names:
			if len(each_name.strip()) != 0:
				final_names.append(each_name)
		
		shuffle(final_names)
		
		team_1 = final_names[:len(final_names)//2]
		team_2 = final_names[len(final_names)//2:]
		
		return render_template("index.html", team_1=team_1, team_2=team_2, old_names = id_names)
		
		
	return render_template("index.html", team_1=team_1, team_2=team_2, old_names = id_names)