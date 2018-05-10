def lambda_handler(event, context):
	if event['request']['type'] == "LaunchRequest":
		return on_launch(event, context)
	elif event['request']['type'] == 'IntentRequest':
		return on_intent(event['request'])
	elif event['request']['type'] == 'SessionEndedRequest':
		return on_session_ended()

def on_launch(event, context):
	welcomeMessage = getWelcomeMessage()
	return response_card(welcomeMessage, False, {}, "Welcome", welcomeMessage, "How can I help you?")


def on_intent(request):
	intent = request['intent']
	intent_name = request['intent']['name']

	if 'dialogState' in request:
		if request['dialogState'] == "STARTED" or request['dialogState'] == "IN_PROGRESS":
			return dialog_response(request['dialogState'], False)


	if intent_name == "AMAZON.HelpIntent":
		return do_help()
	elif intent_name == "AMAZON.StopIntent":
		return do_stop(attributes)
	elif intent_name == "AMAZON.CancelIntent":
		return do_stop()
	else:
		print ("Invalid Intent reply with help")
		do_help()

def getSlotValue(intent, slot):
	if 'slots' in intent:
		if slot in intent['slots']:
			if 'value' in intent['slots'][slot]:
				return intent['slots'][slot]['value']
	
	return -1


def getWelcomeMessage():
	# TODO: Improve this
	Messages = [
		"Namaste, What can I do for you?",
		"Please put me on work.",
		"Welcome, how can I help you?"
	]
	return getRandom(Messages)

def do_help():
	Messages = [
		# REPLACE: your help messages here
	]
	return response_plain_text(
			getRandom(Messages),
			False,
			{}
		)

def do_stop():
	Messages = [
		"Good Bye!!"
	]
	# TODO: Improve this
	return response_card(
			getRandom(Messages),
			True,
			{},
			"TATA",
			"We hope to see you again.",
			"Is there anything I can do for you?"
		)


def dialog_response(attributes, endsession):

	return {
		'version': '1.0',
		'sessionAttributes': attributes,
		'response':{
			'directives': [
				{
					'type': 'Dialog.Delegate'
				}
			],
			'shouldEndSession': endsession
		}
	}

def response_plain_text(output, shouldEndSession, attributes) : 
	print("\n")
	print(output)
	print("\n")
	""" create a simple json plain text response  """
	return {
		'version'   : '1.0',
		'response'  : {
			'shouldEndSession'  : endsession,
			'outputSpeech'  : {
				'type'      : 'PlainText',
				'text'      : output
			}
		},
		'sessionAttributes' : attributes
	}


def response_card(output, endsession, attributes, title, cardContent, repromt = ""):
	print("\n")
	print(output)
	print("\n")
	""" create a simple json plain text response  """
	return {
		'version'   : '1.0',
		'response'  : {
			'shouldEndSession'  : endsession,
			'outputSpeech'  : {
				'type'      : 'PlainText',
				'text'      : output
			},
			'card' : {
				'type' : 'Simple',
				'title' : title,
				'content' : cardContent    
			},
			'repromt' : {
				'outputSpeech' : {
					'type' : 'PlainText',
					'text' : repromt
				}
			}
		},
		'sessionAttributes' : attributes
	}


def dialog_elicit_slot(output):
	print output, "\n"
	return {
		"version": "1.0",
		"sessionAttributes": {},
		"response": {
			"outputSpeech": {
				"type": "PlainText",
				"text": output
				# outputSpeech contains the list of options I want the user to select from
			},
			"shouldEndSession": False,
			"directives": [
				{
					"type": "Dialog.ElicitSlot",
					"slotToElicit": "MULTIPLEX",
					"updatedIntent": {
						"name": "GetMovieDetails",
						"confirmationStatus": "NONE",
					}
				}
			]
		}
	}

