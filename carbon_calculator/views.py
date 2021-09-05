from django.shortcuts import render,redirect
from sklearn.ensemble import RandomForestRegressor
from .calculator_form import CalculatorForm
import numpy as np
import math
import pickle
from django.views.decorators.http import require_POST
# Create your views here.

# Model path
MODEL_PATH=r'./carbon_calculator/ai/vehicle_carbon_emission_model.sav'

# Set the max carbon threshold for the vehicle
THRESHOLD=10
def index(request):
	#form
	context={}
	return render(request,'carbon_calculator/index.html',context)
# Function to return to home page when user taps back
def go_home(request):
	return redirect('index')
# Function to calculate the emission
@require_POST
def result(request):
	form=CalculatorForm(request.POST)
	engine_size=request.POST['Engine Size']
	fuel_consumption=request.POST['Fuel Consumption']
	num_cylinders=request.POST["Number of cylinder"]
	data=[engine_size,num_cylinders,fuel_consumption]
	data=np.expand_dims(data,axis=0)
	#load the model
	model=pickle.load(open(MODEL_PATH,'rb'))
	#make the prediction
	prediction=model.predict(data)
	if prediction[0]>THRESHOLD:
		is_allowed=True
	else:
		is_allowed=False	
	print(is_allowed)		
	#print(request.POST['Engine Size'])
	context={'emission':f'{math.ceil(prediction[0])}g/km','is_allowed':is_allowed}
	return render(request,'carbon_calculator/submit.html',context)
	