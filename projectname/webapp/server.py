from flask import Flask, render_template, request
import functions as func

# Create the application object
app = Flask(__name__)

@app.route("/")
def home_page():   
  return render_template('index.html')
	
	
@app.route('/output')
def recommendation_output():
#  	 
   	# Pull input
  some_input =request.args.get('user_input')
   
   	# Case if empty
  if some_input =="":
    return render_template("index.html",
                            my_input = some_input, 
                            my_form_result="Empty")
  else:
    some_output="Market Value is"
    some_number=func.value_predict(some_input)
    some_image=func.create_word_cloud(some_input)
    return render_template("index.html",
                            my_input=some_input,
                            my_output=some_output,
                            my_number=some_number,
                            my_img_name=some_image,
                            my_form_result="NotEmpty")


# start the server with the 'run()' method
if __name__ == "__main__":
  app.run(debug=True) #will run locally http://127.0.0.1:5000/
