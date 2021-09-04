from django import forms

class CalculatorForm(forms.Form):
	engine_size=forms.DecimalField()
	num_cylinders=forms.IntegerField()
	fuel_consumption=forms.DecimalField()